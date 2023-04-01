# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import time
import logging
from odoo import api, models, _
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)


class ReportGeneralLedger(models.AbstractModel):
    _inherit = 'report.accounting_pdf_reports.report_generalledger'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        init_balance = data['form'].get('initial_balance', True)
        sortby = data['form'].get('sortby', 'sort_date')
        display_account = data['form']['display_account']
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in
                     self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]
        # Filter by selected accounts
        if data['form']['account_ids'] and data['form']['analytic_account']:
            raise ValidationError("Please choose only one type analytic account or account ")
        elif data['form']['account_ids']:
            accounts = self.env['account.account'].search([('id', 'in', data['form']['account_ids'])])
        elif data['form']['analytic_account']:
            print(data['form']['analytic_account'])
            accounts = self.env['account.analytic.account'].search([('id', 'in', data['form']['analytic_account'])])
            print(list(accounts))
        else:
            raise ValidationError("Sorry you need to choose Account or Analytic Account")
            accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
        accounts_res = self.with_context(data['form'].get('used_context', {}))._get_account_move_entry(accounts,
                                                                                                       init_balance,
                                                                                                       sortby,
                                                                                                       display_account)

        print(accounts_res)
        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
            'print_journal': codes,
        }
