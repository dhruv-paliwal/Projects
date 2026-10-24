"""
Models for LPG Distribution & Consumer Management System.
Optimized for high-volume consumer queries (22,000+ consumers across Kanpur, Hamirpur & adjoining regions).
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Consumer(models.Model):
    """
    Consumer Model engineered for scaling past 22,000+ local consumers.
    Utilizes composite indexes across region, consumer_id, and phone number for sub-millisecond retrieval.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]

    REGION_CHOICES = [
        ('Kanpur Nagar', 'Kanpur Nagar'),
        ('Kanpur Dehat', 'Kanpur Dehat'),
        ('Hamirpur City', 'Hamirpur City'),
        ('Hamirpur Rural', 'Hamirpur Rural'),
        ('Ghatampur', 'Ghatampur'),
        ('Rath', 'Rath'),
        ('Maudaha', 'Maudaha'),
        ('Sumerpur', 'Sumerpur'),
        ('Barra & Kidwai Nagar', 'Barra & Kidwai Nagar'),
        ('Civil Lines & Kalyanpur', 'Civil Lines & Kalyanpur'),
    ]

    CONNECTION_CHOICES = [
        ('DOMESTIC_SINGLE', 'Domestic 14.2kg (Single Bottle / SBC)'),
        ('DOMESTIC_DOUBLE', 'Domestic 14.2kg (Double Bottle / DBC)'),
        ('COMMERCIAL', 'Commercial 19kg (Hotel & Industry)'),
        ('FTL_5KG', '5kg Free Trade LPG (Migrant / Mini)'),
        ('PMUY_UJJAWALA', 'PM Ujjawala Yojana (Subsidized)'),
    ]

    consumer_id = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        help_text="Unique Consumer 17-digit or formatted agency LPG ID (e.g., LPG-KNP-01429)"
    )
    name = models.CharField(
        max_length=150,
        db_index=True,
        help_text="Full legal name of the registered consumer"
    )
    phone = models.CharField(
        max_length=15,
        db_index=True,
        help_text="10-digit mobile number for SMS dispatch alerts"
    )
    region = models.CharField(
        max_length=60,
        choices=REGION_CHOICES,
        default='Kanpur Nagar',
        db_index=True,
        help_text="Operational delivery zone / municipal territory"
    )
    address = models.TextField(
        help_text="Primary delivery address with mohalla/colony/village details"
    )
    landmark = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Identifiable local landmark (e.g. Near Shiv Mandir, Opp Chauraha)"
    )
    pincode = models.CharField(
        max_length=10,
        default='208001',
        db_index=True,
        help_text="6-digit Indian Postal PIN Code"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        db_index=True,
        help_text="Account standing: ACTIVE, INACTIVE, or SUSPENDED"
    )
    connection_type = models.CharField(
        max_length=40,
        choices=CONNECTION_CHOICES,
        default='DOMESTIC_SINGLE',
        help_text="Category of connection"
    )
    aadhaar_linked = models.BooleanField(
        default=True,
        help_text="PAHAL / DBTL Direct Benefit Transfer link status"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "LPG Consumer"
        verbose_name_plural = "LPG Consumers"
        ordering = ['-created_at']
        indexes = [
            # High-performance compound indexes for search across 22,000+ consumers
            models.Index(fields=['region', 'status'], name='idx_cons_region_status'),
            models.Index(fields=['phone', 'status'], name='idx_cons_phone_status'),
            models.Index(fields=['name', 'region'], name='idx_cons_name_region'),
            models.Index(fields=['pincode', 'region'], name='idx_cons_pin_region'),
        ]

    def __str__(self):
        return f"{self.consumer_id} - {self.name} ({self.region})"

    def to_dict(self):
        """Standardized JSON serialization dictionary."""
        return {
            'id': self.id,
            'consumer_id': self.consumer_id,
            'name': self.name,
            'phone': self.phone,
            'region': self.region,
            'address': self.address,
            'landmark': self.landmark or '',
            'pincode': self.pincode,
            'status': self.status,
            'connection_type': self.get_connection_type_display(),
            'connection_type_code': self.connection_type,
            'aadhaar_linked': self.aadhaar_linked,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
        }


class CylinderStock(models.Model):
    """
    Inventory model tracking plant and godown physical stock levels.
    """
    CYLINDER_CHOICES = [
        ('14.2kg Domestic', '14.2kg Domestic Refill'),
        ('19kg Commercial', '19kg Commercial Jumbo'),
        ('5kg Mini', '5kg Free Trade Mini / FTL'),
    ]

    cylinder_type = models.CharField(
        max_length=60,
        unique=True,
        choices=CYLINDER_CHOICES,
        help_text="Standard cylinder capacity and variant"
    )
    total_quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total physical cylinders in agency godown (filled + empty)"
    )
    available_quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Filled, safety-inspected cylinders ready for immediate delivery"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Retail selling price per cylinder refill in INR (₹)"
    )
    subsidy_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Direct Benefit Subsidy credited to consumer bank account in INR (₹)"
    )
    low_stock_threshold = models.PositiveIntegerField(
        default=100,
        help_text="Inventory threshold triggering reorder warnings"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cylinder Inventory"
        verbose_name_plural = "Cylinder Inventories"
        ordering = ['cylinder_type']

    def __str__(self):
        return f"{self.cylinder_type} - {self.available_quantity}/{self.total_quantity} Filled @ ₹{self.price}"

    @property
    def reserved_quantity(self):
        """Cylinders currently in transit or earmarked for booked orders."""
        return max(0, self.total_quantity - self.available_quantity)

    @property
    def stock_percentage(self):
        """Percentage of total stock ready for immediate dispatch."""
        if self.total_quantity == 0:
            return 0.0
        return round((self.available_quantity / self.total_quantity) * 100, 1)

    @property
    def is_low_stock(self):
        """Boolean indicator for replenishment alert."""
        return self.available_quantity <= self.low_stock_threshold

    def to_dict(self):
        return {
            'id': self.id,
            'cylinder_type': self.cylinder_type,
            'total_quantity': self.total_quantity,
            'available_quantity': self.available_quantity,
            'reserved_quantity': self.reserved_quantity,
            'stock_percentage': self.stock_percentage,
            'price': float(self.price),
            'subsidy_amount': float(self.subsidy_amount),
            'low_stock_threshold': self.low_stock_threshold,
            'is_low_stock': self.is_low_stock,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else '',
        }


class DeliveryRoute(models.Model):
    """
    Logistics Route model grouping deliveries geographically for daily agency dispatch vans.
    """
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled / Loading'),
        ('IN_TRANSIT', 'In Transit / Dispatched'),
        ('COMPLETED', 'Delivered & Reconciled'),
        ('DELAYED', 'Delayed / Bad Weather'),
    ]

    route_name = models.CharField(
        max_length=150,
        db_index=True,
        help_text="Route designation (e.g., Kanpur South - Kidwai Nagar Sector 2)"
    )
    region = models.CharField(
        max_length=60,
        default='Kanpur Nagar',
        db_index=True,
        help_text="Zone covered by this vehicle run"
    )
    delivery_agent = models.CharField(
        max_length=120,
        help_text="Designated delivery executive / driver name"
    )
    agent_phone = models.CharField(
        max_length=15,
        blank=True,
        default='',
        help_text="Contact number of delivery agent"
    )
    vehicle_number = models.CharField(
        max_length=30,
        blank=True,
        default='',
        help_text="Vehicle registration (e.g. UP-78-BT-4921)"
    )
    assigned_consumers = models.PositiveIntegerField(
        default=0,
        help_text="Count of consumer cylinder drop-offs assigned on this route"
    )
    date = models.DateField(
        db_index=True,
        help_text="Delivery schedule run date"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED',
        db_index=True
    )
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Delivery Route"
        verbose_name_plural = "Delivery Routes"
        ordering = ['-date', 'route_name']
        indexes = [
            models.Index(fields=['date', 'status'], name='idx_route_date_status'),
            models.Index(fields=['region', 'date'], name='idx_route_region_date'),
        ]

    def __str__(self):
        return f"{self.route_name} | {self.delivery_agent} ({self.date}) [{self.status}]"

    def to_dict(self):
        return {
            'id': self.id,
            'route_name': self.route_name,
            'region': self.region,
            'delivery_agent': self.delivery_agent,
            'agent_phone': self.agent_phone,
            'vehicle_number': self.vehicle_number,
            'assigned_consumers': self.assigned_consumers,
            'date': self.date.strftime('%Y-%m-%d') if self.date else '',
            'status': self.status,
            'notes': self.notes,
        }


