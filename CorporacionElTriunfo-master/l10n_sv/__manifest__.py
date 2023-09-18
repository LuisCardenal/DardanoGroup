{
    'name': 'El Salvador - Accounting',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': ['account', 'stock', 'sale_margin'],
    'data': [
        # 'data/l10n_sv_chart_data.xml',
        # 'data/account_tax_group_data.xml',
        # 'data/account_chart_template_data.xml',
        # 'data/account_tax_template_data.xml',
        # 'data/account_chart_template_configure_data.xml',
        'views/financial_global_report_views.xml',
        'views/stock_kardex_report_views.xml',
        'views/measure_margin_custom_views.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',
}
