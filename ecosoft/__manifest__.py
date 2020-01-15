# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Ecosoft Customization',
    'version': '13.0.1.0.0',
    'category': 'Localization',
    'description': """
* New Report Layout
* Fix SO and INV form
  * Add Tax Branch
  * Remove Tax Column
    """,
    'author': 'Ecosoft',
    'website': 'http://ecosoft.co.th/',
    'depends': ['web',
                'l10n_th_partner'],
    'data': [
        'data/report_layout.xml',
        'report/invoice_report_templates.xml',
        'report/sale_report_templates.xml',
    ],
}
