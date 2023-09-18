# -*- coding: utf-8 -*-
{
    'name': "Reportes contables El Salvador",

    'summary': """
       """,

    'description': """
    Modulo para reportes contables en El Salvador.
    """,

    'author': "Rocketters",
    'website': "https://rocketters.com/",

    'category': 'Account',
    'version': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'product'],

    # always loaded
    'data': [
        'views/product_template_sv.xml',
        'views/informe.xml',

    ],
    # only loaded in demonstration mode
}
