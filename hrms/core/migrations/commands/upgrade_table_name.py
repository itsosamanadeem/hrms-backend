import logging
from alembic.operations import Operations
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from alembic.config import Config
from sqlalchemy import text, inspect

log = logging.getLogger("hrms.alembic.rename_table")
log.setLevel(logging.INFO)

def upgrade_table_name(config: Config, old_table: str, new_table: str):
    """
    Safely rename a table in PostgreSQL, including sequences, indexes, FKs, and metadata registration.
    """
    script = ScriptDirectory.from_config(config)

    def do_rename(rev, context):
        conn = context.connection
        op = Operations(context)

        inspector = inspect(conn)
        if old_table not in inspector.get_table_names():
            raise ValueError(f"Table '{old_table}' does not exist")

        log.info(f"Renaming table '{old_table}' -> '{new_table}'")
        op.rename_table(old_table, new_table)

        # Rename sequences (for SERIAL / Identity columns)
        for column in inspector.get_columns(new_table):
            if column["default"] and "nextval" in str(column["default"]):
                seq_name = column["default"].split("'")[1].split("'")[0]
                new_seq_name = seq_name.replace(old_table, new_table)
                log.info(f"Renaming sequence '{seq_name}' -> '{new_seq_name}'")
                conn.execute(text(f'ALTER SEQUENCE "{seq_name}" RENAME TO "{new_seq_name}"'))

        # Rename indexes
        for idx in inspector.get_indexes(new_table):
            if old_table in idx["name"]:
                old_idx_name = idx["name"]
                new_idx_name = old_idx_name.replace(old_table, new_table)
                log.info(f"Renaming index '{old_idx_name}' -> '{new_idx_name}'")
                conn.execute(text(f'ALTER INDEX "{old_idx_name}" RENAME TO "{new_idx_name}"'))

        # Rename foreign key constraints referencing this table
        for table_name in inspector.get_table_names():
            for fk in inspector.get_foreign_keys(table_name):
                if fk["referred_table"] == old_table:
                    old_fk_name = fk["name"]
                    new_fk_name = old_fk_name.replace(old_table, new_table)
                    log.info(f"Renaming foreign key '{old_fk_name}' -> '{new_fk_name}' on table '{table_name}'")
                    conn.execute(text(f'ALTER TABLE "{table_name}" RENAME CONSTRAINT "{old_fk_name}" TO "{new_fk_name}"'))

        # Update ir_hr_model metadata table if exists
        if "ir_hr_model" in inspector.get_table_names():
            log.info(f"Updating 'ir_hr_model' for table '{old_table}' -> '{new_table}'")
            conn.execute(
                text("UPDATE ir_hr_model SET name = :new_name WHERE name = :old_name"),
                {"old_name": old_table, "new_name": new_table},
            )

        log.info("Table rename completed successfully")

    with EnvironmentContext(
        config,
        script,
        as_sql=False,
        fn=do_rename,
    ):
        pass
