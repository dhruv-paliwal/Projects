"""
Script to generate a comprehensive, professional Microsoft PowerPoint presentation (.pptx)
for the LPG Distribution & Consumer Management System.
Features 12 bespoke 16:9 widescreen slides with modern enterprise cards,
rich typography, color-coded badges, and authentic project specifications.
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Initialize Widescreen Presentation (16:9)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Brand Color Palette
TERRACOTTA = RGBColor(226, 114, 91)     # #E2725B
SAFFRON = RGBColor(255, 153, 51)        # #FF9933
TURMERIC = RGBColor(255, 192, 0)        # #FFC000
DARK_CHARCOAL = RGBColor(24, 21, 20)    # #181514
MEDIUM_SLATE = RGBColor(60, 52, 49)     # #3C3431
MUTED_GRAY = RGBColor(110, 102, 99)     # #6E6663
CREAM_BG = RGBColor(250, 250, 250)      # #FAFAFA
WHITE = RGBColor(255, 255, 255)
BORDER_WARM = RGBColor(226, 217, 208)   # #E2D9D0
GREEN_ACCENT = RGBColor(46, 125, 50)    # #2E7D32
LIGHT_ORANGE = RGBColor(255, 244, 230)
LIGHT_GREEN = RGBColor(232, 245, 233)


def add_header(slide, title_text, category_text="LPG DISTRIBUTION MANAGEMENT SYSTEM"):
    """Adds a standard bespoke header with category tag and accent bar."""
    # Top accent line
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.06))
    accent.fill.solid()
    accent.fill.fore_color.rgb = SAFFRON
    accent.line.fill.background()

    # Category Pill
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(8), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = TERRACOTTA

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.733), Inches(0.7))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = DARK_CHARCOAL


def create_card(slide, left, top, width, height, bg_color=WHITE, border_color=BORDER_WARM):
    """Creates a card container shape with subtle outline."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card


# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)

# Background Card
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = CREAM_BG
bg1.line.fill.background()

# Top Saffron/Terracotta Accent Bar
accent1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
accent1.fill.solid()
accent1.fill.fore_color.rgb = TERRACOTTA
accent1.line.fill.background()

# Hero Container
hero = create_card(slide1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), WHITE, BORDER_WARM)

# Badge: Official Distributor
badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.3), Inches(3.2), Inches(0.45))
badge.fill.solid()
badge.fill.fore_color.rgb = LIGHT_ORANGE
badge.line.color.rgb = SAFFRON
badge.line.width = Pt(1.5)
tf_b = badge.text_frame
p_b = tf_b.paragraphs[0]
p_b.text = "अधिकृत एलपीजी वितरण केंद्र | UP-KNP-78401"
p_b.font.size = Pt(11)
p_b.font.bold = True
p_b.font.color.rgb = TERRACOTTA
p_b.alignment = PP_ALIGN.CENTER

# Title
tbox = slide1.shapes.add_textbox(Inches(1.3), Inches(1.9), Inches(10.7), Inches(1.6))
tf = tbox.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "LPG Distribution & Consumer Management System"
p1.font.size = Pt(32)
p1.font.bold = True
p1.font.color.rgb = DARK_CHARCOAL

p2 = tf.add_paragraph()
p2.text = "High-Scale Operational Logistics & Supply Chain Command Center (Kanpur & Hamirpur Territory)"
p2.font.size = Pt(16)
p2.font.color.rgb = MEDIUM_SLATE
p2.space_before = Pt(8)

# 3 Highlights Cards inside Slide 1
highlights = [
    ("22,000+ Consumers", "High-performance indexing across Kanpur Nagar, Kanpur Dehat, and Hamirpur local mohallas."),
    ("Full-Stack MVT & SPA", "Django ORM backend paired with bespoke AngularJS 1.8 & Bootstrap 5 Indian palette."),
    ("Dual Command Interface", "Instant single-page operational terminal + Streamlit data intelligence platform.")
]

