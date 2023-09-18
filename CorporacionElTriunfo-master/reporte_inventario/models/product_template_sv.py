from datetime import datetime

from odoo import models, fields, api


class ProductInventario(models.Model):
    _inherit = 'product.template'

    total_cost = fields.Float(string="Costo Total", compute="_total_cost", required=False)
    fiscal_year = fields.Many2one(comodel_name='account.fiscal.year',string="Año fiscal")
    journal_categ_inform = fields.Many2one(comodel_name="product.category")
    journal_cat = fields.Many2one(related="categ_id.property_stock_valuation_account_id",
                                  string="Cuenta de valorización de inventario")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index = 1)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id, required=True)

    # @api.depends('fiscal_year', 'date_from')
    # def _set_year(self, fiscal_year):
    #     if fiscal_year == datetime.now().year:
    #         for year in self:
    #             year.current_year = year.name
    #     return year.current_year

    @api.depends('qty_available', 'standard_price')
    def _total_cost(self):
        for rec in self:
            rec.total_cost = rec.qty_available * rec.standard_price

    # @api.depends('name', 'date_from', 'date_to')
    # def _fiscal_year(self):
    #     for rec in self:
    #         rec.current_year = rec.name


class CategoryJournalInventory(models.Model):
    _inherit = 'product.category'

    journal_category = fields.Many2one(comodel_name="product.category",
                                       string="Cuenta de valorizacion en categoria")
    journal_category_show = fields.Many2one(related="journal_category.property_stock_valuation_account_id",
                                            string="Cuenta de valorizacion en categoria")

    @api.depends('property_stock_valuation_account_id')
    def _get_journal_category(self):
        for rec in self:
            rec.journal_category = rec.property_stock_valuation_account_id



