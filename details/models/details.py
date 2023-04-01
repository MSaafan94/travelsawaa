# -*- coding: utf-8 -*-
from datetime import datetime, date
from datetime import timedelta

from odoo import models, fields, api, _

import dateutil
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'


class SaleOrderr(models.Model):
    _inherit = 'sale.order'
    description = "Sale Order"

    sale_order_accommodation = fields.One2many('sale.order.accommodation', 'sale_id', string='Accommodation')
    sale_order_accommodation_inv = fields.One2many('sale.order.accommodation.inv', 'sale_id', string='Accommodation')
    sale_order_accommodation1 = fields.One2many('sale.order.city1', 'sale_id', string='accommodation1')
    sale_order_accommodation2 = fields.One2many('sale.order.city2', 'sale_id', string='accommodation2')
    sale_order_accommodation3 = fields.One2many('sale.order.city3', 'sale_id', string='accommodation3')
    sale_order_accommodation4 = fields.One2many('sale.order.city4', 'sale_id', string='accommodation4')
    sale_order_accommodation5 = fields.One2many('sale.order.city5', 'sale_id', string='accommodation5')
    sale_order_accommodation6 = fields.One2many('sale.order.city6', 'sale_id', string='accommodation6')
    sale_order_flight_int = fields.One2many('sale.order.flightint', 'sale_id', string='flight')
    sale_order_flight_int_inv = fields.One2many('sale.order.flightint.inv', 'sale_id', string='flight')
    sale_order_flight_dom = fields.One2many('sale.order.flightdom', 'sale_id', string='flight')
    sale_order_visa = fields.One2many('sale.order.visa', 'sale_id', string='visa')
    sale_order_visa_inv = fields.One2many('sale.order.visa.inv', 'sale_id', string='visa')
    sale_order_medical = fields.One2many('sale.order.medical', 'sale_id', string='medical')
    sale_order_medical_inv = fields.One2many('sale.order.medical.inv', 'sale_id', string='medical')
    sale_order_vaccination = fields.One2many('sale.order.vaccination', 'sale_id', string='vaccination')
    sale_order_vaccination_inv = fields.One2many('sale.order.vaccination.inv', 'sale_id', string='vaccination')
    sale_order_program = fields.One2many('sale.order.program', 'sale_id', string='program')
    sale_order_program_inv = fields.One2many('sale.order.program.inv', 'sale_id', string='program')
    sale_order_transfer = fields.One2many('sale.order.transfer', 'sale_id', string='transfer')
    sale_order_transfer_inv = fields.One2many('sale.order.transfer.inv', 'sale_id', string='transfer')
    balance = fields.One2many('balance.balance', 'balance_id')
    individual = fields.Selection([('individual', 'Individual'), ('visa', 'Visa'), ('group', 'Group')],
                                  track_visibility='always', string="Branch")
    revised = fields.Selection([('revised', 'Revised')], track_visibility='always')
    completed = fields.Selection([('completed', 'Completed')], track_visibility='always')
    infant_inv = fields.Integer(string='Infant', track_visibility='always')
    child_inv = fields.Integer(string='Child', track_visibility='always')
    adult_inv = fields.Integer(string='Adult', track_visibility='always')
    year = fields.Selection([('2022', '2022'), ('2023', '2023'), ('2024', '2024')],
                            related='sale_order_template_id.year', )

    # def compute_year_from_quotation(self):
    #     if self.sale_order_template_id:
    #         print('asd')

    @api.multi
    def unlink(self):
        if not self.env.user.has_group('details.group_sale_super_manager'):
            raise ValidationError("Sorry you can not delete")
        super(SaleOrderr, self).unlink()

    @api.onchange('starttime', 'endtime')
    def change_checkin_and_out(self):
        # if self.sale_order_accommodation:
        for line in self.sale_order_accommodation:
            line.check_in_date = self.starttime.date()
            line.check_out_date = self.endtime.date()
        # if self.sale_order_accommodation_inv:
        for line in self.sale_order_accommodation_inv:
            line.check_in_date = self.starttime.date()
            line.check_out_date = self.endtime.date()

    @api.multi
    @api.onchange('endtime')
    def _age_on_travel_date_accommodation(self):
        for line in self.sale_order_accommodation:
            if line.partner_id.birthday:
                total_days = self.endtime.date() - line.partner_id.birthday
                years = int(abs(total_days.days / 365))
                remaining_days = total_days.days % 365
                if remaining_days >= 30:
                    months = int(abs(remaining_days / 30))
                else:
                    months = 0
                if (remaining_days % 30) < 30:
                    days = int((remaining_days % 30))
                else:
                    days = 0
                line.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"

    @api.multi
    @api.onchange('name_of_persons', 'partner_id', )
    def get_sale_order_details(self):
        sales_details = [(5, 0, 0,)]
        if self.partner_id:
            sales_details.append((0, 0, {
                'partner_id': self.partner_id.id,
            }))
        for rec in self.name_of_persons:
            sales_details.append((0, 0, {
                'partner_id': rec.id,
            }))
        self.sale_order_accommodation = sales_details
        self.sale_order_accommodation1 = sales_details
        self.sale_order_accommodation2 = sales_details
        self.sale_order_accommodation3 = sales_details
        self.sale_order_accommodation4 = sales_details
        self.sale_order_accommodation5 = sales_details
        self.sale_order_accommodation6 = sales_details
        self.sale_order_flight_int = sales_details
        self.sale_order_flight_dom = sales_details
        self.sale_order_visa = sales_details
        self.sale_order_medical = sales_details
        self.sale_order_vaccination = sales_details
        self.sale_order_program = sales_details
        self.sale_order_transfer = sales_details
        self.sale_order_accommodation_inv = sales_details
        self.sale_order_flight_int_inv = sales_details
        self.sale_order_visa_inv = sales_details
        self.sale_order_medical_inv = sales_details
        self.sale_order_vaccination_inv = sales_details
        self.sale_order_program_inv = sales_details
        self.sale_order_transfer_inv = sales_details


