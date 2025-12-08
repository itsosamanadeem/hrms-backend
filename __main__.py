import sys
from pathlib import Path
from alembic.config import Config
from alembic import command
from hrms.core.boot.initializer import initialize_system
# from hrms.api.main import start_app
import uvicorn

def parse_args():
    args = {
        "--init-db": False,
        "--stamp": False,
        "--revision": None,
        "--upgrade": False,
        "--run-server": False,
        "--host": "0.0.0.0",
        "--port": "8000",
    }

    for i, arg in enumerate(sys.argv):
        if arg == "--init-db":
            args["--init-db"] = True

        if arg == "--stamp":
            args["--stamp"] = True

        if arg == "--revision" and i + 1 < len(sys.argv):
            args["--revision"] = sys.argv[i + 1]

        if arg == "--upgrade":
            args["--upgrade"] = True

        if arg == "--run-server":
            args["--run-server"] = True

        if arg == "--host" and i + 1 < len(sys.argv):
            args["--host"] = sys.argv[i + 1]

        if arg == "--port" and i + 1 < len(sys.argv):
            args["--port"] = sys.argv[i + 1]

    return args

# --- Alembic Utility ---
ALEMBIC_CFG = Config(str(Path(__file__).resolve().parent / "alembic.ini"))

def alembic_stamp():
    command.stamp(ALEMBIC_CFG, "head")
    print("Database stamped to head")

def alembic_revision(message: str):
    if not message:
        raise ValueError("Please provide a message for revision using --revision 'message'")
    command.revision(ALEMBIC_CFG, message=message, autogenerate=True)
    print(f"Revision generated: {message}")

def alembic_upgrade():
    command.upgrade(ALEMBIC_CFG, "head")
    print("Database upgraded to head")

def run_server(host,port):
    # app = start_app()
    uvicorn.run("hrms.api.main:app", host=host, port=int(port), reload=True)

# --- Main Execution ---
if __name__ == "__main__":
    args = parse_args()

    if args["--init-db"]:
        initialize_system()
        print("Database initialized successfully.")

    if args["--stamp"]:
        alembic_stamp()

    if args["--revision"]:
        alembic_revision(args["--revision"])

    if args["--upgrade"]:
        alembic_upgrade()

    if args["--run-server"]:
        run_server(args["--host"], args["--port"])