# core/migrations/manager.py
import os
import glob
import time
import re
import textwrap
from typing import Dict, List
from alembic.config import Config
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import Enum as SAEnum
from hrms.core.utilities.database import Base, DATABASE_URL

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ALEMBIC_DIR = os.path.join(PROJECT_ROOT, "alembic")
VERSIONS_DIR = os.path.join(ALEMBIC_DIR, "versions")
ALEMBIC_INI = os.path.join(PROJECT_ROOT, "alembic.ini")


def ensure_versions_dir():
    os.makedirs(VERSIONS_DIR, exist_ok=True)


def _engine():
    return create_engine(DATABASE_URL)


def detect_diffs():
    eng = _engine()
    with eng.connect() as conn:
        ctx = MigrationContext.configure(conn, opts={"compare_type": True})
        diffs = compare_metadata(ctx, Base.metadata)
    return diffs


def find_fresh_revision(pattern="*_auto_*.py", wait_secs=3.0):
    deadline = time.time() + wait_secs
    while time.time() < deadline:
        files = glob.glob(os.path.join(VERSIONS_DIR, pattern))
        if files:
            files_sorted = sorted(files, key=os.path.getmtime, reverse=True)
            return files_sorted[0]
        time.sleep(0.05)
    # fallback: newest file
    files = glob.glob(os.path.join(VERSIONS_DIR, "*.py"))
    files_sorted = sorted(files, key=os.path.getmtime, reverse=True)
    return files_sorted[0] if files_sorted else None


def collect_enums_from_metadata() -> Dict[str, List[str]]:
    enums = {}
    for table in Base.metadata.sorted_tables:
        for col in table.columns:
            if isinstance(col.type, SAEnum):
                enum_name = getattr(col.type, "name", None)
                enum_values = list(col.type.enums or [])
                if not enum_name:
                    enum_name = f"{table.name}_{col.name}_enum"
                enums[enum_name] = enum_values
    return enums


def patch_revision_add_enums(rev_path: str, enums: Dict[str, List[str]]):
    if not enums:
        return
    with open(rev_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "from sqlalchemy.dialects import postgresql" not in content:
        content = content.replace("import sqlalchemy as sa", "import sqlalchemy as sa\nfrom sqlalchemy.dialects import postgresql")

    create_lines = []
    drop_lines = []
    for name, values in enums.items():
        vals_literal = ", ".join(repr(v) for v in values)
        create_lines.append(f"    {name}_enum = postgresql.ENUM({vals_literal}, name={repr(name)})")
        create_lines.append(f"    {name}_enum.create(op.get_bind(), checkfirst=True)")
        create_lines.append("")
        drop_lines.insert(0, f"    {name}_enum = postgresql.ENUM({vals_literal}, name={repr(name)})")
        drop_lines.insert(0, f"    {name}_enum.drop(op.get_bind(), checkfirst=True)")
        drop_lines.insert(0, "")

    create_block = "\n".join(create_lines).rstrip() + "\n\n"
    drop_block = "\n".join(drop_lines).rstrip() + "\n\n"

    content = re.sub(r"(def upgrade\(\):\n)", r"\1" + create_block, content, count=1, flags=re.MULTILINE)
    content = re.sub(r"(def downgrade\(\):\n)", r"\1" + drop_block, content, count=1, flags=re.MULTILINE)

    with open(rev_path, "w", encoding="utf-8") as f:
        f.write(content)


def patch_revision_defer_fks_and_create_tables(rev_path: str):
    eng = _engine()
    inspector = inspect(eng)
    existing_tables = set(inspector.get_table_names())

    with open(rev_path, "r", encoding="utf-8") as f:
        content = f.read()

    meta_tables = [t for t in Base.metadata.sorted_tables if t.name not in existing_tables]

    create_blocks = []
    drop_blocks = []
    for t in meta_tables:
        columns = []
        for col in t.columns:
            col_repr = f"sa.Column({repr(col.name)}, {repr(str(col.type))}"
            if col.primary_key:
                col_repr += ", primary_key=True"
            if not col.nullable:
                col_repr += ", nullable=False"
            if col.unique:
                col_repr += ", unique=True"
            if col.server_default is not None:
                col_repr += f", server_default=sa.text({repr(str(col.server_default.arg))})"
            col_repr += ")"
            columns.append(col_repr)
        cols_joined = ",\n        ".join(columns)
        create_stmt = textwrap.dedent(f"""\
            op.create_table(
                {repr(t.name)},
                {cols_joined},
            )
        """)
        drop_stmt = f"op.drop_table({repr(t.name)})"
        create_blocks.append(create_stmt)
        drop_blocks.insert(0, drop_stmt)

    if create_blocks:
        insertion = "\n\n# Auto-created missing tables (from metadata)\n" + "\n\n".join(create_blocks) + "\n\n"
        content = re.sub(r"(def upgrade\(\):\n)", r"\1" + insertion, content, count=1, flags=re.MULTILINE)

    if drop_blocks:
        drop_insertion = "\n\n# Auto-drop missing tables (reverse order)\n" + "\n    ".join(drop_blocks) + "\n\n"
        content = re.sub(r"(def downgrade\(\):\n)", r"\1" + "    " + drop_insertion, content, count=1, flags=re.MULTILINE)

    with open(rev_path, "w", encoding="utf-8") as f:
        f.write(content)


class MigrationManager:
    def __init__(self, alembic_ini_path: str = ALEMBIC_INI):
        ensure_versions_dir()
        self.alembic_cfg = Config(alembic_ini_path)
        if not self.alembic_cfg.get_main_option("script_location"):
            self.alembic_cfg.set_main_option("script_location", ALEMBIC_DIR)

    def run(self, message: str = "auto_migration", apply: bool = True):
        diffs = detect_diffs()
        if not diffs:
            print("✅ No schema changes detected")
            return

        print("⚡ Detected schema changes. Generating migration revision...")
        command.revision(self.alembic_cfg, autogenerate=True, message=message)

        rev_file = find_fresh_revision()
        print("Generated revision:", rev_file)

        enums = collect_enums_from_metadata()
        if enums:
            print("Patching revision to create ENUM types first:", list(enums.keys()))
            patch_revision_add_enums(rev_file, enums)
        else:
            print("No ENUM types detected to patch.")

        print("Patching revision to ensure missing tables are created and FKs deferred as needed...")
        patch_revision_defer_fks_and_create_tables(rev_file)

        print("Migration file created at:", rev_file)
        if apply:
            print("Applying migration (alembic upgrade head)...")
            command.upgrade(self.alembic_cfg, "head")
            print("✅ Migration applied")
        else:
            print("Dry-run: migration not applied. Review the file and apply with alembic upgrade head.")
