def get_module_name(model_class):
    """
    Extracts module name from:
    hrms.addons.<module>.model.<file>
    """
    module_path = model_class.__module__.split('.')
    if "addons" in module_path:
        addons_index = module_path.index("addons")
        if len(module_path) > addons_index + 1:
            return module_path[addons_index + 1]
    return "base"