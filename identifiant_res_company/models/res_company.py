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


class res_company(models.Model):
    _inherit = "res.company"

    numero_matricule_fiscal = fields.Char(size=7, required=True)
    cle_matricule_fiscal = fields.Char(size=1, required=True)
    code_tva = fields.Char(size=1, required=True)
    code_categorie = fields.Char(size=1, required=True)
    num_etab_secondaire = fields.Char(size=3, default='000', required=True)

    _sql_constraints = [ ('unique_identifiant', 'unique(numero_matricule_fiscal, cle_matricule_fiscal, code_tva, code_categorie, num_etab_secondaire)', 'Matricule Fiscal existe !')  ]



    @api.constrains('numero_matricule_fiscal')
    def verify_numero_matricule_fiscal(self):
        for rec in self:
            if rec.numero_matricule_fiscal:
                if rec.numero_matricule_fiscal.isnumeric() == False:
                    raise ValidationError("Num"u"\u00E9""ro matricule doit "u"\u00EA""tre num"u"\u00E9""rique")
                if len(rec.numero_matricule_fiscal) != 7:
                    raise ValidationError("Num"u"\u00E9""ro matricule fiscal doit "u"\u00EA""tre compos"u"\u00E9"" de 7 chiffres")


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
    