class Balances(models.Model):
    _name = 'balance.balance'
    currency_id = fields.Many2one('res.currency', string='Currency', track_visibility='always')
    date = fields.Date(track_visibility='always')
    number = fields.Char(track_visibility='always')
    partner_id = fields.Many2one('res.partner', string='Partner', track_visibility='always')
    reference = fields.Char(track_visibility='always')
    journal_id = fields.Many2one('account.journal', track_visibility='always')
    amount = fields.Monetary(track_visibility='always')
    status = fields.Selection([('draft', 'Unposted'), ('posted', 'Posted')], track_visibility='always')
    add = fields.Boolean(track_visibility='always')
    balance_id = fields.Many2one('sale.order', track_visibility='always')
    linked_with = fields.Char(readonly=True, track_visibility='always')

    # def get_sales_id(self):
    #     self.linked_with = self.id

    @api.multi
    @api.onchange('add')
    def calculate_total_paid(self):
        if self.add:
            self.balance_id.total_paymentt += self.amount


class SaleOrderAccommodation(models.Model):
    _name = 'sale.order.accommodation'

    serial_number = fields.Integer(string="S/N", name="S/N")
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    individual = fields.Selection(related='sale_id.individual')
    name = fields.Char(string="Name ___________", related='partner_id.name', readonly=False, store=True)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    phone_number = fields.Char(string='Phone_Number', related='partner_id.phone', readonly=False, store=True)
    whatsapp_num = fields.Char(string='Whatsapp_Num', related='partner_id.phone', readonly=False, store=True)
    date_of_birth = fields.Date(string='Date_of_birth')
    age = fields.Integer(string='Age', related='partner_id.years', readonly=False, store=True)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    city_name = fields.Many2one('res.country', string='City Name', store=True)
    room_id = fields.Integer(string='Room ID(S)')
    room_type = fields.Selection([('single_room', 'Single Room'), ('single_room_extra_bed', 'Single Room + Extra Bed'),
                                  ('double_king_bed', 'Double King Bed'),
                                  ('double_king_bed_extra_bed', 'Double King Bed + Extra Bed'),
                                  ('double_twin_bed', 'Double Twin Bed'),
                                  ('double_twin_bed_extra_bed', 'Double Twin Bed + Extra Bed'),
                                  ('triple_room', 'Triple Room'), ('family_room', 'Family Room'),
                                  ('junior_suite', 'Junior Suite'), ('executive_suite', 'Executive Suite'),
                                  ('silver_suite', 'Silver Suite'), ('villa', 'Villa'),
                                  ('villa_with_private_pool', 'Villa with Private Pool'),
                                  ('ocean_villa', 'Ocean Villa'),
                                  ('ocean_villa_with_private_pool', 'Ocean Villa with Private Pool'),
                                  ('overwater_villa', 'Overwater Villa'),
                                  ('overwater_villa_with_private_pool', 'Overwater Villa with Private Pool'),
                                  ('suite_with_private_pool', 'Suite with Private Pool'),
                                  ('beach_Villa', 'Beach Villa'),
                                  ('beach_villa_with_private_pool', 'Beach Villa with Private Pool'), ],
                                 string='Room Type(S)', store=True)
    room_view = fields.Many2one('room.view', string="Room View(S)")
    city_home = fields.Many2one('city.home', string="Hometown")
    room_special_request = fields.Many2many('room.special', string='Room Special Request(S)')
    meal_plan = fields.Many2one('meal.plan', index=True, string='Meal Plan(S)')
    notes = fields.Char(string='Notes')
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ________________ ")
    hotel_name = fields.Many2many('model.hotel', string='Hotel', )
    check_in_date = fields.Date(string='Check_In', compute="_get_date_from_quotation", readonly=False, store=True)
    check_out_date = fields.Date(string='Check_Out', compute="_get_date_from_quotation", readonly=False, store=True)
    no_of_nights = fields.Char(string='No. Of Nights', compute='_no_of_nights', )
    age_on_travel_date = fields.Char(string='Age On Travel', )

    def _get_date_from_quotation(self):
        self.check_in_date = self.sale_id.starttime.date()
        self.check_out_date = self.sale_id.endtime.date()

    # @api.one
    # @api.depends('nationality')
    # def get_hotels_test(self):
    #     return {'domain': {'hotel_name': [('id', 'in', self.sale_id.sale_order_template_id.hotel.ids)]}}

    @api.one
    @api.depends('check_in_date', 'check_out_date')
    def _no_of_nights(self):
        if self.check_in_date and self.check_out_date:
            d1 = self.check_in_date
            d2 = self.check_out_date
            g = str(d2 - d1).split()[0]
            if g == '0:00:00':
                self.no_of_nights = '0 night'
            else:
                self.no_of_nights = g + 'night'

    # @api.one
    # def _age_on_travel_date(self):
    #     if self.partner_id.birthday:
    #         total_days = self.sale_id.endtime.date() - self.partner_id.birthday
    #         print(total_days)
    #         years = int(abs(total_days.days / 365))
    #         remaining_days = total_days.days % 365
    #         if remaining_days >= 30:
    #             months = int(abs(remaining_days / 30))
    #         else:
    #             months = 0
    #         if (remaining_days % 30) < 30:
    #             days = int((remaining_days % 30))
    #         else:
    #             days = 0
    #         self.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"


class SaleOrderCity1(models.Model):
    _name = 'sale.order.city1'

    serial_number = fields.Integer(string="S/N", name="S/N")
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Name ___________", related='partner_id.name', readonly=False, store=True)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    phone_number = fields.Char(string='Phone_Number', related='partner_id.phone', readonly=False, store=True)
    whatsapp_num = fields.Char(string='Whatsapp_Num', related='partner_id.phone', readonly=False, store=True)
    date_of_birth = fields.Date(string='Date_of_birth')
    age = fields.Integer(string='Age', related='partner_id.years', readonly=False, store=True)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    city_name = fields.Many2one('res.country', string='City Name', store=True)

    room_id = fields.Integer(string='Room ID')
    room_type = fields.Selection([('single_room', 'Single Room'), ('single_room_extra_bed', 'Single Room + Extra Bed'),
                                  ('double_king_bed', 'Double King Bed'),
                                  ('double_king_bed_extra_bed', 'Double King Bed + Extra Bed'),
                                  ('double_twin_bed', 'Double Twin Bed'),
                                  ('double_twin_bed_extra_bed', 'Double Twin Bed + Extra Bed'),
                                  ('triple_room', 'Triple Room'), ('family_room', 'Family Room'),
                                  ('junior_suite', 'Junior Suite'), ('executive_suite', 'Executive Suite'),
                                  ('silver_suite', 'Silver Suite'), ('villa', 'Villa'),
                                  ('villa_with_private_pool', 'Villa with Private Pool'),
                                  ('ocean_villa', 'Ocean Villa'),
                                  ('ocean_villa_with_private_pool', 'Ocean Villa with Private Pool'),
                                  ('overwater_villa', 'Overwater Villa'),
                                  ('overwater_villa_with_private_pool', 'Overwater Villa with Private Pool'),
                                  ('suite_with_private_pool', 'Suite with Private Pool'),
                                  ('beach_Villa', 'Beach Villa'),
                                  ('beach_villa_with_private_pool', 'Beach Villa with Private Pool'), ],
                                 string='Room Type', store=True)
    room_view = fields.Many2one('room.view', string="Room View")
    room_special_request = fields.Many2many('room.special', string='Room Special Request')
    meal_plan = fields.Many2one('meal.plan', string='Meal Plan', )
    notes = fields.Char(string='Notes')
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ________________ ")
    hotel_name = fields.Many2many('model.hotel', string='Hotel', readonly=False, compute='get_hotels_test')
    check_in_date = fields.Date(string='Check_In', compute="_get_date_from_quotation", readonly=False, store=True)
    check_out_date = fields.Date(string='Check_Out', compute="_get_date_from_quotation", readonly=False, store=True)
    no_of_nights = fields.Char(string='No. Of Nights', compute='_no_of_nights', )
    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')

    def _get_date_from_quotation(self):
        self.check_in_date = self.sale_id.starttime.date()
        self.check_out_date = self.sale_id.endtime.date()

    @api.one
    @api.depends('nationality')
    def get_hotels_test(self):
        template = self.sale_id.sale_order_template_id
        return {'domain': {'hotel_name': [('id', 'in', template.hotel.ids)]}}

    @api.one
    @api.depends('check_in_date', 'check_out_date')
    def _no_of_nights(self):
        if self.check_in_date and self.check_out_date:
            d1 = self.check_in_date
            d2 = self.check_out_date
            g = str(d2 - d1).split()[0]
            if g == '0:00:00':
                self.no_of_nights = '0 night'
            else:
                self.no_of_nights = g + ' night'

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = self.sale_id.endtime.date() - self.partner_id.birthday
            years = int(abs(total_days.days / 365))
            remaining_days = total_days.days % 365
            if remaining_days >= 30:
                months = int(abs(remaining_days / 30))
            else:
                months = 0
            if (remaining_days % 30) < 30:
                days = int((remaining_days % 30))
            else:
                days = 0
            self.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"


class SaleOrderCity2(models.Model):
    _name = 'sale.order.city2'

    serial_number = fields.Integer(string="S/N", name="S/N")
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Name ___________", related='partner_id.name', readonly=False, store=True)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    phone_number = fields.Char(string='Phone_Number', related='partner_id.phone', readonly=False, store=True)
    whatsapp_num = fields.Char(string='Whatsapp_Num', related='partner_id.phone', readonly=False, store=True)
    date_of_birth = fields.Date(string='Date_of_birth')
    age = fields.Integer(string='Age', related='partner_id.years', readonly=False, store=True)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    city_name = fields.Many2one('res.country', string='City Name', store=True)

    room_id = fields.Integer(string='Room ID')
    room_view = fields.Many2one('room.view', string='Room View')
    room_type = fields.Selection([('single_room', 'Single Room'), ('single_room_extra_bed', 'Single Room + Extra Bed'),
                                  ('double_king_bed', 'Double King Bed'),
                                  ('double_king_bed_extra_bed', 'Double King Bed + Extra Bed'),
                                  ('double_twin_bed', 'Double Twin Bed'),
                                  ('double_twin_bed_extra_bed', 'Double Twin Bed + Extra Bed'),
                                  ('triple_room', 'Triple Room'), ('family_room', 'Family Room'),
                                  ('junior_suite', 'Junior Suite'), ('executive_suite', 'Executive Suite'),
                                  ('silver_suite', 'Silver Suite'), ('villa', 'Villa'),
                                  ('villa_with_private_pool', 'Villa with Private Pool'),
                                  ('ocean_villa', 'Ocean Villa'),
                                  ('ocean_villa_with_private_pool', 'Ocean Villa with Private Pool'),
                                  ('overwater_villa', 'Overwater Villa'),
                                  ('overwater_villa_with_private_pool', 'Overwater Villa with Private Pool'),
                                  ('suite_with_private_pool', 'Suite with Private Pool'),
                                  ('beach_Villa', 'Beach Villa'),
                                  ('beach_villa_with_private_pool', 'Beach Villa with Private Pool'), ],
                                 string='Room Type', store=True)
    room_view = fields.Many2one('room.view', string="Room View")
    room_special_request = fields.Many2many('room.special', string='Room Special Request')
    meal_plan = fields.Many2one('meal.plan', index=True, string='Meal Plan')
    notes = fields.Char(string='Notes')
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ________________ ")
    hotel_name = fields.Many2many('model.hotel', string='Hotel', readonly=False, compute='get_hotels_test')
    check_in_date = fields.Date(string='Check_In', compute="_get_date_from_quotation", readonly=False, store=True)
    check_out_date = fields.Date(string='Check_Out', compute="_get_date_from_quotation", readonly=False, store=True)
    no_of_nights = fields.Char(string='No. Of Nights', compute='_no_of_nights', )

    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')

    def _get_date_from_quotation(self):
        self.check_in_date = self.sale_id.starttime.date()
        self.check_out_date = self.sale_id.endtime.date()

    @api.one
    @api.depends('nationality')
    def get_hotels_test(self):
        template = self.sale_id.sale_order_template_id
        return {'domain': {'hotel_name': [('id', 'in', template.hotel.ids)]}}

    @api.one
    @api.depends('check_in_date', 'check_out_date')
    def _no_of_nights(self):
        if self.check_in_date and self.check_out_date:
            d1 = self.check_in_date
            d2 = self.check_out_date
            g = str(d2 - d1).split()[0]
            if g == '0:00:00':
                self.no_of_nights = '0 night'
            else:
                self.no_of_nights = g + ' night'

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = self.sale_id.endtime.date() - self.partner_id.birthday
            years = int(abs(total_days.days / 365))
            remaining_days = total_days.days % 365
            if remaining_days >= 30:
                months = int(abs(remaining_days / 30))
            else:
                months = 0
            if (remaining_days % 30) < 30:
                days = int((remaining_days % 30))
            else:
                days = 0
            self.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"


