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

import time
from datetime import datetime

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning


Datetime_FORMAT = '%Y-%m-%d'

class hr_overtime(models.Model):
    _name = 'hr.overtime'
    _description = 'Employee Overtime'
    
    _rec_name = 'employee_id'
    
    
    @api.multi
    def unlink(self):
        for request in self:
            if request.state not in ('draft', 'cancel'):
                raise Warning(_('You cannot delete an overtime request which is not draft or cancelled.'))
        return super(hr_overtime, self).unlink()

    @api.model
    def _employee_get(self):
        ids = self.env['hr.employee'].search([('user_id', '=', self._uid)], limit=1)
        if ids:
            return ids
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id.category_ids:
            self.category_id = self.employee_id.category_ids[0].id
        self.company_id = self.employee_id.company_id.id
        self.manager_id = self.employee_id.parent_id.id
        self.department_manager_id = self.employee_id.department_id and self.employee_id.department_id.manager_id and self.employee_id.department_id.manager_id.id or False
    
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(string='Description', required=False, states={'draft':[('readonly', False)]}, readonly=True)
    number_of_hours = fields.Float(string='Number Of Hours', states={'draft':[('readonly', False)]}, readonly=True, store=True)
    include_payroll = fields.Boolean(string='Include In Payroll', help='Tick if you want to include this overtime in employee payroll', default=True)
    state = fields.Selection(selection=[('draft', 'New'), ('confirm', 'Waiting First Approval'),('approve_by_department', 'Waiting Department Approval'), ('refuse', 'Refused'),
                                        ('validate', 'Done'), ('cancel', 'Cancelled')],
                                string='Status', readonly=True, default='draft', track_visibility='onchange')
    user_id = fields.Many2one(related='employee_id.user_id', string='User', store=True, default=lambda self: self.env.user, states={'draft':[('readonly', False)]}, readonly=True)
    date_from = fields.Datetime(string='Start Date', states={'draft':[('readonly', False)]}, readonly=True, default=fields.datetime.now()) 
    date_to = fields.Datetime(string='End Date', states={'draft':[('readonly', False)]}, readonly=True)
    approve_date = fields.Date(string='Department Approved Date', readonly=True, copy=False)
    hr_approve_date = fields.Date(string='Approved Date', readonly=True, copy=False)
    employee_id = fields.Many2one('hr.employee', string="Employee", select=True, required=True, default=_employee_get, states={'draft':[('readonly', False)]}, readonly=True)
    manager_id = fields.Many2one('hr.employee', 'Manager', states={'draft':[('readonly', False)]}, readonly=True, help='This area is automatically filled by the user who will approve the request', copy=False)
    notes = fields.Text(string='Notes',)
    department_id = fields.Many2one(related='employee_id.department_id', string='Department', type='many2one', relation='hr.department', readonly=True, store=True)
    category_id = fields.Many2one('hr.employee.category', string="Category", readonly=False, states={'validate':[('readonly', True)]}, help='Category of Employee')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=False, states={'validate':[('readonly', True)]})
    approve_hr_manager_id = fields.Many2one('res.users', string='Approved By', readonly=True, copy=False)
    approve_dept_manager_id = fields.Many2one('res.users', string='Department Manager', readonly=True, copy=False)
    multiple_overtime_id = fields.Many2one('hr.overtime.multiple', string="Overtime Multiple Request")
    department_manager_id = fields.Many2one('hr.employee', string='Department Manager(to hide)')
    
    @api.onchange('date_from')
    def onchange_start_date(self):
        if self.date_to and self.date_from:
            date_start = datetime.strptime(self.date_from, "%Y-%m-%d %H:%M:%S")
            date_end = datetime.strptime(self.date_to, "%Y-%m-%d %H:%M:%S")
            diff_hours = date_end - date_start
            self.number_of_hours = (diff_hours.seconds / 3600.00) + (diff_hours.days * 24.00)
        else:
            self.number_of_hours = 0.0
    
    @api.onchange('date_to')
    def onchange_end_date(self):
        if self.date_to and self.date_from:
            date_start = datetime.strptime(self.date_from, "%Y-%m-%d %H:%M:%S")
            date_end = datetime.strptime(self.date_to, "%Y-%m-%d %H:%M:%S")
            diff_hours = date_end - date_start
            self.number_of_hours = (diff_hours.seconds / 3600.00) + (diff_hours.days * 24.00)
        else:
            self.number_of_hours = 0.0
    
    @api.multi
    def set_to_draft(self):
        self.write({
            'state': 'draft',
            'approve_date': False,
            'hr_approve_date': False,
            'approve_hr_manager_id': False,
            'approve_dept_manager_id' : False
            
        })
        return True
    
    @api.multi
    def ot_cancel(self):
        self.write({'state': 'cancel'})
        return True
    
    @api.multi
    def ot_refuse(self):
        obj_emp = self.env['hr.employee']
        ids2 = obj_emp.search([('user_id', '=', self._uid)], limit=1)
        manager = ids2 or False
        self.write({'state': 'refuse', 'manager_id':  manager and manager.id or False})
        return True
    
    @api.multi
    def ot_validate(self):
        obj_emp = self.env['hr.employee']
        ids2 = obj_emp.search([('user_id', '=', self._uid)], limit=1)
        manager = ids2 or False
        return self.write({'state':'validate', 'manager_id':  manager and manager.id or False,  'approve_date': time.strftime('%Y-%m-%d'), 'approve_dept_manager_id': self.env.user.id})
    
    @api.multi
    def ot_confirm(self):
        return self.write({'state':'confirm'})

    @api.multi
    def department_approval(self):
        return self.write({'state':'approve_by_department', 'approve_hr_manager_id': self.env.user.id, 'hr_approve_date': time.strftime('%Y-%m-%d')})

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    overtime_ids = fields.One2many('hr.overtime', 'employee_id', string='Overtimes')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
