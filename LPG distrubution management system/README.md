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

---

## 🛠️ Complete Tech Stack
1. **Backend**: Python 3.13, Django 6.1 (MVT architecture, Django ORM, Atomic Transactions, Paged Querysets).
2. **Database**: MySQL 8.0+ via official `mysql-connector-python` (`mysql.connector.django` engine) with composite indexing optimized for 22,000+ records.
3. **Frontend SPA**: AngularJS 1.8.2, HTML5, CSS3, Bootstrap 5.3 (custom warm overrides), FontAwesome 6 icons.
4. **Deployment & Visualization**: Streamlit 1.66+ dashboard directly interacting with Django ORM / MySQL and Pandas analytics.

---

## 📂 Project Structure
```text
C:\Users\Dhruv\.gemini\antigravity\scratch\lpg_manager\
├── dashboard\
│   ├── migrations\
│   │   ├── 0001_initial.py       # Full schema migrations for scale
│   ├── admin.py                  # Django Admin management classes
│   ├── apps.py                   # App configuration
│   ├── models.py                 # High-performance models with composite indexes
│   ├── urls.py                   # API and SPA route mappings
│   └── views.py                  # JSON REST endpoints and MVT entry point
├── lpg_manager\
│   ├── settings.py               # Database connector, static files, and IST settings
│   ├── urls.py                   # Root URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
├── static\
│   ├── css\
│   │   └── style.css             # Bespoke Indian palette & Bootstrap 5 overrides
│   └── js\
│       └── app.js                # AngularJS app, controllers, and inrCurrency filter
├── templates\
│   └── index.html                # Single-Page Application (SPA) entry point
├── seed.py                       # Realistic seed data script for Kanpur & Hamirpur
├── streamlit_app.py              # Operational Streamlit reporting & dispatch terminal
├── requirements.txt              # Production dependency specifications
├── .env.example                  # Environment configuration template
└── manage.py
```

---

## ⚡ Setup & Launch Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. MySQL Database Configuration
In MySQL CLI or MySQL Workbench, execute:
```sql
CREATE DATABASE IF NOT EXISTS lpg_manager_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON lpg_manager_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

Configure your credentials in `.env` (or environment variables):
```env
DB_ENGINE=mysql
DB_NAME=lpg_manager_db
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 3. Run Migrations & Populate Authentic Agency Data
```bash
python manage.py makemigrations dashboard
python manage.py migrate
python seed.py
```

### 4. Launch Simultaneously

#### Terminal 1: Django Backend & AngularJS Frontend (Port 8000)
```bash
python manage.py runserver 127.0.0.1:8000
```
*Access the Bespoke AngularJS SPA at: `http://127.0.0.1:8000/`*  
*Django Admin Portal: `http://127.0.0.1:8000/admin/`*

#### Terminal 2: Streamlit Operational Dashboard (Port 8501)
```bash
python -m streamlit run streamlit_app.py --server.port 8501
```
*Access Streamlit Command Hub at: `http://127.0.0.1:8501/`*

---

## 🔌 API Endpoints
- `GET /api/stats/` : Returns real-time KPI metrics (revenue in ₹, active consumers, stock aggregates).
- `GET /api/stock/` : Returns domestic (14.2kg), commercial (19kg), and mini (5kg) stock breakdown.
- `GET /api/consumers/?q=<query>&region=<region>&page=1` : High-speed search with pagination across 22,000+ consumer records.
- `POST /api/orders/` : Atomically creates new booking, deducts available godown stock, assigns delivery route, and issues 6-digit Delivery Authentication Code (DAC OTP).
- `GET /api/orders/?status=<status>` : Orders and deliveries log.
- `POST /api/orders/<order_id>/status/` : Updates delivery state (`DISPATCHED`, `OUT_FOR_DELIVERY`, `DELIVERED`, `CANCELLED`).
- `GET /api/routes/` : Logistics routes covering Kanpur Nagar, Kanpur Dehat, Hamirpur, and Rath.
