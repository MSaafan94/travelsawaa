# -*- coding: utf-8 -*-
from odoo import http

# class Detailes(http.Controller):
#     @http.route('/detailes/detailes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/detailes/detailes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('detailes.listing', {
#             'root': '/detailes/detailes',
#             'objects': http.request.env['detailes.detailes'].search([]),
#         })

#     @http.route('/detailes/detailes/objects/<model("detailes.detailes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('detailes.object', {
#             'object': obj
#         })