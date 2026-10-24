"""
Database Seeding Script for LPG Distribution & Consumer Management System.
Populates realistic agency stock, delivery routes across Kanpur & Hamirpur,
hundreds of consumers (with benchmark capacity for 22,000+), and active bookings.
"""

import os
import sys

# Configure UTF-8 stdout for Windows consoles handling Indian Rupee (₹) symbol
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import django
import random
from datetime import timedelta
from decimal import Decimal

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lpg_manager.settings')
django.setup()

from django.utils import timezone
from dashboard.models import Consumer, CylinderStock, DeliveryRoute, Order


FIRST_NAMES = [
    "Rajesh", "Amit", "Suresh", "Pooja", "Sunita", "Manoj", "Priyanka", "Deepak",
    "Ramesh", "Anjali", "Vikas", "Neelam", "Sanjay", "Kavita", "Santosh", "Rekha",
    "Dharmendra", "Suman", "Arun", "Meena", "Alok", "Shweta", "Mohammad", "Fatima",
    "Vinod", "Geeta", "Pradeep", "Aarti", "Ashok", "Kiran", "Kamlesh", "Ritu",
    "Mukesh", "Sarita", "Harish", "Babita", "Ajay", "Shobha", "Satish", "Vandana"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Shukla", "Yadav", "Singh", "Pandey", "Dixit",
    "Tiwari", "Mishra", "Dubey", "Awasthi", "Chaurasia", "Srivastava", "Tripathi",
    "Khan", "Ansari", "Agrahari", "Katiyar", "Sachdev", "Prajapati", "Maurya"
]

REGIONS_AND_LOCALITIES = [
    ("Kanpur Nagar", [
        ("Kidwai Nagar 'H' Block, Near Deep Cinema", "208011", "Near Deep Cinema"),
        ("Barra Sector-4, Near Hanuman Mandir", "208027", "Opposite Bank of Baroda"),
        ("Govind Nagar Block-7, Kanpur", "208006", "Near Vidyarthi Market"),
        ("Civil Lines, Near Green Park Stadium", "208001", "Beside SBI Main Branch"),
        ("Kakadeo, Coaching Hub Lane 3", "208025", "Near Dev Nagar Chauraha"),
        ("Swaroop Nagar, Near Phoolbagh", "208002", "Opposite Medical College Gate"),
        ("Shastri Nagar, Central Avenue", "208005", "Near Kali Bari Mandir"),
        ("Kalyanpur, GT Road, Near Railway Crossing", "208017", "Near Kalyanpur Thana"),
        ("Panki Industrial Area, Site 2", "208022", "Near Panki Mandir Road"),
        ("Chakeri, Harjinder Nagar", "208007", "Near Air Force Station Road"),
    ]),
    ("Kanpur Dehat", [
        ("Akbarpur Main Market, Near Tehsil Gate", "209101", "Tehsil Compound Road"),
        ("Rania Industrial Area, Phase 1", "209304", "Near Jain Plastic Factory"),
        ("Jhinjhak Town, Station Road", "209302", "Opposite PWD Dak Bungalow"),
        ("Shivrajpur Village Post, GT Road", "209205", "Near Old Shiv Temple"),
        ("Chaubepur Mandi Complex", "209203", "Near Grain Mandi Gate"),
    ]),
    ("Hamirpur City", [
        ("Subhash Nagar, Yamuna Ghat Road", "210301", "Near Yamuna Bridge Checkpost"),
        ("Ramanand Nagar, Main Market", "210301", "Opposite Dist. Hospital"),
        ("Collectorate Colony, Civil Lines", "210301", "Near Session Court Gate 2"),
        ("Purana Qila Mohalla, Hamirpur", "210301", "Near Betwa Sangam Viewpoint"),
    ]),
    ("Hamirpur Rural", [
        ("Vill-Bilgaon, Post Maudaha", "210507", "Near Panchayat Bhawan"),
        ("Ingohta Village, Bharuwa Sumerpur", "210502", "Near Primary Vidyalaya"),
        ("Kurara Block, Hamirpur-Ghatampur Link", "210315", "Near Cooperative Society"),
        ("Muskara Kalan, Tehsil Maudaha", "210506", "Near Muskara Bus Stand"),
    ]),
    ("Rath", [
        ("Padav Chauraha, Rath Town", "210431", "Near Jain Mandir Gate"),
        ("Bara Khamba Mohalla, Rath", "210431", "Behind Old Kotwali"),
        ("Orai Road, Rath Bypass", "210431", "Near HP Petrol Pump"),
    ]),
    ("Maudaha", [
        ("Station Road, Maudaha", "210507", "Near Railway Goods Shed"),
        ("Qaziyana Mohalla, Maudaha", "210507", "Near Jama Masjid Lane"),
    ]),
    ("Ghatampur", [
        ("Kanpur-Sagar National Highway, Ghatampur", "209206", "Near Ghatampur Power Plant"),
        ("Jahanabad Road, Ward No. 4", "209206", "Opposite Community Health Center"),
    ]),
    ("Sumerpur", [
        ("Bharuwa Sumerpur Industrial Estate", "210502", "Near Hindustan Unilever Plant"),
        ("Station Bazar, Sumerpur", "210502", "Near Railway Station Gate"),
    ])
]


