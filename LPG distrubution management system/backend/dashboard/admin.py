"""
Django Admin Configuration for LPG Distribution Dashboard.
"""

from django.contrib import admin
from .models import Consumer, CylinderStock, DeliveryRoute, Order


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('consumer_id', 'name', 'phone', 'region', 'status', 'connection_type', 'created_at')
    list_filter = ('status', 'region', 'connection_type', 'aadhaar_linked')
    search_fields = ('consumer_id', 'name', 'phone', 'address', 'landmark')
    ordering = ('-created_at',)
    list_per_page = 50


@admin.register(CylinderStock)
class CylinderStockAdmin(admin.ModelAdmin):
    list_display = ('cylinder_type', 'available_quantity', 'total_quantity', 'stock_percentage', 'price', 'subsidy_amount', 'updated_at')
    list_editable = ('available_quantity', 'total_quantity', 'price')


@admin.register(DeliveryRoute)
class DeliveryRouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'region', 'delivery_agent', 'vehicle_number', 'assigned_consumers', 'date', 'status')
    list_filter = ('status', 'region', 'date')
    search_fields = ('route_name', 'delivery_agent', 'vehicle_number')
    ordering = ('-date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'consumer', 'cylinder_type', 'quantity', 'total_price', 'delivery_status', 'payment_status', 'booking_date')
    list_filter = ('delivery_status', 'payment_status', 'booking_date', 'cylinder_type')
    search_fields = ('order_id', 'consumer__name', 'consumer__consumer_id', 'consumer__phone')
    ordering = ('-booking_date',)
    list_per_page = 50
