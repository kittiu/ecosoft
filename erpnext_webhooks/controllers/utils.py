import logging

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class WebhookUtils(models.AbstractModel):
    _name = "webhook.utils"
    _description = "Utils Class"

    def _search_key(self, model):
        """ Return the unique search key for each model, else use 'name' """
        keys = {
            "product.product": "default_code",
            "res.partner": "ref",
        }
        key = keys.get(model, "name")
        return key

    @api.model
    def friendly_create_data(self, model, vals):
        """ Accept friendly data_dict in following format to create data,
            and auto_create data if found no match.
        -------------------------------------------------------------
        vals:
        {
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
        data_dict = vals.get("payload", {})
        auto_create = vals.get("auto_create", {})
        res = {}
        rec = self.env[model].new()  # Dummy reccord
        rec_fields = []
        line_fields = []
        for field, model_field in rec._fields.items():
            if field in data_dict and model_field.type != "one2many":
                rec_fields.append(field)
            elif field in data_dict:
                line_fields.append(field)
        rec_dict = {k: v for k, v in data_dict.items() if k in rec_fields}
        rec_dict = self._finalize_data_to_write(rec, rec_dict, auto_create)
        # Prepare Line Dict (o2m)
        for line_field in line_fields:
            final_line_dict = []
            # Loop all o2m lines, and recreate it
            for line_data_dict in data_dict[line_field]:
                rec_fields = []
                line_fields = []
                for field, model_field in rec[line_field]._fields.items():
                    if field in line_data_dict and model_field.type != "one2many":
                        rec_fields.append(field)
                    elif field in line_data_dict:
                        line_fields.append(field)
                line_dict = {k: v for k, v in line_data_dict.items() if k in rec_fields}
                if line_fields:
                    raise ValidationError(
                        _(
                            "friendly_create_data() support "
                            "only 1 level of one2many lines"
                        )
                    )
                line_dict = self._finalize_data_to_write(
                    rec[line_field], line_dict, auto_create
                )
                final_line_dict.append((0, 0, line_dict))
            rec_dict[line_field] = final_line_dict
        obj = rec.create(rec_dict)
        res = {
            "is_success": True,
            "result": {"id": obj.id},
            "messages": _("Record created successfully"),
        }
        return res

    @api.model
    def friendly_update_data(self, model, vals, key_field):
        """ Accept friendly data_dict in following format to update existing rec
        This method, will always delete o2m lines and recreate it.
        -------------------------------------------------------------
        vals:
        {
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
        },
        key_field: search_key  # i.e., name, ref, code, etc.
        """
        data_dict = vals.get("payload", {})
        auto_create = vals.get("auto_create", {})
        res = {}
        # Prepare Header Dict (non o2m)
        if not key_field or key_field not in data_dict:
            raise ValidationError(_("Method update_data() key_field is not valid!"))
        rec = self.env[model].search([(key_field, "=", data_dict[key_field])])
        if not rec:
            raise ValidationError(
                _('Search key "%s" not found!') % data_dict[key_field]
            )
        elif len(rec) > 1:
            raise ValidationError(
                _('Search key "%s" found mutiple matches!') % data_dict[key_field]
            )
        rec_fields = []
        line_fields = []
        for field, model_field in rec._fields.items():
            if field in data_dict and model_field.type != "one2many":
                rec_fields.append(field)
            elif field in data_dict:
                line_fields.append(field)
        rec_dict = {k: v for k, v in data_dict.items() if k in rec_fields}
        rec_dict = self._finalize_data_to_write(rec, rec_dict, auto_create)
        # Prepare Line Dict (o2m)
        for line_field in line_fields:
            lines = rec[line_field]
            # First, delete all lines o2m
            lines.unlink()
            final_line_dict = []
            final_line_append = final_line_dict.append
            # Loop all o2m lines, and recreate it
            for line_data_dict in data_dict[line_field]:
                rec_fields = []
                rec_fields_append = rec_fields.append
                line_fields = []
                for field, model_field in rec[line_field]._fields.items():
                    if field in line_data_dict and model_field.type != "one2many":
                        rec_fields_append(field)
                    elif field in line_data_dict:
                        line_fields.append(field)
                line_dict = {k: v for k, v in line_data_dict.items() if k in rec_fields}
                if line_fields:
                    raise ValidationError(
                        _(
                            "friendly_update_data() support "
                            "only 1 level of one2many lines"
                        )
                    )
                line_dict = self._finalize_data_to_write(lines, line_dict, auto_create)
                final_line_append((0, 0, line_dict))
            rec_dict[line_field] = final_line_dict
        rec.write(rec_dict)
        res = {
            "is_success": True,
            "result": {"id": rec.id},
            "messages": _("Record updated successfully"),
        }
        return res

    @api.model
    def _finalize_data_to_write(self, rec, rec_dict, auto_create={}):
        """ For many2one, many2many, use name search to get id """
        final_dict = {}
        for key, value in rec_dict.items():
            ffield = rec._fields.get(key, False)
            if ffield:
                ftype = ffield.type
                if key in rec_dict.keys() and ftype in ("many2one", "many2many"):
                    model = rec._fields[key].comodel_name
                    Model = self.env[model]
                    if rec_dict[key] and isinstance(rec_dict[key], str):
                        search_vals = []
                        if ftype == "many2one":
                            search_vals = [rec_dict[key]]
                        elif ftype == "many2many":
                            search_vals = rec_dict[key].split(",")
                            value = []  # for many2many, result will be tuple
                        for val in search_vals:
                            values = Model.name_search(val, operator="=")
                            # If failed, try again by ID
                            if len(values) != 1:
                                if val and isinstance(val, int):
                                    rec = Model.search([("id", "=", val)])
                                    if len(rec) == 1:
                                        values = [(rec.id,)]
                            # Found > 1, can't continue
                            if len(values) > 1:
                                raise ValidationError(
                                    _('"%s" matched more than 1 record') % val
                                )
                            # If not found, but auto_create it
                            if len(values) != 1 and auto_create.get(key):
                                new_recs = []
                                if isinstance(auto_create[key], list):
                                    new_recs += auto_create[key]
                                if isinstance(auto_create[key], dict):
                                    new_recs.append(auto_create[key])
                                for new_rec in new_recs:
                                    self.friendly_create_data(model, {"payload": new_rec})
                                values = Model.name_search(val, operator="=")
                            elif not values:
                                raise ValidationError(_('"%s" found no match.') % val)
                            if ftype == "many2one":
                                value = values[0][0]
                            elif ftype == "many2many":
                                value.append((4, values[0][0]))
            final_dict.update({key: value})
        return final_dict

    @api.model
    def create_data(self, model, vals):
        _logger.info("[{}].create_data(), input: {}".format(model, vals))
        res = self.friendly_create_data(model, vals)
        if res["is_success"]:
            res_id = res["result"]["id"]
            p = self.env[model].browse(res_id)
            res["result"][self._search_key(model)] = p[self._search_key(model)]
        _logger.info("[{}].create_data(), output: {}".format(model, res))
        return res

    @api.model
    def update_data(self, model, vals):
        _logger.info("[{}].update_data(), input: {}".format(model, vals))
        res = self.friendly_update_data(model, vals, self._search_key(model))
        if res["is_success"]:
            res_id = res["result"]["id"]
            p = self.env[model].browse(res_id)
            res["result"][self._search_key(model)] = p[self._search_key(model)]
        _logger.info("[{}].update_data(), output: {}".format(model, res))
        return res

    @api.model
    def create_update_data(self, model, vals):
        _logger.info("[{}].create_update_data(), input: {}".format(model, vals))
        # Update
        search_value = vals["payload"].get(self._search_key(model))
        if not self.search([(self._search_key(model), "=", search_value)]):
            return self.create_data(vals)  # fall back to create
        res = self.friendly_update_data(model, vals, self._search_key(model))
        if res["is_success"]:
            res_id = res["result"]["id"]
            p = self.env[model].browse(res_id)
            res["result"][self._search_key(model)] = p[self._search_key(model)]
        _logger.info("[{}].create_update_data(), output: {}".format(model, res))
        return res
