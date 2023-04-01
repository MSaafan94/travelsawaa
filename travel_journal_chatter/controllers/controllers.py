# -*- coding: utf-8 -*-
from odoo import http

# class TravelJournalChatter(http.Controller):
#     @http.route('/travel_journal_chatter/travel_journal_chatter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travel_journal_chatter/travel_journal_chatter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('travel_journal_chatter.listing', {
#             'root': '/travel_journal_chatter/travel_journal_chatter',
#             'objects': http.request.env['travel_journal_chatter.travel_journal_chatter'].search([]),
#         })

#     @http.route('/travel_journal_chatter/travel_journal_chatter/objects/<model("travel_journal_chatter.travel_journal_chatter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travel_journal_chatter.object', {
#             'object': obj
#         })