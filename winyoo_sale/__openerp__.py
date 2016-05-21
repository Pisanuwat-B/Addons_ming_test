# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 EANG COMPANY
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


{
    'name': 'Tinnakorn Module for Sales',
    'version': '0.1',
    'category': 'Tools',
    'description': """
Module for Sale Tinnakorn
Winyoo create 2015
    """,
    'author': 'Winyoo Kongkavitool',
    'depends': ['sale','sale_order_dates','sale_quotation_number'], # depends--> look at folder's name
    'data': ['sale_view.xml',
             'report_saleorder.xml',
             'security/sale_security.xml',
             #'security/ir.model.access.csv',
             #'data/crm.case.categ.csv',
             'crm_case_phone_form_view.xml',
             'crm_phonecall_report_view.xml',
             #'sale_sequence.xml',
             #'sale_report_view.xml',
             ], #XML File that included in my module
             
    'demo': [], #CSV Sample Data
    'installable': True, #  False mean no button to install
    'auto_install': False, #dangerous put auto_install
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
