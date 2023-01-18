{
    'name' : 'CUSTOM_REQUISITION',
    'version' : '1.0.0',
    'author' : 'rifat',
    'category' : 'product_requisition/CUSTOM_REQUISITION',
    'sequence' : 1,
    'summary' : 'Practice purpose',
    'description' : 'Still no idea',
    'depends' : ['base', 'purchase', 'stock'],
    'data' : [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/email_template.xml',
        'data/purchase_email_template.xml',
        'views/menu.xml',
        'views/requisition.xml',
        'report/report.xml',
        'report/CPR_template.xml',


    ],
    'demo' : [],
    'installable' : True,
    'application': True,
    'auto_install' : False,
    'asset' : {},
}