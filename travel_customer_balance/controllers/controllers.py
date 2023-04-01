# -*- coding: utf-8 -*-
# from odoo import http


# class HakCustomerBalance(http.Controller):
#     @http.route('/hak_customer_balance/hak_customer_balance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hak_customer_balance/hak_customer_balance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hak_customer_balance.listing', {
#             'root': '/hak_customer_balance/hak_customer_balance',
#             'objects': http.request.env['hak_customer_balance.hak_customer_balance'].search([]),
#         })

#     @http.route('/hak_customer_balance/hak_customer_balance/objects/<model("hak_customer_balance.hak_customer_balance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hak_customer_balance.object', {
#             'object': obj
#         })