for idx, (title, desc) in enumerate(highlights):
    cx = Inches(1.3 + idx * 3.65)
    c_card = create_card(slide1, cx, Inches(3.8), Inches(3.4), Inches(2.3), CREAM_BG, BORDER_WARM)
    
    # Top card border accent
    sub_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(3.8), Inches(3.4), Inches(0.08))
    sub_bar.fill.solid()
    sub_bar.fill.fore_color.rgb = [TERRACOTTA, SAFFRON, TURMERIC][idx]
    sub_bar.line.fill.background()

    tb = slide1.shapes.add_textbox(cx + Inches(0.2), Inches(4.0), Inches(3.0), Inches(1.9))
    tf_c = tb.text_frame
    tf_c.word_wrap = True
    pt = tf_c.paragraphs[0]
    pt.text = title
    pt.font.size = Pt(15)
    pt.font.bold = True
    pt.font.color.rgb = DARK_CHARCOAL
    
    pd_elem = tf_c.add_paragraph()
    pd_elem.text = desc
    pd_elem.font.size = Pt(11)
    pd_elem.font.color.rgb = MUTED_GRAY
    pd_elem.space_before = Pt(6)


# ==============================================================================
# SLIDE 2: EXECUTIVE SUMMARY & OPERATIONAL VISION
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Executive Summary & Operational Vision", "MISSION & SCOPE")

cards2 = [
    ("Operational Challenges", [
        "Unsynchronized paper logs causing domestic & commercial cylinder discrepancies.",
        "Manual tracking of 22,000+ consumers across dispersed urban and rural clusters.",
        "Lack of real-time stock visibility between plant godown, dispatch vans, and depot.",
        "Delay in customer DAC OTP authentication and DBTL subsidy reconciliation."
    ], TERRACOTTA),
    ("Engineered Solution", [
        "Automated, transactional LPG booking with sub-millisecond consumer lookup.",
        "Atomic stock deduction with row-level locks preventing godown overbooking.",
        "Intelligent logistics dispatch grouping orders by municipal corridors in Kanpur & Hamirpur.",
        "Bespoke Indian enterprise interface providing warm, high-contrast, eye-friendly usability."
    ], GREEN_ACCENT),
    ("Measurable Impact", [
        "100% stock audit precision across 14.2kg Domestic, 19kg Commercial & 5kg Mini.",
        "Zero booking race conditions during morning peak demand hours.",
        "Faster dispatch turnaround: bookings allocated to delivery agents automatically.",
        "Standardized Indian Rupee (₹) pricing and digital UPI / COD tracking."
    ], SAFFRON)
]

