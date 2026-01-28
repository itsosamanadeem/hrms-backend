from sqlalchemy import Column, Integer, ForeignKey, Table
from hrms.addons.base.model.base_model import HRMSBase

ir_hr_group_role_rel = Table(
    "ir_hr_group_role_rel",
    HRMSBase.metadata,
    Column("id", Integer, primary_key=True),
    Column("group_id", Integer, ForeignKey("ir_hr_group.id")),
    Column("role_id", Integer, ForeignKey("ir_hr_role.id")),
)
