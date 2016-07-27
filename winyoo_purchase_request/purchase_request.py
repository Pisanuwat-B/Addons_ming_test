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
from openerp.exceptions import ValidationError
from openerp.exceptions import except_orm, Warning, RedirectWarning

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    @api.multi
    @api.onchange('line_ids')
    def check_last_record(self):
        show_warning = False
        str_var = 'ปริมาณสินค้าครั้งล่าสุดของ \n'
        str1 = 'ปริมาณของสินค้าได้เปลี่ยนแปลงเกิน 30% ของครั้งล่าสุด \n'
        str2 = r'product quantity change more than 30% of the most recent record '+'\n'
        str3 = "\n แต่ไม่เป็นไรหรอก แค่เตือนเฉยๆ"
        print ('++')
        print ('++')

        for rec in self.line_ids:
            print ('  ')
            print ('-- rec.name')
            print rec.name
            print ('-- rec.product_id.id')
            print rec.product_id.id
            print ('-- qty in form')
            print rec.product_qty
            print ('-- rec.id')
            print rec.id
            print ('-- type rec.id')
            print type(rec.id)
            print ('-- search')
            print self.env['purchase.request.line'].search([('name','=',rec.name)])
            print '  '

            if type(rec.id) != int:
                print '++++++++++++++++++++++++++ create ++++++++++++++++++++++++++++'
                print '  '

                if len(self.env['purchase.request.line'].search([('name','=',rec.name)])) != 0:
                    last_qty = self.env['purchase.request.line'].search([('name','=',rec.name)])[-1].product_qty
                    print '-- last_qty'
                    print last_qty
                    var = self.env['purchase.request.line'].search([('name','=',rec.name)])[-1].product_qty *30/100
                    print '-- var'
                    print var

                    if (rec.product_qty > (last_qty+var)) or (rec.product_qty < (last_qty-var)):
                        print str2
                        show_warning = True
                        str_name = rec.name.encode('utf-8')
                        print '-- type rec.name'
                        print type(rec.name)
                        str_qty = str(last_qty)
                        str_var += str_name+' คือ '+str_qty+'\n'
                        print ('  ')                        
                        print '++++++++++++++++++++++ end create loop +++++++++++++++++++++++'
                        print ('  ')

            else:
                print '=============== EDIT ================='
                print ('  ')
                print ('-- number of record')
                print len(self.env['purchase.request.line'].search([('name','=',rec.name),('id','!=',rec.id)]))
                print ('-- record list')
                print (self.env['purchase.request.line'].search([('name','=',rec.name),('id','!=',rec.id)]))
                
                if len(self.env['purchase.request.line'].search([('name','=',rec.name),('id','!=',rec.id)])) != 0:
                    print ('-- qty in most recent record')
                    last_qty = self.env['purchase.request.line'].search([('name','=',rec.name),('id','!=',rec.id)])[-1].product_qty
                    print last_qty
                    var = self.env['purchase.request.line'].search([('name','=',rec.name),('id','!=',rec.id)])[-1].product_qty *30/100
                    print '-- var: '
                    print var
                    print '-- range of qty w/o warning'
                    print 'min : ',self.env['purchase.request.line'].search([('name','=',rec.name),('id','!=',rec.id)])[-1].product_qty + var
                    print 'max : ',self.env['purchase.request.line'].search([('name','=',rec.name),('id','!=',rec.id)])[-1].product_qty - var

                    if (rec.product_qty > (last_qty+var)) or (rec.product_qty < (last_qty-var)):
                        print str2
                        show_warning = True
                        str_name = str(rec.name)
                        str_qty = str(last_qty)
                        str_name = rec.name.encode('utf-8')
                        str_var += str_name+' คือ '+str_qty+'\n'
                        print '-- type rec.name'
                        print type(rec.name)
                        print ('  ')
                        print '=============== END EDIT ================='
                        print ('  ')

            print ('--')
            print ('end loop')
            print ('--')

        if show_warning == True:
            warning = {
                'title': 'Warning!',
                'message' : str1+str2+'\n'+str_var+str3}
            return {'warning': warning}
        
        print ('--xx--')
        print ('  ')  


# class PurchaseRequestLine(models.Model):

#     _inherit = "purchase.request.line"