for idx, (title, bullets, accent_col) in enumerate(cards2):
    cx = Inches(0.8 + idx * 3.95)
    create_card(slide2, cx, Inches(1.8), Inches(3.8), Inches(5.1), WHITE, BORDER_WARM)
    
    # Top color stripe
    bar = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.8), Inches(3.8), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_col
    bar.line.fill.background()

    tb = slide2.shapes.add_textbox(cx + Inches(0.25), Inches(2.05), Inches(3.3), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    for bullet in bullets:
        pb = tf.add_paragraph()
        pb.text = "• " + bullet
        pb.font.size = Pt(12)
        pb.font.color.rgb = MEDIUM_SLATE
        pb.space_before = Pt(10)


# ==============================================================================
# SLIDE 3: SYSTEM ARCHITECTURE & TECH STACK
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Full-Stack Technology Architecture", "SYSTEM ARCHITECTURE")

stack_tiers = [
    ("Presentation Tier (SPA)", "AngularJS 1.8.2 + Bootstrap 5.3", [
        "Single-Page Application with zero reload latency.",
        "Two-way data binding with custom '{[ ... ]}' interpolation.",
        "Custom inrCurrency filter formatting Indian numbering (₹).",
        "WCAG AAA High-Visibility Contrast mode toggle."
    ], TERRACOTTA),
    ("Backend Application Tier", "Python 3.13 + Django 6.1 (MVT)", [
        "Django ORM with select_for_update() row locking.",
        "REST JSON API endpoints for stock, consumers, & routes.",
        "Transaction-safe order generation and DAC OTP creation.",
        "Native Indian Standard Time (IST) localization."
    ], SAFFRON),
    ("Database & Persistence Tier", "MySQL 8.0 (mysql-connector-python)", [
        "Official Oracle mysql.connector.django driver.",
        "Optimized compound indexes for 22,000+ consumer scale.",
        "Resilient zero-downtime development fallback engine.",
        "Strict foreign key integrity protecting cylinder inventory."
    ], TURMERIC),
    ("Operational Analytics Tier", "Streamlit 1.66 + Pandas", [
        "Live executive command center with cached queries.",
        "Native visualization for godown inventory & routes.",
        "Direct-in-dashboard refill booking terminal.",
        "Dedicated .streamlit theme lock enforcing warm palette."
    ], GREEN_ACCENT)
]

for idx, (tier_title, sub, details, color) in enumerate(stack_tiers):
    cx = Inches(0.8 + idx * 2.96)
    create_card(slide3, cx, Inches(1.8), Inches(2.85), Inches(5.1), WHITE, BORDER_WARM)
    
    bar = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.8), Inches(2.85), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = slide3.shapes.add_textbox(cx + Inches(0.18), Inches(2.05), Inches(2.5), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = tier_title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    ps = tf.add_paragraph()
    ps.text = sub
    ps.font.size = Pt(11)
    ps.font.bold = True
    ps.font.color.rgb = color
    ps.space_before = Pt(4)

    for d in details:
        pd = tf.add_paragraph()
        pd.text = "✔ " + d
        pd.font.size = Pt(11)
        pd.font.color.rgb = MEDIUM_SLATE
        pd.space_before = Pt(8)


# ==============================================================================
# SLIDE 4: DATABASE ENGINEERING (22,000+ CONSUMER SCALE)
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Database Schema Engineered for 22,000+ Consumers", "DATA MODELING & SCALABILITY")

models_info = [
    ("Consumer Model", "Master Directory (22,000+ Records)", [
        "Unique consumer_id (e.g. LPG-KNP-01429), name, phone, address, and landmark.",
        "Optimized region field: Kanpur Nagar, Kanpur Dehat, Hamirpur City, Hamirpur Rural, Rath, Maudaha, etc.",
        "Composite DB Indexes: [region, status], [phone, status], [consumer_id, status] ensuring <20ms lookups.",
        "Tracks DBTL Aadhaar-linked status and connection types (Domestic SBC/DBC, PMUY, Commercial)."
    ]),
    ("CylinderStock Model", "Inventory & Bottling Godown", [
        "Tracks 14.2kg Domestic Refill, 19kg Commercial Jumbo, and 5kg Mini FTL.",
        "Atomic quantity tracking: total_quantity, available_quantity, and reserved_quantity.",
        "Explicit pricing fields in INR (₹) including govt subsidy amount (e.g. ₹903 base, ₹200 subsidy).",
        "Properties for stock_percentage, low_stock_threshold, and replenishment warnings."
    ]),
    ("DeliveryRoute Model", "Logistics & Dispatch Scheduling", [
        "Assigned delivery agents (Ramesh Yadav, Suresh Verma, etc.) and phone contacts.",
        "Vehicle registration tags (UP-78-AG-4912, UP-91-K-5521) for Kanpur & Hamirpur routes.",
        "Dynamic assigned_consumers drop-off counter updated on booking confirmation.",
        "Status tracking: SCHEDULED, IN_TRANSIT, COMPLETED, and DELAYED."
    ]),
    ("Order Model", "Transaction & Audit Trail", [
        "Unique order_id receipt (e.g. ORD-202610-91283) linked via ForeignKeys to Consumer, Stock, & Route.",
        "Generates authentic 6-digit Delivery Authentication Code (DAC OTP) for doorstep validation.",
        "Payment reconciliation: Cash on Delivery (COD), UPI (PhonePe/GPay), and Agency Counter.",
        "Compound indexed on [delivery_status, booking_date] for instantaneous dashboard queries."
    ])
]

for idx, (m_title, m_sub, m_bullets) in enumerate(models_info):
    row = idx // 2
    col = idx % 2
    cx = Inches(0.8 + col * 5.95)
    cy = Inches(1.8 + row * 2.65)
    
    create_card(slide4, cx, cy, Inches(5.8), Inches(2.45), WHITE, BORDER_WARM)
    
    # Left accent indicator
    left_bar = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, cy, Inches(0.08), Inches(2.45))
    left_bar.fill.solid()
    left_bar.fill.fore_color.rgb = TERRACOTTA if idx % 2 == 0 else SAFFRON
    left_bar.line.fill.background()

    tb = slide4.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.12), Inches(5.4), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = m_title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    ps = tf.add_paragraph()
    ps.text = m_sub
    ps.font.size = Pt(10.5)
    ps.font.bold = True
    ps.font.color.rgb = TERRACOTTA
    ps.space_before = Pt(2)

    for b in m_bullets:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = MEDIUM_SLATE
        pb.space_before = Pt(4)


