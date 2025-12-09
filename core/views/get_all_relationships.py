
def get_all_relationships():
    import sqlalchemy.orm
    from hrms.core.utilities.database import Base

    models = {}

    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        table_name = model_class.__tablename__
        models[table_name] = model_class

    return models