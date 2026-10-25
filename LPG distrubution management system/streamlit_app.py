"""
LPG Distribution & Consumer Management Dashboard - Streamlit Deployment Interface
Bespoke Indian Enterprise Design with Warm Palette (Terracotta Red, Deep Saffron, Turmeric Yellow).
Queries Django ORM / MySQL Database for high-speed reporting, analytics, and operational tracking.
"""

import os
import sys
import datetime
from decimal import Decimal

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Configure Django environment to access ORM directly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lpg_manager.settings')
import django
django.setup()

import streamlit as st
import pandas as pd
from django.db.models import Sum, Count, Q
from django.utils import timezone

from dashboard.models import Consumer, CylinderStock, DeliveryRoute, Order

# Page Configuration
st.set_page_config(
    page_title="LPG Distribution & Consumer Command Center",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Warm Indian Palette CSS Injections
CUSTOM_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700&display=swap');

  :root {
    --terracotta-red: #E2725B;
    --terracotta-hover: #D05E47;
    --deep-saffron: #FF9933;
    --turmeric-yellow: #FFC000;
    --bg-cream: #FAFAFA;
    --text-primary: #181514;
    --text-secondary: #3A3432;
    --border-warm: #E5DDD5;
  }

  /* Global page background and typography - High Contrast Text */
  .stApp {
    background-color: var(--bg-cream) !important;
    font-family: 'Inter', sans-serif !important;
    color: #181514 !important;
  }

  /* Crisp readable dark text for standard Streamlit components */
  div[data-testid="stMarkdownContainer"] p,
  div[data-testid="stMarkdownContainer"] span,
  div[data-testid="stCaptionContainer"] p,
  div[data-testid="stText"] p,
  .stRadio label span,
  .stSelectbox label p,
  .stTextInput label p,
  .stNumberInput label p,
  .stTextArea label p {
    color: #181514 !important;
    font-weight: 500 !important;
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    color: #120F0E !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
  }

  /* Bespoke Top Header Banner - High Contrast Warm Indian Enterprise */
  .agency-header-banner {
    background: #FFFFFF !important;
    border: 1.5px solid #E2D9D0 !important;
    border-left: 6px solid #E2725B !important;
    border-top: 3.5px solid #FF9933 !important;
    border-radius: 12px !important;
    padding: 22px 28px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 4px 20px -2px rgba(90, 60, 40, 0.06), 0 2px 6px -1px rgba(90, 60, 40, 0.03) !important;
  }

  .agency-header-banner h2 {
    color: #120F0E !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    margin: 8px 0 4px 0 !important;
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.02em !important;
  }

  .agency-header-banner p {
    color: #3A322F !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
  }

  .agency-badge {
    background: #FFF4E5 !important;
    border: 1.5px solid #FF9933 !important;
    color: #B25300 !important;
    padding: 5px 12px !important;
    border-radius: 6px !important;
    font-weight: 800 !important;
    font-size: 0.85rem !important;
    display: inline-block !important;
  }

  .status-badge-online {
    background: #E8F5E9 !important;
    border: 1.5px solid #81C784 !important;
    color: #1B5E20 !important;
    padding: 6px 14px !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 7px !important;
  }

  .tech-badge {
    color: #5A504B !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    margin-top: 5px !important;
  }

  /* Metric cards */
  div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-warm) !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
    box-shadow: 0 2px 8px rgba(90, 60, 40, 0.04) !important;
    border-left: 4px solid var(--terracotta-red) !important;
  }

  div[data-testid="stMetricLabel"] p {
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
    color: #3A3432 !important;
  }

  div[data-testid="stMetricValue"] div {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    color: #120F0E !important;
  }

  div[data-testid="stMetricDelta"] span {
    color: #1E6E2E !important;
    font-weight: 600 !important;
  }

  /* Input fields and Selectboxes */
  .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
    color: #120F0E !important;
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-warm) !important;
    font-weight: 500 !important;
  }

  /* Buttons */
  .stButton > button {
    background-color: var(--terracotta-red) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--terracotta-red) !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 8px 18px !important;
    box-shadow: 0 2px 6px rgba(226, 114, 91, 0.25) !important;
    transition: all 0.2s ease !important;
  }

  .stButton > button * {
    color: #FFFFFF !important;
  }

  .stButton > button:hover {
    background-color: var(--terracotta-hover) !important;
    border-color: var(--terracotta-hover) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
  }

  /* Sidebar styling */
  section[data-testid="stSidebar"] {
    background-color: #F5EFEB !important;
    border-right: 1px solid var(--border-warm) !important;
  }

  section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label {
    color: #181514 !important;
    font-weight: 500 !important;
  }
    border-right: 1px solid var(--border-warm) !important;
  }

  /* Rupee highlighting */
  .rupee-amt {
    font-weight: 700;
    color: var(--terracotta-red);
  }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def format_inr(number):
    """Format number into Indian Rupee string with Rupee (₹) symbol."""
    if number is None:
        return "₹0.00"
    num = float(number)
    is_neg = num < 0
    num = abs(num)
    formatted = f"{num:,.2f}"
    return f"{'-' if is_neg else ''}₹{formatted}"


