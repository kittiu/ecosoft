# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    name = fields.Char(translate=False)
