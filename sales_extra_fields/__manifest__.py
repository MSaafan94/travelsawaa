{
    'name': 'TravelSwa Sale Customize',
    'description': 'A Module to Add custom fields in sale form',
    'category': 'App',
    'version': '12.0',
    'depends': ['base', 'sale', 'crm', 'hr', 'sales_team', 'stock', 'purchase',],
    'data': [
        'security/security.xml',
        'security/ind_security.xml',
        'security/ir.model.access.csv',
        'views/css_loader.xml',
        'views/sale_view.xml',
        'views/hotel_view.xml',
        'views/destination_view.xml',
        'views/sale_template.xml',
        'views/crm_lead.xml',
        'views/res_partner.xml',
        'views/rooms.xml',
        'views/meal_plan.xml',
        'views/special_requests.xml',
        'views/flight.xml',
        'views/program.xml',
        'views/vaccination.xml',
        'views/visa.xml',
        'views/responsibility.xml',
        'views/account_invoice.xml',
        'wizard/transfer_salesperson.xml',
    ],
}
