# -*- coding: utf-8 -*-
from odoo import http

# class RemoveAddProduct(http.Controller):
#     @http.route('/remove_add_product/remove_add_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/remove_add_product/remove_add_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('remove_add_product.listing', {
#             'root': '/remove_add_product/remove_add_product',
#             'objects': http.request.env['remove_add_product.remove_add_product'].search([]),
#         })

#     @http.route('/remove_add_product/remove_add_product/objects/<model("remove_add_product.remove_add_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('remove_add_product.object', {
#             'object': obj
#         })