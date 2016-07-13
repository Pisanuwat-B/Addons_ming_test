# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

class Problem(models.Model):
    _name= 'it_problem.problem'
    
    mainpro = fields.Selection([('program','เสนอโปรแกรม'),('car','ร้องเรียนกระบวนการที่ไม่เป็นไปตามข้อตกลง'),('ask','คำถามเกี่ยวกับโปรแกรมและกระบวนการ')
                                ,('report','แก้ไขเอกสาร'),('idea','แนะนำและเสนอข้อคิดเห็นเกี่ยวกับงาน')], default='program')
    topicp = fields.Char(required=True)
#     ptype = fields.Selection([("sale","Sale"),("purchase","Purchase"),("accounting","Accounting")])
    ptype = fields.Many2one('res.groups')
    date = fields.Date(default = fields.Date.today())
    name = fields.Many2one('res.users', default=lambda self: self.env.user)
    notep = fields.Text('รายละเอีดเพิ่มเติม')
#     test = fields.Reference(selection=[('res.groups','group')], default=lambda self: self.env.group)
#     test = fields.Many2one('res.groups', default=)

    @api.multi
    def test_problem(self):
        print "------------------------------------------------------------------"
        print "self.env = ", self.env
        print "self.env.user = ", self.env.user
        print "self.env.user.name = ", self.env.user.name
        print "self.env.cr = ", self.env.cr
#         print "self.env['res.groups'].search   ", self.env['res.groups'].search
        print "------------------------------------------------------------------"   
 
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: