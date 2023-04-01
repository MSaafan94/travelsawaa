{
    'name': 'crm module',
    'description': 'cusrom crm module',
    'category': 'App',
    'version': '12.0',
    'depends': ['base', 'crm','sale','sales_extra_fields','documents'],
    'data': [
        'views/crm_uncreate_customer_view.xml',
        'views/sales_uncreate_customer_view.xml',
        'views/stage_field_domain.xml',
        # 'views/disable_attachment.xml',
        'views/document_inh.xml',
        'security/document_folders.xml'
    ],

}
