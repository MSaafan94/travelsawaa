from odoo import models,fields ,api
from odoo.exceptions import ValidationError
class SaleOrderInh(models.Model):
    _inherit = 'sale.order'
    # international_group=fields.Integer(compute="calculate_international_group", store=True)
    # international_system = fields.Integer(compute="calculate_international_system", store=True)

    def action_confirm_order(self):
        for rec in self:
                if self.env.user.has_group('sales_extra_fields.group_manager_quotation_template'):
                    rec.state = 'sale'
                else:
                    raise ValidationError('you don\' have authority.')


