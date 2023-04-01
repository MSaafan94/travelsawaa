# -*- coding: utf-8 -*-
from odoo import http

# class CustomAccounts(http.Controller):
#     @http.route('/custom_accounts/custom_accounts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_accounts/custom_accounts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_accounts.listing', {
#             'root': '/custom_accounts/custom_accounts',
#             'objects': http.request.env['custom_accounts.custom_accounts'].search([]),
#         })

#     @http.route('/custom_accounts/custom_accounts/objects/<model("custom_accounts.custom_accounts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_accounts.object', {
#             'object': obj
#         })