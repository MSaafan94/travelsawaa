from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'operation.operation'
    _description = 'Description'
    _inherits = {'sale.order.template': 'trip_reference'}

    trip_reference = fields.Many2one('sale.order.template',string="trip reference")
    # sale_orders=fields.One2many('sale.order','',string="trip reference")


    @api.multi
    @api.onchange('trip_reference')
    def get_traps(self):
        print(self)
        if self.trip_reference:
            print(self.env['sale.order'].search([('sale_order_template_id','=',self.trip_reference.id)]))