class Order(models.Model):
    """
    Core Order Transaction model connecting Consumer, Cylinder Variant, and Logistics Route.
    """
    DELIVERY_STATUS_CHOICES = [
        ('BOOKED', 'Booked / Confirmed'),
        ('DISPATCHED', 'Dispatched / In Van'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Successfully Delivered'),
        ('CANCELLED', 'Cancelled / Refused'),
    ]

    PAYMENT_CHOICES = [
        ('CASH_ON_DELIVERY', 'Cash on Delivery (COD)'),
        ('UPI_ONLINE', 'UPI (Google Pay / PhonePe / Paytm)'),
        ('AGENCY_COUNTER', 'Prepaid at Agency Counter'),
    ]

    order_id = models.CharField(
        max_length=35,
        unique=True,
        db_index=True,
        help_text="Unique booking receipt ID (e.g., ORD-202610-91283)"
    )
    consumer = models.ForeignKey(
        Consumer,
        on_delete=models.CASCADE,
        related_name='orders',
        db_index=True,
        help_text="Registered consumer making the booking"
    )
    cylinder_type = models.ForeignKey(
        CylinderStock,
        on_delete=models.PROTECT,
        related_name='orders',
        db_index=True,
        help_text="Cylinder stock category"
    )
    route = models.ForeignKey(
        DeliveryRoute,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        help_text="Assigned dispatch van route"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Number of cylinder refills requested"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per cylinder at the time of booking in INR (₹)"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_index=True,
        help_text="Total payable invoice amount in INR (₹)"
    )
    delivery_status = models.CharField(
        max_length=25,
        choices=DELIVERY_STATUS_CHOICES,
        default='BOOKED',
        db_index=True
    )
    payment_status = models.CharField(
        max_length=30,
        choices=PAYMENT_CHOICES,
        default='CASH_ON_DELIVERY'
    )
    payment_reference = models.CharField(
        max_length=60,
        blank=True,
        default='',
        help_text="UPI transaction reference / UTR or receipt number"
    )
    delivery_dac = models.CharField(
        max_length=6,
        blank=True,
        default='',
        help_text="4 or 6-digit Delivery Authentication Code (DAC OTP)"
    )
    notes = models.TextField(blank=True, default='')
    booking_date = models.DateTimeField(auto_now_add=True, db_index=True)
    delivery_date = models.DateField(null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "LPG Cylinder Booking"
        verbose_name_plural = "LPG Cylinder Bookings"
        ordering = ['-booking_date']
        indexes = [
            # High frequency dashboard and reporting indexes
            models.Index(fields=['delivery_status', 'booking_date'], name='idx_ord_status_date'),
            models.Index(fields=['consumer', 'delivery_status'], name='idx_ord_consumer_status'),
            models.Index(fields=['booking_date', 'total_price'], name='idx_ord_date_price'),
        ]

    def __str__(self):
        return f"{self.order_id} | {self.consumer.name} ({self.cylinder_type.cylinder_type}) - ₹{self.total_price}"

    def save(self, *args, **kwargs):
        # Auto-compute total price if not populated
        if not self.total_price and self.unit_price and self.quantity:
            self.total_price = self.unit_price * self.quantity
        # Auto-generate unique order receipt ID if missing
        if not self.order_id:
            self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'consumer_id': self.consumer.consumer_id,
            'consumer_name': self.consumer.name,
            'consumer_phone': self.consumer.phone,
            'consumer_region': self.consumer.region,
            'consumer_address': self.consumer.address,
            'cylinder_type': self.cylinder_type.cylinder_type,
            'cylinder_type_id': self.cylinder_type.id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'delivery_status': self.delivery_status,
            'delivery_status_display': self.get_delivery_status_display(),
            'payment_status': self.payment_status,
            'payment_status_display': self.get_payment_status_display(),
            'payment_reference': self.payment_reference,
            'delivery_dac': self.delivery_dac,
            'route_id': self.route.id if self.route else None,
            'route_name': self.route.route_name if self.route else 'Unassigned Depot Queue',
            'delivery_agent': self.route.delivery_agent if self.route else 'Unassigned',
            'agent_phone': self.route.agent_phone if self.route else '',
            'booking_date': self.booking_date.strftime('%Y-%m-%d %H:%M') if self.booking_date else '',
            'delivery_date': self.delivery_date.strftime('%Y-%m-%d') if self.delivery_date else '',
            'notes': self.notes,
        }
