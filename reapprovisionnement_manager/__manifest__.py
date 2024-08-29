# -*- coding: utf-8 -*-
{
    'name': "Reapprovisionnement manager",

    'version': '15.0.0.0.0',
    'category': 'BASE',
    'sequence': 75,
    'author': 'Exploit Consult',
    'summary': 'Reapprovisionnement manager',
    'description': "génération des Ordres de Fabrication à partir des bons de livraisons",
    'license': 'LGPL-3',
    'website': 'https://www.exploit-consult.com',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/reapprovisionnement_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/icon.png'],
}
