from sqlalchemy.orm import registry
from hrms.core.utilities.database import Base

def get_all_models():
    models = set()
    try:
        for mapper in Base.registry.mappers:
            cls = mapper.class_
            models.add(cls)
    except Exception:
        def recurse(cls):
            for sub in cls.__subclasses__():
                try:
                    if hasattr(sub, '__tablename__') and sub.__tablename__:
                        models.add(sub)
                except Exception:
                    pass
                recurse(sub)
        recurse(Base)


    return models