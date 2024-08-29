

from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

import collections
import logging

_logger = logging.getLogger(__name__)

class res_partner_inherit(models.Model):
    _inherit = 'res.partner'

    is_virtual_customer = fields.Boolean(string="Est un client virtuel")

class account_account_inherit(models.Model):
    _inherit = 'account.account'

    is_account_of_sale = fields.Boolean(string="Est un compte de vente")

class account_tax_inherit(models.Model):
    _inherit = 'account.tax'

    is_default_sale_tax = fields.Boolean(string="Est un tax de vente par defaut")

class pos_order_inherit(models.Model):
    _inherit = 'pos.order'




    def action_generate_invoices(self):
        #client_passager_record = self.env['pos.order'].search([('client_passager', '=', True)], order='id', limit=1)

        selected_ids = self.env.context.get('active_ids', [])
        if selected_ids:
            orders = self.env['pos.order'].search([('id', 'in', selected_ids),('account_move', '!=', False)])
            all_good = True
            done = True
            i = 0
            while i < len(orders):
                if orders[i].account_move != False:
                    all_good = False
                if orders[i].state == 'done':
                    done = False
                i += 1
            #if done:
            if all_good:

                virtual_customer = self.env['res.partner'].search([('is_virtual_customer', '=', True)], limit=1)

                if virtual_customer:
                    vals = {
                        'partner_id': virtual_customer.id,
                        'move_type': 'out_invoice',
                        'journal_id': self.config_id.invoice_journal_id.id,

                    }
                    facture = self.env['account.move'].create(vals)


                    #_logger.info('******* facture %s', facture)

                    if facture:
                        _logger.info('******* facture')
                        # my_dict = []
                        # liste = []
                        # for order in orders:
                        order_lines = self.env['pos.order.line'].read_group(domain=[('order_id', 'in', selected_ids)],
                                                                           fields=['product_id', 'price_unit', 'qty'],
                                                                           groupby=['product_id', 'price_unit'], lazy=False)

                        for my_dict in order_lines:

                            the_tax = self.env['account.tax'].search([('is_default_sale_tax', '=', True)], limit=1)
                            account_of_sale = self.env['account.account'].search([('is_account_of_sale', '=', True)],
                                                                                           limit=1)
                            _logger.info('********************* account_of_sale %s', account_of_sale)
                            product = self.env['product.product'].search([('id', '=', my_dict['product_id'][0])], limit=1)
                            if the_tax:
                                vals = {
                                    'move_id': facture.id,
                                    'product_id': product.id,
                                    'name': product.name,
                                    'quantity': my_dict['qty'],
                                    #'account_id': product.categ_id.property_account_income_categ_id.id,
                                    'exclude_from_invoice_tab': False,
                                    'product_uom_id': product.uom_id.id,
                                    'price_unit': my_dict['price_unit'],
                                    #'display_type': 'line_section',
                                    'account_id': account_of_sale.id,
                                    'tax_ids': product.taxes_id,
                                    #'tax_ids': [(4,the_tax.id)],

                                }
                            else:
                                vals = {
                                    'move_id': facture.id,
                                    'product_id': my_dict['product_id'][0],
                                    'name': product.name,
                                    'quantity': my_dict['qty'],
                                    'product_uom_id': product.uom_id.id,
                                    'price_unit': my_dict['price_unit'],

                                    'account_id': account_of_sale.id,


                                }
                                if account_of_sale:
                                    vals = {
                                        'move_id': facture.id,
                                        'product_id': product.id,
                                        'name': product.name,
                                        'quantity': my_dict['qty'],
                                        # 'account_id': product.categ_id.property_account_income_categ_id.id,
                                        'exclude_from_invoice_tab': False,
                                        'product_uom_id': product.uom_id.id,
                                        'price_unit': my_dict['price_unit'],
                                        # 'display_type': 'line_section',
                                        'account_id': account_of_sale.id,
                                        'tax_ids': product.taxes_id,
                                        # 'tax_ids': [(4,the_tax.id)],

                                    }
                                else:
                                    raise ValidationError('veillez spécifier un compte de vente !')
                            invoice_lines = self.env['account.move.line'].with_context(check_move_validity = False).create(vals)
                            _logger.info('******* invoice_lines %s', invoice_lines)
                            facture.with_context(check_move_validity=False)._recompute_dynamic_lines(recompute_all_taxes=True)

                        self.account_move = facture.id
                        return {
                            #'name': _('Your String'),
                            'view_type': 'form',
                            'view_mode': 'form',
                            'res_model': 'account.move',
                            'res_id': facture.id,
                            'type': 'ir.actions.act_window',
                            'target': 'current',
                            'nodestroy': True
                        }
                    else:
                        raise ValidationError('probléme de création de la facture !')
                        # my_dict.append({virtual_customer: order.lines})
                else:
                    raise ValidationError('veillez spécifier un client passager !')
            else:
                raise ValidationError('il y a des commandes qui sont déja facturées !')
            # else:
            #     raise ValidationError('il y a des commandes qui sont déja comptabilisées !')


