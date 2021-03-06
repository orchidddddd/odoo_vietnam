# -*- coding: utf-8 -*-
{
    'name': "opration_edit",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'mrp', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/operation_view.xml',
        'views/product_template_edit_view.xml',
        'wizard/autobom_wizard.xml',
        'views/account_edit.xml',
        'views/lot_edit.xml',
        'wizard/everyday_add_stay_cost.xml',
        'data/data_account_type_old.xml',
        'data/automation.xml',
        'data/sequence_customized_lot_number.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}