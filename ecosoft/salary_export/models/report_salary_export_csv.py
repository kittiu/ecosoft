# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import csv
import pytz

from odoo import models, _
from odoo.exceptions import UserError


class SalaryExportCSV(models.AbstractModel):
    _name = "report.report_csv.salary_export"
    _inherit = "report.report_csv.abstract"
    _description = "Salary Export to CSV"

    def generate_csv_report(self, writer, data, exports):
        tz = self.env.context.get('tz') or self.env.user.tz or 'UTC'
        banks = self.env.user.partner_id.company_id.bank_ids.filtered(
            lambda l: l.bank_id.name == "Kasikorn Bank")
        if not banks:
            raise UserError(_("No Kasikorn Bank in this company"))
        for obj in exports:
            tz_date = obj.date.astimezone(pytz.timezone(tz))
            obj_date = tz_date.strftime('%y%m%d')
            obj_date_transfer = obj.date_transfer.strftime('%y%m%d')
            i = 0
            for line in obj.line_ids:
                i += 1
                acc_number, acc_holder_name = (
                    line.employee_id.bank_account_id.acc_number or "",
                    line.employee_id.bank_account_id.acc_holder_name or ""
                )
                writer.writerow({
                    "1-1": "D",
                    "2-7": str(i).zfill(6),
                    "8-8": "".rjust(1),
                    "9-12": "".rjust(4),
                    "13-13": "".rjust(1),
                    "14-20": "".rjust(7),
                    "21-21": "".rjust(1),
                    "22-31": acc_number,
                    "32-32": "".rjust(1),
                    "33-47": "{0:.2f}".format(line.amount).replace(".","").zfill(15),
                    "48-48": "".rjust(1),
                    "49-54": obj_date,
                    "55-55": "".rjust(1),
                    "56-78": "".rjust(23),
                    "79-79": "".rjust(1),
                    "80-129": acc_holder_name.ljust(50),
                    "130-135": obj_date_transfer,
                    "136-138": "".rjust(3),
                    "139-154": "".rjust(16),
                    "155-204": "".rjust(50),
                    "205-205": "".rjust(1),
                    "206-255": "".rjust(50),
                    "256-305": "".rjust(50),
                    "306-318": "".rjust(13),
                    "319-331": "".rjust(13),
                    "332-344": "".rjust(13),
                    "345-354": "".rjust(10),
                    "355-367": "".rjust(13),
                    "368-397": "".rjust(30),
                    "398-427": "".rjust(30),
                    "428-457": "".rjust(30),
                    "458-487": "".rjust(30),
                })

    def csv_report_options(self):
        res = super().csv_report_options()
        res["fieldnames"].append("1-1")
        res["fieldnames"].append("2-7")
        res["fieldnames"].append("8-8")
        res["fieldnames"].append("9-12")
        res["fieldnames"].append("13-13")
        res["fieldnames"].append("14-20")
        res["fieldnames"].append("21-21")
        res["fieldnames"].append("22-31")
        res["fieldnames"].append("32-32")
        res["fieldnames"].append("33-47")
        res["fieldnames"].append("48-48")
        res["fieldnames"].append("49-54")
        res["fieldnames"].append("55-55")
        res["fieldnames"].append("56-78")
        res["fieldnames"].append("79-79")
        res["fieldnames"].append("80-129")
        res["fieldnames"].append("130-135")
        res["fieldnames"].append("136-138")
        res["fieldnames"].append("139-154")
        res["fieldnames"].append("155-204")
        res["fieldnames"].append("205-205")
        res["fieldnames"].append("206-255")
        res["fieldnames"].append("256-305")
        res["fieldnames"].append("306-318")
        res["fieldnames"].append("319-331")
        res["fieldnames"].append("332-344")
        res["fieldnames"].append("345-354")
        res["fieldnames"].append("355-367")
        res["fieldnames"].append("368-397")
        res["fieldnames"].append("398-427")
        res["fieldnames"].append("428-457")
        res["fieldnames"].append("458-487")
        res["delimiter"] = ";"
        res["quoting"] = csv.QUOTE_NONE
        return res

    def create_csv_report(self, docids, data):
        (fdata, ext) = super().create_csv_report(docids, data)
        fdata = fdata.replace(";", "")
        return "%s\n%s" % (self._get_header(docids), fdata), ext

    def _get_header(self, docids):
        tz = self.env.context.get('tz') or self.env.user.tz or 'UTC'
        # Bank
        banks = self.env.user.partner_id.company_id.bank_ids.filtered(
            lambda l: l.bank_id.name == "Kasikorn Bank")
        if not banks:
            raise UserError(_("No Kasikorn Bank in this company"))
        company_acc_holder_name = banks[0].acc_holder_name if banks else ""
        company_acc_number = banks[0].acc_number if banks else ""
        company_acc_number = company_acc_number.replace(" ", "")
        # Amount
        obj = self.env["salary.export"].browse(docids)
        obj.ensure_one()
        total_amount = sum(obj.line_ids.mapped("amount"))
        tz_date = obj.date.astimezone(pytz.timezone(tz))
        obj_date = tz_date.strftime('%y%m%d')
        obj_date_transfer = obj.date_transfer.strftime('%y%m%d')
        emp_count = len(obj.line_ids)
        header = {
            "1-1": "H",
            "2-4": "PCT",
            "5-20": "".rjust(16),
            "21-26": "000000",
            "27-27": "".rjust(1),
            "28-31": "".rjust(4),
            "32-32": "".rjust(1),
            "33-39": "".rjust(7),
            "40-40": "".rjust(1),
            "41-50": company_acc_number,
            "51-51": "".rjust(1),
            "52-66": '{0:.2f}'.format(total_amount).replace(".","").zfill(15),
            "67-67": "".rjust(1),
            "68-73": obj_date_transfer,
            "74-74": "".rjust(1),
            "75-97": "".rjust(23),
            "98-98": "".rjust(1),
            "99-148": company_acc_holder_name.ljust(50),
            "149-154": obj_date,
            "155-172": ("%sN" % emp_count).zfill(18),
            "173-173": "N",
            "174-178": "".rjust(5),
        }
        return "".join(header.values())
