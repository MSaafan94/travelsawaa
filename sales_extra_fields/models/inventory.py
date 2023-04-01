# from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class SaleOrderTemplateOption(models.Model):
    _inherit = "sale.order.template.option"
    _order = 'sequence'

    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of sale quote lines.",
                              default=10)
    hotel = fields.Many2one('model.hotel', string="Hotel")
    inventory = fields.Float(string="Inventory", default=100)
    stock = fields.Float(string="Stock", compute="_compute_stock",)
    available = fields.Float(string="Available", compute="_compute_available")
    analytic_tag_ids = fields.Many2one('account.analytic.tag', 'Analytic Tags')
    template_name = fields.Char(related='sale_order_template_id.name', store=True)
    product_category = fields.Selection([('room', 'Room'), ('visa', 'Visa'), ('program', 'Program'), ('domestic', 'Domestic'), ('international', 'International')], compute='compute_type',)

    @api.one
    def compute_type(self):
        self.product_category = self.product_id.product_category

    @api.depends('product_id', 'inventory', 'stock')
    def _compute_stock(self):
        for rec in self:
            rec.stock = 0
            rec.available = 0
            if rec.product_id:
                sale_order_domain = [('product_id', '=', rec.product_id.id), ('state', 'not in', (['draft', 'waiting',
                                                                                                   'sent', 'expired']))]
                sale_order_line_ids = self.env['sale.order.line'].sudo().search(sale_order_domain).filtered(
                    lambda x: x.order_id.sale_order_template_id.id == rec.sale_order_template_id.id)
                rec.stock = sum(sale_order_line_ids.mapped('product_uom_qty'))

    @api.one
    @api.depends('stock', 'inventory')
    def _compute_available(self):
        for rec in self:
            # rec.available = rec.inventory - rec.stock
            if not rec.product_category == 'room':
                rec.available = rec.inventory - rec.stock
            else:
                rec.available = self.sale_order_template_id.available_rooms
