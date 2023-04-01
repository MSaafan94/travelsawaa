# -*- coding: utf-8 -*-
from odoo import fields, models,api, _
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger('ManualCurrencySaleInherit')

class SaleOrder(models.Model):
    _inherit ='sale.order'
    manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
    manual_currency_rate = fields.Float('Rate', digits=(12, 4))

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        invoice_ids = super(SaleOrder, self).action_invoice_create(grouped=grouped, final=final)
        for order in self:
            if order.manual_currency_rate_active:
                order.invoice_ids.write({'manual_currency_rate_active':order.manual_currency_rate_active,'manual_currency_rate':order.manual_currency_rate})
        return invoice_ids
    
    @api.multi
    def action_confirm(self):
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate)
        result = super(SaleOrder, self).action_confirm()
        
    @api.depends('pricelist_id', 'date_order', 'company_id')
    def _compute_currency_rate(self):
        for order in self:
            if order.manual_currency_rate_active:
                order.currency_rate = self.env['res.currency'].with_context(override_currency_rate=self.manual_currency_rate)._get_conversion_rate(order.company_id.currency_id, order.currency_id, order.company_id, order.date_order)
            else:
                order.currency_rate = self.env['res.currency']._get_conversion_rate(order.company_id.currency_id, order.currency_id, order.company_id, order.date_order)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if self.order_id.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.order_id.manual_currency_rate)
        return super(SaleOrderLine, self).product_id_change()


    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.order_id.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.order_id.manual_currency_rate)
        return super(SaleOrderLine, self).product_uom_change()

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        if order.manual_currency_rate_active:
            res.write({'manual_currency_rate_active':order.manual_currency_rate_active,'manual_currency_rate':order.manual_currency_rate})
        return res
