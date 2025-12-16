HRMS Project
Human Resource Management System (HRMS)

A modern HRMS backend built with FastAPI, SQLAlchemy, PostgreSQL, and Pydantic v2 for managing employees, attendance, leaves, and other HR processes.

🚀 Features
1. Employee Management

Add, update, and delete employee records

Employee details:

Name

Email

Phone

Job title

Department

Employee type & group

Support for nested employee-related data

2. Attendance Management

Record employee attendance

Optional leave linkage

Multiple leave types supported:

Sick

Annual

Hajj

Retrieve attendance:

By employee

By attendance record ID

Delete attendance records

3. Leave Management

Apply leaves for employees

Track:

Leave type

Start & end dates

Reason

Retrieve leave history per employee

4. FastAPI & Pydantic v2

Modern REST API design

Automatic Swagger & ReDoc documentation

Strong type validation

Nested Pydantic v2 schemas

Production-ready schema conversion

5. Database & ORM

PostgreSQL backend

SQLAlchemy ORM

Proper model relationships

Eager loading for better performance

Alembic migrations supported

⚙️ Environment Variables (config.env)
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=hrms_db
DB_HOST=localhost
DB_PORT=5432

📥 Cloning the Repository
git clone https://github.com/itsosamanadeem/hrms-backend.git
cd hrms-backend

🐳 Docker Compose (PostgreSQL + HRMS + Portainer)
version: '3.8'

services:
  hrms_app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: hrms_app
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=postgres
      - DB_PASSWORD=hrms
      - DB_NAME=postgres
      - SECRET_KEY=V-YWu6ClrSOjaJ_BgXq4zwK9KUy7poM5H11hCg5H0ypuN0gUVaa6oh99-zljjXd1t7WMGd8zl_eloSJXecgjHA
      - REFRESH_SECRET_KEY=ZIGz5X1j4hzHhyHriZE71f07SRuBNoptVRC_IIpFwu_Jpu6WArCmNA5OqskE7FDpYSY6dzWmYzYDDeLDFbsJNA
    depends_on:
      - db
    restart: always

  db:
    image: postgres:latest
    container_name: hrms_db
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=hrms
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - hrms_db_data:/var/lib/postgresql/data/pgdata
    restart: always

  portainer:
    container_name: portainer
    image: portainer/portainer-ce:latest
    ports:
      - "9000:9000"
    volumes:
      - portainer_data:/data
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped

volumes:
  hrms_db_data:
  portainer_data:

🐳 Docker Usage Notes (Important)
No Manual Migrations Needed with Docker

If you are using Docker Compose, you do not need to run Alembic migrations manually.

Simply start or restart the backend container:

docker compose up -d
docker compose restart hrms_app


✅ The backend container will:

Run Alembic migrations automatically (via entrypoint.sh)

Skip already applied migrations safely

Start the FastAPI server

Connect to PostgreSQL using Docker networking

❌ Do not run this manually when using Docker:

alembic upgrade head

🔁 Does entrypoint.sh Run on Container Restart?

Yes.

Every time the container is started or restarted, Docker automatically executes the ENTRYPOINT.

This means:

entrypoint.sh runs on:

docker compose up

docker compose restart hrms_app

Container crash & auto-restart

Database migrations are always applied safely

No data loss (PostgreSQL uses volumes)

✅ Recommended entrypoint.sh
#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000

🧪 Local Installation (Without Docker)
# Create virtual environment
python -m venv .env
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations manually
alembic upgrade head

# Start server
uvicorn main:app --reload

📚 API Documentation

Swagger UI:
http://127.0.0.1:8000/docs

ReDoc:
http://127.0.0.1:8000/redoc

📜 License & Contribution

License restricts taking ownership of the code

Enhancements and contributions are welcome

Follow:

Project structure

Pydantic v2 best practices

Clean commit history

👨‍💻 Author

Osama Nadeem
GitHub: https://github.com/itsosamanadeem/hrms-backend

Year: 2025