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
from openerp.tools.float_utils import float_round
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta

class product_template(models.Model):
    _inherit = 'product.template'
    #name = fields.Char('Nameจัดซื้อและบัญชี', required=True, translate=True, select=True)
    print_name = fields.Char('Print Name',size=60,
        #required=False,
        help="ชื่อที่ใช้ print ในใบเสนอราคาและ DO")
    #ดึงตัว uom_id มาเพือเปลี่ยนค่า default
    buy_from = fields.Selection([("a","สินค้าซื้อจากต่างประเทศ"),
                                 ("b","สินค้าซื้อจากในประเทศ"),
                                 ("a_and_b","สินค้าซื้อได้จากในและต่างประเทศ")])        

    package = fields.Char('Package Size',size=20, translate=True,
        help="The size and package ขนาดและชนิดของบรรจุภัณฑ์ เช่น 25 kg/bag")
    pack = fields.Char('ชนิดบรรจุภัณฑ์ (Package)',size=10, translate=True,
        help="package ชนิดของบรรจุภัณฑ์ เช่น drum, bag")
    nperpack = fields.Float('จำนวนขนาด (Quantity per pack)',digits=(8,3),
        help="จำนวนเท่าของหน่วยขายต่อขนาดที่ขาย  เช่น สินค้าถุง25kg ถ้าราคาเป็นต่อ kg ขนาดคือ 25  ถ้าราคาเป็นต่อถุง ขนาดคือ 1")
    origin_country = fields.Char('ประเทศผู้ผลิต (Country of Origin)',size=20,
        help="The country of origin, ประเทศที่ผลิต")
    manu_short = fields.Char('ชื่อย่อผู้ผลิต (Manufacturing)',size=20,
        help="Supplier ShortName ชื่อผู้ผลิต สั้นๆ ไม่ใช่ผู้ชาย")
    #_order = 'manu_short desc, name asc'
    receive_warning = fields.Text('ข้อระวังรับสินค้า (Receive Warning)',
        help='ใส่ข้อระวังในขณะรับสินค้า เช่น สินค้าเป็นกรด สินค้าห้ามกระแทก')
    deliver_warning = fields.Text('ข้อระวังส่งสินค้า (Deliver Warning)',
        help='แสดงผลที่ DOP ใส่ข้อระวังและการเตรียมส่งสินค้า เช่น ต้องเคาะดูว่าแข็งไหม ต้องติดสติกเกอร์ก่อนส่ง')
        
    @api.onchange('type')
    def onchange_typetrack(self):
        type=self.type
        if type=="product":
            self.track_all=True
        if type=="consu":
            self.track_all=False
        if type=="service":
            self.track_all=False             

