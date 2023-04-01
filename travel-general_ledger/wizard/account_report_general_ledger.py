# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

from odoo import fields, models


class AccountReportGeneralLedger(models.TransientModel):
    _inherit = "account.report.general.ledger"

    account_ids = fields.Many2many('account.account', string='Accounts')
    analytic_account = fields.Many2many('account.analytic.account', string="Analytic Account")
    currency_id = fields.Many2one('res.currency', string='Currency')
    initial_balance = fields.Boolean(string='Include Initial Balances', default=True,
                                     help='If you selected date, this field allow you to add a row to display the amount of debit/credit/balance that precedes the filter you\'ve set.')

    def _print_report(self, data):
        res = super(AccountReportGeneralLedger, self)._print_report(data)
        data['form'].update(self.read(['account_ids', 'analytic_account', 'currency_id'])[0],)
        return res
