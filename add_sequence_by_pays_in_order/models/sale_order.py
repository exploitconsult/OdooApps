# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    suffixe_order = fields.Char()
    prefix_order = fields.Char()
    suffixe_command = fields.Char()
    prefix_command = fields.Char()
    num_order = fields.Char()
    num_command = fields.Char()

# class ResContryInherit(models.Model):
#     _inherit = "res.country"
#
#     num_order = fields.Char()
#     num_command = fields.Char()

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    pays_id = fields.Many2one('res.country')

    nom = fields.Char()
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, related='nom')
    num = fields.Integer()

    @api.onchange('pays_id')
    def get_name(self):
        self.num += 1
        if self.company_id.suffixe_order and self.company_id.prefix_order and self.company_id.num_order and self.num == 2:
            datee = list(str(date.today().year))
            year = ''
            i = 0
            for d in datee:
                if i >= 2:
                    year += str(d)
                i+=1

            _logger.info('************ %s company', self.company_id.name)

            self.nom = str(self.company_id.prefix_order) + str(year) +'-'+ str(self.company_id.num_order)  + str(self.pays_id.code) + str(self.company_id.suffixe_order)

            num_order = list(self.company_id.num_order)
            num = ''
            i= len(num_order)
            j=0
            bool = True
            while j < i:
                if num_order[j] =='9':
                    bool = False
                    num_order[j-1] = str(int(num_order[j-1]) + 1)
                    num_order[j] = 0
                j += 1
            if bool:
                _logger.info('*********** int(num_order[len(num_order) - 1]) + 1 %s', int(num_order[len(num_order) - 1]) + 1)
                num_order[len(num_order) - 1] = str(int(num_order[len(num_order) - 1]) + 1)

            num = ''
            for n in num_order:
                num += str(n)


            self.company_id.num_order = num
        else:
            nom = 'Nouveau'






    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        if self.company_id.suffixe_command and self.company_id.prefix_command and self.company_id.num_command:
            datee = list(str(date.today().year))
            year = ''
            i = 0
            for d in datee:
                if i >= 2:
                    year += str(d)
                i+=1

            _logger.info('************ %s company', self.company_id.name)
            self.nom = str(self.company_id.prefix_command) + year +'-'+ str(self.company_id.num_command)  + str(self.pays_id.code) + str(self.company_id.suffixe_command)

            num_command = list(self.company_id.num_command)
            num = ''
            i= len(num_command)
            j=0
            bool = True
            while j < i:
                if num_command[j] =='9':
                    bool = False
                    num_command[j-1] = str(int(num_command[j-1]) + 1)
                    num_command[j] = 0
                j += 1
            if bool:
                num_command[len(num_command) - 1] = str(int(num_command[len(num_command) - 1]) + 1)

            num = ''
            for n in num_command:
                num += str(n)


            self.company_id.num_command = num
        return True