# ==============================================================================
# SLIDE 5: BESPOKE UI/UX DESIGN MANDATE
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Bespoke Indian-Inspired UI/UX Design System", "AESTHETICS & ACCESSIBILITY")

palettes = [
    ("Terracotta Red", "#E2725B", TERRACOTTA, "Primary Actions & Buttons", "Used for high-priority CTA buttons, booking triggers, and critical metric indicators."),
    ("Deep Saffron", "#FF9933", SAFFRON, "Headers & Logistics Accents", "Anchors navigation headers, territory badges, and route status highlights."),
    ("Turmeric Yellow", "#FFC000", TURMERIC, "Subtle Alerts & DAC Pills", "Provides eye-friendly warnings for low stock levels and customer authentication chips."),
    ("Warm Off-White", "#FAFAFA", CREAM_BG, "Eye-Strain Reduction", "Eliminates glare in busy distribution offices while avoiding generic dark-mode cliches.")
]

for idx, (p_name, p_hex, p_rgb, p_role, p_desc) in enumerate(palettes):
    cx = Inches(0.8 + idx * 2.96)
    create_card(slide5, cx, Inches(1.8), Inches(2.85), Inches(2.6), WHITE, BORDER_WARM)
    
    # Color swatch
    swatch = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.2), Inches(2.0), Inches(2.45), Inches(0.9))
    swatch.fill.solid()
    swatch.fill.fore_color.rgb = p_rgb
    swatch.line.color.rgb = BORDER_WARM
    
    tb = slide5.shapes.add_textbox(cx + Inches(0.18), Inches(3.0), Inches(2.5), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = p_name
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    p_code = tf.add_paragraph()
    p_code.text = f"{p_hex} • {p_role}"
    p_code.font.size = Pt(10)
    p_code.font.bold = True
    p_code.font.color.rgb = TERRACOTTA
    
    pd = tf.add_paragraph()
    pd.text = p_desc
    pd.font.size = Pt(9.5)
    pd.font.color.rgb = MUTED_GRAY
    pd.space_before = Pt(3)

# Bottom Feature Callout
f_card = create_card(slide5, Inches(0.8), Inches(4.7), Inches(11.733), Inches(2.2), WHITE, BORDER_WARM)
bar_bot = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.733), Inches(0.08))
bar_bot.fill.solid()
bar_bot.fill.fore_color.rgb = TERRACOTTA
bar_bot.line.fill.background()

tb_f = slide5.shapes.add_textbox(Inches(1.1), Inches(4.9), Inches(11.2), Inches(1.9))
tf_f = tb_f.text_frame
tf_f.word_wrap = True
p = tf_f.paragraphs[0]
p.text = "Key UI/UX Innovations & Accessibility Mandates"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = DARK_CHARCOAL

features = [
    ("Strict Indian Rupee (₹) Standard:", "All currency formatted with '₹' using Indian numbering system (Lakhs/Crores)."),
    ("Max-Visibility Contrast Mode:", "Accessible one-click toggle delivering pure #000000 text and reinforced borders for high-glare godown screens."),
    ("No AI/Bootstrap Boilerplate:", "Harsh lines replaced with 8-12px rounded radii, soft organic elevation shadows, and vernacular Hindi branding.")
]
for f_title, f_text in features:
    pf = tf_f.add_paragraph()
    pf.text = f"✔ {f_title} {f_text}"
    pf.font.size = Pt(11)
    pf.font.color.rgb = MEDIUM_SLATE
    pf.space_before = Pt(4)


# ==============================================================================
# SLIDE 6: BACKEND LOGIC & CONCURRENCY CONTROL
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Backend Logic, APIs & Transaction Safety", "CORE BACKEND ENGINE")

