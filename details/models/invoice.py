from odoo import models, fields, api, _
from datetime import *


class DueDate(models.Model):
    _inherit = 'account.invoice'

    date_due = fields.Date(compute="date_due_method", store=True)
    custom_date_due = fields.Date()

    @api.one
    @api.depends('sale_order_template_id', 'custom_date_due')
    def date_due_method(self):
        if self.custom_date_due:
            self.date_due = self.custom_date_due
        elif self.sale_order_template_id:
            self.date_due = self.sale_order_template_id.starttime.date()
