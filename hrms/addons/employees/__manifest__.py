manifest = {
    "name": "Employees",
    "category": "Human Resources",
    "version": "1.0.0",
    "depends": ['base'],
    "data": {
        "views": [
            "views/employee.xml",
            "views/employee_list.xml",
            # "views/department_views.py",
        ],
    },
    "application": True,
    "cover_image": "static/cover.svg",
    "auto_install": True
}
