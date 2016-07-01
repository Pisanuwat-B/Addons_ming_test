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
from docutils.parsers import null

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    is_lead = fields.Boolean('ผู้สนใจ(ยังไม่เป็นลูกค้า)', help="สำหรับคนที่ยังไม่เป็นลูกค้าเรา แต่อยากจะขอ Quotation")
    email_print = fields.Char('Email Print')
    supplier_type = fields.Selection([('a','ขายสินค้าสร้างรายได้'),('b','ขายสินค้าเบ็ดเตล็ดหรือบริการ')], 
        string="Supplier Type",
        help="Type of Supplier ขายสินค้าสร้างรายได้ หรือ ขายสินค้าเบ็ดเตล็ดหรือบริการ")  
    
    # ถ้าไปใส่ คำสั่ง onchange= ในหน้า view ตัว onchange ตัวนี้จะไม่ทำงาน 
    @api.onchange('is_lead')
    def onchange_is_lead(self):
        is_lead=self.is_lead
        if is_lead==True:
            #self.is_company=False
            self.supplier=False
            self.parent_id=None
            
    @api.onchange('supplier')
    def onchange_supplier(self):
        supplier=self.supplier
        #print "supplier: ", supplier
        #print "self: ", self
        #print "self.fields_get(): ", self.fields_get()
        
        
        if supplier==True:
            #print "1user_id: ", self.user_id
            self.user_id=None
            #print "2user_id: ", self.user_id
            self.is_lead=False
            self.customer=False
        if supplier==False:
            self.supplier_type=None
            self.customer=True
    
    @api.onchange('customer')
    def onchange_customer(self):
        customer=self.customer
        if customer==True:
            self.supplier_type=None
            self.supplier=False
        if customer==False:
            self.supplier=True
        #else:
        #    self.city="is_leaseFalse"
    #@api.onchange('user_id')
    #def onchange_salesperson_name(self):
    #    is_lead=self.is_lead
    #    if self.user_id in :
    #        self.is_company=False
    #        self.parent_id=null
    #        self.city="not in salesco"
    #    else:
    #        self.city="is salesco"
        #groups="base.group_no_one"
#แก้ไข name_get เพื่อให้ดึงชื่อ Saleขึ้นมาด้วยตามหลังชื่อลูกค้า
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.parent_id and not record.is_company:
                name = "%s, %s" % (record.parent_name, name)
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, without_company=True, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            name = name.replace('\n\n','\n') #ถ้ามีขึ้นบันทัดใหม่ สองครั้ง ให้ขึ้นแค่ครั้งเดียว
            name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            if record.user_id:
                name = "%s, %s" % (name,record.user_id.partner_id.name or '')
            else:
                name = "%s,-" %(name)
            res.append((record.id, name))
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: