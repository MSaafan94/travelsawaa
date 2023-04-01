# -*- coding: utf-8 -*-
from odoo import http

# class PolarisAccount(http.Controller):
#     @http.route('/polaris_account/polaris_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/polaris_account/polaris_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('polaris_account.listing', {
#             'root': '/polaris_account/polaris_account',
#             'objects': http.request.env['polaris_account.polaris_account'].search([]),
#         })

#     @http.route('/polaris_account/polaris_account/objects/<model("polaris_account.polaris_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('polaris_account.object', {
#             'object': obj
#         })