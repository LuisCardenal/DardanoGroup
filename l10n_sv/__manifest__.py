# -*- coding: utf-8 -*-
{
    'name': "Localization SV Rocketters",

    'summary': """
       """,

    'description': """
    Modulo para automatizar contabilidad de El Salvador.
    """,

    'author': "Rocketers",
    'website': "https://rocketters.com/",

    'category': 'Account',
    'version': '1',
    'license': 'LGPL-3',
    'summary': 'En este modulo se puede automatizar el apartado de reportes y facturas agregando nuevos campos relevantes.',

    # any module necessary for this one to work correctly
    'depends': ['account', 'base', 'contacts', 'hr', 'sale'],

    # always loaded
    'data': [

        'views/hr_employee_view.xml',
        'views/res_partner_sv.xml',
        'views/account_move_view_sv.xml',
        'views/account_journal_view.xml',
        'views/sale_order_sv.xml',
        # 'views/informe.xml',
        # 'views/product_template_sv.xml',



    ],
    # only loaded in demonstration mode
}
