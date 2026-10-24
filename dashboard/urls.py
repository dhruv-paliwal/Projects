"""
URL routing configuration for dashboard app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Frontend SPA entry point
    path('', views.index_view, name='index'),

    # JSON API Endpoints
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/consumers/', views.api_consumers, name='api_consumers'),
    path('api/stock/', views.api_stock, name='api_stock'),
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/orders/<str:order_id>/status/', views.api_update_order_status, name='api_update_order_status'),
    path('api/routes/', views.api_routes, name='api_routes'),
]
