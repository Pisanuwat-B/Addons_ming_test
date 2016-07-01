# -*- coding: utf-8 -*-
{
    'name': "Tinnakorn Module: modified Ineco Thai Account",

  
    'description': """
        Long description of module's purpose
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['ineco_thai_account','base'],

    # always loaded
    'data': [
             'res_partner_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
