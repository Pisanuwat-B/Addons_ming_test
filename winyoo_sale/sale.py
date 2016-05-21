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
    
    
    @api.multi
    def button_mycancel(self):
        ctx=dict(self._context)
        return self.with_context(ctx).write({'state':'cancel'})
 
    
    

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    _order = 'order_id asc, sequence, id'   

# แก้ให้ Description ใส่เฉพาะที่เราต้องการเพิ่ม ไม่ต้องใส่ชื่อ มาด้วย แล้วชื่อก็บังคับ เปลี่ยนไม่ได้
    name = fields.Text('Description รายละเอียดใต้ชื่อสินค้า', 
            required=False, default=' ', readonly=True, states={'draft': [('readonly', False)]},
            help="รายละเอียดใต้ชื่อสินค้าในใบเสนอราคาและใบดีโอ เช่น สินค้าน้ำมันพืชปทุม หรือ สินค้าทีโอแอล หรือ ราคาสำหรับขั้นต่ำ 100 kg")
    #'name': fields.text('Description', required=True, readonly=True, states={'draft': [('readonly', False)]}),
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name=' ', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        lang = lang or context.get('lang', False)
        if not partner_id:
            raise osv.except_osv(_('No Customer Defined!'), _('Before choosing a product,\n select a customer in the sales form.'))
        warning = False
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'lang': lang, 'partner_id': partner_id}
        partner = partner_obj.browse(cr, uid, partner_id)
        lang = partner.lang
        context_partner = {'lang': lang, 'partner_id': partner_id}

        if not product:
            return {'value': {'th_weight': 0,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        result = {}
        warning_msgs = ''
        product_obj = product_obj.browse(cr, uid, product, context=context_partner)

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False

        fpos = False
        if not fiscal_position:
            fpos = partner.property_account_position or False
        else:
            fpos = self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position)
        if update_tax: #The quantity only have changed
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)

        if not flag:
            result['name'] = ' ' #self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                result['name'] += product_obj.description_sale
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        'product_uos':
                        [('category_id', '=', uos_category_id)]}
        elif uos and not uom: # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom: # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight        # Round the quantity up

        if not uom2:
            uom2 = product_obj.uom_id
        # get unit price

        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                    'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
        else:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                    product, qty or 1.0, partner_id, {
                        'uom': uom or result.get('product_uom'),
                        'date': date_order,
                        })[pricelist]
            if price is False:
                warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
                        "You have to change either the product, the quantity or the pricelist.")

                warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
            else:
                result.update({'price_unit': price})
        if warning_msgs:
            warning = {
                       'title': _('Configuration Error!'),
                       'message' : warning_msgs
                    }
        return {'value': result, 'domain': domain, 'warning': warning} 
    
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: