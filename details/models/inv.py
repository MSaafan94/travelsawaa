# -*- coding: utf-8 -*-
from datetime import datetime, date
from datetime import timedelta
from odoo import models, fields, api, _
import dateutil
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class SaleOrderAccommodationInv(models.Model):
    _name = 'sale.order.accommodation.inv'

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
    age_on_travel_date = fields.Char(string='Age On Travel',)

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




class SaleOrderFlightInv(models.Model):
    _name = 'sale.order.flightint.inv'

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


class SaleOrderVisaInv(models.Model):
    _name = 'sale.order.visa.inv'

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
    destination = fields.Many2one('model.destination',)

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


class SaleOrderMedicalInv(models.Model):
    _name = 'sale.order.medical.inv'

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


class SaleOrderVaccinationInv(models.Model):
    _name = 'sale.order.vaccination.inv'

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


class SaleOrderProgramInv(models.Model):
    _name = 'sale.order.program.inv'

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


class SaleOrderTransferInv(models.Model):
    _name = 'sale.order.transfer.inv'

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