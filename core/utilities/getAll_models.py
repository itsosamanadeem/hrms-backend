from sqlalchemy.orm import DeclarativeMeta
from core.utilities.database import Base

def get_all_models():
    """Returns only real SQLAlchemy mapped models (skips mixins & abstract classes)."""
    models = set()

    def recurse(cls):
        for subclass in cls.__subclasses__():
            # Must be a SQLAlchemy declarative model
            if isinstance(subclass, DeclarativeMeta):
                tablename = getattr(subclass, "__tablename__", None)

                # Only real models have __tablename__
                if tablename not in (None, "", False):
                    models.add(subclass)

            recurse(subclass)

    recurse(Base)
    return models

def model_columns(model_name):
    all_models = get_all_models()

    # Build map: "tablename" → ModelClass
    model_map = {cls.__tablename__.lower(): cls for cls in all_models}

    key = model_name.lower()

    if key not in model_map:
        raise ValueError(f"Model '{model_name}' not found in loaded models.")

    model_class = model_map[key]
    print(f"Using Model Class: {model_class.__name__}")

    model_columns = {col.name for col in model_class.__table__.columns}
    
    return model_columns
