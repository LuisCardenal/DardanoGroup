# -*- coding: utf-8 -*-
{
    'name': "Reporte cotizacion de El Aserradero",

    'author': "Rocket Digital Crafters",
    'website': "https://rocketters.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/cotizacion_aserradero_vista.xml',
        'report/cotizacion_reporte_formato.xml',
    ],
}
