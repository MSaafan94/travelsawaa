from odoo import fields, models, api


class Document(models.Model):
    _inherit = 'documents.folder'
    _description = 'Description'
    all = fields.Boolean(string="all users")
    users_ids = fields.Many2many('res.users',string="access users ")
