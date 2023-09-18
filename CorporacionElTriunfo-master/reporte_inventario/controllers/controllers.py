# -*- coding: utf-8 -*-
# from odoo import http


# class ReporteInventario(http.Controller):
#     @http.route('/reporte_inventario/reporte_inventario', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reporte_inventario/reporte_inventario/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reporte_inventario.listing', {
#             'root': '/reporte_inventario/reporte_inventario',
#             'objects': http.request.env['reporte_inventario.reporte_inventario'].search([]),
#         })

#     @http.route('/reporte_inventario/reporte_inventario/objects/<model("reporte_inventario.reporte_inventario"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reporte_inventario.object', {
#             'object': obj
#         })
