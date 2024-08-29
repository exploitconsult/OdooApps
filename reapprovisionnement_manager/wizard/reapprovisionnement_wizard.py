from odoo import api, fields, models
import logging
import collections
from collections import defaultdict
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)



class StockLocationInherit(models.Model):

    _inherit = 'stock.location'


    is_origin = fields.Boolean(string="Est un emplacement origine")

class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    def button_mark_done(self):
        self._onchange_move_finished_product()
        self._button_mark_done_sanity_checks()

        if not self.env.context.get('button_mark_done_production_ids'):
            self = self.with_context(button_mark_done_production_ids=self.ids)
        res = self._pre_button_mark_done()
        if res is not True:
            return res

        if self.env.context.get('mo_ids_to_backorder'):
            productions_to_backorder = self.browse(self.env.context['mo_ids_to_backorder'])
            productions_not_to_backorder = self - productions_to_backorder
            close_mo = False
        else:
            productions_not_to_backorder = self
            productions_to_backorder = self.env['mrp.production']
            close_mo = True

        self.workorder_ids.button_finish()

        backorders = productions_to_backorder._generate_backorder_productions(close_mo=close_mo)
        productions_not_to_backorder._post_inventory(cancel_backorder=True)
        productions_to_backorder._post_inventory(cancel_backorder=True)

        # if completed products make other confirmed/partially_available moves available, assign them
        done_move_finished_ids = (
                    productions_to_backorder.move_finished_ids | productions_not_to_backorder.move_finished_ids).filtered(
            lambda m: m.state == 'done')
        done_move_finished_ids._trigger_assign()

        # Moves without quantity done are not posted => set them as done instead of canceling. In
        # case the user edits the MO later on and sets some consumed quantity on those, we do not
        # want the move lines to be canceled.
        (productions_not_to_backorder.move_raw_ids | productions_not_to_backorder.move_finished_ids).filtered(
            lambda x: x.state not in ('done', 'cancel')).write({
            'state': 'done',
            'product_uom_qty': 0.0,
        })

        for production in self:
            production.write({
                'date_finished': fields.Datetime.now(),
                'product_qty': production.qty_produced,
                'priority': '0',
                'is_locked': True,
                'state': 'done',
            })

        for workorder in self.workorder_ids.filtered(lambda w: w.state not in ('done', 'cancel')):
            workorder.duration_expected = workorder._get_duration_expected()

        if not backorders:
            if self.env.context.get('from_workorder'):
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mrp.production',
                    'views': [[self.env.ref('mrp.mrp_production_form_view').id, 'form']],
                    'res_id': self.id,
                    'target': 'main',
                }
            return True
        context = self.env.context.copy()
        context = {k: v for k, v in context.items() if not k.startswith('default_')}
        for k, v in context.items():
            if k.startswith('skip_'):
                context[k] = False
        action = {
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
            'context': dict(context, mo_ids_to_backorder=None, button_mark_done_production_ids=None)
        }
        if len(backorders) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': backorders[0].id,
            })
        else:
            action.update({
                'name': _("Backorder MO"),
                'domain': [('id', 'in', backorders.ids)],
                'view_mode': 'tree,form',
            })
        return action


    def _action_cancel(self):
        documents_by_production = {}
        for production in self:
            documents = defaultdict(list)
            for move_raw_id in self.move_raw_ids.filtered(lambda m: m.state not in ('done', 'cancel')):
                iterate_key = self._get_document_iterate_key(move_raw_id)
                if iterate_key:
                    document = self.env['stock.picking']._log_activity_get_documents({move_raw_id: (move_raw_id.product_uom_qty, 0)}, iterate_key, 'UP')
                    for key, value in document.items():
                        documents[key] += [value]
            if documents:
                documents_by_production[production] = documents
            # log an activity on Parent MO if child MO is cancelled.
            finish_moves = production.move_finished_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            if finish_moves:
                production._log_downside_manufactured_quantity({finish_move: (production.product_uom_qty, 0.0) for finish_move in finish_moves}, cancel=True)

        self.workorder_ids.filtered(lambda x: x.state not in ['done', 'cancel']).action_cancel()
        finish_moves = self.move_finished_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
        raw_moves = self.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel'))

        (finish_moves | raw_moves)._action_cancel()
        picking_ids = self.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
        picking_ids.action_cancel()

        for production, documents in documents_by_production.items():
            filtered_documents = {}
            for (parent, responsible), rendering_context in documents.items():
                if not parent or parent._name == 'stock.picking' and parent.state == 'cancel' or parent == production:
                    continue
                filtered_documents[(parent, responsible)] = rendering_context
            production._log_manufacture_exception(filtered_documents, cancel=True)

        # In case of a flexible BOM, we don't know from the state of the moves if the MO should
        # remain in progress or done. Indeed, if all moves are done/cancel but the quantity produced
        # is lower than expected, it might mean:
        # - we have used all components but we still want to produce the quantity expected
        # - we have used all components and we won't be able to produce the last units
        #
        # However, if the user clicks on 'Cancel', it is expected that the MO is either done or
        # canceled. If the MO is still in progress at this point, it means that the move raws
        # are either all done or a mix of done / canceled => the MO should be done.
        self.filtered(lambda p: p.state not in ['done', 'cancel']).write({'state': 'done'})
        self.state='cancel'

        return True

