from alembic.config import Config
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine
from core.utilities.database import Base, DATABASE_URL

def detect_pending_migrations():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        diffs = compare_metadata(ctx, Base.metadata)
    return diffs

def run_auto_migration():
    diffs = detect_pending_migrations()
    if not diffs:
        print("✅ No schema changes detected")
        return


    print("⚡ Detected schema changes. Generating migration...")
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg,'head')
    command.revision(alembic_cfg, autogenerate=True, message="auto migration")
    command.upgrade(alembic_cfg, "head")
    print("🚀 Auto migration applied")