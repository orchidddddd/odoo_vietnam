# -*- coding: utf-8 -*-
from odoo import http

# class OprationEdit(http.Controller):
#     @http.route('/opration_edit/opration_edit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/opration_edit/opration_edit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('opration_edit.listing', {
#             'root': '/opration_edit/opration_edit',
#             'objects': http.request.env['opration_edit.opration_edit'].search([]),
#         })

#     @http.route('/opration_edit/opration_edit/objects/<model("opration_edit.opration_edit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('opration_edit.object', {
#             'object': obj
#         })