class product_product(models.Model):

    _inherit = 'product.product'
    

    
    @api.one
    @api.depends('qty_available', 'nperpack')
    def _compute_available(self):
        if self.qty_available and self.nperpack:
            self.qty_available2 = self.qty_available / self.nperpack
        else:
            self.qty_available2 = 0.0

    qty_available2 = fields.Float(string='Packing On Hand', digits=(8,3),
        readonly=True, compute='_compute_available',)

    @api.one
    @api.depends()
    def _compute_usage_quarter(self):
        self.qty_usage_quarter = 0.0
        self.qty_available_quarter = 0.0
        self.qty_forcast_quarter = 0.0
        product_obj = self.env['product.product']
        domain_quant = []
        domain_move_out = []
        last_quarter = timedelta(days=-90)
        date_from = datetime.now() + last_quarter
        from_date = '%s-%s-%s' % (date_from.year, date_from.month,date_from.day)
        to_date = fields.Date.context_today(self)
        domain_products = [('product_id', '=', self.id)]
        domain_move_out += [('date','>=',from_date),('date','<=',to_date)] + \
                           [('state', '=','done')] + domain_products
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = product_obj._get_domain_locations()
        #All Activity in Warehouse
        #domain_move_out_loc = domain_quant_loc
        domain_move_out_loc = [('location_dest_id.usage','=','customer')] #Only Sending Customer
        domain_quant += domain_products
        domain_quant += domain_quant_loc

        domain_move_out += domain_move_out_loc
        moves_out = self.env['stock.move'].read_group(domain_move_out, ['product_id', 'product_qty'], ['product_id'])
        if moves_out:
            moves_count_count = moves_out
            moves_out = dict(map(lambda x: (x['product_id'][0], x['product_qty']), moves_out))
            #self.qty_usage_quarter = float_round(moves_out.get(self.id, 0.0), precision_rounding=self.uom_id.rounding)

            moves_out_count = dict(map(lambda x: (x['product_id'][0], x['product_id_count']), moves_count_count))
            total = float_round(moves_out.get(self.id, 0.0), precision_rounding=self.uom_id.rounding)
            avg = float_round(total / moves_out_count.get(self.id, 1.0), precision_rounding=self.uom_id.rounding)
            self.qty_usage_quarter = avg
            self.qty_available_quarter = self.qty_available / avg
            self.qty_forcast_quarter = (self.qty_available + self.incoming_qty) / avg

    qty_usage_quarter = fields.Float(string='Average Quarter', digits=(8,3), readonly=True,
        compute='_compute_usage_quarter',)
    qty_available_quarter = fields.Float(string='Available Quarter', digits=(8,3), readonly=True,
        compute='_compute_usage_quarter',)
    qty_forcast_quarter = fields.Float(string='Forcast Quarter', digits=(8,3), readonly=True,
        compute='_compute_usage_quarter',)

    @api.one
    @api.depends()
    def _compute_usage_year(self):
        self.qty_usage_year = 0.0
        self.qty_available_year = 0.0
        product_obj = self.env['product.product']
        domain_quant = []
        domain_move_out = []
        last_year = timedelta(days=-360)
        date_from = datetime.now() + last_year
        from_date = '%s-%s-%s' % (date_from.year, date_from.month,date_from.day)
        to_date = fields.Date.context_today(self)
        domain_products = [('product_id', '=', self.id)]
        domain_move_out += [('date','>=',from_date),('date','<=',to_date)] + \
                           [('state', '=','done')] + domain_products
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = product_obj._get_domain_locations()
        #All Activity in Warehouse
        #domain_move_out_loc = domain_quant_loc
        domain_move_out_loc = [('location_dest_id.usage','=','customer')] #Only Sending Customer
        domain_quant += domain_products
        domain_quant += domain_quant_loc

        domain_move_out += domain_move_out_loc
        moves_out = self.env['stock.move'].read_group(domain_move_out, ['product_id', 'product_qty'], ['product_id'])
        if moves_out:
            moves_count_count = moves_out
            moves_out = dict(map(lambda x: (x['product_id'][0], x['product_qty']), moves_out))
            #self.qty_usage_quarter = float_round(moves_out.get(self.id, 0.0), precision_rounding=self.uom_id.rounding)

            moves_out_count = dict(map(lambda x: (x['product_id'][0], x['product_id_count']), moves_count_count))
            total = float_round(moves_out.get(self.id, 0.0), precision_rounding=self.uom_id.rounding)
            avg = float_round(total / moves_out_count.get(self.id, 1.0), precision_rounding=self.uom_id.rounding)
            self.qty_usage_year = avg
            self.qty_available_year = self.qty_available / avg

    qty_usage_year = fields.Float(string='Average Year', digits=(8,3), readonly=True,
        compute='_compute_usage_year',)
    qty_available_year = fields.Float(string='Available Year', digits=(8,3), readonly=True,
        compute='_compute_usage_year',)

class product_category(models.Model):

    _inherit = "product.category"
    #_columns = {
    #    'name': fields.char('Name', required=True, translate=True, select=True),
    #    'complete_name': fields.function(_name_get_fnc, type="char", string='Name'),
    #    'parent_id': fields.many2one('product.category','Parent Category', select=True, ondelete='cascade'),
    #    'child_id': fields.one2many('product.category', 'parent_id', string='Child Categories'),
    #    'sequence': fields.integer('Sequence', select=True, help="Gives the sequence order when displaying a list of product categories."),
    #    'type': fields.selection([('view','View'), ('normal','Normal')], 'Category Type', help="A category of the view type is a virtual category that can be used as the parent of another category to create a hierarchical structure."),
    #    'parent_left': fields.integer('Left Parent', select=1),
    #    'parent_right': fields.integer('Right Parent', select=1),}
    _order ='name'



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
