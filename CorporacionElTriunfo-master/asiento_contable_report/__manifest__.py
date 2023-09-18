# -*- coding: utf-8 -*-
{
    'name': "Formato reporte asiento contable",

    'summary': """
       """,

    'description': """
    
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['account', 'base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/asiento_contable_reporte.xml',
        'report/asiento_contable_reporte_view.xml',
        'report/report.xml',
        'report/factura_consumidor_final_exento_view.xml',
        'report/factura_credito_fiscal_view.xml',
        'report/report_consumidor_final_view.xml',
        'report/report_exportacion_view.xml',
        'report/report_nota_de_credito_view.xml',
        'report/report_nota_devolucion_view.xml',
        'report/report_credito_fiscal_exento_view.xml',
        'report/report_retencion.xml',
        'report/report_consumidor_final_retencion_view.xml',
    ],
    # only loaded in demonstration mode
}
