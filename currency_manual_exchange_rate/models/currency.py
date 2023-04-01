# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons.base.models.res_currency import Currency
import logging
_logger = logging.getLogger()

class CurrencyExt(models.Model):
    _inherit ='res.currency'
    
    @api.model_cr
    def _register_hook(self):
          
        def _convert_enhanced(self, from_amount, to_currency, company, date, round=True):
            """Returns the converted amount of ``from_amount``` from the currency
               ``self`` to the currency ``to_currency`` for the given ``date`` and
               company.
    
               :param company: The company from which we retrieve the convertion rate
               :param date: The nearest date from which we retriev the conversion rate.
               :param round: Round the result or not
            """
            self, to_currency = self or to_currency, to_currency or self
            assert self, "convert amount from unknown currency"
            assert to_currency, "convert amount to unknown currency"
            assert company, "convert amount from unknown company"
            assert date, "convert amount from unknown date"
            _logger.info('Convert ' + str(from_amount) + ' From ' + str(self.name) + ' to ' + str(to_currency.name))
            # apply conversion rate
            if self == to_currency:
                to_amount = from_amount
            else:
                conversion_rate = self._context.get('override_currency_rate', False)
                _logger.info('Override conversion rate ' + str(conversion_rate))
                if not conversion_rate:
                    conversion_rate = self._get_conversion_rate(self, to_currency, company, date)
                    
                to_amount = from_amount * conversion_rate
            # apply rounding
            _logger.info(str(to_amount) + ' Converted FROM ' + str(from_amount))
            return to_currency.round(to_amount) if round else to_amount
        
        @api.model
        def _get_conversion_rate_enhanced(self, from_currency, to_currency, company, date):
            _logger.info('Get conversion rate from ' + str(from_currency.name) + ' to ' + str(to_currency.name) + ' date ' + str(date))
            res = self._context.get('override_currency_rate', False)
            _logger.info('--Override conversion rate ' + str(res))
            if not res:
                currency_rates = (from_currency + to_currency)._get_rates(company, date)
                #_logger.info('Currency Rates are ' + str(currency_rates))
                res = currency_rates.get(to_currency.id) / currency_rates.get(from_currency.id)
            _logger.info( str(res) + ' conversion rate from ' + str(from_currency.name) + ' to ' + str(to_currency.name) + ' date ' + str(date))
            #print(what)
            return res
        
        Currency._convert = _convert_enhanced
        Currency._get_conversion_rate = _get_conversion_rate_enhanced
        return super(CurrencyExt, self)._register_hook()