# class StockMoveInherit(models.Model):
#
#     _inherit = 'stock.move'
#
#     def unlink(self):
#         _logger.info('********** unlink')
#         self.created_production_id.product_qty -= self.product_uom_qty
#         res = super(StockMoveInherit, self).unlink()
#         # here you can do accordingly
#         return res



class HrReapprovisionnementWizard(models.TransientModel):

    _name = 'reapprovisionnement.manager.wizard'
    _description = 'reapprovisionnement manager'




    date_debut = fields.Datetime(string="Date Début", required=True)
    date_fin = fields.Datetime(string="Date Fin", required=True, default=fields.Datetime.now())




    # def generate_reapprovisionnement(self):
    #     objects = [{'product_id': 235, 'product_qty': 1.0, 'product_uom_id': 10, 'state': 'confirmed'}, {'product_id': 267, 'product_qty': 1.0, 'product_uom_id': 26, 'state': 'confirmed'}]
    #     for object in objects:
    #         self.env['mrp.production'].create(object)


    def generate_reapprovisionnement(self):
        for rec in self:
            location_origin = rec.env['stock.location'].search([('is_origin', '=', True)], limit=1)
            if location_origin:
                lines = rec.env['stock.picking'].search([('location_id', '=', location_origin.id), ('state', 'in', ['confirmed', 'assigned']), ('scheduled_date', '>=', rec.date_debut), ('scheduled_date', '<', rec.date_fin)])
                if lines:
                    #liste = []

                    my_dict = []
                    for l in lines:
                        for line in l.move_ids_without_package:
                            #_logger.info('*********%s', line.created_production_id.id)

                            if line.created_production_id.id == False:
                                my_dict.append({line.product_id.id : line.product_uom_qty})
                                _logger.info('************* line.product_uom_qty %s', line.product_uom_qty)
                            #liste.append(line.product_id.id)
                    counter = collections.Counter()
                    for d in my_dict:
                        counter.update(d)

                    res = dict(counter)
                    #_logger.info('********** res %s', res)
                    liste_of = []
                    if res:
                        for r in res:
                            #_logger.info('************** r %s', r)
                            #_logger.info('************** r %s', res[r])
                            object = {'product_id': r,
                                      'product_qty': res[r],
                                      'product_uom_id': rec.env['product.product'].search([('id', '=', r)]).uom_id.id,
                                      #'state': 'confirmed'
                                    }
                            order = rec.env['mrp.production'].create(object)
                            #order._onchange_product_id()
                            #order._onchange_bom_id()
                            if not order.product_id:
                                order.bom_id = False
                            elif not order.bom_id or order.bom_id.product_tmpl_id != order.product_tmpl_id or (
                                    order.bom_id.product_id and order.bom_id.product_id != order.product_id):
                                bom = order.env['mrp.bom']._bom_find(order.product_id, picking_type=order.picking_type_id,
                                                                    company_id=order.company_id.id, bom_type='normal')[
                                    order.product_id]
                                if bom:
                                    order.bom_id = bom.id
                                    #self.product_qty = self.bom_id.product_qty
                                    order.product_uom_id = order.bom_id.product_uom_id.id
                                else:
                                    order.bom_id = False
                                    order.product_uom_id = order.product_id.uom_id.id
                            if not order.product_id and order.bom_id:
                                order.product_id = order.bom_id.product_id or order.bom_id.product_tmpl_id.product_variant_ids[
                                                                            :1]
                            #self.product_qty = self.bom_id.product_qty or 1.0
                            order.product_uom_id = order.bom_id and order.bom_id.product_uom_id.id or order.product_id.uom_id.id
                            order.move_raw_ids = [(2, move.id) for move in
                                                 order.move_raw_ids.filtered(lambda m: m.bom_line_id)]
                            order.move_finished_ids = [(2, move.id) for move in order.move_finished_ids]
                            order.picking_type_id = order.bom_id.picking_type_id or order.picking_type_id
                            order._onchange_move_raw()
                            liste_of.append(order)
                    else:
                        raise ValidationError('Il n''y a pas des ordres de fabrications à générées dans cet intervalle !')
                    if liste_of:
                        for of in liste_of:
                            product = of.product_id.id
                            #_logger.info('******** product %s', product)
                            for l in lines:
                                for line in l.move_ids_without_package:
                                    if line.product_id.id == product:
                                        line.created_production_id = of.id
                                        #_logger.info('******** line.created_production_id %s', line.created_production_id)

                    # table = list(dict.fromkeys(liste))
                    # # _logger.info('********** liste %s', liste)
                    # # _logger.info('********** table %s', table)
                else:
                    raise ValidationError('Il n''y a pas des ordres de fabrications à générées dans cet intervalle !')
            else:
                raise ValidationError('Il faut définir l emplacement d origine avec le champ "est un emplacement d origine" qui ce trouve dans la fiche emplacement!')