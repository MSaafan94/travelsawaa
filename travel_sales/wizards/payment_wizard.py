from odoo import fields, models, api


class PaymentWizards(models.TransientModel):
    _name = 'payment.wizard'
    _description = 'Description'

    journal_id = fields.Many2one('account.journal', "Journal", required=True, domain=[('type', 'in', ('bank', 'cash'))])
    amount = fields.Monetary(string='Payment Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    date = fields.Date(default=lambda self: fields.Date.today())
    split = fields.Boolean(default=False)
    journal_entry = fields.One2many('split.journal', 'journal_entry',)
    # so = fields.Many2one('sale.order')

    def confirm_payment(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        sale_id = self.env['sale.order'].browse(docs).id
        sale_id.create_payment(self.journal_id.id, self.amount, self.date,)

    def confirm_refund(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        sale_id = self.env['sale.order'].browse(docs).id
        sale_id.create_refund(self.journal_id.id, self.amount, self.date,)


class SplitJournal(models.TransientModel):
    _name = 'split.journal'
    journal_entry = fields.Many2one('payment.wizard')
    amount = fields.Float()
    partner = fields.Many2one('res.partner')
    so = fields.Many2one('sale.order')