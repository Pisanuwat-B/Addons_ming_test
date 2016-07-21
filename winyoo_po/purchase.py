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
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools.float_utils import float_compare
from openerp.exceptions import ValidationError
# from openerp.osv import fields, osv

class purchase_order(models.Model):

    _inherit = ['purchase.order']
    #po_authority = fields.Char('Approve By',size=30,
    #    help="Person who can sign this document ชื่อคนเซ็นต์")
    po_authority = fields.Char('Approve By',size=30,
        help="ชื่อคนเซ็นต์",
        default="Prayoon Kongkavitool")
    #incoterm_short = fields.Char('Incoterm',size=25, translate=True, required=True,
    #    help="Incoterm ex. CIF BKK, FOB Shanghai, DDP") 
    #incoterm_short = fields.Selection([('a','DDP'),('b','CIF Bangkok'),('c','CIF'),('d','FOB'),('e','EXWORK')],string='Incoterm', required=True,
    #    help="Incoterm ex. CIF BKK, FOB Shanghai, DDP")     

    
    po_name = fields.Char('PO Number(Print)',size=25,
        help="PO Number for print to supplier เช่น GADOT07/15")
    pr_name = fields.Char('PR Number',size=25,
        help="PR Number เลขที่ PR ")
    po_type = fields.Selection([('a','For Sell'),('b','For Use')], string="PO Type",
        help="Type of PO ซื้อมาขาย หรือ ซื้อมาใช้")  

    # ----------Below are fields for logistic cost ------------- 
    #freight_cost = fields.Float('Freight Cost', digits_compute=dp.get_precision('Product Unit of Measure'), 
    #    help="ค่าขนส่งสินค้า เช่น ค่าเรือ ค่าเครื่องบิน แต่ไม่รวม" )  
    freight_cost = fields.Float('Fr: Freight Cost(THB)', digits=(12,2), 
        help="ค่าขนส่งสินค้า เช่น ค่าเรือ ค่าเครื่องบิน แต่ไม่รวมLocal Charge เช่นค่าแลก D/O")  
    local_charge = fields.Float('Fr: Local Charge(THB)', digits=(12,2), 
        help="Local Charge เก็บโดยผู้ขนส่ง เช่น D/O, Handling, THC, CFS ")
    port_charge = fields.Float('Po: Port Charge(THB)', digits=(12,2), 
        help="Port Charge เก็บโดยท่าเรือหรือท่าอากาศยาน รวมถึงผู้ขนส่งในท่า เช่น Lift on/off, Gate Charge, ค่าขนส่งในท่า")
    port_storage = fields.Float('Po: Storage Charge(THB)', digits=(12,2), 
        help="Storage & Detention Charge ค่าเก็บสินค้า และค่าคืนตู้ช้ากว่ากำหนด เป็นพวกค่าปรับ")
    shipping_charge = fields.Float('Sh: Shipping Charge(THB)', digits=(12,2), 
        help="Shipping Charge(THB) ค่าใช้จ่ายที่เก็บโดยชิปปิ้ง เป็นค่าเคลียสินค้า รวมถึงค่าเอกสารกรมศุลกากร(ใบฟ้า) ")
    transport_internal = fields.Float('Sh: Transport from Port(THB)', digits=(12,2), 
        help="Transport from Port(THB) ค่ารถกระบะ หรือรถลากที่ส่งมาโกดังเรา หรือส่งไปที่ลูกค้าโดยตรง")
    import_tax = fields.Float('Cu: Import Tax(THB)', digits=(12,2), 
        help="Import Tax(THB) ค่าภาษานำเข้า หรือ ทารีฟ")
    other_logistic = fields.Float('Ot: Other Cost(THB)', digits=(12,2), 
        help="Other Cost(THB) อื่นๆ ใช้กรณีที่ในบิลไม่ระบุว่าจ่ายใคร จริงๆช่องนี้ควรจะว่างตลอด")
    #total_logistic = fields.Float('Total Logistic Charge(THB)', digits=(12,2), 
    #    help="Total Logistic Charge(THB) ค่าใช้จ่ายทั้งหมด เอาเลขข้างบนมาบวกกัน")
    
    total_logistic = fields.Float(string="Total Logistic (THB)", 
        compute='_total_logis',
        digits=(12,2),
        default=0,
        store=True,
        help="Total Logistic Charge(THB) ค่าใช้จ่ายทั้งหมด เอาเลขข้างบนมาบวกกัน")
    
    @api.depends('freight_cost', 'local_charge','port_charge','port_storage','shipping_charge','transport_internal','import_tax','other_logistic')
    def _total_logis(self):
        for record in self:
            # compute total logistic
            self.total_logistic = self.freight_cost+self.local_charge+self.port_charge+self.port_storage+self.shipping_charge+self.transport_internal+self.import_tax+self.other_logistic
    #----------------------
    
    @api.onchange('freight_cost', 'local_charge','port_charge','port_storage','shipping_charge','transport_internal','import_tax','other_logistic')
    def _onchange_total_logistic(self):
        self.total_logistic = self.freight_cost+self.local_charge+self.port_charge+self.port_storage+self.shipping_charge+self.transport_internal+self.import_tax+self.other_logistic
    #----------------------
    shipping_company = fields.Char('Shipping Company',size=20, translate=True,
        help="Shipping company (Customs Broker) ชื่อบริษัทที่เคลียสินค้า")
    freight_company = fields.Char('Freight Company',size=20, translate=True,
        help="Freight company ชื่อบริษัทผู้ขนส่งสินค้าข้ามประเทศ")    
    #----------------------

    def action_picking_create(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids):
            picking_vals = {
                'picking_type_id': order.picking_type_id.id,
                'partner_id': order.partner_id.id,
                'date': order.date_order,
                'po_name': order.po_name,
                'origin': order.name
            }
            picking_id = self.pool.get('stock.picking').create(cr, uid, picking_vals, context=context)
            self._create_stock_moves(cr, uid, order, order.order_line, picking_id, context=context)
        return picking_id
#   ตรวจสอบการซ้ำ เลข PO แต่มันไปขัดกับ purchase_order_revision เพราะตอกด revision มันจะสร้างชื่อเดิมซ้ำ เลยไม่ยอม
#     @api.one
#     @api.constrains('po_name')
#     def _po_number(self):
#         if(self.env['purchase.order'].search([('po_name','=',self.po_name.rstrip()),('id','!=',self.id)]).name)!=False:
#             raise ValidationError("PO ซ้ำ : this PO number is already existed.")

    
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    #'name': fields.text('Description', required=True)
    name = fields.Text('Description ใต้ชื่อสินค้า', required=True)

    @api.multi
    def onchange_product_id(self, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft'):
        print "PurchaseOrderLine++++++++++++++++++++++++++++++++++++++++++++++++++++"
        res = super(PurchaseOrderLine, self).onchange_product_id(pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=date_order, fiscal_position_id=fiscal_position_id, date_planned=date_planned,
            name=name, price_unit=price_unit)
        #print "product_id: ", product_id
        #print "name before: ", name
        name = False
        if not product_id:
            return res
        product_product = self.env['product.product']
        product = product_product.browse(product_id)
        if not name or not uom_id:
            dummy =' '
            name = ' '
            print "product.description_purchase: ", product.description_purchase
            if product.description_purchase:
                name += product.description_purchase
            res['value'].update({'name': name})        
        return res
    


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: