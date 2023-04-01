# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PurchaseOrder(models.Model):
    _inherit ='purchase.order'
    
    manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
    manual_currency_rate = fields.Float('Rate', digits=(12, 4))

    @api.multi
    def button_confirm(self):
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate)
        result = super(PurchaseOrder, self).button_confirm()
        return result
        
    @api.multi
    def button_approve(self, force=False):
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate)
        result = super(PurchaseOrder, self).button_approve(force=force)
        return result

class PurchaseOrderLine(models.Model):
    _inherit ='purchase.order.line'
    
    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if self.order_id.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.order_id.manual_currency_rate)
        result = super(PurchaseOrderLine, self)._onchange_quantity()
        return result
    
class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if self.purchase_id:
            self.manual_currency_rate_active = self.purchase_id.manual_currency_rate_active
            self.manual_currency_rate = self.purchase_id.manual_currency_rate
        result = super(AccountInvoice, self).purchase_order_change()
        return result