class SaleOrderCity3(models.Model):
    _name = 'sale.order.city3'

    serial_number = fields.Integer(string="S/N", name="S/N")
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Name ___________", related='partner_id.name', readonly=False, store=True)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    phone_number = fields.Char(string='Phone_Number', related='partner_id.phone', readonly=False, store=True)
    whatsapp_num = fields.Char(string='Whatsapp_Num', related='partner_id.phone', readonly=False, store=True)
    date_of_birth = fields.Date(string='Date_of_birth')
    age = fields.Integer(string='Age', related='partner_id.years', readonly=False, store=True)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    city_name = fields.Many2one('res.country', string='City Name', store=True)

    room_id = fields.Integer(string='Room ID')
    room_type = fields.Selection([('single_room', 'Single Room'), ('single_room_extra_bed', 'Single Room + Extra Bed'),
                                  ('double_king_bed', 'Double King Bed'),
                                  ('double_king_bed_extra_bed', 'Double King Bed + Extra Bed'),
                                  ('double_twin_bed', 'Double Twin Bed'),
                                  ('double_twin_bed_extra_bed', 'Double Twin Bed + Extra Bed'),
                                  ('triple_room', 'Triple Room'), ('family_room', 'Family Room'),
                                  ('junior_suite', 'Junior Suite'), ('executive_suite', 'Executive Suite'),
                                  ('silver_suite', 'Silver Suite'), ('villa', 'Villa'),
                                  ('villa_with_private_pool', 'Villa with Private Pool'),
                                  ('ocean_villa', 'Ocean Villa'),
                                  ('ocean_villa_with_private_pool', 'Ocean Villa with Private Pool'),
                                  ('overwater_villa', 'Overwater Villa'),
                                  ('overwater_villa_with_private_pool', 'Overwater Villa with Private Pool'),
                                  ('suite_with_private_pool', 'Suite with Private Pool'),
                                  ('beach_Villa', 'Beach Villa'),
                                  ('beach_villa_with_private_pool', 'Beach Villa with Private Pool'), ],
                                 string='Room Type', store=True)
    room_view = fields.Many2one('room.view', string="Room View")
    room_special_request = fields.Many2many('room.special', string='Room Special Request')
    meal_plan = fields.Many2one('meal.plan', index=True, string='Meal Plan')
    notes = fields.Char(string='Notes')
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ________________ ")
    hotel_name = fields.Many2many('model.hotel', string='Hotel', readonly=False, compute='get_hotels_test')
    check_in_date = fields.Date(string='Check_In', compute="_get_date_from_quotation", readonly=False, store=True)
    check_out_date = fields.Date(string='Check_Out', compute="_get_date_from_quotation", readonly=False, store=True)
    no_of_nights = fields.Char(string='No. Of Nights', compute='_no_of_nights', )

    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')

    def _get_date_from_quotation(self):
        self.check_in_date = self.sale_id.starttime.date()
        self.check_out_date = self.sale_id.endtime.date()

    @api.one
    @api.depends('nationality')
    def get_hotels_test(self):
        template = self.sale_id.sale_order_template_id
        return {'domain': {'hotel_name': [('id', 'in', template.hotel.ids)]}}

    @api.one
    @api.depends('check_in_date', 'check_out_date')
    def _no_of_nights(self):
        if self.check_in_date and self.check_out_date:
            d1 = self.check_in_date
            d2 = self.check_out_date
            g = str(d2 - d1).split()[0]
            if g == '0:00:00':
                self.no_of_nights = '0 night'
            else:
                self.no_of_nights = g + ' night'

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = self.sale_id.endtime.date() - self.partner_id.birthday
            years = int(abs(total_days.days / 365))
            remaining_days = total_days.days % 365
            if remaining_days >= 30:
                months = int(abs(remaining_days / 30))
            else:
                months = 0
            if (remaining_days % 30) < 30:
                days = int((remaining_days % 30))
            else:
                days = 0
            self.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"


