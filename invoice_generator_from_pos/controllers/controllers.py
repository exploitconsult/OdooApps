# -*- coding: utf-8 -*-
# from odoo import http


# class ReaprovisionnementManager(http.Controller):
#     @http.route('/reaprovisionnement_manager/reaprovisionnement_manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reaprovisionnement_manager/reaprovisionnement_manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reaprovisionnement_manager.listing', {
#             'root': '/reaprovisionnement_manager/reaprovisionnement_manager',
#             'objects': http.request.env['reaprovisionnement_manager.reaprovisionnement_manager'].search([]),
#         })

#     @http.route('/reaprovisionnement_manager/reaprovisionnement_manager/objects/<model("reaprovisionnement_manager.reaprovisionnement_manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reaprovisionnement_manager.object', {
#             'object': obj
#         })
