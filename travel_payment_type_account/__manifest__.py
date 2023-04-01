# -*- coding: utf-8 -*-
{
    'name': "Travel Payment Type Account",

    'summary': """
        """,


    'author': "Amr Gaber",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'account', 'mail', ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/account_payment.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}