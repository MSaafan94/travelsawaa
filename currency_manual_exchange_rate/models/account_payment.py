# -*- coding: utf-8 -*-
from odoo import fields, models,api, _
import logging
_logger = logging.getLogger(__name__)

class AccountAbstractPayment(models.AbstractModel):
    _inherit = "account.abstract.payment"

    def _compute_total_invoices_amount(self):
        """ Compute the sum of the residual of invoices, expressed in the payment currency """
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate) 
        return super(AccountAbstractPayment, self)._compute_total_invoices_amount()


class AccountPayment(models.Model):
    _inherit ='account.payment'

    manual_currency_rate_active = fields.Boolean('Apply Manual Exchange')
    manual_currency_rate = fields.Float('Rate', digits=(12, 4))

    def _create_transfer_entry(self, amount):
        """ Create the journal entry corresponding to the 'incoming money' part of an internal transfer, return the reconciliable move line
        """
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate)
        return super(AccountPayment, self)._create_transfer_entry(amount=amount)

    @api.one
    @api.depends('invoice_ids', 'amount', 'payment_date', 'currency_id','manual_currency_rate')
    def _compute_payment_difference(self):
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate)
        return super(AccountPayment, self)._compute_payment_difference()


    def _create_payment_entry(self, amount):
        """ Create a journal entry corresponding to a payment, if the payment references invoice(s) they are reconciled.
            Return the journal entry.
        """
        if self.manual_currency_rate_active:
            self = self.with_context(override_currency_rate=self.manual_currency_rate)
        return super(AccountPayment, self)._create_payment_entry(amount=amount)

        
        