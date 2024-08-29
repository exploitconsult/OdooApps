# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"


    
    type_identifiant = fields.Selection([
            ('1', 'Matricule Fiscal '),
            ('2', 'Num'u"\u00E9"'ro de la carte d'u"\u2019"'identit'u"\u00E9"' nationale'),
            ('3', 'Num'u"\u00E9"'ro de la carte du s'u"\u00E9"'jour pour les 'u"\u00E9"'trangers '),
            ('4', 'Identifiant des personnes non domicili'u"\u00E9"'es ni 'u"\u00E9"'tablies en Tunisie'),
            ],default='1', required=True)

    #numero_matricule_fiscal = fields.Char(size=7)
    numero_matricule_fiscal = fields.Char()
    cle_matricule_fiscal = fields.Char(size=1)
    code_tva = fields.Char(size=1)
    code_categorie = fields.Char(size=1)
    num_etab_secondaire = fields.Char(size=3, default='000')



    cin = fields.Char(size=8)
    carte_sejour = fields.Char(size=8)
    id_non_domicile_ni_etablie = fields.Char(size=8)


    _sql_constraints = [ ('unique_identifiant', 'unique(numero_matricule_fiscal, cle_matricule_fiscal, code_tva, code_categorie, num_etab_secondaire)', 'Matricule Fiscal existe !'), ('unique_cin', 'unique(cin)', 'Num'u"\u00E9"'ro de la carte d'u"\u2019"'identit'u"\u00E9"' nationale existe !'), ('unique_carte_sejour', 'unique(carte_sejour)', 'Num'u"\u00E9"'ro de la carte du s'u"\u00E9"'jour pour les 'u"\u00E9"'trangers existe !'), ('unique_id_non_domicile_ni_etablie', 'unique(id_non_domicile_ni_etablie)', 'Identifiant des personnes non domicili'u"\u00E9"'es ni 'u"\u00E9"'tablies en Tunisie existe !') ]

    @api.onchange('type_identifiant')
    def _onchange_type_identifiant(self):
        for rec in self:
            if rec.type_identifiant == '1':

                rec.cin = ''
                rec.carte_sejour = ''
                rec.id_non_domicile_ni_etablie = ''

                rec.num_etab_secondaire = '000'

            if rec.type_identifiant == '2':

                rec.numero_matricule_fiscal = ''
                rec.cle_matricule_fiscal = ''
                rec.code_tva = ''
                rec.code_categorie = ''
                rec.num_etab_secondaire = ''

                rec.carte_sejour = ''
                rec.id_non_domicile_ni_etablie = ''

            if rec.type_identifiant == '3':

                rec.numero_matricule_fiscal = ''
                rec.cle_matricule_fiscal = ''
                rec.code_tva = ''
                rec.code_categorie = ''
                rec.num_etab_secondaire = ''

                rec.cin = ''
                rec.id_non_domicile_ni_etablie = ''

            if rec.type_identifiant == '4':

                rec.numero_matricule_fiscal = ''
                rec.cle_matricule_fiscal = ''
                rec.code_tva = ''
                rec.code_categorie = ''
                rec.num_etab_secondaire = ''

                rec.cin = ''
                rec.carte_sejour = ''

            if rec.type_identifiant == False:

                rec.numero_matricule_fiscal = ''
                rec.cle_matricule_fiscal = ''
                rec.code_tva = ''
                rec.code_categorie = ''
                rec.num_etab_secondaire = ''
                rec.cin = ''
                rec.carte_sejour = ''
                rec.id_non_domicile_ni_etablie = ''


        
            

    # @api.constrains('numero_matricule_fiscal')
    # def verify_numero_matricule_fiscal(self):
    #     for rec in self:
    #         if rec.numero_matricule_fiscal:
    #             if rec.numero_matricule_fiscal.isnumeric() == False:
    #                 raise ValidationError("Num"u"\u00E9""ro matricule doit "u"\u00EA""tre num"u"\u00E9""rique")
    #             if len(rec.numero_matricule_fiscal) != 7:
    #                 raise ValidationError("Num"u"\u00E9""ro matricule fiscal doit "u"\u00EA""tre compos"u"\u00E9"" de 7 chiffres")




    @api.constrains('cle_matricule_fiscal')
    def verify_cle_matricule_fiscal(self):
        for rec in self:
            if rec.cle_matricule_fiscal:
                if rec.cle_matricule_fiscal.isalpha() == False:
                    raise ValidationError("Cl"u"\u00E9"" matricule doit "u"\u00EA""tre une lettre alphab"u"\u00E9""tique")
                if rec.cle_matricule_fiscal.isupper() == False:
                    raise ValidationError("Cl"u"\u00E9"" matricule fiscal doit "u"\u00EA""tre une lettre alphab"u"\u00E9""tique en majuscule")


    @api.constrains('code_tva')
    def verify_code_tva(self):
        for rec in self:
            if rec.code_tva:
                if rec.code_tva.isalpha() == False:
                    raise ValidationError("Code TVA doit "u"\u00EA""tre une lettre alphab"u"\u00E9""tique")
                if rec.code_tva.isupper() == False:
                    raise ValidationError("Code TVA doit "u"\u00EA""tre une lettre alphab"u"\u00E9""tique en majuscule")


    @api.constrains('code_categorie')
    def verify_code_categorie(self):
        for rec in self:
            if rec.code_categorie:
                if rec.code_categorie.isalpha() == False:
                    raise ValidationError("Code cat"u"\u00E9""gorie doit "u"\u00EA""tre une lettre alphab"u"\u00E9""tique")
                if rec.code_categorie.isupper() == False:
                    raise ValidationError("Code cat"u"\u00E9""gorie doit "u"\u00EA""tre une lettre alphab"u"\u00E9""tique en majuscule")


    @api.constrains('num_etab_secondaire')
    def verify_num_etab_secondaire(self):
        for rec in self:
            if rec.num_etab_secondaire:
                if rec.num_etab_secondaire.isnumeric() == False:
                    raise ValidationError("N"u"\u00B0"" "u"\u00E9""tablissement secondaire doit "u"\u00EA""tre num"u"\u00E9""rique")
                if len(rec.num_etab_secondaire) != 3:
                    raise ValidationError("N"u"\u00B0"" "u"\u00E9""tablissement secondaire doit "u"\u00EA""tre compos"u"\u00E9"" de 3 chiffres")



    @api.constrains('cin')
    def verify_cin(self):
        for rec in self:
            if rec.cin:
                if rec.cin.isnumeric() == False:
                    raise ValidationError("Num"u"\u00E9""ro de la carte d"u"\u2019""identit"u"\u00E9"" doit "u"\u00EA""tre num"u"\u00E9""rique")
                if len(rec.cin) != 8:
                    raise ValidationError("Num"u"\u00E9""ro de la carte d"u"\u2019""identit"u"\u00E9"" doit "u"\u00EA""tre compos"u"\u00E9"" de 8 chiffres")

    @api.constrains('carte_sejour')
    def verify_carte_sejour(self):
        for rec in self:
            if rec.carte_sejour:
                if rec.carte_sejour.isnumeric() == False:
                    raise ValidationError("Num"u"\u00E9""ro de la carte du s"u"\u00E9""jour pour les "u"\u00E9""trangers doit "u"\u00EA""tre num"u"\u00E9""rique")
                if len(rec.carte_sejour) != 8:
                    raise ValidationError("Num"u"\u00E9""ro de la carte du s"u"\u00E9""jour pour les "u"\u00E9""trangers doit "u"\u00EA""tre compos"u"\u00E9"" de 8 chiffres")

    @api.constrains('id_non_domicile_ni_etablie')
    def verify_id_non_domicile_ni_etablie(self):
        for rec in self:
            if rec.id_non_domicile_ni_etablie:
                if rec.id_non_domicile_ni_etablie.isnumeric() == False:
                    raise ValidationError("Identifiant des personnes non domicili"u"\u00E9""es ni "u"\u00E9""tablies en Tunisie "u"\u00EA""tre num"u"\u00E9""rique")
                if len(rec.id_non_domicile_ni_etablie) != 8:
                    raise ValidationError("Identifiant des personnes non domicili"u"\u00E9""es ni "u"\u00E9""tablies en Tunisie "u"\u00EA""tre compos"u"\u00E9"" de 8 chiffres")
    




