def get_all_modules_in_addons():
    import pkgutil
    from pathlib import Path
    import hrms.addons
    modules = []
    for _, module_name, _ in pkgutil.iter_modules(hrms.addons.__path__):
        modules.append(module_name)
    return modules