# Data Loading Functions with st.cache_data for speed
@st.cache_data(ttl=15)
def get_stock_data():
    stocks = list(CylinderStock.objects.all())
    data = []
    for s in stocks:
        data.append({
            'ID': s.id,
            'Cylinder Variant': s.cylinder_type,
            'Available (Filled)': s.available_quantity,
            'Reserved / Transit': s.reserved_quantity,
            'Total Godown Stock': s.total_quantity,
            'Price (INR)': float(s.price),
            'Price (Formatted)': format_inr(s.price),
            'Subsidy (INR)': float(s.subsidy_amount),
            'Subsidy (Formatted)': format_inr(s.subsidy_amount),
            'Availability %': s.stock_percentage,
            'Low Stock Alert': s.is_low_stock
        })
    return pd.DataFrame(data)


@st.cache_data(ttl=15)
def get_kpi_metrics():
    today = timezone.now().date()
    total_consumers = Consumer.objects.count()
    active_consumers = Consumer.objects.filter(status='ACTIVE').count()
    
    stock_agg = CylinderStock.objects.aggregate(
        tot=Sum('total_quantity'),
        avail=Sum('available_quantity')
    )
    tot_stock = stock_agg['tot'] or 0
    avail_stock = stock_agg['avail'] or 0
    
    today_orders = Order.objects.filter(booking_date__date=today)
    today_count = today_orders.count()
    today_rev = today_orders.exclude(delivery_status='CANCELLED').aggregate(r=Sum('total_price'))['r'] or Decimal('0.00')
    pending = Order.objects.filter(delivery_status__in=['BOOKED', 'DISPATCHED', 'OUT_FOR_DELIVERY']).count()
    delivered = today_orders.filter(delivery_status='DELIVERED').count()
    active_routes = DeliveryRoute.objects.filter(date=today).count()

    return {
        'total_consumers': total_consumers,
        'active_consumers': active_consumers,
        'total_stock': tot_stock,
        'available_stock': avail_stock,
        'today_bookings': today_count,
        'today_revenue': float(today_rev),
        'pending_deliveries': pending,
        'delivered_today': delivered,
        'active_routes': active_routes
    }


@st.cache_data(ttl=15)
def get_orders_df(limit=200):
    orders = Order.objects.select_related('consumer', 'cylinder_type', 'route').all()[:limit]
    data = []
    for o in orders:
        data.append({
            'Order Receipt': o.order_id,
            'Booking Time': o.booking_date.strftime('%Y-%m-%d %H:%M') if o.booking_date else '',
            'Consumer ID': o.consumer.consumer_id,
            'Consumer Name': o.consumer.name,
            'Mobile': o.consumer.phone,
            'Territory': o.consumer.region,
            'Cylinder': o.cylinder_type.cylinder_type,
            'Quantity': o.quantity,
            'Total Price': float(o.total_price),
            'Total Price (₹)': format_inr(o.total_price),
            'Delivery DAC': o.delivery_dac,
            'Status': o.get_delivery_status_display(),
            'Payment Mode': o.get_payment_status_display(),
            'Route': o.route.route_name if o.route else 'Direct Agency Counter'
        })
    return pd.DataFrame(data)


