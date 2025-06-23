{
    'name': 'Insurance Management',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': """Insurance Management & Operations of the customers and manage
     the insurance claims and the salary of agents with or without the 
     commission. haha hehe hoho huhu""",
    'description': """Insurance Management and claims based on policies allows
     the user to create insurance policies it's working""",
    'author': 'Ankhbayar De',   
    'company': 'TEEE',
    'maintainer': 'TEEE',
    'website': 'https://www.tee.education/',
    'depends': ['account', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_type_data.xml',
        'data/insurance_details_data.xml',
        'data/claim_details_data.xml',
        'views/claim_details_views.xml',
        'views/employee_details_views.xml',
        'views/insurance_details_views.xml',
        'views/policy_details_views.xml',
        'views/insurance_management_menus.xml',
        'views/policy_type_views.xml',
        'views/payment_type_views.xml',
        'wizard/insurance_report_wizard_views.xml',
        'report/insurance_policy_report.xml',
        'report/insurance_policy_template.xml',      
        'wizard/insure_wiz.xml',
        'report/insurance_per_person_report_template.xml',
        'views/ai_detection_views.xml',
        'data/ir_cron.xml',
],
    'assets': {
        'web.assets_backend': [
            'account/static/src/components/**/*',
        ],

    'controllers': [
        'controllers/ai_detection_controller.py',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}