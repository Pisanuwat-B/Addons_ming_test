
from openerp import models, fields, api, _
from datetime import datetime

class winyoo_crm_phonecall(models.Model):
    _inherit = ['crm.phonecall']
    
    partner_id = fields.Many2one('res.partner', string="Contact",
        domain=[('customer','=',True)])