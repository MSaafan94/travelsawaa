# -*- coding: utf-8 -*-
import logging

from num2words import num2words

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError
from datetime import timedelta, datetime


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    active = fields.Boolean("Active", default=True, track_visibility='always')
    user = fields.Many2one('res.users', string="Payment Created User", readonly=True, track_visibility='always')
    sale_id = fields.Many2one("sale.order", track_visibility='always')
    analytic_account = fields.Many2one('account.analytic.account', track_visibility='always')
    with_cheque = fields.Boolean("Payment With Cheque", track_visibility='always')
    cheque_number = fields.Char("Cheque Number", track_visibility='always')
    cheque_date = fields.Date("Cheque Date", track_visibility='always')
    bank_name = fields.Char("Bank Name", track_visibility='always')
    approved_user = fields.Char("Approved user", readonly=True, track_visibility='always')
    created_user = fields.Char("Approved user", track_visibility='always')
    payment_method_id = fields.Many2one('account.payment.method', required=False, track_visibility='always')
    journal_id = fields.Many2one('account.journal', required=False, track_visibility='always')
    trip_reference = fields.Char("Trip Reference", track_visibility='always')

    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
        self.approved_user = self.env.user.name
        return res

    @api.model
    def create(self, vals):
        rslt = super(AccountPayment, self).create(vals)
        # When a payment is created by the multi payments wizard in 'multi' mode,
        # its partner_bank_account_id will never be displayed, and hence stay empty,
        # even if the payment method requires it. This condition ensures we set
        # the first (and thus most prioritary) account of the partner in this field
        # in that situation.
        rslt.created_user = rslt.env.user.name
        return rslt


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_count = fields.Integer(compute='_compute_payment_count', copy=False)
    total_payments = fields.Monetary(compute='_compute_total_paid_amounts', string="Total Paid", store=True)
    total_due = fields.Monetary(compute='_compute_total_paid_amounts', string="Total Due", store=True)
    payment_quotation = fields.One2many('payments.payments', 'payment_quotation_id', )
    extra_money = fields.Float()
    year = fields.Selection([('2022', '2022'), ('2023', '2023'), ('2024','2024')], related='sale_order_template_id.year', store=True)


    @api.multi
    def action_confirm(self):
        for line in self.order_line:
            if self.state == 'draft' and line.product_uom_qty > line.available:
                raise UserError("Ordered Quantity of [{}] is greater than available quantity !".format(line.name))
            elif self.state == 'update' and line.available < 0:
                raise UserError("Ordered Quantity of [{}] is greater than available quantity !".format(line.name))
        res = super(SaleOrder, self).action_confirm()
        return res

    @api.depends('payment_count')
    def get_payments(self):
        account_payment = [(5, 0, 0,)]
        payments = self.env['account.payment'].search([('state', 'in', ['posted', 'locked']), ('sale_id', '=', self.id),
                                                       ('partner_id', '=', self.partner_id.id)])
        if payments:
            for line in payments:
                account_payment.append((0, 0, {
                    'payment_amount': line.amount,
                    'customer': line.partner_id.name,
                    'paid_on': line.payment_date,
                    'payment_date': line.payment_date,
                    'payment_type': line.payment_type,
                    'journal_id': line.journal_id,
                    'name': line.name,
                    'state': line.state,
                }))
            self.payment_quotation = account_payment
        # self.total_payments += self.extra_money
        return self.payment_quotation

    def auto_cancel_sale_order(self):
        try:
            sale_order = self.env['sale.order']
            sale_order_ids = sale_order.search([('state', '=', 'draft'), ('validity_date', '<', str(datetime.now()))])
            for sale_order in sale_order_ids:
                sale_order.write({'state': 'expired'})

        except:
            return "internal error"

    @api.one
    @api.depends('payment_quotation')
    def _compute_total_paid_amounts(self):
        for line in self.payment_quotation:
            if line.is_added:
                if line.payment_type == 'outbound':
                    self.total_payments -= line.payment_amount
                    # self.total_payments -= line.payment_amount
                    self.total_due = self.amount_total - self.total_payments
                else:
                    self.total_payments += line.payment_amount
                    self.total_due = self.amount_total - self.total_payments

    def _compute_payment_count(self):
        for payment in self:
            payment.payment_count = self.env['account.payment'].search_count(
                ['|', ('sale_id', '=', self.id), ('partner_id', '=', self.partner_id.id)])

    def transfer_optional_products(self):
        transfers_products = []
        if self.state not in ['draft', 'sent', 'update']:
            raise UserError(_('You cannot add options to a confirmed order.'))
        for line in self.sale_order_option_ids:
            if line.transfer == True and line.quantity <= line.available:
                sale_order_line = {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price_unit,
                    'product_uom': line.uom_id.id,
                    'discount': line.discount,
                    'company_id': line.order_id.company_id.id
                }
                if line.analytic_tag_id:
                    sale_order_line['analytic_tag_ids'] = [(4, line.analytic_tag_id.id)]
                transfers_products.append((0, 0, sale_order_line))
            elif line.transfer == True and line.quantity > line.available:
                raise UserError(_('You cannot add {} as it is unavailable quantity.'.format(line.name)))

        self.order_line = transfers_products
        for line in self.sale_order_option_ids:
            line.transfer = False

    @api.multi
    def action_set_draft(self):
        for line in self.order_line:
            line.reserved = line.product_uom_qty

        return self.write({
            'state': 'update',
            'signature': False,
            'signed_by': False,
        })

    def get_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warning : you must select Journal',
            'res_model': 'payment.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('travel_sales.payment_wizard_view_form', False).id,
            'target': 'new',
        }

    def create_payment(self, journal_id, amount, date, ):
        for rec in self:
            values = {
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': rec.partner_id.id,
                'amount': amount,
                'sale_id': rec.id,
                'journal_id': journal_id,
                'state': 'draft',
                'trip_reference': rec.sale_order_template_id.name,
                'user': self.env.user.id,
                'payment_date': date,
            }
            self.env['account.payment'].sudo().create(values)

    def get_refund(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warning : you must select Journal',
            'res_model': 'payment.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('travel_sales.payment_wizard_view_form_refund', False).id,
            'target': 'new',
        }

    def create_refund(self, journal_id, amount, date, ):
        for rec in self:
            values = {
                'payment_type': 'outbound',
                'partner_type': 'customer',
                'partner_id': rec.partner_id.id,
                'amount': amount,
                'sale_id': rec.id,
                'journal_id': journal_id,
                'state': 'draft',
                'trip_reference': rec.sale_order_template_id.name,
                'user': self.env.user.id,
                'payment_date': date,
            }
            self.env['account.payment'].sudo().create(values)

    def payment_action(self):
        action = self.env['ir.actions.act_window'].for_xml_id('account', 'action_account_payments')
        action['domain'] = ['|', ('sale_id', '=', self.id), ('partner_id', '=', self.partner_id.id)]
        return action


class Payments(models.Model):
    _name = "payments.payments"

    currency_id = fields.Many2one('res.currency', string='Currency')
    customer = fields.Char()
    payment_date = fields.Date()
    name = fields.Char()
    journal_id = fields.Many2one('account.journal')
    payment_amount = fields.Monetary()
    payment_quotation_id = fields.Many2one('sale.order')
    state = fields.Selection(
        [('draft', 'draft'), ("posted", 'posted'), ("canceled", 'canceled'), ('locked', 'Locked'),
         ("reconciled", 'reconciled'),
         ('sent', 'sent')])
    is_added = fields.Boolean(string='Add', track_visibility='always', default=True)
    payment_type = fields.Selection([('inbound', 'Inbound'), ("outbound", 'Outbound')])