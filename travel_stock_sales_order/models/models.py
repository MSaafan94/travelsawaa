# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class stock_on_hand(models.Model):
    _inherit = 'sale.order.line'
    
    qty_availablee = fields.Float(string='in stock', compute='_get_qty_available')
    vir_available = fields.Float(string='after reserved ', compute='_get_vir_available')
    reserved = fields.Float(string='reserved ', compute='_reserved')

    @api.depends('product_id', 'vir_available')
    def _reserved(self):
        for rec in self:
            rec.reserved = rec.qty_availablee - rec.vir_available

    @api.depends('product_id')
    def _get_qty_available(self):
        qty_line_obj = self.env['product.template']
        for rec in self:       
            qty_available_obj = qty_line_obj.search([['name', '=', rec.product_id.name]])
            print(qty_available_obj.qty_available)
            rec.qty_availablee = qty_available_obj.qty_available

    @api.depends('product_id', 'product_uom_qty')
    def _get_vir_available(self):
        vir_line_obj = self.env['product.template']
        for rec in self:
            vir_available_obj = vir_line_obj.search([['name', '=', rec.product_id.name]])
            rec.vir_available = vir_available_obj.virtual_available

    
    

