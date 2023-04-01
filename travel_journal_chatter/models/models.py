# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TravelJournalChatter(models.Model):
    # _inherit = 'account.move'['']
    # _name = 'travel_journal_chatter.travel_journal_chatter'

    _name = 'account.move'
    _inherit = ['mail.thread', 'account.move']

    name = fields.Char(string='Number', required=True, copy=False, default='/', track_visibility="always")
    ref = fields.Char(string='Reference', copy=False)
    date = fields.Date(required=True, states={'posted': [('readonly', True)]}, index=True,
                       default=fields.Date.context_today, track_visibility="always")
    currency_id = fields.Many2one('res.currency', compute='_compute_currency', store=True, string="Currency", track_visibility="always")
    state = fields.Selection([('draft', 'Unposted'), ('posted', 'Posted')], string='Status',
                             required=True, readonly=True, copy=False, default='draft',
                             help='All manually created new journal entries are usually in the status \'Unposted\', '
                                  'but you can set the option to skip that status on the related journal. '
                                  'In that case, they will behave as journal entries automatically created by the '
                                  'system on document validation (invoices, bank statements...) and will be created '
                                  'in \'Posted\' status.', track_visibility="onchange")
    line_ids = fields.One2many('account.move.line', 'move_id', string='Journal Items',
                               states={'posted': [('readonly', True)]}, copy=True, track_visibility="always")
    partner_id = fields.Many2one('res.partner', compute='_compute_partner_id', string="Partner", store=True,
                                 readonly=True, track_visibility="always")
    amount = fields.Monetary(compute='_amount_compute', store=True, track_visibility="always")
    narration = fields.Text(string='Internal Note', track_visibility="always")
    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', store=True,
                                 readonly=True, track_visibility="always")
    matched_percentage = fields.Float('Percentage Matched', compute='_compute_matched_percentage', digits=0, store=True,
                                      readonly=True, help="Technical field used in cash basis method", track_visibility="always")
    # Dummy Account field to search on account.move by account_id
    dummy_account_id = fields.Many2one('account.account', related='line_ids.account_id', string='Account', store=False,
                                       readonly=True, track_visibility="always")
    tax_cash_basis_rec_id = fields.Many2one(
        'account.partial.reconcile',
        string='Tax Cash Basis Entry of',
        help="Technical field used to keep track of the tax cash basis reconciliation. "
             "This is needed when cancelling the source: it will post the inverse journal entry to cancel that part too.", track_visibility="always")
    auto_reverse = fields.Boolean(string='Reverse Automatically', default=False,
                                  help='If this checkbox is ticked, this entry will be automatically reversed at the reversal date you defined.', track_visibility="always")
    reverse_date = fields.Date(string='Reversal Date', help='Date of the reverse accounting entry.')
    reverse_entry_id = fields.Many2one('account.move', String="Reverse entry", store=True, readonly=True, copy=False)
    tax_type_domain = fields.Char(store=False, help='Technical field used to have a dynamic taxes domain on the form view.')



