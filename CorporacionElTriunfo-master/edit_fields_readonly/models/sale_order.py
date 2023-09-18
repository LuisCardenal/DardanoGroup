from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                                         'sale': [('readonly', False)]}, copy=False, default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    def _prepare_confirmation_values(self):
        return {
            'state': 'sale',
            # 'date_order': fields.Datetime.now()
        }
