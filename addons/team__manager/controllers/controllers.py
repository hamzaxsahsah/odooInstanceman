# -*- coding: utf-8 -*-
# from odoo import http


# class TeamManager(http.Controller):
#     @http.route('/team__manager/team__manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/team__manager/team__manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('team__manager.listing', {
#             'root': '/team__manager/team__manager',
#             'objects': http.request.env['team__manager.team__manager'].search([]),
#         })

#     @http.route('/team__manager/team__manager/objects/<model("team__manager.team__manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('team__manager.object', {
#             'object': obj
#         })
