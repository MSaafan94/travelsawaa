from odoo import models, fields, api, _
from datetime import datetime


class SaleOrrder(models.Model):
    _inherit = "sale.order"
    due_date = fields.Date()


    @api.multi
    @api.onchange('sale_order_template_id')
    def change_individual_value(self):
        self.individual = self.sale_order_template_id.individual

    @api.multi
    @api.onchange('sale_order_template_id')
    def get_sale_order_accommodation(self):
        sales_accommodation = [(5, 0, 0,)]
        if self.partner_id:
            meal_plan = self.sale_order_template_id.quot_accommodation.meal_plan.id
            room_view = self.sale_order_template_id.quot_accommodation.room_view.id
            sales_accommodation.append((0, 0, {
                'partner_id': self.partner_id.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation.hotel
            }))

        for rec in self.name_of_persons:
            sales_accommodation.append((0, 0, {
                'partner_id': rec.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation.hotel
            }))

        self.sale_order_accommodation = sales_accommodation

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_accommodation1(self):
        sales_accommodation = [(5, 0, 0,)]
        if self.partner_id:
            meal_plan = self.sale_order_template_id.quot_accommodation1.meal_plan.id
            room_view = self.sale_order_template_id.quot_accommodation1.room_view.id
            sales_accommodation.append((0, 0, {
                'partner_id': self.partner_id.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation1.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation1.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation1.hotel
            }))
        for rec in self.name_of_persons:
            sales_accommodation.append((0, 0, {
                'partner_id': rec.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation1.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation1.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation1.hotel

            }))
        self.sale_order_accommodation1 = sales_accommodation

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_accommodation2(self):
        sales_accommodation = [(5, 0, 0,)]
        if self.partner_id:
            meal_plan = self.sale_order_template_id.quot_accommodation2.meal_plan.id
            room_view = self.sale_order_template_id.quot_accommodation2.room_view.id
            sales_accommodation.append((0, 0, {
                'partner_id': self.partner_id.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation2.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation2.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation2.hotel

            }))

        for rec in self.name_of_persons:
            sales_accommodation.append((0, 0, {
                'partner_id': rec.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation2.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation2.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation2.hotel

            }))
        self.sale_order_accommodation2 = sales_accommodation

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_accommodation3(self):
        sales_accommodation = [(5, 0, 0,)]
        if self.partner_id:
            meal_plan = self.sale_order_template_id.quot_accommodation3.meal_plan.id
            room_view = self.sale_order_template_id.quot_accommodation3.room_view.id
            sales_accommodation.append((0, 0, {
                'partner_id': self.partner_id.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation3.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation3.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation3.hotel

            }))

        for rec in self.name_of_persons:
            sales_accommodation.append((0, 0, {
                'partner_id': rec.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation3.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation3.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation3.hotel

            }))

        self.sale_order_accommodation3 = sales_accommodation

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_accommodation4(self):
        sales_accommodation = [(5, 0, 0,)]
        if self.partner_id:
            meal_plan = self.sale_order_template_id.quot_accommodation4.meal_plan.id
            room_view = self.sale_order_template_id.quot_accommodation4.room_view.id
            sales_accommodation.append((0, 0, {
                'partner_id': self.partner_id.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation4.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation4.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation4.hotel

            }))

        for rec in self.name_of_persons:
            sales_accommodation.append((0, 0, {
                'partner_id': rec.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation4.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation4.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation4.hotel

            }))

        self.sale_order_accommodation4 = sales_accommodation

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_accommodation5(self):
        sales_accommodation = [(5, 0, 0,)]
        if self.partner_id:
            meal_plan = self.sale_order_template_id.quot_accommodation5.meal_plan.id
            room_view = self.sale_order_template_id.quot_accommodation5.room_view.id
            sales_accommodation.append((0, 0, {
                'partner_id': self.partner_id.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation5.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation5.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation5.hotel

            }))

        for rec in self.name_of_persons:
            sales_accommodation.append((0, 0, {
                'partner_id': rec.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation5.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation5.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation5.hotel

            }))
        self.sale_order_accommodation5 = sales_accommodation

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_accommodation6(self):
        sales_accommodation = [(5, 0, 0,)]
        if self.partner_id:
            meal_plan = self.sale_order_template_id.quot_accommodation6.meal_plan.id
            room_view = self.sale_order_template_id.quot_accommodation6.room_view.id
            sales_accommodation.append((0, 0, {
                'partner_id': self.partner_id.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation6.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation6.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation6.hotel

            }))

        for rec in self.name_of_persons:
            sales_accommodation.append((0, 0, {
                'partner_id': rec.id,
                'check_in_date': self.sale_order_template_id.quot_accommodation6.check_in,
                'check_out_date': self.sale_order_template_id.quot_accommodation6.check_out,
                'room_view': self.env['room.view'].search([('id', '=', room_view)], limit=1),
                'meal_plan': self.env['meal.plan'].search([('id', '=', meal_plan)], limit=1),
                'hotel_name': self.sale_order_template_id.quot_accommodation6.hotel

            }))
        self.sale_order_accommodation6 = sales_accommodation

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_visa(self):
        sales_visa = [(5, 0, 0,)]
        if self.partner_id:
            sales_visa.append((0, 0, {
                'partner_id': self.partner_id.id,
                'visa_type': self.sale_order_template_id.visa.visa_type
            }))

        for rec in self.name_of_persons:
            sales_visa.append((0, 0, {
                'partner_id': rec.id,
                'visa_type': self.sale_order_template_id.visa.visa_type
            }))

        self.sale_order_visa = sales_visa

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_vaccination(self):
        sales_vaccination = [(5, 0, 0,)]
        pcr_required = self.sale_order_template_id.vaccination.pcr_required.id
        if self.partner_id:
            sales_vaccination.append((0, 0, {
                'partner_id': self.partner_id.id,
                'pcr_required': self.env['pcr.required'].search([('id', '=', pcr_required)], limit=1),
            }))

        for rec in self.name_of_persons:
            sales_vaccination.append((0, 0, {
                'partner_id': rec.id,
                'pcr_required': self.env['pcr.required'].search([('id', '=', pcr_required)], limit=1),
            }))
        self.sale_order_vaccination = sales_vaccination

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_program(self):
        sales_program = [(5, 0, 0,)]
        program = self.sale_order_template_id.program.program_name
        status = self.sale_order_template_id.program.status

        if self.partner_id:
            sales_program.append((0, 0, {
                'partner_id': self.partner_id.id,
                'status': status,
                'program_name': program

            }))

        for rec in self.name_of_persons:
            sales_program.append((0, 0, {
                'partner_id': rec.id,
                'status': status,
                'program_name': program
            }))
        self.sale_order_program = sales_program

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_flight_int(self):
        sales_flight = [(5, 0, 0,)]
        flight_type = self.sale_order_template_id.flight_international.flight_type
        route = self.sale_order_template_id.flight_international.route
        supplier = self.sale_order_template_id.flight_international.supplier
        dep_flight_no = self.sale_order_template_id.flight_international.dep_flight_no
        dept_date = self.sale_order_template_id.flight_international.dept_date
        arr_date = self.sale_order_template_id.flight_international.arr_date
        deb_flight_route = self.sale_order_template_id.flight_international.deb_flight_route
        dep_flight_timing = self.sale_order_template_id.flight_international.dep_flight_timing
        arr_flight_no = self.sale_order_template_id.flight_international.arr_flight_no
        deptt_date = self.sale_order_template_id.flight_international.deptt_date
        arrr_date = self.sale_order_template_id.flight_international.arrr_date
        arr_flight_route = self.sale_order_template_id.flight_international.arr_flight_route
        arr_flight_timing = self.sale_order_template_id.flight_international.arr_flight_timing
        transit_time = self.sale_order_template_id.flight_international.transit_time
        transit_city = self.sale_order_template_id.flight_international.transit_city
        transitt_time = self.sale_order_template_id.flight_international.transitt_time
        transitt_city = self.sale_order_template_id.flight_international.transitt_city
        attachment = self.sale_order_template_id.flight_international.attachment

        if self.partner_id:
            sales_flight.append((0, 0, {
                'partner_id': self.partner_id.id,
                'route': route,
                'dept_date': dept_date,
                'arr_date': arr_date,
                'flight_type': flight_type,
                "supplier": supplier,
                "dep_flight_no": dep_flight_no,
                "deb_flight_route": deb_flight_route,
                "dep_flight_timing": dep_flight_timing,
                "arr_flight_no": arr_flight_no,
                "deptt_date": deptt_date,
                "arrr_date": arrr_date,
                "arr_flight_route": arr_flight_route,
                "arr_flight_timing": arr_flight_timing,
                "transit_time": transit_time,
                "transit_city": transit_city,
                "transitt_time": transitt_time,
                "transitt_city": transitt_city,
                "attachment": attachment,
            }))
        for rec in self.name_of_persons:
            sales_flight.append((0, 0, {
                'partner_id': rec.id,
                'route': route,
                'dept_date': dept_date,
                'arr_date': arr_date,
                'flight_type': flight_type,
                "supplier": supplier,
                "dep_flight_no": dep_flight_no,
                "deb_flight_route": deb_flight_route,
                "dep_flight_timing": dep_flight_timing,
                "arr_flight_no": arr_flight_no,
                "deptt_date": deptt_date,
                "arrr_date": arrr_date,
                "arr_flight_route": arr_flight_route,
                "arr_flight_timing": arr_flight_timing,
                "transit_time": transit_time,
                "transit_city": transit_city,
                "transitt_time": transitt_time,
                "transitt_city": transitt_city,
                "attachment": attachment,
            }))
        self.sale_order_flight_int = sales_flight

    @api.multi
    @api.onchange('sale_order_template_id',)
    def get_sale_order_flight_dom(self):
        sales_flight = [(5, 0, 0,)]
        flight_type = self.sale_order_template_id.flight_domestic.flight_type
        route = self.sale_order_template_id.flight_domestic.route
        supplier = self.sale_order_template_id.flight_domestic.supplier
        dep_flight_no = self.sale_order_template_id.flight_domestic.dep_flight_no
        dept_date = self.sale_order_template_id.flight_domestic.dept_date
        arr_date = self.sale_order_template_id.flight_domestic.arr_date
        deb_flight_route = self.sale_order_template_id.flight_domestic.deb_flight_route
        dep_flight_timing = self.sale_order_template_id.flight_domestic.dep_flight_timing
        arr_flight_no = self.sale_order_template_id.flight_domestic.arr_flight_no
        deptt_date = self.sale_order_template_id.flight_domestic.deptt_date
        arrr_date = self.sale_order_template_id.flight_domestic.arrr_date
        arr_flight_route = self.sale_order_template_id.flight_domestic.arr_flight_route
        arr_flight_timing = self.sale_order_template_id.flight_domestic.arr_flight_timing
        transit_time = self.sale_order_template_id.flight_domestic.transit_time
        transit_city = self.sale_order_template_id.flight_domestic.transit_city
        transitt_time = self.sale_order_template_id.flight_domestic.transitt_time
        transitt_city = self.sale_order_template_id.flight_domestic.transitt_city
        attachment = self.sale_order_template_id.flight_domestic.attachment

        if self.partner_id:
            sales_flight.append((0, 0, {
                'partner_id': self.partner_id.id,
                'route': route,
                'dept_date': dept_date,
                'arr_date': arr_date,
                'flight_type': flight_type,
                "supplier": supplier,
                "dep_flight_no": dep_flight_no,
                "deb_flight_route": deb_flight_route,
                "dep_flight_timing": dep_flight_timing,
                "arr_flight_no": arr_flight_no,
                "deptt_date": deptt_date,
                "arrr_date": arrr_date,
                "arr_flight_route": arr_flight_route,
                "arr_flight_timing": arr_flight_timing,
                "transit_time": transit_time,
                "transit_city": transit_city,
                "transitt_time": transitt_time,
                "transitt_city": transitt_city,
                "attachment": attachment,
            }))
        #
        for rec in self.name_of_persons:
            sales_flight.append((0, 0, {
                'partner_id': rec.id,
                'route': route,
                'dept_date': dept_date,
                'arr_date': arr_date,
                'flight_type': flight_type,
                "supplier": supplier,
                "dep_flight_no": dep_flight_no,
                "deb_flight_route": deb_flight_route,
                "dep_flight_timing": dep_flight_timing,
                "arr_flight_no": arr_flight_no,
                "deptt_date": deptt_date,
                "arrr_date": arrr_date,
                "arr_flight_route": arr_flight_route,
                "arr_flight_timing": arr_flight_timing,
                "transit_time": transit_time,
                "transit_city": transit_city,
                "transitt_time": transitt_time,
                "transitt_city": transitt_city,
                "attachment": attachment,
            }))
        self.sale_order_flight_dom = sales_flight
