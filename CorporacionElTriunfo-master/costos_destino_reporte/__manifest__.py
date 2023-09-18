# -*- coding: utf-8 -*-
{
    'name': "Reporte para costos en destino",

    'summary': """
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Rocket Digital",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['stock_landed_costs'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/reporte_costos_destinos.xml',
        'report/reporte_costos_destinos_view.xml',
    ],

}
