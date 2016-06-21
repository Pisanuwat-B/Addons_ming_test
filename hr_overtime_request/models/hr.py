#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP SA (<http://www.odoo.com>)
#    Copyright (C) 2014-TODAY Probuse Consulting Service Pvt. Ltd. (<http://probuse.com>).
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
#########################################################################################

from openerp import models, fields, api, _

class hr_employee(models.Model):
    _inherit = 'hr.employee'
    
    overtime_ids = fields.One2many('hr.overtime', 'employee_id', string='Overtimes')
    
    def get_overtime_hours(self, emp_id, date_from, date_to=None):
        if date_to is None:
            date_to = datetime.now().strftime('%Y-%m-%d')
        self._cr.execute("SELECT sum(o.number_of_hours) from hr_overtime as o where \
                            o.include_payroll IS TRUE and o.employee_id=%s \
                            and o.state='validate' AND to_char(o.date_to, 'YYYY-MM-DD') >= %s AND to_char(o.date_to, 'YYYY-MM-DD') <= %s ",
                            (emp_id, date_from, date_to))
        res = self._cr.fetchone()
        return res and res[0] or 0.0

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
