# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger('Invoice-Manual-Currency-Inherit')

class AccountInvoiceLine(models.Model):
    _inherit ='account.invoice.line'
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.invoice_id.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.invoice_id.manual_currency_rate)
        return super(AccountInvoiceLine, self)._onchange_product_id()
    
class AccountInvoice(models.Model):
    _inherit ='account.invoice'
    
    manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
    manual_currency_rate = fields.Float('Rate', digits=(12, 4))

    @api.multi
    def action_move_create(self):
        """ Creates invoice related analytics and financial move lines """
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate)
        return super(AccountInvoice, self).action_move_create()
            
