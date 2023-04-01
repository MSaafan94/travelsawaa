{
    'name': 'travel sales quotation authority',
    'description': 'sales quatation templete module',
    'category': 'App',
    'version': '12.0',
    'depends': ['base', 'crm', 'sale', 'sales_extra_fields', 'details'],
    'data': [
        # 'security/quotation_templetes_groups.xml',
        'views/quotation_template_view.xml',
        'views/from_expired_to_order_view.xml'
    ],
}