backend_cols = [
    ("Atomic Booking Pipeline", [
        "Wrapped inside Django's transaction.atomic() with select_for_update() row-level locking.",
        "Prevents physical inventory race conditions during morning booking surges.",
        "Deducts available godown cylinder stock instantaneously upon validation.",
        "Auto-rolls back with a friendly HTTP 400 if stock is exhausted."
    ], TERRACOTTA),
    ("Intelligent Route Allocation", [
        "Inspects consumer registered region (e.g. Kanpur South vs Hamirpur Rural).",
        "Automatically links booking to active delivery van scheduled for that territory.",
        "Increments assigned_consumers payload count on the delivery agent's schedule.",
        "Enables logistics managers to balance vehicle capacity before morning roll-out."
    ], SAFFRON),
    ("Doorstep Security (DAC OTP)", [
        "Generates authentic 6-digit Delivery Authentication Code (DAC) per order.",
        "Customer presents DAC OTP to delivery agent upon physical cylinder handover.",
        "Prevents diversion or unauthorized cylinder leakage in local areas.",
        "Status transition: BOOKED -> DISPATCHED -> OUT_FOR_DELIVERY -> DELIVERED."
    ], GREEN_ACCENT)
]

for idx, (title, points, color) in enumerate(backend_cols):
    cx = Inches(0.8 + idx * 3.95)
    create_card(slide6, cx, Inches(1.8), Inches(3.8), Inches(5.1), WHITE, BORDER_WARM)
    
    top_strip = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.8), Inches(3.8), Inches(0.1))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = color
    top_strip.line.fill.background()

    tb = slide6.shapes.add_textbox(cx + Inches(0.25), Inches(2.05), Inches(3.3), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    for pt in points:
        pb = tf.add_paragraph()
        pb.text = "• " + pt
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = MEDIUM_SLATE
        pb.space_before = Pt(10)


# ==============================================================================
# SLIDE 7: BESPOKE ANGULARJS SPA FRONTEND
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Bespoke AngularJS 1.8 Single-Page Application", "FRONTEND WORKFLOW")

spa_features = [
    ("Live Top Metric Ribbon", "Real-time KPI synchronization showing total registered consumers, filled stock availability, pending deliveries, and daily revenue in ₹."),
    ("Godown Physical Stock Meters", "Dynamic availability bars with automated color transitions: Green (>50%), Amber (25-50%), and Red (<25% Low Stock Alert)."),
    ("Smart Consumer Auto-Lookup", "Typeahead live search querying ID, mobile, or name across 22,000+ records with immediate Aadhaar-link and connection badges."),
    ("Dynamic Invoice Calculator", "Calculates base refill cost (quantity × price) and automatically applies DBTL Govt Subsidy deduction for domestic & PMUY beneficiaries."),
    ("One-Click Status Transition", "Agency staff can update deliveries from 'Booked' to 'Dispatched' or 'Delivered' via dropdown action buttons with automatic stock restore on cancel."),
    ("Printable Delivery Memo Modal", "Pop-up receipt modal presenting customer details, DAC code, and a one-click print memo button for the customer copy.")
]

for idx, (f_title, f_desc) in enumerate(spa_features):
    row = idx // 2
    col = idx % 2
    cx = Inches(0.8 + col * 5.95)
    cy = Inches(1.8 + row * 1.72)
    
    create_card(slide7, cx, cy, Inches(5.8), Inches(1.58), WHITE, BORDER_WARM)
    
    pin = slide7.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.2), cy + Inches(0.25), Inches(0.25), Inches(0.25))
    pin.fill.solid()
    pin.fill.fore_color.rgb = TERRACOTTA if idx % 2 == 0 else SAFFRON
    pin.line.fill.background()

    tb = slide7.shapes.add_textbox(cx + Inches(0.55), cy + Inches(0.12), Inches(5.1), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f_title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    pd = tf.add_paragraph()
    pd.text = f_desc
    pd.font.size = Pt(10.5)
    pd.font.color.rgb = MEDIUM_SLATE
    pd.space_before = Pt(3)


# ==============================================================================
# SLIDE 8: STREAMLIT DEPLOYMENT INTERFACE
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Streamlit Operational Deployment Interface", "DATA VISUALIZATION & BI")

st_sections = [
    ("Executive Dashboard", [
        "Provides macro-level operational overview directly querying Django ORM.",
        "Interactive bar charts comparing available filled stock vs reserved godown inventory.",
        "Territory order volume charts segmenting demand across Kanpur and Hamirpur.",
        "Live tabular stream of recent bookings with formatted ₹ amounts."
    ]),
    ("Stock Overview & Matrix", [
        "Complete tabular breakdown of 14.2kg Domestic, 19kg Commercial & 5kg Mini.",
        "Direct calculation of godown storage readiness percentage.",
        "Pricing & Subsidy matrix displaying real-time retail refill rates.",
        "Proactive low-stock notification triggers when inventory falls below 20%."
    ]),
    ("Consumer Search (22k+)", [
        "High-performance query engine filtering across 22,000+ local accounts.",
        "Search by Consumer ID, phone number, name, or street landmark.",
        "Region filtering: Kanpur Nagar, Kanpur Dehat, Hamirpur, Ghatampur, Rath, etc.",
        "Displays Aadhaar linkage, status, and connection type in real-time."
    ]),
    ("Route Dispatch & Direct Booking", [
        "Visualizes delivery van load capacity across regional transit corridors.",
        "Enables operators to issue refill bookings directly inside the Streamlit UI.",
        "Atomically reserves cylinder stock and outputs the customer DAC OTP code.",
        "Cached queries (@st.cache_data) with a manual 1-click cache refresh."
    ])
]

for idx, (title, bullets) in enumerate(st_sections):
    row = idx // 2
    col = idx % 2
    cx = Inches(0.8 + col * 5.95)
    cy = Inches(1.8 + row * 2.65)
    
    create_card(slide8, cx, cy, Inches(5.8), Inches(2.45), WHITE, BORDER_WARM)
    
    top_bar = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, cy, Inches(5.8), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = TERRACOTTA if col == 0 else SAFFRON
    top_bar.line.fill.background()

    tb = slide8.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.15), Inches(5.4), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    for b in bullets:
        pb = tf.add_paragraph()
        pb.text = "✔ " + b
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = MEDIUM_SLATE
        pb.space_before = Pt(4)


