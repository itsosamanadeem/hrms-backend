import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging
from dotenv import load_dotenv

load_dotenv(dotenv_path="config.env")

# --- Environment Variables ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# --- Build Database URL ---
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- SQLAlchemy Core Objects ---
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Optional Utility Function ---
def get_db():
    """Dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_connection():
    """Explicitly test connection (optional)."""
    try:
        conn = engine.connect()
        print("Database connection established successfully.")
        Base.metadata.create_all(bind=engine)
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")


# if __name__== "__main__":
#     init_connection()


