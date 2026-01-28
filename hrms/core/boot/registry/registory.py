MODEL_REGISTRY: dict[str, type] = {}

def register_model(key: str, model_cls: type):
    MODEL_REGISTRY[key] = model_cls

def get_model(key: str) -> type:
    if key not in MODEL_REGISTRY:
        raise Exception(f"Model '{key}' not registered")
    return MODEL_REGISTRY[key]
