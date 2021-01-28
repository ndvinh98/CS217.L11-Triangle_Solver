# Copyright 2020 Voltrans (https://voltransvn.com)

{
    "name": "Triangle Solver",
    "summary": "Triangle Solver",
    "version": "13.0.1.0.0",
    "description": """
        Triangle Solver
    """,
    "author": "Voltrans",
    "website": "https://github.com/ndvinh98",
    "category": "math",
    # any module necessary for this one to work correctly
    "depends": ["base",],
    # always loaded
    "data": ["security/ir.model.access.csv", "views/triangle_problem_view.xml",],
    "qweb": [],
    "installable": True,
    "auto_install": False,
    "application": False,
    "external_dependencies": {"python": ["bs4",],},
}
