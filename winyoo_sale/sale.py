# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tinnakorn Group
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# from filename import classname # in my folder
# from ubuntu_library import classname or filename # in ubuntu
# from module import filename or classname #in odoo

from openerp import models, fields, api #import file "model.py", "fields.py", "api.py"  from folder openerp
from dateutil.relativedelta import relativedelta
from datetime import datetime

class sale_order(models.Model):

    _inherit='sale.order' #know Object in Form  #_inherit fix the existing class in the system.
    
    credit_term_id = fields.Many2one('account.payment.term', string='Credit Term',required=False)
    sale_authority = fields.Char('Approve By',size=30,
        help="ชื่อคนเซ็นต์",
        default="Prayoon Kongkavitool")
    #po_type = fields.Selection([('a','For Sell'),('b','For Use')], string="PO Type", required=True,
    #    help="Type of PO ซื้อมาขาย หรือ ซื้อมาใช้")
    
    #Quotation only
    price_valid = fields.Char('Price Validity',size=20, translate=True,
        help="Price valid for ... days or until x/x/20xx กำหนดยืนราคา")
    min_q_delivery = fields.Char('Minimum quantity',size=20, translate=True,
        help="ปริมาณการส่งมอบต่อเที่ยว")
    leadtime_delivery = fields.Char('Lead time',size=30, translate=True,
        help="ระยะเวลาการส่งมอบ")
    place_delivery = fields.Char('Delivery Place',size=25, translate=True,
        help="สถานที่ส่งสินค้าที่ กรณีที่มีที่จัดส่งหลายที่ หรือ ไม่ตรงกับสถานที่ออกบิล")
    #################
    
    _defaults={
               #'date_delivery':(datetime.now()+relativedelta(months=1)).strftime('%Y-%m-%d'),
               }
    _order = 'date_order desc, id desc'

    @api.multi
    def button_mysent(self):
        ctx=dict(self._context)
        return self.with_context(ctx).write({'state':'sent'})
    
#     @api.multi
#     def button_mycancel(self):
#         ctx=dict(self._context)
#         return self.with_context(ctx).write({'state':'cancel'})
    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _order = 'order_id asc, sequence, id'   
  
    name = fields.Text('Description รายละเอียดใต้ชื่อสินค้า', 
            required=True, default=' ', readonly=True, states={'draft': [('readonly', False)]},
            help="รายละเอียดใต้ชื่อสินค้าในใบเสนอราคาและใบดีโอ เช่น สินค้าน้ำมันพืชปทุม หรือ สินค้าทีโอแอล หรือ ราคาสำหรับขั้นต่ำ 100 kg")
    #'name': fields.text('Description', required=True, readonly=True, states={'draft': [('readonly', False)]}),
    print "1SaleOrderLine++++++++++++++++++++++++++++++++++++++++++++++++++++"       
    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0,
            uos=False, name='', partner_id=False, lang=False,
            update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False
    ):
        res = super(SaleOrderLine, self).product_id_change(
            pricelist=pricelist, product=product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name,
            partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        print "2SaleOrderLine+++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "name: ", name
        print "product: ", product
        if product:
            product_obj = self.env['product.product']
            product = product_obj.browse(product)
            #name =' '
            print "product2: ", product
            print "product.description_sale", product.description_sale
            if 'value' not in res:
                res['value'] = {}
            if product.description_sale:
                res['value']['name'] = product.description_sale
            if not product.description_sale:    
               res['value']['name'] = ' '             
        return res

    
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: