# -*- coding: utf-8 -*-
{
    'name': "Générer des factures depuis les commandes de point de vente",

    'version': '15.0.0.0.0',
    'category': 'BASE',
    'sequence': 75,
    'summary': 'IDENTIFIANTS DES SOCIETES',
    'description': "Générer des factures depuis les commandes de point de vente",
    'licence': 'LGPL-3',
    'website': 'https://www.exploit-consult.com',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
'images': ['static/description/icon.png'],
}
