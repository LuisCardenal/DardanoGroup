# -*- coding: utf-8 -*-
{
    'name': "Edit fields",
    'description': "Edit fields that are readable only in the module purchase",
    'author': "Rocket Digital",
    'category': 'Purchase',
    'version': '1.0',
    'depends': ['base', 'purchase', 'stock', 'sale_management'],
    'data': [
        'views/purchase_edit_date.xml',
        'views/stock_edit_date.xml',
    ],
    'license': 'LGPL-3',
}