class SaleOrderCity4(models.Model):
    _name = 'sale.order.city4'

    serial_number = fields.Integer(string="S/N", name="S/N")
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Name ___________", related='partner_id.name', readonly=False, store=True)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    phone_number = fields.Char(string='Phone_Number', related='partner_id.phone', readonly=False, store=True)
    whatsapp_num = fields.Char(string='Whatsapp_Num', related='partner_id.phone', readonly=False, store=True)
    date_of_birth = fields.Date(string='Date_of_birth')
    age = fields.Integer(string='Age', related='partner_id.years', readonly=False, store=True)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    city_name = fields.Many2one('res.country', string='City Name', store=True)

    room_id = fields.Integer(string='Room ID')
    room_type = fields.Selection([('single_room', 'Single Room'), ('single_room_extra_bed', 'Single Room + Extra Bed'),
                                  ('double_king_bed', 'Double King Bed'),
                                  ('double_king_bed_extra_bed', 'Double King Bed + Extra Bed'),
                                  ('double_twin_bed', 'Double Twin Bed'),
                                  ('double_twin_bed_extra_bed', 'Double Twin Bed + Extra Bed'),
                                  ('triple_room', 'Triple Room'), ('family_room', 'Family Room'),
                                  ('junior_suite', 'Junior Suite'), ('executive_suite', 'Executive Suite'),
                                  ('silver_suite', 'Silver Suite'), ('villa', 'Villa'),
                                  ('villa_with_private_pool', 'Villa with Private Pool'),
                                  ('ocean_villa', 'Ocean Villa'),
                                  ('ocean_villa_with_private_pool', 'Ocean Villa with Private Pool'),
                                  ('overwater_villa', 'Overwater Villa'),
                                  ('overwater_villa_with_private_pool', 'Overwater Villa with Private Pool'),
                                  ('suite_with_private_pool', 'Suite with Private Pool'),
                                  ('beach_Villa', 'Beach Villa'),
                                  ('beach_villa_with_private_pool', 'Beach Villa with Private Pool'), ],
                                 string='Room Type', store=True)
    room_view = fields.Many2one('room.view', string="Room View")
    room_special_request = fields.Many2many('room.special', string='Room Special Request')
    meal_plan = fields.Many2one('meal.plan', index=True, string='Meal Plan')
    notes = fields.Char(string='Notes')
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "ID")
    hotel_name = fields.Many2many('model.hotel', string='Hotel', readonly=False, compute='get_hotels_test')
    check_in_date = fields.Date(string='Check_In', compute="_get_date_from_quotation", readonly=False, store=True)
    check_out_date = fields.Date(string='Check_Out', compute="_get_date_from_quotation", readonly=False, store=True)
    no_of_nights = fields.Char(string='No. Of Nights', compute='_no_of_nights', )

    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')

    def _get_date_from_quotation(self):
        self.check_in_date = self.sale_id.starttime.date()
        self.check_out_date = self.sale_id.endtime.date()

    @api.one
    @api.depends('nationality')
    def get_hotels_test(self):
        template = self.sale_id.sale_order_template_id
        return {'domain': {'hotel_name': [('id', 'in', template.hotel.ids)]}}

    @api.one
    @api.depends('check_in_date', 'check_out_date')
    def _no_of_nights(self):
        if self.check_in_date and self.check_out_date:
            d1 = self.check_in_date
            d2 = self.check_out_date
            split = str(d2 - d1).split()[0]
            if split == '0:00:00':
                self.no_of_nights = '0 night'
            else:
                self.no_of_nights = split + ' night'

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = self.sale_id.endtime.date() - self.partner_id.birthday
            years = int(abs(total_days.days / 365))
            remaining_days = total_days.days % 365
            if remaining_days >= 30:
                months = int(abs(remaining_days / 30))
            else:
                months = 0
            if (remaining_days % 30) < 30:
                days = int((remaining_days % 30))
            else:
                days = 0
            self.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"


class SaleOrderCity5(models.Model):
    _name = 'sale.order.city5'

    serial_number = fields.Integer(string="S/N", name="S/N")
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Name ___________", related='partner_id.name', readonly=False, store=True)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    phone_number = fields.Char(string='Phone_Number', related='partner_id.phone', readonly=False, store=True)
    whatsapp_num = fields.Char(string='Whatsapp_Num', related='partner_id.phone', readonly=False, store=True)
    date_of_birth = fields.Date(string='Date_of_birth')
    age = fields.Integer(string='Age', related='partner_id.years', readonly=False, store=True)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    city_name = fields.Many2one('res.country', string='City Name', store=True)

    room_id = fields.Integer(string='Room ID')
    room_type = fields.Selection([('single_room', 'Single Room'), ('single_room_extra_bed', 'Single Room + Extra Bed'),
                                  ('double_king_bed', 'Double King Bed'),
                                  ('double_king_bed_extra_bed', 'Double King Bed + Extra Bed'),
                                  ('double_twin_bed', 'Double Twin Bed'),
                                  ('double_twin_bed_extra_bed', 'Double Twin Bed + Extra Bed'),
                                  ('triple_room', 'Triple Room'), ('family_room', 'Family Room'),
                                  ('junior_suite', 'Junior Suite'), ('executive_suite', 'Executive Suite'),
                                  ('silver_suite', 'Silver Suite'), ('villa', 'Villa'),
                                  ('villa_with_private_pool', 'Villa with Private Pool'),
                                  ('ocean_villa', 'Ocean Villa'),
                                  ('ocean_villa_with_private_pool', 'Ocean Villa with Private Pool'),
                                  ('overwater_villa', 'Overwater Villa'),
                                  ('overwater_villa_with_private_pool', 'Overwater Villa with Private Pool'),
                                  ('suite_with_private_pool', 'Suite with Private Pool'),
                                  ('beach_Villa', 'Beach Villa'),
                                  ('beach_villa_with_private_pool', 'Beach Villa with Private Pool'), ],
                                 string='Room Type', store=True)
    room_view = fields.Many2one('room.view', string="Room View")
    room_special_request = fields.Many2many('room.special', string='Room Special Request')
    meal_plan = fields.Many2one('meal.plan', index=True, string='Meal Plan')
    notes = fields.Char(string='Notes')
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ________________ ")
    # hotel_name = fields.Many2many(string='Hotel', readonly=False, compute='onchange_sale_order_template_idd')
    # hotel_name = fields.Many2many(related="sale_id.hotel", string='Hotel', readonly=False)
    hotel_name = fields.Many2many('model.hotel', string='Hotel', readonly=False, compute='get_hotels_test')
    check_in_date = fields.Date(string='Check_In', compute="_get_date_from_quotation", readonly=False, store=True)
    check_out_date = fields.Date(string='Check_Out', compute="_get_date_from_quotation", readonly=False, store=True)
    no_of_nights = fields.Char(string='No. Of Nights', compute='_no_of_nights', )

    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')

    def _get_date_from_quotation(self):
        self.check_in_date = self.sale_id.starttime.date()
        self.check_out_date = self.sale_id.endtime.date()

    @api.one
    @api.depends('nationality')
    def get_hotels_test(self):
        template = self.sale_id.sale_order_template_id
        return {'domain': {'hotel_name': [('id', 'in', template.hotel.ids)]}}

    @api.one
    @api.depends('check_in_date', 'check_out_date')
    def _no_of_nights(self):
        if self.check_in_date and self.check_out_date:
            d1 = self.check_in_date
            d2 = self.check_out_date
            g = str(d2 - d1).split()[0]
            if g == '0:00:00':
                self.no_of_nights = '0 night'
            else:
                self.no_of_nights = g + ' night'

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = self.sale_id.endtime.date() - self.partner_id.birthday
            years = int(abs(total_days.days / 365))
            remaining_days = total_days.days % 365
            if remaining_days >= 30:
                months = int(abs(remaining_days / 30))
            else:
                months = 0
            if (remaining_days % 30) < 30:
                days = int((remaining_days % 30))
            else:
                days = 0
            self.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"


