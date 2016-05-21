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
#from openerp.addons.base.res.res_partner import format_address


#class crm_lead(models.Model):
#    _name = "crm.lead"
#    _inherit = ['crm.lead']
    
    #Fix opt_out to default with True
#    opt_out = fields.Boolean('Opt-Out (ไม่รับอีเมล)', 
#            oldname='optout',
#            default=True,
#            help="If opt-out is checked, this contact has refused to receive emails for mass mailing and marketing campaign. "
#                   "Filter 'Available for Mass Mailing' allows users to filter the leads when performing mass mailing.")
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: