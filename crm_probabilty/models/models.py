# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmProbability(models.Model):
    _inherit = 'crm.lead'

    custom_probability = fields.Integer(compute='custom_probability_method', store=True)

    passport_check = fields.Boolean()
    professional_job_check = fields.Boolean()
    bank_account_check = fields.Boolean()
    visas_check = fields.Boolean()
    bachelor_check = fields.Boolean()

    @api.one
    @api.depends('passport_check', 'professional_job_check', 'bank_account_check', 'visas_check', 'bachelor_check')
    def custom_probability_method(self):
        if self.passport_check:
            self.custom_probability += 10
        if self.professional_job_check:
            self.custom_probability += 20
        if self.bank_account_check:
            self.custom_probability += 30
        if self.visas_check:
            self.custom_probability += 30
        if self.bachelor_check:
            self.custom_probability += 10

