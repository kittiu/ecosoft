# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Thailand (Ecosoft) - Accounting',
    'version': '1.0',
    'category': 'Localization',
    'description': """
Chart of Accounts for Thailand.
===============================

Thai accounting chart and localization.
    """,
    'author': 'Ecosoft',
    'website': 'http://ecosoft.co.th/',
    'depends': ['account'],
    'data': [
        'data/account_data.xml',
        'data/l10n_th_chart_data.xml',
        'data/account.account.template.csv',
        'data/l10n_th_chart_post_data.xml',
        'data/account_tax_report_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_chart_template_data.xml',
    ],
    'post_init_hook': '_preserve_tag_on_taxes',
}
