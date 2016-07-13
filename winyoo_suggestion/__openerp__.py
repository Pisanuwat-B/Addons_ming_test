# -*- coding: utf-8 -*-
{
    'name': "Winyoo Suggestion",

    'summary': """
        ร่วมกันแจ้งปัญหา แก้ปัญหา และพัฒนางาน """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Care and Winyoo",
    'website': "------",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'solve the problem',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
#         'security/security.xml',
#         'ir.model.access.css',
        'suggestion_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}