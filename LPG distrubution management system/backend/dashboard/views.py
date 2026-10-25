"""
Views and API Endpoints for LPG Distribution & Consumer Management Dashboard.
MVT Pattern: Serves the bespoke AngularJS SPA template and returns robust JSON APIs.
"""

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
import json
import random
from decimal import Decimal

from .models import Consumer, CylinderStock, DeliveryRoute, Order


def index_view(request):
    """
    Renders the Single-Page Application (SPA) entry point template.
    Passes agency contextual metadata for initial render.
    """
    today = timezone.now().date()
    stats = {
        'total_consumers': Consumer.objects.count(),
        'total_stock_available': CylinderStock.objects.aggregate(total=Sum('available_quantity'))['total'] or 0,
        'today_bookings': Order.objects.filter(booking_date__date=today).count(),
        'pending_deliveries': Order.objects.filter(delivery_status__in=['BOOKED', 'DISPATCHED', 'OUT_FOR_DELIVERY']).count(),
        'agency_name': 'Shree Ganesh LPG Agency (Kanpur & Hamirpur Territory)',
        'agency_code': 'UP-KNP-78401',
    }
    return render(request, 'index.html', {'initial_stats': stats})


@require_http_methods(["GET"])
def api_stats(request):
    """
    GET /api/stats/
    Returns high-level operational KPIs for dashboard headers and metric badges.
    """
    today = timezone.now().date()
    
    total_consumers = Consumer.objects.count()
    active_consumers = Consumer.objects.filter(status='ACTIVE').count()
    
    stock_agg = CylinderStock.objects.aggregate(
        total_godown=Sum('total_quantity'),
        total_avail=Sum('available_quantity')
    )
    total_godown = stock_agg['total_godown'] or 0
    total_available = stock_agg['total_avail'] or 0
    total_reserved = max(0, total_godown - total_available)
    
    today_orders = Order.objects.filter(booking_date__date=today)
    today_bookings_count = today_orders.count()
    today_revenue = today_orders.exclude(delivery_status='CANCELLED').aggregate(
        rev=Sum('total_price')
    )['rev'] or Decimal('0.00')
    
    pending_deliveries = Order.objects.filter(
        delivery_status__in=['BOOKED', 'DISPATCHED', 'OUT_FOR_DELIVERY']
    ).count()
    
    delivered_today = today_orders.filter(delivery_status='DELIVERED').count()
    active_routes = DeliveryRoute.objects.filter(date=today).count()
    
    # Low stock alerts count
    low_stock_alerts = sum(1 for s in CylinderStock.objects.all() if s.is_low_stock)

    return JsonResponse({
        'status': 'success',
        'metrics': {
            'total_consumers': total_consumers,
            'active_consumers': active_consumers,
            'total_godown_stock': total_godown,
            'total_available_stock': total_available,
            'total_reserved_stock': total_reserved,
            'today_bookings': today_bookings_count,
            'today_revenue': float(today_revenue),
            'pending_deliveries': pending_deliveries,
            'delivered_today': delivered_today,
            'active_routes': active_routes,
            'low_stock_alerts': low_stock_alerts,
        }
    })


@require_http_methods(["GET"])
def api_consumers(request):
    """
    GET /api/consumers/
    List and search consumers.
    Optimized for high volume (22,000+ consumers) via database indexing and pagination.
    Query params:
      - q: Search string (matches consumer_id, name, phone, address, landmark)
      - region: Filter by region name
      - status: Filter by ACTIVE, INACTIVE, SUSPENDED
      - page: Page number (default 1)
      - page_size: Items per page (default 20, max 100)
    """
    query = request.GET.get('q', '').strip()
    region = request.GET.get('region', '').strip()
    status = request.GET.get('status', '').strip()
    page = request.GET.get('page', 1)
    page_size = min(int(request.GET.get('page_size', 20)), 100)

    consumers_qs = Consumer.objects.all()

    if status:
        consumers_qs = consumers_qs.filter(status=status)
    if region and region != 'ALL':
        consumers_qs = consumers_qs.filter(region=region)
    if query:
        consumers_qs = consumers_qs.filter(
            Q(consumer_id__icontains=query) |
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(address__icontains=query) |
            Q(landmark__icontains=query)
        )

    total_count = consumers_qs.count()
    paginator = Paginator(consumers_qs, page_size)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    consumer_list = [c.to_dict() for c in page_obj.object_list]

    return JsonResponse({
        'status': 'success',
        'total_count': total_count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'page_size': page_size,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'consumers': consumer_list
    })


