# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PaymentsOnInvoice(models.Model):
    _inherit = 'account.invoice'
    payment_counts = fields.Integer(compute='_compute_payment_count', copy=False)
    payment_counts_on_bill = fields.Integer(compute='_compute_payment_count_on_bill', copy=False)

    def _compute_payment_count(self):
        self.payment_counts = self.env['account.payment'].search_count(
            ['|', ('communication', '=', self.reference), ('partner_id', '=', self.partner_id.id)])

    def payment_actions(self):
        action = self.env['ir.actions.act_window'].for_xml_id('account', 'action_account_payments')
        action['domain'] = ['|', ('communication', '=', self.reference), ('partner_id', '=', self.partner_id.id)]
        return action

    def _compute_payment_count_on_bill(self):
        if self.reference:
            self.payment_counts_on_bill = self.env['account.payment'].search_count(
                ['|', ('communication', '=', str(self.move_id.name)), ('communication', '=', self.reference)])
        else:
            self.payment_counts_on_bill = self.env['account.payment'].search_count(
                [('communication', '=', str(self.move_id.name))])

    def payment_actions_on_bill(self):
        action = self.env['ir.actions.act_window'].for_xml_id('account', 'action_account_payments')
        if self.reference:
            action['domain'] = ['|', ('communication', '=', str(self.move_id.name)),
                                ('communication', '=', self.reference)]
        else:
            action['domain'] = [('communication', '=', str(self.move_id.name))]
        return action
