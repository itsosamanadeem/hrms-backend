from hrms.core.utilities.database import Base
from hrms.core.boot.registry.registory import register_model

class HRMSBase(Base):
    __abstract__ = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        table = getattr(cls, "__tablename__", None)
        if table:
            register_model(table, cls)
