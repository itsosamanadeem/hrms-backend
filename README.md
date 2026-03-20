---

# 🚀 HRMS Backend

A modern **Human Resource Management System (HRMS)** backend built using **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Pydantic v2**.

This system provides a scalable and production-ready backend for managing employees, attendance, and leave workflows.

---

## ✨ Features

### 👨‍💼 Employee Management

* Create, update, and delete employees
* Store detailed employee information:

  * Name, Email, Phone
  * Job Title & Department
  * Employee Type & Group
* Supports nested relational data

### ⏱️ Attendance Management

* Record employee attendance
* Link attendance with leave records
* Supports multiple leave types:

  * Sick Leave
  * Annual Leave
  * Hajj Leave
* Fetch attendance:

  * By employee
  * By record ID
* Delete attendance records

### 🌴 Leave Management

* Apply and manage employee leaves
* Track:

  * Leave type
  * Start & End dates
  * Reason
* Retrieve leave history per employee

### ⚡ FastAPI + Pydantic v2

* RESTful API design
* Auto-generated docs (Swagger & ReDoc)
* Strong validation with Pydantic v2
* Clean and scalable schema structure

### 🗄️ Database & ORM

* PostgreSQL database
* SQLAlchemy ORM
* Proper relationships & eager loading
* Alembic-based migrations

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root:

```env
DB_USER=postgres
DB_PASSWORD=hrms
DB_NAME=postgres
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=70f904050848bb41eefc3df40fda038df3c7b5597b606f15051d395b766cd76f
REFRESH_SECRET_KEY=b5ec27383ee0db6478b61b13a409949697baa2a26ffd6b146164a8c9e817203e

MEDIA_DIRECTORY=./storage/media/apps
ADDON_DIRECTORY=./hrms/addons
MEDIA_BASE_URL=/media/apps
```

---

## 📥 Getting Started (Docker Setup)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/itsosamanadeem/hrms-backend.git
cd hrms-backend
```

---

### 2️⃣ Build & Start Containers

```bash
docker compose up --build -d
```

This will:

* Build the HRMS backend container
* Start PostgreSQL database
* Run services in detached mode

---

## 🛠️ Initial HRMS Setup (IMPORTANT)

After containers are running, execute the following commands **inside your project environment**:

### Step-by-Step Setup

```bash
# 1. Stamp database (initialize migration state)
python -m hrms --stamp

# 2. Create migration revision
python -m hrms --revision "Initial setup"

# 3. Apply migrations
python -m hrms --upgrade

# 4. Initialize database (seed / base setup)
python -m hrms --init-db

# 5. Run FastAPI server
python -m hrms --run-server
```

---

## ⚠️ Important Notes

* Run the above commands **only once during initial setup**
* Ensure PostgreSQL container is running before executing commands
* Database credentials must match your `.env` file
* Migration commands are handled via the custom `hrms` CLI

---

## 🧪 Running Without Docker

```bash
# Create virtual environment
python -m venv .env
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python -m hrms --stamp
python -m hrms --revision "Initial setup"
python -m hrms --upgrade
python -m hrms --init-db

# Run server
python -m hrms --run-server
```

---

## 📚 API Documentation

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📁 Project Structure (Simplified)

```
hrms-backend/
│── hrms/
│   ├── models/
│   ├── schemas/
│   ├── api/
│   ├── addons/
│   └── core/
│
│── alembic/
│── storage/
│── main.py
│── requirements.txt
│── docker-compose.yml
```

---

## 🤝 Contribution Guidelines

* Follow clean architecture principles
* Use Pydantic v2 best practices
* Maintain proper commit history
* Keep modules modular and reusable

---

## 📜 License

This project is licensed with restrictions on ownership reuse.
Contributions and improvements are welcome.

---

## 👨‍💻 Author

**Osama Nadeem**
GitHub: [https://github.com/itsosamanadeem/hrms-backend](https://github.com/itsosamanadeem/hrms-backend)
Year: 2025

---
