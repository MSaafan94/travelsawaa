from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class QuotationTemplateInherit(models.Model):
    _name = 'sale.order.template'
    _inherit = ['mail.thread', 'sale.order.template']
    quot_accommodation = fields.One2many('accommodation.main', 'quot_id', string='accommodation', copy=True)
    quot_accommodation_inv = fields.One2many('accommodation.main', 'quot_id', string='accommodation inv', )
    quot_accommodation1 = fields.One2many('accommodation.city1', 'quot_id', string='accommodation1', copy=True)
    quot_accommodation2 = fields.One2many('accommodation.city2', 'quot_id', string='accommodation2', copy=True)
    quot_accommodation3 = fields.One2many('accommodation.city3', 'quot_id', string='accommodation3', copy=True)
    quot_accommodation4 = fields.One2many('accommodation.city4', 'quot_id', string='accommodation4', copy=True)
    quot_accommodation5 = fields.One2many('accommodation.city5', 'quot_id', string='accommodation5', copy=True)
    quot_accommodation6 = fields.One2many('accommodation.city6', 'quot_id', string='accommodation6', copy=True)
    flight_international = fields.One2many('quot.flight.international', 'quot_id', string='flight_international',
                                           copy=True)
    flight_domestic = fields.One2many('quot.flight.domestic', 'quot_id', string='flight_domestic', )
    visa = fields.One2many('quot.visa', 'quot_id', string='visa', copy=True)
    vaccination = fields.One2many('quot.vaccination', 'quot_id', string='vaccination', copy=True)
    program = fields.One2many('quot.program', 'quot_id', string='program', copy=True)
    sale_orders = fields.One2many('sale.order', 'sale_order_template_id', string='sale orders')
    operation = fields.Boolean(string='Operation', track_visibility="always")


    @api.multi
    def unlink(self):
        if not self.env.user.has_group('details.group_sale_super_manager'):
            raise ValidationError("Sorry you can not delete")


class QuotAccommodation(models.Model):
    _name = 'accommodation.main'

    hotel = fields.Many2many('model.hotel', string='Hotel', copy=True)
    check_in = fields.Date(string="Check In")
    check_out = fields.Date(string="Check out")
    room_view = fields.Many2one('room.view', string='Room View')
    meal_plan = fields.Many2one('meal.plan', string="Meal Plan")
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotAccommodation1(models.Model):
    _name = 'accommodation.city1'
    hotel = fields.Many2many('model.hotel', string='Hotel')
    check_in = fields.Date(string="Check In")
    check_out = fields.Date(string="Check out")
    room_view = fields.Many2one('room.view', string='Room View')
    meal_plan = fields.Many2one('meal.plan', string="Meal Plan")
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotAccommodation2(models.Model):
    _name = 'accommodation.city2'
    hotel = fields.Many2many('model.hotel', string='Hotel')
    check_in = fields.Date(string="Check In")
    check_out = fields.Date(string="Check out")
    room_view = fields.Many2one('room.view', string='Room View')
    meal_plan = fields.Many2one('meal.plan', string="Meal Plan")
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotAccommodation3(models.Model):
    _name = 'accommodation.city3'
    hotel = fields.Many2many('model.hotel', string='Hotel')
    check_in = fields.Date(string="Check In")
    check_out = fields.Date(string="Check out")
    room_view = fields.Many2one('room.view', string='Room View')
    meal_plan = fields.Many2one('meal.plan', string="Meal Plan")
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotAccommodation4(models.Model):
    _name = 'accommodation.city4'
    hotel = fields.Many2many('model.hotel', string='Hotel')
    check_in = fields.Date(string="Check In")
    check_out = fields.Date(string="Check out")
    room_view = fields.Many2one('room.view', string='Room View')
    meal_plan = fields.Many2one('meal.plan', string="Meal Plan")
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotAccommodation5(models.Model):
    _name = 'accommodation.city5'
    hotel = fields.Many2many('model.hotel', string='Hotel')
    check_in = fields.Date(string="Check In")
    check_out = fields.Date(string="Check out")
    room_view = fields.Many2one('room.view', string='Room View')
    meal_plan = fields.Many2one('meal.plan', string="Meal Plan")
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotAccommodation6(models.Model):
    _name = 'accommodation.city6'
    hotel = fields.Many2many('model.hotel', string='Hotel')
    check_in = fields.Date(string="Check In")
    check_out = fields.Date(string="Check out")
    room_view = fields.Many2one('room.view', string='Room View')
    meal_plan = fields.Many2one('meal.plan', string="Meal Plan")
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class FlightInternational(models.Model):
    _name = 'quot.flight.international'
    flight_type = fields.Selection(
        [('int_grp', 'INT-GRP'), ('int_sys', 'INT-SYS'), ('without_flight', 'without flight')], store=True)

    route = fields.Selection(
        [('APR&DEP', 'APR&DEP'), ('departure_only', 'departure_only'), ('arrival_only', 'Arrival only'), ],
        default='APR&DEP', store=True)
    dept_date = fields.Datetime(string='DEP Timing')
    arr_date = fields.Datetime(string='ARR Timing')
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    dep_flight_no = fields.Char(string='DEP Flight Num')
    deb_flight_route = fields.Char(string='DEP Flight Route')
    dep_flight_timing = fields.Datetime()
    arr_flight_no = fields.Char(String='ARR Flight No')
    deptt_date = fields.Datetime(string='DEP Timing')
    arrr_date = fields.Datetime(string='ARR Timing')
    arr_flight_route = fields.Char(string='ARR Flight Route')
    arr_flight_timing = fields.Datetime()
    transit_time = fields.Integer(string='Transit Time')
    transit_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    transitt_time = fields.Integer(string='Transit Time')
    transitt_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    attachment = fields.Binary(string='Attachment')
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual')


