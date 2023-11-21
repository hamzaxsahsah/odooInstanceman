# -*- coding: utf-8 -*-
{
    'name': "Instence_Manager",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts','sale_management','hr','sale','portal'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/instenceView/instence_view.xml',
        'views/OdooVersionView/odooV_view.xml',
        'email/email_templs.xml',
        'views/peremetreView/Premetre.xml',
        'views/employeeExtdView/employee_ext.xml',
        'views/saleExtendView/sale_ext.xml',
        'reportTemp/instenceReport/report_temp.xml',
        'wizards/InstenceCreationWizard/views/views.xml',
        'views/instenceView/instance_home.xml',
        'data/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'demo/demo2.xml',
    ],
    'application': 'true',
}