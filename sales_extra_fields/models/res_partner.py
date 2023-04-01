from odoo import fields, models, api, _
# from datetime import date, datetime
import datetime
from odoo.exceptions import UserError
import logging
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    service_type = fields.Many2one('service.type', "Service Type")
    whatsapp_num = fields.Char("WhatsApp Number")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default="male")
    birthday = fields.Date("Birthday", track_visibility="always")
    years = fields.Integer("Years", compute='_check_employee_age', store=True)
    months = fields.Integer("Months", compute='_check_employee_age', store=True)
    days = fields.Integer("Days", compute='_check_employee_age', store=True)
    age_type = fields.Selection([('infant', 'Infant'),
                                 ('child', 'Child'),
                                 ('adult', 'Adult')], string="Age Type", compute='_check_employee_age', store=True)
    email = fields.Char("Email")
    trip_code = fields.Char("Trip Code")
    passport_num = fields.Char("Passport Number")
    passport_expiry = fields.Date("Passport Expiry Date")
    lead_source = fields.Many2one("utm.source", required=False)
    id_number = fields.Char("ID Number")
    destination_1 = fields.Many2one('destination', "Destination 1")
    booking_status = fields.Many2one('booking.status', "Booking Status")
    Description = fields.Text("Description")
    owner = fields.Char("Owner")
    created_at = fields.Datetime("Created at")
    old_data = fields.Boolean("Old Data")
    previous_trips = fields.Char("Previous Trips")
    amount = fields.Float("Amount")
    points_of_loyalty = fields.Float("Points of Loyalty")
    relation = fields.Selection([('father', 'Father'),
                                 ('mother', 'Mother'),
                                 ('son', 'Son'),
                                 ('daughter', 'Daughter'),
                                 ('husband', 'Husband'),
                                 ('wife', 'Wife'),
                                 ('brother', 'Brother'),
                                 ('sister', 'Sister'),
                                 ('grandfather', 'Grandfather'),
                                 ('grandmother', 'Grandmother'),
                                 ('uncle', 'Uncle'),
                                 ('aunt', 'Aunt'),
                                 ('cousin', 'Cousin'),
                                 ('friend', 'Friend')], string="Relationship")

    user_id = fields.Many2one('res.users', string='Salesperson',
                              help='The internal user in charge of this contact.', required=True,
                              default=lambda self: self.env.user)

    def open_whatsapp_web(self):
        if len(self.whatsapp_num) <= 11:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://web.whatsapp.com/send/?phone=+2{}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))
        else:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://web.whatsapp.com/send/?phone={}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))

    def open_whatsapp_mobile(self):
        if len(self.whatsapp_num) <= 11:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://api.whatsapp.com/send/?phone=+2{}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))
        else:
            if self.whatsapp_num:
                return {
                    "type": 'ir.actions.act_url',
                    "url": 'https://api.whatsapp.com/send/?phone={}'.format(self.whatsapp_num),
                    "target": 'new'
                }
            else:
                raise ValidationError("Please Provide Contact number for {}".format(self.partner_id))

    # @api.multi
    # @api.onchange('whatsapp_num')
    # def _check_whats(self):
    #     logging.info("Change whatsapp_num++++")
    #     partners = self.env['res.partner'].search([])
    #     for partner in partners:
    #         if self.whatsapp_num:
    #             if self.whatsapp_num == partner.whatsapp_num or len(self.whatsapp_num) < 11:
    #                 raise UserError("whatsapp_num number is already in used.")

    # @api.multi
    # @api.onchange('phone')
    # def _check_phone(self):
    #     logging.info("Chane phone++++++++++")
    #     partners = self.env['res.partner'].search([])
    #     for partner in partners:
    #         if self.phone:
    #             if self.phone == partner.phone:
    #                 raise UserError("Phone number is already in used.")

    # @api.multi
    # @api.onchange('mobile')
    # def _check_mobile(self):
    #     logging.info("Change mobile++++++++++")
    #     partners = self.env['res.partner'].search([])
    #     for partner in partners:
    #         if self.mobile:
    #             if self.mobile == partner.mobile or len(self.mobile) < 11:
    #                 raise UserError("Mobile number is already in used.")

    def get_transfer_wizard(self):
        ctx = self.env.context
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer Sales Person',
            'res_model': 'transfer.salesperson',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('sales_extra_fields.transfer_salesperson_view_form', False).id,
            'target': 'new',
            'context': ctx
        }

    @api.depends('birthday')
    def _check_employee_age(self):
        for rec in self:
            if rec.birthday:
                total_days = datetime.date.today() - rec.birthday
                years = abs(total_days.days / 365)
                remaining_days = total_days.days % 365
                if remaining_days >= 30:
                    months = abs(remaining_days / 30)
                else:
                    months = 0
                if (remaining_days % 30) < 30:
                    days = (remaining_days % 30)
                else:
                    days = 0
                rec.years = years
                rec.months = months
                rec.days = days
                if 0 <= years < 2:
                    rec.age_type = 'infant'
                elif 2 <= years < 12:
                    rec.age_type = 'child'
                else:
                    rec.age_type = 'adult'


