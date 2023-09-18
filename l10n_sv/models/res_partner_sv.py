from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    export_license = fields.Char(string="Licencia de exportación", help="Ingrese licencia de exportación si creará "
                                                                        "facturas de exportación.")
    document_nit = fields.Char(string='NIT')
    # document_nit_partner = fields.Char(string='Número NIT')
    document_giro = fields.Char(string='Giro')
    document_dui = fields.Char(string='DUI')
    journal_contacts = fields.Many2one(comodel_name='account.journal', string='Diario contable enlazado')


class ResPartnerNIT(models.Model):
    _inherit = 'res.partner'

    nit_res_partner = fields.Char(string="NIT")    

