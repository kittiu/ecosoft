# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, fields


class HrExpense(models.Model):
    _inherit = "hr.expense"

    bill_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vendor",
    )
