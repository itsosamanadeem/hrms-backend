import sys
from alembic.config import Config
from core.migrations.commands.upgrade_table_name import upgrade_table_name

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python alembic_custom.py <old_table> <new_table>")
        sys.exit(1)

    old_table = sys.argv[1]
    new_table = sys.argv[2]

    alembic_cfg = Config("alembic.ini")
    upgrade_table_name(alembic_cfg, old_table, new_table)
