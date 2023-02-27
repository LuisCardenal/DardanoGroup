from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = ['account.move']

    journal_invoice = fields.Many2one(related='partner_id.journal_contacts', string='Diario relacionado: ',
                                      readonly=True)
    journal_id = fields.Many2one(string="Diario ")
    order_id = fields.Many2one(comodel_name='account.move', string='Número de factura')
    name_order = fields.Char(compute='_name_order', string='Número de orden')
    porcentaje_retenido2 = fields.Many2one(comodel_name="account.tax", string="Porcentaje retenido")
    vendor_in_contacts = fields.Many2one(related="partner_id.user_id", string="Vendedor asignado",
                                         help="Vendedor asignado a esta venta")
    def _name_order(self):
        for rec in self:
            rec.name_order = rec.order_id.name
