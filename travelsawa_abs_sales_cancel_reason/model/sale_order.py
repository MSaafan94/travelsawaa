# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api,fields,models,_

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    quota_cancel_reason_id = fields.Many2one("quotation.cancel.reason",string= "Quotation Cancellation Reason",help="This field display reason of quatation cancellation", track_visibility="onchange")
    status_paid_cancel_id = fields.Many2one("status.paid.cancel", string= "Status Paid", track_visibility="onchange")

    # action_cancel function return wizard
    @api.multi
    def action_cancel(self,context=None):
        return {
        'name': ('Add Reason'),
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'add.quotation.reason',
        'view_id': self.env.ref('travelsawa_abs_sales_cancel_reason.view_add_cancel_reason_form').id,
        'type': 'ir.actions.act_window',
        'target':'new'
    	}