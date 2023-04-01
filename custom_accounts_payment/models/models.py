# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class ResPartners(models.Model):
    _inherit = 'res.partner'

    custom_receivable_id = fields.Many2one('account.account')


class AccountPayment(models.Model):
    _inherit = "account.payment"
    destination_account_id = fields.Many2one('account.account', compute='_compute_destination_account_id', readonly=True)
    state = fields.Selection(selection_add=[('locked', 'Locked')])
    locked_move_id = fields.Many2one('account.move', readonly=True)
    # locked_move_line_id = fields.Many2one('account.move.line', string='Locked Move Lines', states="locked")

    @api.one
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id')
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
            partner = self.partner_id.with_context(force_company=self.company_id.id)
            if self.partner_type == 'customer':
                if partner.custom_receivable_id:
                    print('account', partner.custom_receivable_id)
                    self.destination_account_id = partner.custom_receivable_id.id
                else:
                    self.destination_account_id = partner.property_account_receivable_id.id
            else:
                self.destination_account_id = partner.property_account_payable_id.id

    @api.one
    def action_lock(self):
        if self.payment_type == 'inbound' and self.state == 'posted':
            aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
            debit, credit, amount_currency, currency_id = aml_obj.with_context(
                date=self.payment_date)._compute_amount_fields(self.amount, self.currency_id, self.company_id.currency_id)

            move = self.env['account.move'].create(self._get_move_vals())
            partner = self.partner_id.with_context(force_company=self.company_id.id)
            debit_account = None
            credit_account = None
            if self.partner_id:
                partner = self.partner_id.with_context(force_company=self.company_id.id)
                if self.partner_type == 'customer':
                    if partner.custom_receivable_id:
                        debit_account = partner.custom_receivable_id.id
                        credit_account = partner.property_account_receivable_id.id
                    else:
                        raise UserError(_("You must first define a custom receivable account for that customer."))
            line_vals = {
                'account_id': debit_account,
                'name': self.name,
                'debit': round(self.amount, 2),
                'credit': 0.00,
                'partner_id': partner.id,
                'move_id': move.id,

            }
            aml_obj.create(line_vals)
            line_vals = {
                'account_id': credit_account,
                'name': "Customer Payment",
                'debit': 0.00,
                'credit': round(self.amount, 2),
                'partner_id': partner.id,
                'move_id': move.id,
            }
            aml_obj.create(line_vals)

            # counterpart_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, move.id, False)
            # # self.locked_move_line_id = move.id
            move.action_post()
            self.locked_move_id = move.id
            self.state = 'locked'

        elif self.payment_type == 'outbound' and self.state == 'posted':
            aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
            debit, credit, amount_currency, currency_id = aml_obj.with_context(
                date=self.payment_date)._compute_amount_fields(self.amount, self.currency_id, self.company_id.currency_id)

            move = self.env['account.move'].create(self._get_move_vals())
            partner = self.partner_id.with_context(force_company=self.company_id.id)
            debit_account = None
            credit_account = None
            if self.partner_id:
                partner = self.partner_id.with_context(force_company=self.company_id.id)
                if self.partner_type == 'customer':
                    if partner.custom_receivable_id:
                        debit_account = partner.property_account_receivable_id.id
                        credit_account = partner.custom_receivable_id.id
                    else:
                        raise UserError(_("You must first define a custom receivable account for that customer."))
            line_vals = {
                'account_id': credit_account,
                'name': self.name,
                'credit': round(self.amount, 2),
                'debit': 0.00,
                'partner_id': partner.id,
                'move_id': move.id,

            }
            aml_obj.create(line_vals)
            line_vals = {
                'account_id': debit_account,
                'name': "Customer Refund",
                'credit': 0.00,
                'debit': round(self.amount, 2),
                'partner_id': partner.id,
                'move_id': move.id,
            }
            aml_obj.create(line_vals)

            # counterpart_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, move.id, False)
            # # self.locked_move_line_id = move.id
            move.action_post()
            self.locked_move_id = move.id
            self.state = 'locked'

