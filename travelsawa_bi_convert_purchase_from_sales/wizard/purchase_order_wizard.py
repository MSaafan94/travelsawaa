# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class PurchaseOrderCustom(models.Model):
	_inherit = "purchase.order"
	sale_order = fields.Many2one('sale.order', 'Sale Order')
	trip_reference = fields.Many2one('sale.order.template', compute='compute_trip_reference', store=True)

	@api.one
	@api.depends('origin')
	def compute_trip_reference(self):
		if self.origin:
			res = self.env['sale.order'].search([('name', '=', self.origin)])
			if res:
				self.trip_reference = res.sale_order_template_id.id


class TripReferenceAccount(models.Model):
	_inherit = "account.invoice"
	trip_reference = fields.Many2one('sale.order.template', compute='compute_trip_reference', store=True)

	@api.one
	@api.depends('origin')
	def compute_trip_reference(self):
		if self.origin:
			res = self.env['purchase.order'].search([('name', '=', self.origin)])
			if res:
				self.trip_reference = res.trip_reference


class CreatePurchaseOrder(models.TransientModel):
	_name = 'create.purchaseorder'
	_description = "Create Purchase Order"

	new_order_line_ids = fields.One2many('getsale.orderdata', 'new_order_line_id',String="Order Line")
	partner_id = fields.Many2one('res.partner', string='Vendor', required = True)
	date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)

	
	@api.model
	def default_get(self,  default_fields):
		res = super(CreatePurchaseOrder, self).default_get(default_fields)
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		update = []
		for record in data.order_line:
			update.append((0,0,{
							'product_id': record.product_id.id,
							'product_uom': record.product_uom.id,
							'order_id': record.order_id.id,
							'name': record.name,
							'product_qty': record.product_uom_qty,
							'price_unit': record.price_unit,
							'product_subtotal': record.price_subtotal,
							}))
		res.update({'new_order_line_ids':update})
		return res

	@api.multi
	def action_create_purchase_order(self):
		self.ensure_one()
		res = self.env['purchase.order'].browse(self._context.get('id',[]))
		value = []
		pricelist = self.partner_id.property_product_pricelist
		partner_pricelist = self.partner_id.property_product_pricelist
		sale_order_name = ""
		for data in self.new_order_line_ids:
			sale_order_name = data.order_id.name
			if partner_pricelist:
				product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=data.product_uom.id)
				final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(data.product_id, data.product_qty or 1.0, self.partner_id)
			
			else:
			 	final_price = data.product_id.standard_price
			value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'taxes_id' : ([(6,0,data.product_id.supplier_taxes_id.ids)]),
								'date_planned' : str(datetime.now()),
								'price_unit' : final_price,
								}])
		res.create({
						'partner_id' : self.partner_id.id,
						'date_order' : str(self.date_order),
						'order_line':value,
						'origin' : sale_order_name,
						'partner_ref': sale_order_name,
						# 'sale_order': data.order_id.id,
						'trip_reference': data.order_id.sale_order_template_id.id,
						
					})
		
		return res


class Getsaleorderdata(models.TransientModel):
	_name = 'getsale.orderdata'
	_description = "Get Sale Order Data"

	new_order_line_id = fields.Many2one('create.purchaseorder')
		
	product_id = fields.Many2one('product.product', string="Product", required=True)
	name = fields.Char(string="Description")
	product_qty = fields.Float(string='Quantity', required=True)
	date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
	product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
	order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
	price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
	
	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit
