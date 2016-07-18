# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
_STATES = [
    ('draft', 'Draft'),
    ('submitted', 'แจ้งแล้ว'),
    ('received', 'คนที่เกี่ยวข้องรับเรื่อง'),
    ('done', 'เสร็จแล้ว')
]

class Suggestion(models.Model):
    _name= 'suggestion'
    
    @api.model
    def _get_default_name(self):
        return self.env['res.users'].browse(self.env.uid)
    
    main_suggest = fields.Selection([('program','แจ้งแก้ไขโปรแกรม'),('car','ร้องเรียนกระบวนการที่ไม่เป็นไปตามข้อตกลง'),('ask','คำถามเกี่ยวกับโปรแกรมและกระบวนการ')
                                ,('report','แจ้งแก้ไขเอกสาร'),('idea','แนะนำและเสนอข้อคิดเห็นเกี่ยวกับงาน')])
    topic = fields.Char(required=False)
#    department = fields.Selection([("sale","Sale"),("purchase","Purchase"),("accounting","Accounting")])
    functional = fields.Selection([('sale','งานขาย'),
                    ('purchase','งานจัดซื้อ'),
                    ('warehouse','งานคลังสินค้า'),
                    ('delivery','งานจัดส่ง'),
                    ('account','งานเอกสารบัญชี/การเงิน'),
                    ('hr','งานบุคคล'),
                    ('others','งานอื่นๆ')])
    
    found_date = fields.Date(default = fields.Date.today())
#    name = fields.Many2one('res.users', default=lambda self: self.env.user)
    name = fields.Many2one('res.users', default=_get_default_name)
    note = fields.Text('รายละเอียด')
    state = fields.Selection(selection=_STATES,
                             string='Status',
                             required=True,
                             default='draft')    
#    test = fields.Reference(selection=[('res.groups','group')], default=lambda self: self.env.group)
#    test = fields.Many2one('res.groups', default=)

    @api.multi
    def button_suggestion(self):
        print "------------------------------------------------------------------"
        print "self.env = ", self.env
        print "self.env.user = ", self.env.user
        print "self.env.user.name = ", self.env.user.name
        print "self.env.cr = ", self.env.cr
#        print "self.env['res.groups'].search", self.env['res.groups'].search
        print "------------------------------------------------------------------" 
        
#    @api.multi
#    def button_submitted(self):
        


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: