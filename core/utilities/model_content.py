import importlib

class ModelContent:

    def load_models(file_path: str, classes_name: list):
        for class_name in classes_name:
            spec = importlib.util.spec_from_file_location(class_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return getattr(module, class_name)