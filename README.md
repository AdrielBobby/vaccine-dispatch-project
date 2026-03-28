# 💉 Vaccine Dispatch Management System

A Python + MySQL CLI application to manage vaccine inventory, orders, and dispatch operations for pharmaceutical companies.

Built as a Class 12 Computer Science project.

---

## 📋 Features

- **Admin-protected vaccine entry** — only authorized users can add vaccines
- **Order management** — place and track vaccine orders by hospital & state
- **Dispatch tracking** — log dispatched orders with date
- **Sales report** — revenue, profit breakdown per vaccine
- **Pending report** — all orders not yet dispatched
- **Bar chart visualization** — matplotlib-powered dispatch graph

---

## 🗂️ Project Structure

```text
vaccine_dispatch/
├── main.py              # Entry point
├── requirements.txt
├── .env                 # DB credentials (never commit this!)
├── .gitignore
├── db/
│   ├── connection.py    # MySQL connection helper
│   └── setup.py         # DB + table initialization
└── modules/
    ├── vaccine.py       # Add vaccine logic
    ├── order.py         # Place order logic
    ├── dispatch.py      # Record dispatch logic
    └── reports.py       # Reports + graph
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/vaccine-dispatch.git
cd vaccine-dispatch
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your database credentials

Edit the `.env` file:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=VaccineDispatch
```

### 5. Run the app

```bash
python main.py
```

---

## 🗄️ Database Schema

| Table      | Key Fields                                                       |
|-----------|-------------------------------------------------------------------|
| AD_Vaccine | V_ID, V_Name, Manufacturer, Cost, Price                          |
| AD_Order   | O_ID, vaccine_ID (FK), QTY, Hospital, State                      |
| Dispatch   | Order_ID (FK), Vaccine_ID (FK), QTY, Hospital, State, date_Dispatch |

---

## 🔐 Admin Access

The admin key to add vaccines is: `BIOpharmAdMiN`

> ⚠️ In production, store this securely (e.g., hashed in the DB), never hardcode it.

---

## 📦 Requirements

- Python 3.8+
- MySQL 8.0+

---

## 👤 Author

**Adriel** — Class 12 CS Project