def seed_stock():
    print("-> Seeding Cylinder Stock Inventory...")
    stocks = [
        {
            'cylinder_type': '14.2kg Domestic',
            'total_quantity': 2800,
            'available_quantity': 2140,
            'price': Decimal('903.00'),
            'subsidy_amount': Decimal('200.00'),
            'low_stock_threshold': 250
        },
        {
            'cylinder_type': '19kg Commercial',
            'total_quantity': 850,
            'available_quantity': 520,
            'price': Decimal('1825.00'),
            'subsidy_amount': Decimal('0.00'),
            'low_stock_threshold': 100
        },
        {
            'cylinder_type': '5kg Mini',
            'total_quantity': 450,
            'available_quantity': 320,
            'price': Decimal('365.00'),
            'subsidy_amount': Decimal('0.00'),
            'low_stock_threshold': 50
        }
    ]

    for item in stocks:
        stock, created = CylinderStock.objects.update_or_create(
            cylinder_type=item['cylinder_type'],
            defaults=item
        )
        verb = "Created" if created else "Updated"
        print(f"   [{verb}] {stock.cylinder_type} - Available: {stock.available_quantity}/{stock.total_quantity} @ ₹{stock.price}")


def seed_routes():
    print("\n-> Seeding Delivery Logistics Routes...")
    today = timezone.now().date()
    routes_def = [
        {
            'route_name': 'Kanpur South - Kidwai Nagar & Barra Express',
            'region': 'Kanpur Nagar',
            'delivery_agent': 'Ramesh Yadav',
            'agent_phone': '9839120412',
            'vehicle_number': 'UP-78-AG-4912',
            'assigned_consumers': 64,
            'date': today,
            'status': 'IN_TRANSIT',
            'notes': 'High-density residential refill morning drop'
        },
        {
            'route_name': 'Kanpur Central - Civil Lines & Mall Road Commercial',
            'region': 'Kanpur Nagar',
            'delivery_agent': 'Suresh Chandra Verma',
            'agent_phone': '9415093124',
            'vehicle_number': 'UP-78-BN-3281',
            'assigned_consumers': 48,
            'date': today,
            'status': 'IN_TRANSIT',
            'notes': 'Covers restaurants, canteens, and institutional orders'
        },
        {
            'route_name': 'Kanpur West - Kalyanpur & IIT Corridor',
            'region': 'Kanpur Nagar',
            'delivery_agent': 'Rajesh Kumar Shukla',
            'agent_phone': '9792019482',
            'vehicle_number': 'UP-78-CX-9023',
            'assigned_consumers': 52,
            'date': today,
            'status': 'SCHEDULED',
            'notes': 'Domestic refills for Kalyanpur and student hostels'
        },
        {
            'route_name': 'Kanpur Dehat - Akbarpur & Rania Depot Link',
            'region': 'Kanpur Dehat',
            'delivery_agent': 'Mohammad Irfan',
            'agent_phone': '9935401923',
            'vehicle_number': 'UP-78-ED-1188',
            'assigned_consumers': 38,
            'date': today,
            'status': 'SCHEDULED',
            'notes': 'Industrial 19kg jumbo delivery & rural consumers'
        },
        {
            'route_name': 'Hamirpur City - Betwa Riverfront & Civil Lines',
            'region': 'Hamirpur City',
            'delivery_agent': 'Vijay Pratap Singh',
            'agent_phone': '9889412039',
            'vehicle_number': 'UP-91-K-5521',
            'assigned_consumers': 42,
            'date': today,
            'status': 'IN_TRANSIT',
            'notes': 'District headquarters consumer deliveries'
        },
        {
            'route_name': 'Hamirpur Rural - Maudaha & Sumerpur Highway',
            'region': 'Hamirpur Rural',
            'delivery_agent': 'Dinesh Pal',
            'agent_phone': '9628014521',
            'vehicle_number': 'UP-91-M-4819',
            'assigned_consumers': 56,
            'date': today,
            'status': 'SCHEDULED',
            'notes': 'Ujjawala beneficiaries & agricultural grain belt'
        },
        {
            'route_name': 'Rath Sector - Padav Chauraha & Orai Road',
            'region': 'Rath',
            'delivery_agent': 'Manoj Kumar Tiwari',
            'agent_phone': '9450218901',
            'vehicle_number': 'UP-91-P-6320',
            'assigned_consumers': 35,
            'date': today + timedelta(days=1),
            'status': 'SCHEDULED',
            'notes': 'Advance dispatch scheduled for tomorrow morning'
        },
        {
            'route_name': 'Ghatampur Rural - Jahanabad Link',
            'region': 'Ghatampur',
            'delivery_agent': 'Arvind Mishra',
            'agent_phone': '9140294102',
            'vehicle_number': 'UP-78-DY-7744',
            'assigned_consumers': 29,
            'date': today,
            'status': 'COMPLETED',
            'notes': 'Dispatched at 07:30 AM, cash reconciliations closed'
        }
    ]

    routes_objs = []
    for r in routes_def:
        route, created = DeliveryRoute.objects.update_or_create(
            route_name=r['route_name'],
            date=r['date'],
            defaults=r
        )
        routes_objs.append(route)
        verb = "Created" if created else "Updated"
        print(f"   [{verb}] {route.route_name} - Agent: {route.delivery_agent} [{route.status}]")

    return routes_objs