# ==============================================================================
# SLIDE 9: FIELD LOGISTICS & TERRITORIAL REACH
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "Field Logistics & Regional Corridor Coverage", "TERRITORIAL DISPATCH JURISDICTION")

territories = [
    ("Kanpur Nagar Urban Hub", "UP-78-AG / UP-78-BN", [
        "Kidwai Nagar 'H' Block, Barra Sector-4, Govind Nagar Block-7.",
        "Civil Lines & Mall Road commercial and restaurant jumbo deliveries.",
        "Kalyanpur, GT Road, and IIT Kanpur residential colony routes.",
        "High-density morning dispatch runs handled by Ramesh Yadav & Suresh Verma."
    ], TERRACOTTA),
    ("Kanpur Dehat & Industrial Belt", "UP-78-ED / UP-78-DY", [
        "Akbarpur Main Market & Tehsil Gate distribution post.",
        "Rania Industrial Area: 19kg commercial cylinder deliveries for factories.",
        "Ghatampur & Jahanabad National Highway logistics corridor.",
        "Scheduled rural transport runs operated by Driver Mohammad Irfan."
    ], SAFFRON),
    ("Hamirpur City & Riverfront", "UP-91-K", [
        "Subhash Nagar & Yamuna Ghat bridge checkpost route.",
        "Betwa Riverfront Sangam and Collectorate Civil Lines colony.",
        "Ramanand Nagar District Hospital institutional supply hub.",
        "Managed by Delivery Executive Vijay Pratap Singh."
    ], GREEN_ACCENT),
    ("Hamirpur Rural & Rath Sector", "UP-91-M / UP-91-P", [
        "Vill-Bilgaon, Maudaha Tehsil & Ingohta Village Ujjawala drop-offs.",
        "Bharuwa Sumerpur Industrial Estate (HUL Plant link).",
        "Rath Town: Padav Chauraha, Bara Khamba, and Orai Road bypass.",
        "Operated by Drivers Dinesh Pal & Manoj Kumar Tiwari."
    ], TURMERIC)
]

