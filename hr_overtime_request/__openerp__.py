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

{
    'name' : 'HR Overtime Request and Payroll Edited By Winyoo',
    'version': '1.1',
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'category' : 'Human Resources',
    'price': 10.0,
    'currency': 'EUR',
    'website': 'https://www.probuse.com',
    'description': ''' 
This module add below features which can be used to manage overtime requests:
  * Overtime Requests: This will be request by employee.
  * Multiple Overtime Requests: This request can be created by HR Manager or Department Manager on behalf of multiple employees together.
  * Integrate Overtime Requests in Employee Payslips: This will show payslip lines in payslip of employee.

Note: This module add new group called "Department Manager(Overtime)" under Usability group.

Menus:
Human Resources/Overtimes
Human Resources/Overtimes/Overtime Requests
Human Resources/Overtimes/Overtime Requests to Approve
Human Resources/Overtimes/Overtime Requests to Approve By Department
Human Resources/Overtimes/Multiple Overtime Requests
Human Resources/Overtimes/Multiple Requests to Approve
Human Resources/Overtimes/Multiple Requests to Approve By Department
  ''',
    'depends':['hr', 'hr_payroll'],
    'data' : [
              'security/overtime_security.xml',
              'security/ir.model.access.csv',
              'views/hr_overtime_view.xml',
              'views/hr_overtime_multiple_view.xml',
              'views/hr_view.xml',
              'data/ot_salary_rule_data.xml',
              
              ],
    'installable':True,
    'auto_install':False

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
