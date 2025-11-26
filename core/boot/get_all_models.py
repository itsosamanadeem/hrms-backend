from sqlalchemy.orm import registry
from core.utilities.database import Base




def get_all_models():
    # Prefer Base.registry if available
    models = set()
    try:
        for mapper in Base.registry.mappers:
            cls = mapper.class_
            models.add(cls)
    except Exception:
    # fallback: inspect Base subclasses (less robust)
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