# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
# from datetime import datetime, date
from datetime import timedelta


class SaleOrdTemp(models.Model):
    _inherit = 'sale.order.template'

    dashboard = fields.One2many('custom.sales.dashboard', 'trip',)


class CustomSalesDashboard(models.Model):
    _name = "custom.sales.dashboard"

    _inherit = 'sale.order.template'
    color = fields.Integer(string='Color Index')
    # name = fields.Char(string="Name")
    trip = fields.Many2one('sale.order.template', string="trip name")
    destination = fields.Many2one('model.destination')
    total_rooms = fields.Float(related='trip.total_rooms')
    available_rooms = fields.Float(related='trip.available_rooms')
    stock_rooms = fields.Float(related='trip.stock_rooms')
    total_visa = fields.Float(related='trip.total_visa')
    available_visa = fields.Float(related='trip.available_visa')
    stock_visa = fields.Float(related='trip.stock_visa')
    available_program = fields.Float(related='trip.available_program')
    stock_program = fields.Float(related='trip.stock_program')
    available_domestic = fields.Float(related='trip.available_domestic')
    stock_domestic = fields.Float(related='trip.stock_domestic')
    available_international = fields.Float(related='trip.available_international')
    stock_international = fields.Float(related='trip.stock_international')
    cut_of_date = fields.Date(related='trip.cut_of_date')
    remaining_days = fields.Integer(compute='_remaining')

    total_amount = fields.Float(related='trip.total_amount')
    total_paid = fields.Float(related='trip.total_paid')
    # total_due = fields.Chart(related='trip.total_due')

    total_adults = fields.Integer(related='trip.total_adults')
    total_children = fields.Integer(related='trip.total_children')
    total_infants = fields.Integer(related='trip.total_infants')

    @api.depends('cut_of_date')
    def _remaining(self):
        if self.cut_of_date:
            today = fields.Date.today()
            self.remaining_days = (self.cut_of_date - today).days

    # @api.onchange('trip')
    # def change_computation(self):
    #     print(self.trip.name)