for idx, (t_title, t_code, t_points, color) in enumerate(territories):
    cx = Inches(0.8 + idx * 2.96)
    create_card(slide9, cx, Inches(1.8), Inches(2.85), Inches(5.1), WHITE, BORDER_WARM)
    
    bar = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.8), Inches(2.85), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = slide9.shapes.add_textbox(cx + Inches(0.18), Inches(2.05), Inches(2.5), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = t_title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    ps = tf.add_paragraph()
    ps.text = t_code
    ps.font.size = Pt(10.5)
    ps.font.bold = True
    ps.font.color.rgb = color
    ps.space_before = Pt(3)

    for pt in t_points:
        p_sub = tf.add_paragraph()
        p_sub.text = "• " + pt
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = MEDIUM_SLATE
        p_sub.space_before = Pt(8)


# ==============================================================================
# SLIDE 10: PERFORMANCE METRICS & BENCHMARKS
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Performance Benchmarks & Key Operational KPIs", "AUDIT & PERFORMANCE")

kpis = [
    ("22,000+", "Consumer Scalability", "Engineered with composite indexes to handle over 22k registered accounts without query degradation.", TERRACOTTA),
    ("< 45ms", "Average Query Latency", "Sub-50ms REST API response time for paged consumer lookup and live stock checks.", SAFFRON),
    ("100%", "Stock Transaction Safety", "Atomic locks (select_for_update) prevent overselling and inventory leakages.", GREEN_ACCENT),
    ("6-Digit", "Doorstep DAC OTP Security", "Guarantees cylinder delivery authentication directly at consumer residence.", TURMERIC)
]

for idx, (stat, label, desc, color) in enumerate(kpis):
    cx = Inches(0.8 + idx * 2.96)
    create_card(slide10, cx, Inches(1.8), Inches(2.85), Inches(3.2), WHITE, BORDER_WARM)
    
    bar = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.8), Inches(2.85), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()

    tb = slide10.shapes.add_textbox(cx + Inches(0.18), Inches(2.1), Inches(2.5), Inches(2.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = stat
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = color
    
    pl = tf.add_paragraph()
    pl.text = label
    pl.font.size = Pt(13)
    pl.font.bold = True
    pl.font.color.rgb = DARK_CHARCOAL
    pl.space_before = Pt(4)

    pd = tf.add_paragraph()
    pd.text = desc
    pd.font.size = Pt(10.5)
    pd.font.color.rgb = MUTED_GRAY
    pd.space_before = Pt(8)

# Lower comparison table card
bot_card = create_card(slide10, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.7), WHITE, BORDER_WARM)
tb_b = slide10.shapes.add_textbox(Inches(1.1), Inches(5.35), Inches(11.2), Inches(1.4))
tf_b = tb_b.text_frame
tf_b.word_wrap = True

p = tf_b.paragraphs[0]
p.text = "Operational Comparison: Legacy Manual Agency vs Shree Ganesh LPG System"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK_CHARCOAL

comp_points = [
    "Legacy Approach: Handwritten register receipts, unverified phone bookings, manual daily stock reconciliation, zero live van tracking.",
    "Bespoke System: Automated instant DAC generation, 1-click status transitions, live stock visual meters, sub-second 22k consumer lookup."
]
for cp in comp_points:
    p_comp = tf_b.add_paragraph()
    p_comp.text = "✔ " + cp
    p_comp.font.size = Pt(11)
    p_comp.font.color.rgb = MEDIUM_SLATE
    p_comp.space_before = Pt(4)


# ==============================================================================
# SLIDE 11: FUTURE ROADMAP & SCALABILITY
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "Future Roadmap & Technological Expansion", "GROWTH & INNOVATION")

