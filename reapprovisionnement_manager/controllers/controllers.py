# -*- coding: utf-8 -*-
# from odoo import http


# class reapprovisionnementManager(http.Controller):
#     @http.route('/reapprovisionnement_manager/reapprovisionnement_manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reapprovisionnement_manager/reapprovisionnement_manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reapprovisionnement_manager.listing', {
#             'root': '/reapprovisionnement_manager/reapprovisionnement_manager',
#             'objects': http.request.env['reapprovisionnement_manager.reapprovisionnement_manager'].search([]),
#         })

#     @http.route('/reapprovisionnement_manager/reapprovisionnement_manager/objects/<model("reapprovisionnement_manager.reapprovisionnement_manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reapprovisionnement_manager.object', {
#             'object': obj
#         })
