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

class stock_picking(models.Model):

    _inherit = ['stock.picking']
    ro_ref = fields.Char('Ref. RO ใบแจ้งเข้า',size=15, translate=False,
        help="Reference RO Number ใส่เลขใบแจ้งเข้าจัดซื้อ ที่มีเอกสารจัดส่งชุดนี้อยู่")
    invoice_sup_ref = fields.Char('Ref. INVOICE Supplier',size=15, translate=False,
        help="Reference Invoice Number ของ Supplier ใส่เลข invoice สำหรับเอกสารชุดนี้")
    
    dop_ref = fields.Char('Ref. DOP',size=15, translate=False,
        help="Reference DOP Number ใส่เลข DOP ที่มีเอกสารจัดส่งชุดนี้อยู่")
    invoice_ref = fields.Char('Ref. INVOICE',size=15, translate=False,
        help="Reference Invoice Number ใส่เลข invoice สำหรับเอกสารชุดนี้")
    picker_name = fields.Char('Picker Name(ชื่อคนรับสินค้าออก)',size=30, translate=True,
        help="Picker Name(ชื่อคนรับสินค้าออก) เช่น คนขับรถของเรา หรือชื่อเซลที่มาเอาของไปเอง")
    state_confirm_receive = fields.Selection([('1_estimate','A วันที่ประมาณเอง'),('2_sup_confirm','B วันผู้ขายแจ้งกลับ'),('3_sure','C วันแน่นอน(ผู้ส่งบอก)'),('5_done','D รับของแล้ว'),('4_return','X วันที่ของตีกลับ')], string="State Confirm Receive(ของเข้า)",
        help="วันที่ของเข้าแน่ใจได้แค่ไหน")  
    product_type= fields.Selection(related='product_id.type', string="Type of product")

    #tk_delivery_date = fields.Date('Plan Delivery(วันกำหนดส่ง)',
    #    required=True,                           
    #    help="กำหนดวันส่ง โดยจดจาก Delivery Order(DO) ต้องใส่เอง")
    #_columns = {
    #    'min_date':fields.date(string='Scheduled Date (วันกำหนดส่ง)', select=1, help="Scheduled time for the first part of the shipment to be processed. Setting manually a value here would set it as expected date for all the stock moves.", 
    #        track_visibility='onchange'),
    #}
class stock_incoterms(models.Model):
    # เพิ่มคำอธิบายลงไปใน incoterm ช่องนึง
    _inherit = ['stock.incoterms']
        #name = fields.Char('Name', required=True, help="Incoterms are series of sales terms. They are used to divide transaction costs and responsibilities between buyer and seller and reflect state-of-the-art transportation practices.")
        #code = fields.Char('Code', size=3, required=True, help="Incoterm Standard Code")
        #active = fields.Boolean('Active', help="By unchecking the active field, you may hide an INCOTERM you will not use.")
    explanation = fields.Char('คำอธิบาย', help="อธิบายเพิ่มเติมเพื่อเพิ่มความเข้าใจ")
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: