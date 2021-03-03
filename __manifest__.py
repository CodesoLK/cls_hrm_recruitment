{
    'name': 'HRM Recruitment Leaf',
    'version': '1.0',
    'author' : 'Thisura Weerakkody',
    'category': 'Extra tools',
    'sequence': '38',
    'summary': 'FOR HRM of Ceylon Leaf Springs Recruitment Process',
    'depends': [ 'base','hr_recruitment','cls_hrm_leaves','ceylon_leaf_employee'],
                 
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/emp_agecron.xml',
        'views/recruitment_views.xml',
        'views/contract_views.xml',
        'views/employee_views.xml',
        'views/just_perm.xml',

     
     
                                    
    ],
    'demo': [],

'installable': True,
'application': True,
'auto_install': False,
}