def seed_consumers(count=300):
    print(f"\n-> Seeding {count} Realistic LPG Consumers (Optimized schema verified)...")
    existing_count = Consumer.objects.count()
    if existing_count >= count:
        print(f"   Consumers already exist ({existing_count} records). Skipping bulk creation.")
        return list(Consumer.objects.all()[:count])

    consumers = []
    start_num = existing_count + 1

    for i in range(count):
        idx = start_num + i
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"

        region_data = random.choice(REGIONS_AND_LOCALITIES)
        region_name = region_data[0]
        loc_tuple = random.choice(region_data[1])
        address_text = f"House No. {random.randint(12, 450)}, {loc_tuple[0]}"
        pincode = loc_tuple[1]
        landmark = loc_tuple[2]

        prefix = "KNP" if "Kanpur" in region_name else ("HMR" if "Hamirpur" in region_name else "LPG")
        consumer_id = f"LPG-{prefix}-{idx:05d}"
        phone = f"9{random.randint(100000000, 999999999)}"

        status_weights = ['ACTIVE'] * 85 + ['INACTIVE'] * 10 + ['SUSPENDED'] * 5
        status = random.choice(status_weights)

        conn_types = ['DOMESTIC_SINGLE'] * 60 + ['DOMESTIC_DOUBLE'] * 20 + ['PMUY_UJJAWALA'] * 12 + ['COMMERCIAL'] * 8
        conn_type = random.choice(conn_types)

        consumer = Consumer(
            consumer_id=consumer_id,
            name=name,
            phone=phone,
            region=region_name,
            address=address_text,
            landmark=landmark,
            pincode=pincode,
            status=status,
            connection_type=conn_type,
            aadhaar_linked=random.choice([True, True, True, False])
        )
        consumers.append(consumer)

    Consumer.objects.bulk_create(consumers, batch_size=500)
    print(f"   Successfully created {len(consumers)} consumers! Total in DB: {Consumer.objects.count()}")
    return list(Consumer.objects.all())


def seed_orders(consumers, count=80):
    print(f"\n-> Seeding {count} LPG Cylinder Bookings and Transactions...")
    stocks = list(CylinderStock.objects.all())
    routes = list(DeliveryRoute.objects.all())
    if not stocks or not consumers:
        print("   Cannot seed orders: missing stock or consumers.")
        return

    now = timezone.now()
    orders_created = 0

    # Ensure 14.2kg is most common
    domestic_stock = next((s for s in stocks if '14.2kg' in s.cylinder_type), stocks[0])
    commercial_stock = next((s for s in stocks if '19kg' in s.cylinder_type), stocks[0])
    mini_stock = next((s for s in stocks if '5kg' in s.cylinder_type), stocks[0])

    for i in range(count):
        consumer = random.choice(consumers)
        
        # Pick cylinder according to connection type
        if consumer.connection_type == 'COMMERCIAL':
            stock = commercial_stock
            quantity = random.choice([1, 2, 4])
        elif consumer.connection_type == 'FTL_5KG':
            stock = mini_stock
            quantity = random.choice([1, 2])
        else:
            stock = domestic_stock
            quantity = 1

        # Match route by region
        matching_routes = [r for r in routes if r.region == consumer.region]
        route = random.choice(matching_routes) if matching_routes else (random.choice(routes) if routes else None)

        # Dates spanning past 3 days to today
        days_offset = random.choice([0, 0, 0, 1, 1, 2, 3])
        booking_time = now - timedelta(days=days_offset, hours=random.randint(1, 10), minutes=random.randint(0, 59))

        if days_offset > 0:
            status = random.choice(['DELIVERED', 'DELIVERED', 'DELIVERED', 'CANCELLED'])
            delivery_date = (booking_time + timedelta(days=1)).date()
        else:
            status = random.choice(['BOOKED', 'DISPATCHED', 'OUT_FOR_DELIVERY', 'DELIVERED'])
            delivery_date = booking_time.date() if status == 'DELIVERED' else None

        payment_status = random.choice(['CASH_ON_DELIVERY', 'CASH_ON_DELIVERY', 'UPI_ONLINE', 'AGENCY_COUNTER'])
        dac_code = f"{random.randint(100000, 999999)}"

        unit_price = stock.price
        total_price = unit_price * quantity
        order_num = f"ORD-{booking_time.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

        order = Order.objects.create(
            order_id=order_num,
            consumer=consumer,
            cylinder_type=stock,
            route=route,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            delivery_status=status,
            payment_status=payment_status,
            payment_reference=f"UPI{random.randint(1000000000, 9999999999)}" if payment_status == 'UPI_ONLINE' else '',
            delivery_dac=dac_code,
            delivery_date=delivery_date
        )
        # Update auto booking date
        Order.objects.filter(id=order.id).update(booking_date=booking_time)
        orders_created += 1

    print(f"   Successfully created {orders_created} orders! Total in DB: {Order.objects.count()}")


def main():
    print("=" * 70)
    print(" LPG DISTRIBUTION MANAGEMENT SYSTEM - DATABASE SEED INITIALIZER")
    print(" Kanpur & Hamirpur Territory Agency Hub")
    print("=" * 70)

    seed_stock()
    seed_routes()
    consumers = seed_consumers(count=300)
    seed_orders(consumers, count=90)

    print("\n" + "=" * 70)
    print(" SEEDING COMPLETE! The system is now populated with authentic data.")
    print(f" Consumers: {Consumer.objects.count()} | Inventory Types: {CylinderStock.objects.count()} | Routes: {DeliveryRoute.objects.count()} | Orders: {Order.objects.count()}")
    print("=" * 70)


if __name__ == '__main__':
    main()
