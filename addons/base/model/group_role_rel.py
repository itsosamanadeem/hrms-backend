from sqlalchemy import Column, Integer, ForeignKey, Table
from hrms.core.utilities.database import Base

ir_hr_group_role_rel = Table(
    "ir_hr_group_role_rel",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("group_id", Integer, ForeignKey("ir_hr_group.id")),
    Column("role_id", Integer, ForeignKey("ir_hr_role.id")),
)