phases = [
    ("Phase 1: Automated SMS & WhatsApp Alerts", [
        "Instant WhatsApp booking receipt sent to consumer mobile upon creation.",
        "Automatic SMS broadcast with delivery DAC code and assigned driver contact.",
        "Delivery confirmation alert notifying DBTL subsidy credit to bank."
    ], TERRACOTTA),
    ("Phase 2: Mobile Delivery Driver App", [
        "Lightweight Progressive Web App (PWA) for van drivers in Kanpur & Hamirpur.",
        "Real-time turn-by-turn route navigation optimized by mohalla clusters.",
        "Driver OTP entry terminal to mark orders DELIVERED instantly at doorstep."
    ], SAFFRON),
    ("Phase 3: Dynamic BharatQR & Soundbox", [
        "Dynamic UPI QR code generated on delivery invoice for instant cashless payment.",
        "Automatic webhook updating Order payment_status to 'PAID' via UPI UTR.",
        "Voice confirmation soundbox integration for agency counter pickups."
    ], GREEN_ACCENT)
]

for idx, (p_title, p_points, p_col) in enumerate(phases):
    cx = Inches(0.8 + idx * 3.95)
    create_card(slide11, cx, Inches(1.8), Inches(3.8), Inches(5.1), WHITE, BORDER_WARM)
    
    top_bar = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.8), Inches(3.8), Inches(0.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = p_col
    top_bar.line.fill.background()

    tb = slide11.shapes.add_textbox(cx + Inches(0.25), Inches(2.05), Inches(3.3), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = p_title
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = DARK_CHARCOAL
    
    for pt in p_points:
        pb = tf.add_paragraph()
        pb.text = "• " + pt
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = MEDIUM_SLATE
        pb.space_before = Pt(10)


# ==============================================================================
# SLIDE 12: CONCLUSION & LIVE DEMONSTRATION
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)

# Background
bg12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg12.fill.solid()
bg12.fill.fore_color.rgb = CREAM_BG
bg12.line.fill.background()

# Top accent bar
top12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
top12.fill.solid()
top12.fill.fore_color.rgb = TERRACOTTA
top12.line.fill.background()

# Center Card
card12 = create_card(slide12, Inches(1.5), Inches(1.0), Inches(10.333), Inches(5.5), WHITE, BORDER_WARM)

tb12 = slide12.shapes.add_textbox(Inches(2.0), Inches(1.4), Inches(9.333), Inches(4.7))
tf12 = tb12.text_frame
tf12.word_wrap = True

p_b12 = tf12.paragraphs[0]
p_b12.text = "अधिकृत एलपीजी वितरण केंद्र • KANPUR & HAMIRPUR COMMAND"
p_b12.font.size = Pt(12)
p_b12.font.bold = True
p_b12.font.color.rgb = TERRACOTTA
p_b12.alignment = PP_ALIGN.CENTER

p_t12 = tf12.add_paragraph()
p_t12.text = "Thank You! Questions & Discussion"
p_t12.font.size = Pt(32)
p_t12.font.bold = True
p_t12.font.color.rgb = DARK_CHARCOAL
p_t12.alignment = PP_ALIGN.CENTER
p_t12.space_before = Pt(8)

p_s12 = tf12.add_paragraph()
p_s12.text = "LPG Distribution & Consumer Management System | Shree Ganesh LPG Agency"
p_s12.font.size = Pt(15)
p_s12.font.color.rgb = MEDIUM_SLATE
p_s12.alignment = PP_ALIGN.CENTER
p_s12.space_before = Pt(6)

# Server Endpoints Box
endpoints = [
    ("AngularJS SPA Portal:", "http://127.0.0.1:8000/"),
    ("Streamlit Command Hub:", "http://127.0.0.1:8501/"),
    ("Django Admin Registry:", "http://127.0.0.1:8000/admin/"),
    ("Lead Architect & Engineer:", "Dhruv Paliwal (dhruvpaliwal26306dps@gmail.com)")
]

for label, val in endpoints:
    pe = tf12.add_paragraph()
    pe.text = f"{label}  {val}"
    pe.font.size = Pt(13)
    pe.font.bold = True
    pe.font.color.rgb = DARK_CHARCOAL
    pe.alignment = PP_ALIGN.CENTER
    pe.space_before = Pt(10)


# Save presentation
output_path = os.path.join(os.path.dirname(__file__), "LPG_Distribution_Management_System_Presentation.pptx")
prs.save(output_path)
print(f"Presentation saved successfully at: {output_path}")
