{
    'name': 'Tax Declaration Management',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Module quản lý khai báo thuế GTGT',
    'sequence': 1,
    'author': 'Custom',
    'depends': ['base', 'account'],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/kt_thue_gtgt_views.xml',
        'views/kt_thue_gtgt_ht_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
