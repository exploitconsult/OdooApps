# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'IDENTIFIANT RES COMPANY',
    'version': '15.0.0.0.0',
    'category': 'BASE',
    'sequence': 75,
    'summary': 'IDENTIFIANTS DES SOCIETES',
    'description': "Ajouter des identifants pour les sociétés comme la matricule fiscal, le code TVA, le code catégorie "
                   "le numéro établissement secondaire... etc ",
    'licence': 'LGPL-3',
    'website': 'https://www.exploit-consult.com',
    'images': [

    ],
    'depends': [
        'base',
        'base_setup',


    ],
    'data': [

        'views/res_company_view.xml',


    ],

    'images': ['static/description/icon.png'],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
