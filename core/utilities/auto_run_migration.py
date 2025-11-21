# auto_migrate.py
import os
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from core.utilities.database import Base, DATABASE_URL

def detect_pending_migrations():
    """
    Returns a list of pending schema differences between models and DB
    """
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        diffs = compare_metadata(ctx, Base.metadata)
    return diffs

def run_auto_migration():
    """
    Auto-generate and apply migration
    """
    diffs = detect_pending_migrations()
    if not diffs:
        print("✅ No schema changes detected")
        return

    print("⚡ Detected schema changes:", diffs)
    
    # Load alembic config
    alembic_cfg = Config("alembic.ini")
    
    # Generate migration file
    command.revision(alembic_cfg, autogenerate=True, message="auto migration")
    
    # Apply migration
    command.upgrade(alembic_cfg, "head")
    print("🚀 Auto migration applied")
