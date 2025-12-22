from hrms.core.utilities.database import SessionLocal
from hrms.addons.base.model.ir_hr_system_boot import IrHrSystemBootStrap
from hrms.addons.base.model.ir_hr_users import User
from hrms.core.security import hash_password

def seed_super_user(db):
    
    bootstrap = db.query(IrHrSystemBootStrap).filter(
        IrHrSystemBootStrap.key == "super_admin"
    ).first()

    if bootstrap and bootstrap.completed:
        return

    admin = User(
        name="Administrator",
        email="admin@hrms.local",
        password=hash_password("Admin@123"),
        role="super_admin",
        is_super_admin=True,
        is_active=True,
        must_change_password=True,
        must_change_email=True,
    )

    db.add(admin)
    db.add(IrHrSystemBootStrap(
        key="super_admin",
        completed=True
    ))

    db.commit()