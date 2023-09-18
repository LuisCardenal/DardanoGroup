from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = ['account.journal']

    serie_correlativo_autorizado = fields.Char(string="Número de serie en factura")
    numero_resolucion = fields.Char(string="Número de Resolución")


