# Copyright 2022 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import http
from odoo.http import request
from odoo import models


class ERPNextController(http.Controller):

    @http.route("/api/create_data", type="json", auth="none")
    def create_data(self, model, vals):
        """
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
        """
        # Authentication
        header = request.httprequest.headers
        db, login, password = header["db"], header["login"], header["password"]
        uid = request.session.authenticate(db, login, password)
        # Create Data
        res = request.env["webhook.utils"].create_data(model, vals)
        return res