class FlightDomestic(models.Model):
    _name = 'quot.flight.domestic'
    flight_type = fields.Selection(
        [('dom_sys', 'DOM-SYS'), ('DOM-GRP', 'DOM-GRP'), ('without_flight', 'Without Flight')],
        default='dom_sys', store=True)
    route = fields.Selection(
        [('APR&DEP', 'APR&DEP'), ('departure_only', 'departure_only'), ('arrival_only', 'Arrival only'), ],
        default='APR&DEP', store=True)
    dept_date = fields.Datetime(string='DEP Timing')
    arr_date = fields.Datetime(string='ARR Timing')
    supplier = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', 1)])
    dep_flight_no = fields.Char(string='DEP Flight Num')
    deb_flight_route = fields.Char(string='DEP Flight Route')
    dep_flight_timing = fields.Datetime()
    arr_flight_no = fields.Char(String='ARR Flight No')
    deptt_date = fields.Datetime(string='DEP Timing')
    arrr_date = fields.Datetime(string='ARR Timing')
    arr_flight_route = fields.Char(string='ARR Flight Route')
    arr_flight_timing = fields.Datetime()
    transit_time = fields.Integer(string='Transit Time')
    transit_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    transitt_time = fields.Integer(string='Transit Time')
    transitt_city = fields.Many2one('res.country', string='Transit City', readonly=False, store=True)
    attachment = fields.Binary(string='Attachment')
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual')


class QuotVisa(models.Model):
    _name = 'quot.visa'
    visa_type = fields.Selection([('embassy_client', 'Embassy - Client'), ('embassy_company', 'Embassy - Company'),
                                  ('embassy_assist_only', 'Embassy - Assist Only'),
                                  ('online_client', 'Online - Client'), ('online_company', 'Online - Company'),
                                  ('no_visa_required', 'No Visa Required'), ], default='no_visa_required',
                                 string='Visa Type & Responsibility', store=True)
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotVaccination(models.Model):
    _name = 'quot.vaccination'

    pcr_required = fields.Many2one('pcr.required', string='PCR Required')

    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class QuotProgram(models.Model):
    _name = 'quot.program'

    program_name = fields.Many2many('program.city', string='Program Name', )
    status = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='yes', store=True)
    quot_id = fields.Many2one('sale.order.template')
    individual = fields.Selection(related='quot_id.individual', )


class DocumentFix(models.Model):
    _inherit = 'ir.attachment'

    folder_id = fields.Many2one('documents.folder', track_visibility="onchange", index=True)

