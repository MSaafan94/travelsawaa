from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round, float_is_zero, pycompat
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _run_valuation(self, quantity=None):
        self.ensure_one()
        if self.purchase_line_id:
            if self.purchase_line_id.order_id.manual_currency_rate_active:
                self = self.with_context(override_currency_rate=self.purchase_line_id.order_id.manual_currency_rate)
        elif self.sale_line_id:
            if self.sale_line_id.order_id.manual_currency_rate_active:
                self = self.with_context(override_currency_rate=self.sale_line_id.order_id.manual_currency_rate)
        return super(StockMove, self)._run_valuation(quantity=quantity)
