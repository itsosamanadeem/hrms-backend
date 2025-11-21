from fastapi import FastAPI
from core.module_loader import loader
from core.utilities.auto_run_migration import run_auto_migration

app = FastAPI(title="HRMS")

@app.on_event("startup")
def main():
    # Load your modules first
    loader()
    
    # Detect and apply schema changes automatically
    run_auto_migration()

@app.get("/")
def read_root():
    return {"message": "Welcome to the HRMS API!"}
