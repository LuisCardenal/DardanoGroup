from odoo import models, fields, api


class SaleOrderDocumentType(models.Model):
    _inherit = ['sale.order']

    journal_type_sv = fields.Many2one(comodel_name='account.journal', string='Tipo de documento.',
                                      domain="[('type', '=', 'sale')]", )
    document_type_sv = fields.Char(related='journal_type_sv.serie_correlativo_autorizado', string='Tipo de factura',
                                   help='Selecciona para imprimir el numero de serie en la factura')
    vendor_in_contacts_sale = fields.Many2one(related="partner_id.user_id", string="Vendedor asignado",
                                              help="Vendedor asignado a esta venta")



class SaleOrderName(models.Model):
    _inherit = 'sale.order'

    def _get_user_name(self):
        for record in self:
            name = record.partner_id.user_id.name
            first_name = name.split(" ")[0]
            last_name = name.split(" ")[-1]
            display_name = "{} {}".format(first_name, last_name)
            record.user_name = display_name

    user_name = fields.Char(compute='_get_user_name')
