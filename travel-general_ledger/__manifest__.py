# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).
{
    'name': 'Travel General Ledger Account Filter',
    'version': '11.0.0.1',
    'category': 'Account',
    'sequence': 1,
    'author': 'Saafan',
    'summary': 'General Ledger report with Account Filter',
    'description': """
Add additional features
================================
    """,
    'depends': ['account', 'accounting_pdf_reports'],
    'data': [
        'report/account_general_ledger.xml',
        'wizard/account_report_general_ledger_view.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'live_test_url': 'https://www.youtube.com/watch?v=TvEzyfDkhyI'
}