@require_http_methods(["GET"])
def api_stock(request):
    """
    GET /api/stock/
    Check current cylinder inventory across domestic and commercial variants.
    """
    stocks = CylinderStock.objects.all().order_by('cylinder_type')
    stock_data = [s.to_dict() for s in stocks]

    total_godown = sum(s['total_quantity'] for s in stock_data)
    total_available = sum(s['available_quantity'] for s in stock_data)
    total_reserved = sum(s['reserved_quantity'] for s in stock_data)

    return JsonResponse({
        'status': 'success',
        'stocks': stock_data,
        'summary': {
            'total_godown_stock': total_godown,
            'total_available_stock': total_available,
            'total_reserved_stock': total_reserved,
            'overall_health_percentage': round((total_available / total_godown * 100), 1) if total_godown > 0 else 0
        }
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_orders(request):
    """
    GET /api/orders/ - List recent orders with pagination and status filtering
    POST /api/orders/ - Atomically create a new cylinder booking and update stock
    """
    if request.method == "GET":
        status_filter = request.GET.get('status', '').strip()
        search_query = request.GET.get('q', '').strip()
        page = request.GET.get('page', 1)
        page_size = min(int(request.GET.get('page_size', 20)), 100)

        orders_qs = Order.objects.select_related('consumer', 'cylinder_type', 'route').all()

        if status_filter and status_filter != 'ALL':
            orders_qs = orders_qs.filter(delivery_status=status_filter)
        if search_query:
            orders_qs = orders_qs.filter(
                Q(order_id__icontains=search_query) |
                Q(consumer__name__icontains=search_query) |
                Q(consumer__consumer_id__icontains=search_query) |
                Q(consumer__phone__icontains=search_query)
            )

        total_count = orders_qs.count()
        paginator = Paginator(orders_qs, page_size)

        try:
            page_obj = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        orders_list = [o.to_dict() for o in page_obj.object_list]

        return JsonResponse({
            'status': 'success',
            'total_count': total_count,
            'num_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'orders': orders_list
        })

    # POST - Create new booking
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Invalid JSON payload: {str(e)}'}, status=400)

    consumer_ref = data.get('consumer_id') or data.get('consumer_pk')
    cylinder_type_id = data.get('cylinder_type_id') or data.get('cylinder_type')
    quantity = int(data.get('quantity', 1))
    payment_status = data.get('payment_status', 'CASH_ON_DELIVERY')
    payment_reference = data.get('payment_reference', '').strip()
    notes = data.get('notes', '').strip()

    if not consumer_ref:
        return JsonResponse({'status': 'error', 'message': 'Consumer identification is required.'}, status=400)
    if not cylinder_type_id:
        return JsonResponse({'status': 'error', 'message': 'Cylinder type selection is required.'}, status=400)
    if quantity <= 0:
        return JsonResponse({'status': 'error', 'message': 'Booking quantity must be at least 1.'}, status=400)

    # Locate Consumer
    try:
        if str(consumer_ref).isdigit():
            consumer = Consumer.objects.filter(Q(id=int(consumer_ref)) | Q(consumer_id=str(consumer_ref))).first()
        else:
            consumer = Consumer.objects.filter(consumer_id=str(consumer_ref).strip()).first()
        if not consumer:
            return JsonResponse({'status': 'error', 'message': f'Consumer not found for reference "{consumer_ref}".'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error locating consumer: {str(e)}'}, status=400)

    # Atomic Booking Transaction with select_for_update to protect inventory
    try:
        with transaction.atomic():
            # Retrieve cylinder stock with row lock
            if str(cylinder_type_id).isdigit():
                stock = CylinderStock.objects.select_for_update().filter(id=int(cylinder_type_id)).first()
            else:
                stock = CylinderStock.objects.select_for_update().filter(cylinder_type=str(cylinder_type_id)).first()

            if not stock:
                return JsonResponse({'status': 'error', 'message': 'Specified cylinder type was not found.'}, status=404)

            # Check stock availability
            if stock.available_quantity < quantity:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Insufficient physical stock for {stock.cylinder_type}. Only {stock.available_quantity} available in godown.'
                }, status=400)

            # Deduct inventory atomically
            stock.available_quantity -= quantity
            stock.save(update_fields=['available_quantity', 'updated_at'])

            # Automatically match route for consumer's territory
            today = timezone.now().date()
            route = DeliveryRoute.objects.filter(
                region=consumer.region,
                date__gte=today,
                status__in=['SCHEDULED', 'IN_TRANSIT']
            ).order_by('date').first()

            if route:
                route.assigned_consumers += quantity
                route.save(update_fields=['assigned_consumers'])

            # Generate 6-digit Delivery Authentication Code (DAC OTP)
            dac_otp = f"{random.randint(100000, 999999)}"

            # Compute invoice price
            unit_price = stock.price
            total_price = unit_price * quantity

            order = Order.objects.create(
                consumer=consumer,
                cylinder_type=stock,
                route=route,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                delivery_status='BOOKED',
                payment_status=payment_status,
                payment_reference=payment_reference,
                delivery_dac=dac_otp,
                notes=notes
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Booking confirmed for {consumer.name}! DAC Code: {dac_otp}',
                'order': order.to_dict(),
                'updated_stock': stock.to_dict()
            }, status=201)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Transaction failed: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def api_routes(request):
    """
    GET /api/routes/
    Fetch delivery routes with agent details, vehicle registrations, and assigned consumer counts.
    """
    region = request.GET.get('region', '').strip()
    status = request.GET.get('status', '').strip()

    routes_qs = DeliveryRoute.objects.all().order_by('-date', 'route_name')

    if region and region != 'ALL':
        routes_qs = routes_qs.filter(region=region)
    if status and status != 'ALL':
        routes_qs = routes_qs.filter(status=status)

    routes_list = [r.to_dict() for r in routes_qs]

    return JsonResponse({
        'status': 'success',
        'count': len(routes_list),
        'routes': routes_list
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_update_order_status(request, order_id):
    """
    POST /api/orders/<order_id>/status/
    Update order status (e.g. from BOOKED -> DISPATCHED -> DELIVERED).
    Handles stock replenishment if cancelled.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = {}

    new_status = data.get('status')
    if not new_status or new_status not in dict(Order.DELIVERY_STATUS_CHOICES):
        return JsonResponse({'status': 'error', 'message': 'Valid delivery status is required.'}, status=400)

    try:
        with transaction.atomic():
            order = Order.objects.select_for_update().filter(Q(id=order_id) | Q(order_id=order_id)).first()
            if not order:
                return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)

            old_status = order.delivery_status
            order.delivery_status = new_status

            if new_status == 'DELIVERED':
                order.delivery_date = timezone.now().date()
            elif new_status == 'CANCELLED' and old_status != 'CANCELLED':
                # Restore stock if cancelled
                stock = CylinderStock.objects.select_for_update().filter(id=order.cylinder_type_id).first()
                if stock:
                    stock.available_quantity += order.quantity
                    stock.save(update_fields=['available_quantity', 'updated_at'])

            order.save()
            return JsonResponse({
                'status': 'success',
                'message': f'Order {order.order_id} status updated to {order.get_delivery_status_display()}',
                'order': order.to_dict()
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
