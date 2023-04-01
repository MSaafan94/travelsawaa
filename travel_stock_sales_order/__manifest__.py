# -*- coding: utf-8 -*-
{
    'name': "Travel Stock Qty On Hand",

    'summary': """
       Show quantity on hand in sale order line.""",

    'description': """
        Show quantity on hand in sale order line per selected product.
    """,

    'author': "Saafan",
   

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','stock','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
     'images': ['static/description/icon.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
