import os, ast
from core.utilities.model_content import ModelContent as CM


class CheckModelFiles:
        
    def check_model_file(model_files, models_path):
        for model_file in model_files:
            model_file_path = os.path.join(models_path, f"{model_file}.py")
            # print(f"this is the model file path : {model_file_path}")
            if not os.path.exists(model_file_path):
                print(f"Model file not found: {model_file_path}")
                continue

            # Step 4a: Detect the first class in the file (assumes one class per file)
            classes_name = []
            with open(model_file_path, "r") as mf:
                file_ast = ast.parse(mf.read(), filename=model_file_path)
                class_nodes = [node for node in file_ast.body if isinstance(node, ast.ClassDef)]
                # print(f'this is class node {class_nodes}')
                if not class_nodes:
                    print(f"No class found in {model_file}.py")
                    continue
                for class_name in class_nodes:
                    classes_name.append(class_name)

            print(f"Loading class: {class_name} from {model_file}.py")

            model_class = CM.load_models(model_file_path, classes_name)

            return model_class, model_file_path