# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from datetime import timedelta
from openerp.exceptions import ValidationError, Warning


class fixLength_Acc(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.constrains('tax_detail')
    def check_Length_acc_tax_detail(self):
        tax_d = self.tax_detail
#         print "---------------------------------------------"
#         print tax_d
        if tax_d:
            lenTax = len(tax_d)
            if lenTax != 5:
                raise ValidationError("คุณใส่ Branch No %s ตัว ไม่ตรงตามกำหนด(5 ตัวอักษร)" %lenTax)
                #raise Warning(_("คุณใส่ Branch No มากเกินกำหนด(5 ตัวอักษร)%s") %(len(self.tax_detail))) 
        else:
            lenTax = 0

 
    @api.one
    @api.constrains('pid')
    def check_Length_acc_pid(self):
        if self.pid:
            lenPid = len(self.pid)
            if lenPid != 13:
                raise ValidationError("คุณใส่ Tax ID %s ตัว ไม่ตรงตามกำหนด (13 ตัวเลข)" %lenPid)
        else:
            lenPid = 0

        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:   