@st.cache_data(ttl=15)
def get_routes_df():
    routes = DeliveryRoute.objects.all().order_by('-date', 'route_name')
    data = []
    for r in routes:
        data.append({
            'Route Name': r.route_name,
            'Territory Region': r.region,
            'Delivery Agent': r.delivery_agent,
            'Driver Phone': r.agent_phone,
            'Vehicle Reg': r.vehicle_number,
            'Assigned Consumers': r.assigned_consumers,
            'Date': r.date.strftime('%Y-%m-%d') if r.date else '',
            'Status': r.get_status_display()
        })
    return pd.DataFrame(data)


# Top Agency Header Banner
st.markdown("""
<div class="agency-header-banner">
  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
    <div>
      <span class="agency-badge">अधिकृत एलपीजी वितरण केंद्र</span>
      <h2 style="color: #120F0E !important; margin: 8px 0 4px 0; font-weight: 800; font-family: 'Outfit', sans-serif;">Shree Ganesh LPG Agency Command Center</h2>
      <p style="color: #3A322F !important; margin: 0; font-size: 0.95rem; font-weight: 600;">Kanpur Nagar, Kanpur Dehat & Hamirpur Operational Jurisdiction | Agency Code: <strong style="color: #E2725B !important;">UP-KNP-78401</strong></p>
    </div>
    <div style="text-align: right;">
      <div class="status-badge-online">
        <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background-color: #2E7D32;"></span>
        <strong style="color: #1B5E20 !important;">Plant Depot Online (IST)</strong>
      </div>
      <div class="tech-badge" style="color: #5A504B !important; font-weight: 600; font-size: 0.82rem; margin-top: 5px;">Django ORM / MySQL Integration</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/10041/10041797.png", width=64)
st.sidebar.title("Agency Portal")
st.sidebar.markdown("**Kanpur & Hamirpur Territory**")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio(
    "Operational Navigation",
    ["Executive Dashboard", "Stock Overview", "Consumer Search", "Route Management", "Issue Refill Booking"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Agency Code: **UP-KNP-78401**")
st.sidebar.caption("Database: **MySQL (mysql-connector-python)**")
st.sidebar.caption(f"Last Refreshed: {timezone.now().strftime('%H:%M:%S IST')}")

if st.sidebar.button("🔄 Refresh Real-Time Data"):
    st.cache_data.clear()
    st.rerun()

# Global Top KPI Metrics Bar
kpi = get_kpi_metrics()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Consumers", f"{kpi['total_consumers']:,}", f"{kpi['active_consumers']:,} Active Accounts")
with col2:
    st.metric("Available Cylinders", f"{kpi['available_stock']:,}", f"Godown: {kpi['total_stock']:,}")
with col3:
    st.metric("Pending Deliveries", f"{kpi['pending_deliveries']:,}", f"{kpi['delivered_today']:,} Delivered Today")
with col4:
    st.metric("Today's Revenue", format_inr(kpi['today_revenue']), f"{kpi['today_bookings']} Refill Bookings")

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 1: EXECUTIVE DASHBOARD
# ==============================================================================
if nav_choice == "Executive Dashboard":
    st.subheader("📊 Operational Analytics & Supply Health")

    stock_df = get_stock_data()
    orders_df = get_orders_df(limit=100)

    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        st.markdown("##### 📦 Cylinder Availability vs Total Godown Capacity")
        if not stock_df.empty:
            chart_data = stock_df.set_index('Cylinder Variant')[['Available (Filled)', 'Reserved / Transit']]
            st.bar_chart(chart_data, color=["#E2725B", "#FF9933"])
        else:
            st.info("No stock data currently recorded.")

    with col_chart2:
        st.markdown("##### 📈 Recent Booking Activity & Values")
        if not orders_df.empty:
            territory_counts = orders_df['Territory'].value_counts()
            st.bar_chart(territory_counts, color="#2E7D32")
        else:
            st.info("No orders found to aggregate.")

    st.markdown("---")
    st.markdown("##### 🚚 Real-Time Order Stream (Latest 15 Bookings)")

    if not orders_df.empty:
        display_cols = ['Order Receipt', 'Booking Time', 'Consumer Name', 'Territory', 'Cylinder', 'Quantity', 'Total Price (₹)', 'Delivery DAC', 'Status', 'Payment Mode']
        st.dataframe(
            orders_df[display_cols].head(15),
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No recent bookings recorded.")


# ==============================================================================
# SECTION 2: STOCK OVERVIEW
# ==============================================================================
elif nav_choice == "Stock Overview":
    st.subheader("📦 Godown & Bottling Plant Cylinder Inventory")
    st.markdown("Real-time monitoring of 14.2kg Domestic, 19kg Commercial, and 5kg Mini Cylinders.")

    stock_df = get_stock_data()

    if not stock_df.empty:
        st.dataframe(
            stock_df[['Cylinder Variant', 'Available (Filled)', 'Reserved / Transit', 'Total Godown Stock', 'Price (Formatted)', 'Subsidy (Formatted)', 'Availability %', 'Low Stock Alert']],
            width="stretch",
            hide_index=True
        )

        st.markdown("#### Physical Inventory Allocation")
        st.bar_chart(stock_df.set_index('Cylinder Variant')[['Available (Filled)', 'Total Godown Stock']], color=["#E2725B", "#3D3532"])

        st.markdown("#### Pricing & Subsidy Matrix (INR)")
        pricing_col1, pricing_col2, pricing_col3 = st.columns(3)
        for idx, row in stock_df.iterrows():
            target_col = [pricing_col1, pricing_col2, pricing_col3][idx % 3]
            with target_col:
                st.info(f"**{row['Cylinder Variant']}**\n\nPrice: **{row['Price (Formatted)']}**\n\nGovt Subsidy: **{row['Subsidy (Formatted)']}**\n\nStock Readiness: **{row['Availability %']}%**")
    else:
        st.warning("No cylinder stocks available in database.")


# ==============================================================================
# SECTION 3: CONSUMER SEARCH (22,000+ SCALE)
# ==============================================================================
elif nav_choice == "Consumer Search":
    st.subheader("👥 LPG Consumer Directory (22,000+ Scale)")
    st.markdown("Search verified consumer accounts across Kanpur Nagar, Kanpur Dehat, and Hamirpur local territories.")

    search_col1, search_col2, search_col3 = st.columns([2, 1, 1])

    with search_col1:
        search_query = st.text_input("🔍 Search by Consumer ID, Name, Phone Number, or Landmark", placeholder="e.g. LPG-KNP-00001, Sharma, 9839...")
    with search_col2:
        region_filter = st.selectbox(
            "Territory Region",
            ['ALL', 'Kanpur Nagar', 'Kanpur Dehat', 'Hamirpur City', 'Hamirpur Rural', 'Ghatampur', 'Rath', 'Maudaha', 'Sumerpur']
        )
    with search_col3:
        status_filter = st.selectbox("Status", ['ALL', 'ACTIVE', 'INACTIVE', 'SUSPENDED'])

    # Build Django ORM query with high-speed indexes
    consumers_qs = Consumer.objects.all()

    if region_filter != 'ALL':
        consumers_qs = consumers_qs.filter(region=region_filter)
    if status_filter != 'ALL':
        consumers_qs = consumers_qs.filter(status=status_filter)
    if search_query.strip():
        q = search_query.strip()
        consumers_qs = consumers_qs.filter(
            Q(consumer_id__icontains=q) |
            Q(name__icontains=q) |
            Q(phone__icontains=q) |
            Q(address__icontains=q) |
            Q(landmark__icontains=q)
        )

    matched_count = consumers_qs.count()
    st.markdown(f"**Total Matching Consumers:** `{matched_count}` records")

    # Limit display to 100 for snappy UI rendering
    display_consumers = consumers_qs[:100]
    c_data = []
    for c in display_consumers:
        c_data.append({
            'Consumer ID': c.consumer_id,
            'Name': c.name,
            'Mobile Phone': c.phone,
            'Region': c.region,
            'Address': c.address,
            'Landmark': c.landmark or '',
            'PIN': c.pincode,
            'Connection Type': c.get_connection_type_display(),
            'Status': c.status,
            'Aadhaar Linked': '✅ Linked' if c.aadhaar_linked else '❌ Pending'
        })

    if c_data:
        st.dataframe(pd.DataFrame(c_data), width="stretch", hide_index=True)
    else:
        st.warning("No consumers matched your search parameters.")


# ==============================================================================
# SECTION 4: ROUTE MANAGEMENT
# ==============================================================================
elif nav_choice == "Route Management":
    st.subheader("🚚 Dispatch Logistics & Route Allocations")
    st.markdown("Daily dispatch runs connecting bottling depots to Kanpur and Hamirpur distribution corridors.")

    routes_df = get_routes_df()

    if not routes_df.empty:
        st.dataframe(routes_df, width="stretch", hide_index=True)

        st.markdown("#### Allocated Drop-Offs by Logistics Corridor")
        st.bar_chart(routes_df.set_index('Route Name')['Assigned Consumers'], color="#E2725B")
    else:
        st.info("No delivery routes scheduled.")


# ==============================================================================
# SECTION 5: ISSUE REFILL BOOKING
# ==============================================================================
elif nav_choice == "Issue Refill Booking":
    st.subheader("📝 Direct Agency Refill Booking Terminal")
    st.markdown("Issue an immediate cylinder refill booking, deducting stock atomically and generating customer DAC.")

    with st.form("quick_booking_form"):
        form_col1, form_col2 = st.columns(2)

        with form_col1:
            consumer_id_input = st.text_input("Registered Consumer ID or Phone", placeholder="e.g. LPG-KNP-00001 or 9839120412")
            stock_objs = list(CylinderStock.objects.all())
            stock_map = {f"{s.cylinder_type} - {format_inr(s.price)} ({s.available_quantity} available)": s for s in stock_objs}
            stock_selection = st.selectbox("Cylinder Variant", list(stock_map.keys()))
            quantity = st.number_input("Booking Quantity", min_value=1, max_value=5, value=1)

        with form_col2:
            payment_mode = st.selectbox(
                "Payment Mode",
                ["CASH_ON_DELIVERY", "UPI_ONLINE", "AGENCY_COUNTER"],
                format_func=lambda x: {
                    'CASH_ON_DELIVERY': 'Cash on Delivery (COD)',
                    'UPI_ONLINE': 'UPI (PhonePe / Google Pay / Paytm)',
                    'AGENCY_COUNTER': 'Prepaid at Agency Counter'
                }.get(x, x)
            )
            payment_ref = st.text_input("Payment Reference / UTR (if online)", placeholder="Optional UTR number")
            notes = st.text_area("Delivery Instructions", placeholder="e.g. Deliver before 2 PM")

        submitted = st.form_submit_button("Confirm Booking & Issue DAC Code")

        if submitted:
            if not consumer_id_input.strip():
                st.error("Please enter a Consumer ID or phone number.")
            else:
                cid = consumer_id_input.strip()
                consumer = Consumer.objects.filter(Q(consumer_id=cid) | Q(phone=cid)).first()
                if not consumer:
                    st.error(f"Consumer matching '{cid}' not found in registry.")
                else:
                    selected_stk = stock_map[stock_selection]
                    if selected_stk.available_quantity < quantity:
                        st.error(f"Insufficient stock! Only {selected_stk.available_quantity} available.")
                    else:
                        from django.db import transaction
                        import random
                        with transaction.atomic():
                            selected_stk.available_quantity -= quantity
                            selected_stk.save()

                            dac_code = f"{random.randint(100000, 999999)}"
                            unit_price = selected_stk.price
                            total_price = unit_price * quantity

                            # Route match
                            route = DeliveryRoute.objects.filter(region=consumer.region, status__in=['SCHEDULED', 'IN_TRANSIT']).first()
                            if route:
                                route.assigned_consumers += quantity
                                route.save()

                            order = Order.objects.create(
                                consumer=consumer,
                                cylinder_type=selected_stk,
                                route=route,
                                quantity=quantity,
                                unit_price=unit_price,
                                total_price=total_price,
                                delivery_status='BOOKED',
                                payment_status=payment_mode,
                                payment_reference=payment_ref,
                                delivery_dac=dac_code,
                                notes=notes
                            )

                            st.success(f"🎉 Refill Confirmed for **{consumer.name}** ({consumer.consumer_id})!")
                            st.info(f"**Customer Delivery Authentication Code (DAC OTP):** `{dac_code}`\n\nTotal Payable: **{format_inr(total_price)}**")
                            st.cache_data.clear()
