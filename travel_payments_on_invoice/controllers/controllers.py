# -*- coding: utf-8 -*-
from odoo import http

# class PaymentsOnInvoice(http.Controller):
#     @http.route('/payments_on_invoice/payments_on_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payments_on_invoice/payments_on_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payments_on_invoice.listing', {
#             'root': '/payments_on_invoice/payments_on_invoice',
#             'objects': http.request.env['payments_on_invoice.payments_on_invoice'].search([]),
#         })

#     @http.route('/payments_on_invoice/payments_on_invoice/objects/<model("payments_on_invoice.payments_on_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payments_on_invoice.object', {
#             'object': obj
#         })