# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import _, fields, models
import textwrap


class StockKardexReportWiz(models.TransientModel):
    _name = 'stock.kardex.report.product.wiz'
    _description = 'Wizard to create kardex reports of stock moves'

    date_from = fields.Datetime(
        string='From', required=True, default=fields.Datetime.now)
    date_to = fields.Datetime(
        string='To', required=True, default=fields.Datetime.now)
    product = fields.Many2one('product.product', required=True)
    location = fields.Many2one('stock.location', required=True)

    def open_table(self):
        self.env['stock.kardex.report'].search([]).unlink()
        self._cr.execute('''
        SELECT
        a.done - b.done
        AS
        total
        FROM
        (
            SELECT sum(qty_done)
            AS
            done
            FROM
            stock_move_line
            WHERE
            product_id = %s
            AND
            state = \'done\'
            AND
            date < %s
            AND
            location_dest_id = %s
        )
        a
        CROSS JOIN
        (
            SELECT sum(qty_done)
            AS
            done
            FROM
            stock_move_line
            WHERE
            product_id = %s
            AND
            state = \'done\'
            AND
            date < %s
            AND
            location_id = %s
        )
        b
        ''', [
            self.product.id, self.date_from, self.location.id,
            self.product.id, self.date_from, self.location.id
        ])
        start_qty = self._cr.dictfetchall()
        total = 0
        if start_qty[0]['total']:
            total = start_qty[0]['total']
        self._cr.execute("""WITH one AS (
            SELECT sml.product_id, sml.product_uom_id,sml.qty_done, sml.move_id, sml.location_id, sml.location_dest_id, 
            sm.date, sm.origin, sm.state, sml.id, sm.partner_id, sm.price_unit, sm.sale_line_id, sm.purchase_line_id
            FROM stock_move_line sml
            INNER JOIN stock_move sm
            ON sml.move_id = sm.id
            WHERE
            sm.date >= %s
            AND sm.date <= %s),
            two AS (
                SELECT *
                FROM one
                WHERE location_id = %s
                OR location_dest_id = %s)
            SELECT *
            FROM two
            WHERE product_id = %s
            AND state = 'done'
            ORDER BY date;""", [
            self.date_from, self.date_to,
            self.location.id, self.location.id,
            self.product.id
        ])
        moves = self._cr.dictfetchall()
        report_list = []
        report_list.append({
            'product_id': self.product.id,
            'qty_done': 0,
            'date': self.date_from,
            'origin': _('Initial Balance'),
            'balance': total,
        })

        for rec in moves:
            done_qty = rec['qty_done']
            if rec['location_id'] == self.location.id:
                done_qty = -rec['qty_done']
            total += done_qty
            origin = rec['origin']

            partner_id = rec['partner_id']
            price_subtotal = 0

            if not partner_id:
                purchase_id = rec['purchase_line_id']
                if purchase_id:
                    self._cr.execute('''
                    SELECT partner_id, price_subtotal
                    FROM purchase_order_line
                    WHERE id = %s
                    ''', [
                        purchase_id
                    ])
                    partner = self._cr.fetchone()
                    if partner is not None:
                        partner_id = partner[0]
                        price_subtotal = partner[1]

            price_unit = rec['price_unit']

            if not price_unit:
                sales_id = rec['sale_line_id']
                if sales_id:
                    self._cr.execute('''
                    SELECT price_unit, price_subtotal
                    FROM sale_order_line
                    WHERE id = %s
                    ''', [
                        sales_id
                    ])
                    price = self._cr.fetchone()
                    if price is not None:
                        price_unit = price[0]
                        price_subtotal = price[1]

            if origin:
                origin = textwrap.shorten(
                    rec['origin'], width=80, placeholder="...")
            line = {
                'move_id': rec['move_id'],
                'product_id': rec['product_id'],
                'product_uom_id': rec['product_uom_id'],
                'price': price_subtotal,
                'unit_price': price_unit,
                'owner_id': partner_id,
                'qty_done': done_qty,
                'location_id': rec['location_id'],
                'location_dest_id': rec['location_dest_id'],
                'date': rec['date'],
                'balance': total,
                'origin': origin,
            }
            report_list.append(line)
        self.env['stock.kardex.report'].create(report_list)
        tree_view_id = self.env.ref(
            'stock_kardex_report.stock_kardex_report_tree_view').id
        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_id': tree_view_id,
            'view_mode': 'tree',
            'name': _('Stock Report'),
            'res_model': 'stock.kardex.report',
        }
        return action
