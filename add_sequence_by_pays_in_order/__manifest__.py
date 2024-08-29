# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: fasluca(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

{
    'name': 'Add sequence by country in order',
    'version': '15.0.0.0.0',
    'category': 'BASE',
    'sequence': 75,
    'author': 'Exploit Consult',
    'summary': 'Add sequence by country in order',
    'description': "génération des séquences par pays pour les devis et les bons de commande",
    'license': 'LGPL-3',
    'website': 'https://www.exploit-consult.com',
    'depends': ['base',
                'sale',
                'identifiant_res_company',


                ],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/template.xml',


    ],
    'demo': [
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
