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

class AddQuotationCancelReason(models.TransientModel):
    _name = "add.quotation.reason"
 
    quota_cancel_reason_id = fields.Many2one("quotation.cancel.reason",string= "Quotation Cancellation Reason", required =True, help="This field display reason of quotation cancellation")
    status_paid_cancel_id = fields.Many2one("status.paid.cancel", string= "Status Paid", required= False)
    # status_paid_cancel_id = fields.Selection([('yes', 'Yes'), ('no', 'No')])


    # def inbox_message(self):
    #     """
    #     Send user chat notification on picking validation.
    #     """
    #
    #     # construct the message that is to be sent to the user
    #     message_text = f'<strong>Title</strong> ' \
    #                    f'<p>This picking has been validated!</p>'
    #
    #     # odoo runbot
    #     odoobot_id = self.env['ir.model.data'].sudo().xmlid_to_res_id("base.partner_root")
    #
    #     # find if a channel was opened for this user before
    #     channel = self.env['mail.channel'].sudo().search([
    #         ('name', '=', 'Picking Validated'),
    #         ('channel_partner_ids', 'in', [self.env.user.partner_id.id])
    #     ],
    #         limit=1,
    #     )
    #
    #     if not channel:
    #         # create a new channel
    #         channel = self.env['mail.channel'].with_context(mail_create_nosubscribe=True).sudo().create({
    #             'channel_partner_ids': [(4, self.env.user.partner_id.id), (4, odoobot_id)],
    #             'public': 'private',
    #             'channel_type': 'chat',
    #             'email_send': False,
    #             'name': f'Picking Validated',
    #             'display_name': f'Picking Validated',
    #         })
    #
    #     # send a message to the related user
    #     channel.sudo().message_post(
    #         body=message_text,
    #         author_id=odoobot_id,
    #         message_type="comment",
    #         subtype="mail.mt_comment",
    #     )
    #                 # create a new one
    # chanel_object = self.env['mail.channel']
    # channel_exist = chanel_object.search([('channel_partner_ids', 'in', [40])])
    # channel = chanel_object.create({
    #     'channel_partner_ids': [(4, partner_id) for partner_id in [40]],
    #     'public': 'private',
    #     'channel_type': 'chat',
    #     'email_send': False,
    #     # 'name': ', '.join(self.env['res.partner'].sudo().browse(partners_to).mapped('name')),
    #     'name': "tyesss",
    # })
    #           })
    #
    #         # send a message to the related user
    #         channel.sudo().message_post(
    #             body=message_text,
    #             author_id=odoobot_id,
    #             message_type="comment",
    #             subtype="mail.mt_comment",
    #         )
    # chanel_object.browse(118).message_post(body='tetetet', message_type="notification", subtype="mail.mt_comment")
    # new_channel.message_post(body=notification, message_type="notification", subtype="mail.mt_comment")
    #         # send a message to the related user
    #         channel.sudo().message_post(
    #             body=message_text,
    #             author_id=odoobot_id,
    #             message_type="comment",
    #             subtype="mail.mt_comment",
    #         )

    # For adding the reason of cancel quotation on sales quotation
    @api.multi
    def cancel_quotation(self):
        if self.env.context.get('active_model') == 'sale.order':
            active_model_id = self.env.context.get('active_id')
            sale_obj = self.env['sale.order'].search([('id', '=', active_model_id)])
            sale_order_data = {'quota_cancel_reason_id': self.quota_cancel_reason_id.id, 'state': 'cancel'}
            if self.status_paid_cancel_id:
                sale_order_data['status_paid_cancel_id'] = self.status_paid_cancel_id.id
            sale_obj.write(sale_order_data)

	