class SaleOrderCity6(models.Model):
    _name = 'sale.order.city6'

    serial_number = fields.Integer(string="S/N", name="S/N")
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Name ___________", related='partner_id.name', readonly=False, store=True)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    phone_number = fields.Char(string='Phone_Number', related='partner_id.phone', readonly=False, store=True)
    whatsapp_num = fields.Char(string='Whatsapp_Num', related='partner_id.phone', readonly=False, store=True)
    date_of_birth = fields.Date(string='Date_of_birth')
    age = fields.Integer(string='Age', related='partner_id.years', readonly=False, store=True)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    city_name = fields.Many2one('res.country', string='City Name', store=True)

    room_id = fields.Integer(string='Room ID')
    room_type = fields.Selection([('single_room', 'Single Room'), ('single_room_extra_bed', 'Single Room + Extra Bed'),
                                  ('double_king_bed', 'Double King Bed'),
                                  ('double_king_bed_extra_bed', 'Double King Bed + Extra Bed'),
                                  ('double_twin_bed', 'Double Twin Bed'),
                                  ('double_twin_bed_extra_bed', 'Double Twin Bed + Extra Bed'),
                                  ('triple_room', 'Triple Room'), ('family_room', 'Family Room'),
                                  ('junior_suite', 'Junior Suite'), ('executive_suite', 'Executive Suite'),
                                  ('silver_suite', 'Silver Suite'), ('villa', 'Villa'),
                                  ('villa_with_private_pool', 'Villa with Private Pool'),
                                  ('ocean_villa', 'Ocean Villa'),
                                  ('ocean_villa_with_private_pool', 'Ocean Villa with Private Pool'),
                                  ('overwater_villa', 'Overwater Villa'),
                                  ('overwater_villa_with_private_pool', 'Overwater Villa with Private Pool'),
                                  ('suite_with_private_pool', 'Suite with Private Pool'),
                                  ('beach_Villa', 'Beach Villa'),
                                  ('beach_villa_with_private_pool', 'Beach Villa with Private Pool'), ],
                                 string='Room Type', store=True)
    room_view = fields.Many2one('room.view', string="Room View")
    room_special_request = fields.Many2many('room.special', string='Room Special Request')
    meal_plan = fields.Many2one('meal.plan', index=True, string='Meal Plan')
    notes = fields.Char(string='Notes')
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ________________ ")
    # hotel_name = fields.Many2many(string='Hotel', readonly=False, compute='onchange_sale_order_template_idd')
    # hotel_name = fields.Many2many(related="sale_id.hotel", string='Hotel', readonly=False)
    hotel_name = fields.Many2many('model.hotel', string='Hotel', readonly=False, compute='get_hotels_test')
    check_in_date = fields.Date(string='Check_In', compute="_get_date_from_quotation", readonly=False, store=True)
    check_out_date = fields.Date(string='Check_Out', compute="_get_date_from_quotation", readonly=False, store=True)
    no_of_nights = fields.Char(string='No. Of Nights', compute='_no_of_nights', )

    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')

    def _get_date_from_quotation(self):
        self.check_in_date = self.sale_id.starttime.date()
        self.check_out_date = self.sale_id.endtime.date()

    @api.one
    @api.depends('nationality')
    def get_hotels_test(self):
        template = self.sale_id.sale_order_template_id
        return {'domain': {'hotel_name': [('id', 'in', template.hotel.ids)]}}

    @api.one
    @api.depends('check_in_date', 'check_out_date')
    def _no_of_nights(self):
        if self.check_in_date and self.check_out_date:
            d1 = self.check_in_date
            d2 = self.check_out_date
            count = str(d2 - d1).split()[0]
            if count == '0:00:00':
                self.no_of_nights = '0 night'
            else:
                self.no_of_nights = count + ' night'

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = self.sale_id.endtime.date() - self.partner_id.birthday
            years = int(abs(total_days.days / 365))
            remaining_days = total_days.days % 365
            if remaining_days >= 30:
                months = int(abs(remaining_days / 30))
            else:
                months = 0
            if (remaining_days % 30) < 30:
                days = int((remaining_days % 30))
            else:
                days = 0
            self.age_on_travel_date = str(years) + " years " + str(months) + " months " + str(days) + " days"


class SaleOrderFlight(models.Model):
    _name = 'sale.order.flightint'

    name = fields.Char(string="Name ______________", related='partner_id.name', readonly=False, store=True)
    sequence = fields.Integer(default=10)
    individual = fields.Selection(related='sale_id.individual')
    serial_number = fields.Integer(string="S/N", name="S/N")
    flight_status = fields.Selection([('hold', 'Hold'), ('issued', 'Issued'),
                                      ('waiting_issuing', 'Waiting Issuing '), ('sent_to_client', 'Sent to Client')],
                                     default='hold', store=True)
    route = fields.Selection(
        [('APR&DEP', 'APR&DEP'), ('departure_only', 'departure_only'), ('arrival_only', 'Arrival only'), ],
        default='APR&DEP', store=True, string="Route(S)")
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier(S)', domain=[('supplier', '=', 1)])
    hold_dead_line = fields.Datetime(string="Hold Deadline")
    booking_ref_pic = fields.Binary()
    booking_ref = fields.Char()
    extra_luggage = fields.Selection(
        [('extra_bag_apr_dep', 'Extra Bag Apr &DEP'), ('extra_bag_on_arr', 'Extra Bag on ARR'),
         ('extra_bag_on_dep', 'Extra Bag on DEP')], store=True, string="Extra Luggage(S)")
    dept_date = fields.Datetime(string='DEP Timing')
    arr_date = fields.Datetime(string='ARR Timing')
    deptt_date = fields.Datetime(string='DEP  Timing')
    arrr_date = fields.Datetime(string='ARR  Timing')
    dep_flight_no = fields.Char(string='DEP Flight Num')
    deb_flight_route = fields.Char(string='DEP Flight Route')
    dep_flight_timing = fields.Datetime(string="DEP Timing")
    arr_flight_no = fields.Char(String='ARR Flight No')
    arr_flight_route = fields.Char(string='ARR Flight Route')
    arr_flight_timing = fields.Datetime(string="ARR Timing")
    transit_time = fields.Integer(string='Transit Time')
    transit_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    transitt_time = fields.Integer(string='Transit Time')
    transitt_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    attachment = fields.Binary(string='Attachment')
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ______________")
    flight_type = fields.Selection(
        [('int_grp', 'INT-GRP'), ('int_sys', 'INT-SYS'), ('without_flight', 'without flight')],
        string='Flight Type(S)')

    grp = fields.Integer('international group', default=0)
    sys = fields.Integer('international system', default=0)
    without_flight_counter = fields.Integer('without flight', default=0)

    @api.onchange('flight_type')
    def flight_type_change(self):
        without_flight_counter = 0
        grp = 0
        sys = 0
        objects = list(self.sale_id.sale_order_flight_int)
        objects.pop()
        for line in objects:
            if line.flight_type == 'without_flight':
                without_flight_counter += 1
            if line.flight_type == 'int_grp':
                grp += 1
            if line.flight_type == 'int_sys':
                sys += 1
        print(grp)
        print(without_flight_counter)
        print(sys)
        self.without_flight_counter = without_flight_counter
        print(self.without_flight_counter)
        self.grp = grp
        self.sys = sys
        # for line in self:
        #     line.without_flight_counter=without_flight_counter
        #     line.grp=grp
        #     line.sys=sys


