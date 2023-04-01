# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class ReportFloghtData(models.AbstractModel):
    _name = 'report.details.sale_flight'
    _description = 'Module Reference Report (base)'


    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('details.sale_flight')
        selected_modules = self.env['sale.order'].browse(docids)
        print('aaaaaaaaa')
        return {
            'doc_ids': docids,
            'doc_model': "sale.order",
            'docs': selected_modules,
            'aa':[{'a':'aaaaaaaaaaaaaaaa'}],
        }
