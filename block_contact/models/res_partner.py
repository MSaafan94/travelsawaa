from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    x_block_user = fields.Selection([('False', 'Not Blocked'),('True', 'Blocked')], default = "False", required = "True", string = 'Block User', track_visibility='always')
