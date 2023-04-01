# -*- coding: utf-8 -*-
from odoo import http

# class TravelDashboard(http.Controller):
#     @http.route('/travel_dashboard/travel_dashboard/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travel_dashboard/travel_dashboard/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('travel_dashboard.listing', {
#             'root': '/travel_dashboard/travel_dashboard',
#             'objects': http.request.env['travel_dashboard.travel_dashboard'].search([]),
#         })

#     @http.route('/travel_dashboard/travel_dashboard/objects/<model("travel_dashboard.travel_dashboard"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travel_dashboard.object', {
#             'object': obj
#         })