# -*- coding: utf-8 -*-

# from odoo import models, fields, api, _
# from odoo.exceptions import UserError, ValidationError
from copy import deepcopy
import logging
import time
from datetime import date
from collections import OrderedDict, defaultdict
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools.misc import formatLang, format_date
from odoo.tools import float_is_zero, float_compare
from odoo.tools.safe_eval import safe_eval
from odoo.addons import decimal_precision as dp
from lxml import etree


class account_payment(models.Model):
    _inherit = "account.payment"

    payment_type = fields.Selection([('inbound', 'Inbound'), ('outbound', 'Outbound')], required=True, track_visibility='always')
    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Vendor')], track_visibility='always')
    partner_id = fields.Many2one('res.partner', string='Partner', track_visibility='always')

    amount = fields.Monetary(string='Payment Amount', required=True, track_visibility='always')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id, track_visibility='always')
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today, required=True, copy=False, track_visibility='always')
    communication = fields.Char(string='Memo', track_visibility='always')
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True,
                                 domain=[('type', 'in', ('bank', 'cash'))], track_visibility='always')


    def action_validate_invoice_payment(self):
        """ Posts a payment used to pay an invoice. This function only posts the
        payment by default but can be overridden to apply specific post or pre-processing.
        It is called by the "validate" button of the popup window
        triggered on invoice form by the "Register Payment" button.
        """
        if any(len(record.invoice_ids) != 1 for record in self):
            # For multiple invoices, there is account.register.payments wizard
            raise UserError(_("This method should only be called to process a single invoice's payment."))

    @api.multi
    def post(self, invoice=False):
        if not self.env.user.has_group('account.group_account_manager') and (self.payment_type == 'inbound' or self.partner_type == 'customer'):
            raise UserError(_('please head to the accounting team to confirm it for you'))
        super(account_payment, self).post()

