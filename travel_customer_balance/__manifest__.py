# -*- coding: utf-8 -*-
{
    'name': "Travel Partner Balance Customer/Vendor",

    'summary': """
       This module will show partner balance customer balance vendor balance on Sale order and invoice""",

    'description': """
        This module will show partner balance customer balance vendor balance on Sale order and invoice
    """,

    'author': "Saafan",
    'category': 'Base',
    'website': 'https://www.blinkingerp.com/',
    'license': 'AGPL-3',



    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','purchase'],

	'images': ['static/description/Banner.png'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
