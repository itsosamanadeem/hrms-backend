# HRMS Project

**Human Resource Management System (HRMS)**

A modern HRMS backend built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Pydantic v2** for managing employees, attendance, leaves, and other HR processes.

---

## Features

### 1. Employee Management

* Add, update, and delete employee records
* Employee details: name, email, phone, job title, department, employee type and group
* Support for nested employee-related data

### 2. Attendance Management

* Record employee attendance with optional leaves
* Supports multiple leave types (Sick, Annual, Hajj)
* Retrieve attendance by employee or by record ID
* Delete attendance records

### 3. Leave Management

* Apply leaves for employees
* Track leave types, start/end dates, and reason
* Retrieve leave history per employee

### 4. FastAPI & Pydantic v2

* Modern API design with type validation and auto-documentation
* Efficient nested Pydantic models for relationships
* Production-ready Pydantic v2 schema conversion

### 5. Database & ORM

* PostgreSQL backend
* SQLAlchemy ORM with relationships
* Eager loading for performance
* Alembic migrations supported

### 6. Environment Variables (config.env)

```
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=hrms_db
DB_HOST=localhost
DB_PORT=5432
```

### 7. Cloning

```bash
# Clone the repo
git clone https://github.com/itsosamanadeem/hrms-backend.git
cd hrms-backend
```

### 8. Docker Compose for PostgreSQL & Portainer

```yaml
version: '3.8'
services:
  db:
    image: postgres:latest
    ports:
      - '5432:5432'
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=hrms
      - POSTGRES_USER=postgres
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - hrms_db_data:/var/lib/postgresql/data/pgdata
    restart: always

  portainer:
    container_name: Portainer
    image: portainer/portainer-ce:latest
    ports:
      - '9000:9000'
    volumes:
      - portainer_data:/data
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped

volumes:
  hrms_db_data:
  portainer_data:
```

### 9. Installation & Run

```bash
# Create virtual environment
python -m venv .env
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

### 10. Documentation

* FastAPI provides **Swagger UI**: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

### 11. License & Contribution

* License restricts taking ownership of code; users can enhance and contribute
* Contributions should follow project structure and Pydantic v2 best practices

---

**Author:** Osama Nadeem
**GitHub:** [https://github.com/itsosamanadeem/hrms-backend](https://github.com/itsosamanadeem/hrms-backend)
**Date:** 2025
