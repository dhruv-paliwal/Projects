# Shree Ganesh LPG Agency - Distribution & Consumer Management System
### Specialized Enterprise System for Kanpur Nagar, Kanpur Dehat & Hamirpur Territory (Agency Code: UP-KNP-78401)

A complete, production-ready, full-stack enterprise web platform and operational command center engineered specifically for authorized LPG distributorship agencies handling over **22,000+ registered domestic and commercial consumers**.

---

## 🎨 Bespoke Indian Enterprise Aesthetic (UI/UX Mandate)
- **Palette**:
  - **Terracotta Red** (`#E2725B`): Primary CTA buttons, action badges, and key metric highlights.
  - **Deep Saffron** (`#FF9933`): Section headers, top navigation accents, and delivery route pills.
  - **Turmeric Yellow** (`#FFC000`): Subtle operational alerts, pending delivery indicators, and DAC chips.
  - **Soft Off-White / Cream** (`#FAFAFA`): Eye-strain-reducing background with soft warm drop shadows (`rgba(90, 60, 40, 0.05)`).
- **Currency Standard**: Explicitly formatted with the **Indian Rupee (₹)** symbol using Indian numbering nomenclature (e.g., `₹903.00`, `₹1,825.00`, `₹1,24,500.00`).
- **Typography**: Modern, crisp geometric typography powered by Google Fonts (`Inter` and `Outfit`).
- **High-Visibility Mode**: Accessible toggle button on top navbar to switch between standard warm theme and ultra-high contrast black text (`#000000`).

---

## 📁 Clean Multi-Tier Project Organization

```text
LPG distrubution management system/
│
├── backend/                                  # Django ORM & Backend MVT Logic
│   ├── dashboard/                            # Operational App Module
│   │   ├── migrations/                       # Database schema migrations
│   │   ├── admin.py                          # Django Admin management
│   │   ├── apps.py                           # App config
│   │   ├── models.py                         # High-performance models (22k+ scale)
│   │   ├── urls.py                           # JSON API & SPA routes
│   │   └── views.py                          # REST JSON endpoints & template view
│   ├── lpg_manager/                          # Project Settings & Root Dispatcher
│   │   ├── settings.py                       # MySQL connector & IST config
│   │   ├── urls.py                           # Main URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── db.sqlite3                            # Local development database
│   ├── manage.py                             # Django CLI management utility
│   └── seed.py                               # Realistic agency mock data generator
│
├── frontend/                                 # Bespoke Client Single-Page Application
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css                     # Warm Indian aesthetic & Bootstrap 5 overrides
│   │   └── js/
│   │       └── app.js                        # AngularJS 1.8 SPA logic & inrCurrency filter
│   └── templates/
│       └── index.html                        # SPA HTML5 entry point template
│
├── .streamlit/
│   └── config.toml                           # Streamlit light theme & color lock
│
├── .env.example                              # Environment variable configuration template
├── .gitignore                                # Git ignore specifications
├── generate_presentation.py                  # Automation script to build PowerPoint deck
├── LPG_Distribution_Management_System_Presentation.pptx # 16:9 Widescreen Presentation (12 Slides)
├── README.md                                 # Full documentation & setup guide
├── requirements.txt                          # Production dependency specifications
├── run_servers.bat                           # One-click Windows server launcher
└── streamlit_app.py                          # Streamlit operational command center
```

---

## ⚡ Launch Instructions

### Option A: One-Click Windows Launcher
Double-click `run_servers.bat` in the `LPG distrubution management system` folder. It will automatically launch both the Django backend server and the Streamlit operations hub in separate windows!

### Option B: Terminal Launch

#### Terminal 1: Launch Django Backend & AngularJS Frontend (Port 8000)
```bash
cd "LPG distrubution management system/backend"
python manage.py runserver 127.0.0.1:8000
```
- **AngularJS SPA Frontend:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
- **Django Admin Portal:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

#### Terminal 2: Launch Streamlit Operational Dashboard (Port 8501)
```bash
cd "LPG distrubution management system"
python -m streamlit run streamlit_app.py --server.port 8501
```
- **Streamlit Command Center:** [http://127.0.0.1:8501/](http://127.0.0.1:8501/)
