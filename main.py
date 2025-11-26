from addons.employees.model.hr_employee import HrEmployee
from addons.attendance.model.attendance_report import IrHrAttendance
from core.router.discover_router import include_routers
from fastapi import FastAPI
from addons.employees.controller.employee_controller import router as employee_router
from addons.attendance.controller.attendance_controller import router as attendance_router

app = FastAPI(title="HRMS API", version="1.0")

include_routers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
