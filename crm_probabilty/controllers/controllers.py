# -*- coding: utf-8 -*-
from odoo import http

# class CrmProbabilty(http.Controller):
#     @http.route('/crm_probabilty/crm_probabilty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_probabilty/crm_probabilty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_probabilty.listing', {
#             'root': '/crm_probabilty/crm_probabilty',
#             'objects': http.request.env['crm_probabilty.crm_probabilty'].search([]),
#         })

#     @http.route('/crm_probabilty/crm_probabilty/objects/<model("crm_probabilty.crm_probabilty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_probabilty.object', {
#             'object': obj
#         })