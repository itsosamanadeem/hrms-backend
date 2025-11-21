from sqlalchemy import inspect, text
from sqlalchemy.orm import Session, clear_mappers
from sqlalchemy.exc import SQLAlchemyError
from core.utilities.database import engine, Base
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreateTableMixin:
    """Dynamic table registration and migration for PostgreSQL with FK safety."""
    def crud_on_model():
        Base.metadata.create_all(bind=engine,checkfirst=True)