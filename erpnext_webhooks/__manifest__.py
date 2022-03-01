# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "REST API for ERPNext Webhook",
    "version": "13.0.1.0.0",
    "category": "Tools",
    "description": """
This module create REST API for ERPNext Webhook to call

* api/create_date(model, vals)

    model = "model.name"
    vals = {
        'payload': {
            'field1': value1,
            'field2_id': value2,  # can be ID or name search string
            'line_ids': [
                {
                    'field3': value3,
                    'field4_id': value4,  # can be ID or name search string
                },
                {..new record..}, {..new record..}, ...
            ],
        }
        'auto_create': {
            'field2_id': {'name': 'some name', ...},
            'field4_id': {'name': 'some name', ...},
            # If more than 1 value, you can use list instead
            # 'field4_id': [{'name': 'some name', ...}, {...}, {...}]
        }
    }

    """,
    "author": "Ecosoft",
    "website": "http://ecosoft.co.th/",
    "depends": ["sale", ],
}
