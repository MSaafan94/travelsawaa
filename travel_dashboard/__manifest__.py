# -*- coding: utf-8 -*-
{
    'name': "travel_dashboard",

    'summary': """
        making a travel dashboard""",

    'description': """
       making a travel dashboard
    """,

    'author': "Saafan",
    'website': "http://www.Saafan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'dashboard',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'board', 'purchase', 'travel_sales'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/menu.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'application': True,
    'images': ['static/description/icon.png'],
}