class ResPartnerWizard(models.TransientModel):
    _name = "res.partner.wizard"

    contact_type = fields.Selection([
        ('New', 'Create New Contact'),
        ('Existing', 'Add Existing Contact')
    ], default="Existing", string="Type")

    relation = fields.Selection([('father', 'Father'),
                                 ('mother', 'Mother'),
                                 ('son', 'Son'),
                                 ('friend', 'Friend'),
                                 ('daughter', 'Daughter'),
                                 ('husband', 'Husband'),
                                 ('wife', 'Wife'),
                                 ('brother', 'Brother'),
                                 ('sister', 'Sister'),
                                 ('grandfather', 'Grandfather'),
                                 ('grandmother', 'Grandmother'),
                                 ('uncle', 'Uncle'),
                                 ('aunt', 'Aunt'),
                                 ('cousin', 'Cousin')], string="Relationship")
    contact = fields.Many2one('res.partner', string="Contact Name", domain="[('parent_id','=',False)]")
    contact_name = fields.Char(string="Contact Name")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")
    birthday = fields.Date("Birthday")
    years = fields.Integer("Years", compute='_check_employee_age', store=True)
    months = fields.Integer("Months", compute='_check_employee_age', store=True)
    days = fields.Integer("Days", compute='_check_employee_age', store=True)
    age_type = fields.Selection([('infant', 'Infant'),
                                 ('child', 'Child'),
                                 ('adult', 'Adult')], string="Age Type", compute='_check_employee_age', store=True)

    lead_source = fields.Many2one("utm.source")
    service_type = fields.Many2one('service.type', "Service Type")
    whatsapp_num = fields.Char("WhatsApp Number")
    destination_1 = fields.Many2one('destination', "Destination 1")

    @api.onchange('contact')
    def change_values(self):
        self.mobile = self.contact.mobile
        self.phone = self.contact.phone
        self.birthday = self.contact.birthday
        self.lead_source = self.contact.lead_source
        self.service_type = self.contact.service_type
        self.whatsapp_num = self.contact.whatsapp_num
        self.destination_1 = self.contact.destination_1

    @api.depends('birthday')
    def _check_employee_age(self):
        for rec in self:
            if rec.birthday:

                total_days = datetime.date.today() - rec.birthday
                years = abs(total_days.days / 365)
                remaining_days = total_days.days % 365
                if remaining_days >= 30:
                    months = abs(remaining_days / 30)
                else:
                    months = 0
                if (remaining_days % 30) < 30:
                    days = (remaining_days % 30)
                else:
                    days = 0
                rec.years = years
                rec.months = months
                rec.days = days
                if 0 <= years < 2:
                    rec.age_type = 'infant'
                elif 2 <= years < 12:
                    rec.age_type = 'child'
                else:
                    rec.age_type = 'adult'

    def add_contact(self):
        if self.contact:
            self.contact.mobile = self.mobile
            self.contact.phone = self.phone
            self.contact.birthday = self.birthday
            self.contact.lead_source = self.lead_source
            self.contact.service_type = self.service_type
            self.contact.whatsapp_num = self.whatsapp_num
            self.contact.destination_1 = self.destination_1
            self.contact.parent_id = self._context.get('active_id')

        elif not self.contact and self.contact_type == 'Existing':
            raise UserError('Fill the contact')

        else:
            partner = self.env['res.partner'].create({
                'name': self.contact_name,
                'mobile': self.mobile,
                'phone': self.phone,
                'birthday': self.birthday,
                'years': self.years,
                'months': self.months,
                'days': self.days,
                'age_type': self.age_type,
                'lead_source': self.lead_source.id,
                'service_type': self.service_type.id,
                'whatsapp_num': self.whatsapp_num,
                'destination_1': self.destination_1.id,
                'parent_id': self._context.get('active_id')
            })

    def create_contact(self):
        context = dict({})
        context['default_parent_id'] = self._context.get('active_id')
        logging.info("parent_id_________________")
        logging.info(context['default_parent_id'])
        return {
            'name': _('Contact'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.partner',
            'view_id': self.env.ref('base.view_partner_form').id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new'
        }