class SaleOrderFlightDom(models.Model):
    _name = 'sale.order.flightdom'

    name = fields.Char(string="Name ______________", related='partner_id.name', readonly=False, store=True)
    sequence = fields.Integer(default=10)
    individual = fields.Selection(related='sale_id.individual')
    serial_number = fields.Integer(string="S/N", name="S/N")
    flight_status = fields.Selection([('hold', 'Hold'), ('issued', 'Issued'),
                                      ('waiting_issuing', 'Waiting Issuing '), ('sent_to_client', 'Sent to Client')],
                                     default='hold', store=True)
    flight_type = fields.Selection(
        [('dom_sys', 'DOM-SYS'), ('DOM-GRP', 'DOM-GRP'), ('without_flight', 'Without Flight')],
        default='dom_sys', store=True, string='Flight Type(S)')
    route = fields.Selection(
        [('APR&DEP', 'APR&DEP'), ('departure_only', 'departure_only'), ('arrival_only', 'Arrival only'), ],
        default='APR&DEP', store=True, string="Route(S)")
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    supplier = fields.Many2one('res.partner', string='Supplier(S)', domain=[('supplier', '=', 1)])
    hold_dead_line = fields.Datetime(string="Hold Deadline")
    booking_ref_pic = fields.Binary()
    booking_ref = fields.Char()
    extra_luggage = fields.Selection(
        [('extra_bag_apr_dep', 'Extra Bag Apr &DEP'), ('extra_bag_on_arr', 'Extra Bag on ARR'),
         ('extra_bag_on_dep', 'Extra Bag on DEP')], store=True, string="Extra Luggage(S)")
    dept_date = fields.Datetime(string='DEP Timing')
    arr_date = fields.Datetime(string='ARR Timing')
    deptt_date = fields.Datetime(string='DEP  Timing')
    arrr_date = fields.Datetime(string='ARR  Timing')
    dep_flight_no = fields.Char(string='DEP Flight Num')
    deb_flight_route = fields.Char(string='DEP Flight Route')
    dep_flight_timing = fields.Datetime(string="DEP Timing")
    arr_flight_no = fields.Char(String='ARR Flight No')
    arr_flight_route = fields.Char(string='ARR Flight Route')
    arr_flight_timing = fields.Datetime(string="ARR Timing")
    transit_time = fields.Integer(string='Transit Time')
    transit_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    transitt_time = fields.Integer(string='Transit Time')
    transitt_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    attachment = fields.Binary(string='Attachment')
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name ______________")


class SaleOrderVisa(models.Model):
    _name = 'sale.order.visa'

    name = fields.Char(string="Name", related='partner_id.name', readonly=False, store=True)
    gender = fields.Selection([('male', 'Male'), ("female", 'Female')], related='partner_id.gender', string='Gender',
                              store=True)
    sequence = fields.Integer(default=10)
    relation = fields.Selection(string='Relation', related='partner_id.relation', readonly=False, store=True)
    nationality = fields.Many2one(string='Nationality', related='partner_id.country_id', readonly=False, store=True)
    phone_number = fields.Char(string='Phone number', related='partner_id.phone', readonly=False, store=True)
    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    visa_type = fields.Selection([('embassy_client', 'Embassy - Client'), ('embassy_company', 'Embassy - Company'),
                                  ('embassy_assist_only', 'Embassy - Assist Only'),
                                  ('online_client', 'Online - Client'), ('online_company', 'Online - Company'),
                                  ('no_visa_required', 'No Visa Required'), ], default='no_visa_required',
                                 string='Visa Type & Responsibility(S)', store=True)
    visa_situation = fields.Selection([('paper_required_from_client', 'Paper Required from Client'),
                                       ('received_visa_documents', 'Received Visa Documents'),
                                       ('submitted_to_embassy', 'Submitted to Embassy'), ('issued', 'Issued'),
                                       ('rejected', 'Rejected'),
                                       ('online_visa_passport_delivered', 'Online Visa Passport Delivered'),
                                       ('received_online_visa', 'Received Online Visa'),
                                       ('sent_online_visa_to_client', 'Sent Online Visa to Client'), ],
                                      default='paper_required_from_client', string='Visa Situation', store=True)
    embassy_appointment = fields.Datetime(string='Embassy Appointment Date')
    receiving_date = fields.Datetime(string='Receiving Date')
    notes = fields.Char()
    fake_ticket = fields.Boolean()
    voucher = fields.Boolean()
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    attachment = fields.Binary()
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "id")

    @api.one
    @api.onchange('endtime')
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = str(self.sale_id.endtime.date() - self.partner_id.birthday).split()[0]
            years = int(int(total_days) / 365)
            if int(total_days) % 30:
                months = (int(total_days) % 30) % 12
            else:
                months = 0
            self.age_on_travel_date = str(years) + "years " + str(months) + "months"


