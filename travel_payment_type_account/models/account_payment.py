
# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date


class account_move_line(models.Model):
    _inherit = 'account.move.line'

    partner_id_account = fields.Many2one('account.account', string='Partner' , )
    is_account = fields.Boolean(string='Account' , default=False)


class account_payment(models.Model):
    _inherit = 'account.payment'

    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Vendor') ,  ('accuont', 'Accounts')]) # , for fds , aps
    is_account = fields.Boolean(string='Account' , compute='onchange_partner_id' , default=False)
    partner_id_account = fields.Many2one('account.account', string='Account' , )
    temp = fields.Boolean(string='emp' , compute='get_account' , default=False)
    internal_cons = fields.Boolean(compute='comp_internal' , default=False)
    analytic_account = fields.Many2one(comodel_name="account.analytic.account", string="Cost Center", required=False, )
    property_account_receivable_id  = fields.Many2one('account.account',related='partner_id.property_account_receivable_id',
                                                      readonly=False,store=True)
    property_account_payable_id  = fields.Many2one('account.account',related='partner_id.property_account_payable_id',readonly=False, store=True)
    payment_amount_change = fields.Monetary(compute='negative_payment', string='Payment amount')
    # payment_amount_change = fields.Monetary()

    @api.one
    @api.depends('amount')
    def negative_payment(self):
        if self.amount and self.payment_type == 'outbound':
            self.payment_amount_change = -abs(self.amount)
        else:
            self.payment_amount_change = self.amount

    def _create_payment_entry(self, amount):
        """ Create a journal entry corresponding to a payment, if the payment references invoice(s) they are reconciled.
            Return the journal entry.
        """

        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        invoice_currency = False
        if self.invoice_ids and all([x.currency_id == self.invoice_ids[0].currency_id for x in self.invoice_ids]):
            # if all the invoices selected share the same currency, record the paiement in that currency too
            invoice_currency = self.invoice_ids[0].currency_id
        debit, credit, amount_currency, currency_id = aml_obj.with_context(
            date=self.payment_date)._compute_amount_fields(amount, self.currency_id, self.company_id.currency_id)

        move = self.env['account.move'].create(self._get_move_vals())

        # Write line corresponding to invoice payment
        counterpart_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, move.id, False)
        counterpart_aml_dict.update(self._get_counterpart_move_line_vals(self.invoice_ids))
        # counterpart_aml_dict.update({'currency_id': currency_id, 'analytic_account_id': self.analytic_account.id if (self.payment_type == 'inbound'
        #                                                                                                             and counterpart_aml_dict.get('credit') != 0)
        counterpart_aml_dict.update({'currency_id': currency_id, 'analytic_account_id': self.analytic_account.id or None})
        counterpart_aml = aml_obj.create(counterpart_aml_dict)

        # Reconcile with the invoices
        if self.payment_difference_handling == 'reconcile' and self.payment_difference:
            writeoff_line = self._get_shared_move_line_vals(0, 0, 0, move.id, False)
            amount_currency_wo, currency_id = aml_obj.with_context(date=self.payment_date)._compute_amount_fields(
                self.payment_difference, self.currency_id, self.company_id.currency_id)[2:]
            # the writeoff debit and credit must be computed from the invoice residual in company currency
            # minus the payment amount in company currency, and not from the payment difference in the payment currency
            # to avoid loss of precision during the currency rate computations. See revision 20935462a0cabeb45480ce70114ff2f4e91eaf79 for a detailed example.
            total_residual_company_signed = sum(invoice.residual_company_signed for invoice in self.invoice_ids)
            total_payment_company_signed = self.currency_id.with_context(date=self.payment_date).compute(self.amount,
                                                                                                         self.company_id.currency_id)
            amount_wo = total_residual_company_signed - total_payment_company_signed
            debit_wo = amount_wo > 0 and amount_wo or 0.0
            credit_wo = amount_wo < 0 and -amount_wo or 0.0
            writeoff_line['name'] = _('Counterpart')
            writeoff_line['account_id'] = self.writeoff_account_id.id
            writeoff_line['debit'] = debit_wo
            writeoff_line['credit'] = credit_wo
            writeoff_line['amount_currency'] = amount_currency_wo
            writeoff_line['currency_id'] = currency_id
            writeoff_line = aml_obj.create(writeoff_line)
            if counterpart_aml['debit']:
                counterpart_aml['debit'] += credit_wo - debit_wo
            if counterpart_aml['credit']:
                counterpart_aml['credit'] += debit_wo - credit_wo
            counterpart_aml['amount_currency'] -= amount_currency_wo
        self.invoice_ids.register_payment(counterpart_aml)

        # Write counterpart lines
        if not self.currency_id != self.company_id.currency_id:
            amount_currency = 0
        liquidity_aml_dict = self._get_shared_move_line_vals(credit, debit, -amount_currency, move.id, False)
        liquidity_aml_dict.update(self._get_liquidity_move_line_vals(-amount))
        liquidity_aml_dict.update(self._get_liquidity_move_line_vals(-amount))
        liquidity_aml_dict.update({'analytic_account_id': self.analytic_account.id if (self.payment_type == 'outbound' and liquidity_aml_dict.get('debit') != 0) else None})
        aml_obj.create(liquidity_aml_dict)

        move.post()
        return move

    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # Use the right sequence to set the name
            if rec.payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if rec.partner_type == 'customer':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if rec.partner_type == 'supplier':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'
                if rec.partner_type == 'accuont':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.account.refund'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.account.invoice'
            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(
                sequence_code)
            if not rec.name and rec.payment_type != 'transfer':
                raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(
                    lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()

            rec.write({'state': 'posted', 'move_name': move.name})
        return True



    @api.depends('is_account' , 'payment_type')
    def comp_internal(self):
        if self.payment_type == 'transfer' or self.is_account : #or self.is_emp
            self.internal_cons = True


    @api.depends( 'partner_type') #'employee_id' ,
    def get_account(self):
        pass




    @api.model
    def _get_shared_move_line_vals(self, debit, credit, amount_currency, move_id, invoice_id=False):
        """ Returns values common to both move lines (except for debit, credit and amount_currency which are reversed)
        """
        return {
            'partner_id': self.partner_id.id or False,
            # 'partner_id_account' : self.partner_id_account.id  or False,
            'is_account' : self.is_account ,
            'invoice_id': invoice_id and invoice_id.id or False,
            'move_id': move_id,
            'debit': debit,
            'credit': credit,
            'amount_currency': amount_currency or False,
            # 'account_id' : self.partner_id_account.id,
        }


    @api.one
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id' , 'partner_id_account')
    def _compute_destination_account_id(self):
        if self.invoice_ids:
            self.destination_account_id = self.invoice_ids[0].account_id.id
        elif self.payment_type == 'transfer':
            if not self.company_id.transfer_account_id.id:
                raise UserError(_('Transfer account not defined on the company.'))
            if self.partner_type == 'accuont': # or self.partner_type == 'employee'
                self.destination_account_id = self.partner_id_account.id
                self.writeoff_account_id = self.partner_id_account.id
            else:
                self.destination_account_id = self.company_id.transfer_account_id.id
        elif self.partner_type == 'accuont':  #or self.partner_type == 'employee'
            self.destination_account_id = self.partner_id_account.id
            self.writeoff_account_id = self.partner_id_account.id


        elif self.partner_id:
            if self.partner_type == 'customer':
                self.destination_account_id = self.partner_id.property_account_receivable_id.id
            else:
                self.destination_account_id = self.partner_id.property_account_payable_id.id



    @api.one
    @api.depends('partner_type')
    def onchange_partner_id (self):

        if self.partner_type == 'accuont':
            self.is_account = True
        else :
            self.is_account = False



    def _get_liquidity_move_line_vals(self, amount):
        name = self.name
        if self.payment_type == 'transfer':
            name = _('Transfer to %s') % self.destination_journal_id.name
        if self.partner_type == 'accuont': # or self.partner_type == 'employee'
            vals = {
                'name': name,
                'account_id': self.partner_id_account.id,
                # 'account_id': self.payment_type in ('outbound',
                #                                     'transfer') and self.journal_id.default_debit_account_id.id or self.journal_id.default_credit_account_id.id,
                'payment_id': self.id,
                'journal_id': self.journal_id.id,
                'currency_id': self.currency_id != self.company_id.currency_id and self.currency_id.id or False,
                # 'analytic_account_id': self.analytic_account.id if self.payment_type == 'inbound' else None,
            }
        else:
            vals = {
                'name': name,
                'account_id': self.payment_type in ('outbound','transfer') and self.journal_id.default_debit_account_id.id or self.journal_id.default_credit_account_id.id,
                'payment_id': self.id,
                'journal_id': self.journal_id.id,
                'currency_id': self.currency_id != self.company_id.currency_id and self.currency_id.id or False,
                # 'analytic_account_id': self.analytic_account.id if self.payment_type == 'inbound' else None,
            }

        vals = {
            'name': name,
            'account_id': self.payment_type in ('outbound', 'transfer') and self.journal_id.default_debit_account_id.id or self.journal_id.default_credit_account_id.id,
            'payment_id': self.id,
            'journal_id': self.journal_id.id,
            # 'analytic_account_tag': [(6, 0, self.analytic_account_tag.ids)],
            'analytic_account_id': self.analytic_account.id if self.payment_type == 'inbound' else None,
            'currency_id': self.currency_id != self.company_id.currency_id and self.currency_id.id or False,
        }


        # If the journal has a currency specified, the journal item need to be expressed in this currency
        if self.journal_id.currency_id and self.currency_id != self.journal_id.currency_id:
            amount = self.currency_id.with_context(date=self.payment_date).compute(amount, self.journal_id.currency_id)
            debit, credit, amount_currency, dummy = self.env['account.move.line'].with_context(date=self.payment_date)._compute_amount_fields(amount, self.journal_id.currency_id, self.company_id.currency_id)
            vals.update({
                'amount_currency': amount_currency,
                'currency_id': self.journal_id.currency_id.id,
            })

        return vals

    def _get_counterpart_move_line_vals(self, invoice=False):
        if self.payment_type == 'transfer':
            name = self.name
        else:
            name = ''
            if self.partner_type == 'customer':
                if self.payment_type == 'inbound':
                    name += _("Customer Payment")
                elif self.payment_type == 'outbound':
                    name += _("Customer Refund")
            elif self.partner_type == 'supplier':
                if self.payment_type == 'inbound':
                    name += _("Vendor Refund")
                elif self.payment_type == 'outbound':
                    name += _("Vendor Payment")
            if invoice:
                name += ': '
                for inv in invoice:
                    if inv.move_id:
                        name += inv.number + ', '
                name = name[:len(name) - 2]

        data ={
            'name': name,
            'account_id': self.destination_account_id.id,
            'journal_id': self.journal_id.id,
            # 'analytic_account_tag': [(6, 0, self.analytic_account_tag.ids)],
            # 'analytic_account_id': self.analytic_account.id if self.payment_type in ['outbound'] else None,
            'currency_id': self.currency_id != self.company_id.currency_id and self.currency_id.id or False,
            'payment_id': self.id,
        }
        return data


