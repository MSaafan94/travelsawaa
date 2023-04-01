from odoo import fields, models, api


class report_account_general_ledger_inh(models.AbstractModel):
    _name = "account.general.ledger"
    _description = "General Ledger Report"
    _inherit = "account.report"