class SaleOrderMedical(models.Model):
    _name = 'sale.order.medical'

    name = fields.Char(string="Name", related='partner_id.name', readonly=False, store=True)
    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')
    sequence = fields.Integer(default=10)
    medical_insurance = fields.Selection([('1', 'Yes'), ('2', 'No')], string="Medical Insurance(S)")
    cost = fields.Integer(string='Cost')
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name")

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = str(self.sale_id.endtime.date() - self.partner_id.birthday).split()[0]
            years = int(int(total_days) / 365)
            if int(total_days) % 30 < 12:
                months = int(total_days) % 30
            else:
                months = 0
            self.age_on_travel_date = str(years) + "years " + str(months) + "months"


class SaleOrderVaccination(models.Model):
    _name = 'sale.order.vaccination'

    name = fields.Char(string="Name", related='partner_id.name', readonly=False, store=True)
    sequence = fields.Integer(default=10)
    age_on_travel_date = fields.Char(string='Age On Travel', compute='_age_on_travel_date')
    age_type = fields.Selection(string='Age type', related='partner_id.age_type', readonly=False, store=True)
    qr_code = fields.Selection([('yes', 'Yes'), ('yes_uploaded', 'Yes Uploaded'), ('not_vaccinated', 'Not Vaccinated'),
                                ('vacc_without_qr', 'Vacc without QR'), ], default='yes',
                               string='Qr Code Vacc. Cert(S)',
                               store=True)
    pcr_required = fields.Many2one('pcr.required', string='PCR Required')
    vaccine_type = fields.Selection([('no', 'No'), ('johnson_one_dose', 'Johnson One Dose'), ('1', 'Sinovac One Dose'),
                                     ('2', 'Sinovac Two Doses'),
                                     ('3', 'Sinovac Three Doses'),
                                     ('4', 'Pfizer One Dose'),
                                     ('5', 'Pfizer Two Doses'),
                                     ('6', 'Pfizer Three Doses'),
                                     ('7', 'Sinopharm One Dose'),
                                     ('8', 'Sinopharm Two Doses'),
                                     ('9', 'Sinopharm Three Doses'),
                                     ('10', 'Moderna One Dose'),
                                     ('11', 'Moderna Two Doses'),
                                     ('12', 'Moderna Three Doses'),
                                     ('13', 'AstraZeneca One Dose'),
                                     ('14', 'AstraZeneca Two Doses'),
                                     ('15', 'AstraZeneca Three Doses'),
                                     ('16', 'Sputnik One Dose'),
                                     ('17', 'Sputnik Two Doses'),
                                     ('18', 'Sputnik Three Doses'),
                                     ('19', 'Covaxin One Dose'),
                                     ('20', 'Covacine Two Doses'),
                                     ('21', 'Covacine Three Doses'),
                                     ('22', 'Covishield One Dose'),
                                     ('23', 'Covishield Two Doses'),
                                     ('24', 'Covishield Three Doses'),
                                     ('25', 'Novavax One Dose'),
                                     ('26', 'Novavax Two Doses'),
                                     ('27', 'Novavax Three Doses'),
                                     ('28', 'Convidecia - CanSino One Dose'),
                                     ('29', 'Sputnik Light One Dose'),
                                     ('30', 'Sputnik Light Two Doses'),
                                     ('31', 'Sputnik Light Three Doses'), ], default='no',
                                    string='Vaccine Type', store=True)
    last_dose_date = fields.Date(string='Last Dose Date')
    attachment = fields.Binary(string='QR Image')
    notes = fields.Char(string="Notes")
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name")

    @api.one
    def _age_on_travel_date(self):
        if self.partner_id.birthday:
            total_days = str(self.sale_id.endtime.date() - self.partner_id.birthday).split()[0]
            years = int(int(total_days) / 365)
            if int(total_days) % 30 < 12:
                months = int(total_days) % 30
            else:
                months = 0
            self.age_on_travel_date = str(years) + "years " + str(months) + "months"


class SaleOrderProgram(models.Model):
    _name = 'sale.order.program'

    name = fields.Char(string="Name", related='partner_id.name', readonly=False, store=True)
    sequence = fields.Integer(default=10)
    age_type = fields.Selection(string='Age Type', related='partner_id.age_type', readonly=False, store=True)
    status = fields.Selection([('yes', 'Yes'), ('no', 'No')], store=True, string="Status(S)")
    program_name = fields.Many2many('program.city', string='Program Name(S)', readonly=False, store=True)
    description = fields.Char()
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    cost = fields.Integer(string='Cost')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name")


class SaleOrderTransfer(models.Model):
    _name = 'sale.order.transfer'

    name = fields.Char(string="Name", related='partner_id.name', readonly=False, store=True)
    sequence = fields.Integer(default=10)
    vehicle_type = fields.Many2one('vehicle.type', store=True, string="Vehicle Type(S)")
    date_of_transfer = fields.Date(string='Date Of Transfer(S)')
    pick_up_time = fields.Float(string='Pick Up Time(S)')
    route = fields.Selection(
        [('airport_hotel', 'Airport - Hotel'), ('hotel_airport', 'Hotel - Airport'), ('hotel_hotel', 'Hotel - Hotel'),
         ('train_station_hotel', 'Train Station - Hotel'), ('hotel_train_station', 'Hotel - Train Station'),
         ('port_hotel', 'Port - Hotel'), ('hotel_port', 'Hotel - Port'), ], string='Route(S)', store=True)
    transfer_cost = fields.Selection([('extra_cost', 'Extra Cost'), ('included', 'Included')], string='Transfer cost',
                                     store=True)
    supplier = fields.Many2one('res.partner', string='Supplier(S)', domain=[('supplier', '=', 1)])
    no_of_luggage = fields.Integer(string='No. of Luggage')
    sale_id = fields.Many2one('sale.order')
    sale_order_template_id = fields.Many2one('sale.order.template')
    partner_id = fields.Many2one('res.partner', "Name")
    cost = fields.Integer(string='Cost(S)')


class ProgramCity(models.Model):
    _name = 'program.city'
    name = fields.Char(string="Program City")


class PcrRequired(models.Model):
    _name = 'pcr.required'
    name = fields.Char(string="PCR Required")


class CityHome(models.Model):
    _name = 'city.home'
    name = fields.Char(string="City Home")


class YearYear(models.Model):
    _name = 'year.year'
    year = fields.Integer(string="Year")
