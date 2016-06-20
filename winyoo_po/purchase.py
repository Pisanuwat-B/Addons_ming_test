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
    po_type = fields.Selection([('a','For Sell'),('b','For Use')], string="PO Type", required=True,
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


class purchase_order_line(models.Model):

    _inherit = ['purchase.order.line']
    
    #---- Change Report to have name and description separately 
    #'name': fields.text('Description', required=True)
    name = fields.Text('Description ใต้ชื่อสินค้า', required=False, default=' ')
    
    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}

        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        if not name or not uom_id:
            # The 'or not uom_id' part of the above condition can be removed in master. See commit message of the rev. introducing this line.
            # ----Winyoo fixed here----
            #dummy, name = product_product.name_get(cr, uid, product_id, context=context_partner)[0]
            dummy =' '
            name = ' '
            if product.description_purchase:
                name += product.description_purchase
            res['value'].update({'name': name})
            
        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if context.get('purchase_uom_check') and self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.datetime.now()


        supplierinfo = False
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if float_compare(min_qty , qty, precision_digits=precision) == 1: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})

        price = price_unit
        if price_unit is False or price_unit is None:
            # - determine price_unit and taxes_id
            if pricelist_id:
                date_order_str = datetime.strptime(date_order, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                price = product_pricelist.price_get(cr, uid, [pricelist_id],
                        product.id, qty or 1.0, partner_id or False, {'uom': uom_id, 'date': date_order_str})[pricelist_id]
            else:
                price = product.standard_price

        taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
        fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
        taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})

        return res    
    
    



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: