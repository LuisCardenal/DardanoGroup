# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models, tools
import textwrap


def _query(with_clause="", fields={}, groupby="", from_clause=""):
    return """
    WITH one AS (
    SELECT sml.product_id, sml.product_uom_id, sml.qty_done, sml.move_id, sml.location_id, sml.location_dest_id, 
    sm.date, sm.origin, sm.state, sml.id, sm.sale_line_id, sm.purchase_line_id, sm.partner_id as partner_sale
    FROM stock_move_line sml
    INNER JOIN stock_move sm
    ON sml.move_id = sm.id
    ), two AS (
    SELECT one.qty_done, one.product_id, one.product_uom_id, one.move_id, one.location_id, one.location_dest_id, 
    one.date, one.origin, one.state, one.id, one.sale_line_id, one.purchase_line_id, one.partner_sale, sl.usage
    FROM one
    INNER JOIN stock_location sl
    ON sl.id = one.location_id
    )
    SELECT *
    FROM two
    WHERE state = 'done'
    GROUP BY 
    id,
    state,
    move_id, 
    product_id, 
    product_uom_id, 
    location_id, 
    location_dest_id, 
    qty_done, 
    date,
    origin, 
    sale_line_id,
    purchase_line_id,
    partner_sale,
    usage
    """


class StockKardexGlobalReport(models.Model):
    _name = 'stock.kardex.global.report'
    _description = 'Wizard to create kardex reports of stock moves'
    _auto = False

    # Campos necesarios para el reporte de kardex
    id = fields.Many2one('stock.move.line', readonly=True)
    state = fields.Char(readonly=True)
    move_id = fields.Many2one('stock.move', readonly=True)
    product_id = fields.Many2one('product.product', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', readonly=True)
    partner_id = fields.Many2one('res.partner', readonly=True, compute='_compute_partner_id')
    location_id = fields.Many2one('stock.location', readonly=True)
    location_dest_id = fields.Many2one('stock.location', readonly=True)
    qty_done = fields.Float('Done', readonly=True, group_operator=False)
    date = fields.Datetime(readonly=True)
    origin = fields.Char(readonly=True)
    balance = fields.Float(readonly=True, group_operator=False, compute='_compute_total_quantity')
    price = fields.Float(readonly=True, group_operator=False, compute='_compute_price_product')
    price_unit = fields.Float(readonly=True, group_operator=False, compute='_compute_price_unit')
    qty = fields.Float(readonly=True, group_operator=False, compute='_compute_qty_done')
    sale_line_id = fields.Many2one('sale.order.line', readonly=True)
    purchase_line_id = fields.Many2one('purchase.order.line', readonly=True)
    document_origin = fields.Char(readonly=True, compute='_compute_name_document')
    partner_sale = fields.Many2one('res.partner', readonly=True)
    usage = fields.Char(readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, _query())
        )

    def _compute_qty_done(self):
        for rec in self:
            if rec.usage == "internal":
                rec.qty = -rec.qty_done
            else:
                rec.qty = rec.qty_done

    def _compute_total_quantity(self):
        for rec in self:
            rec.balance = 0
            self._cr.execute('''
                WITH rn AS (
                SELECT sml.date, ROW_NUMBER() OVER (ORDER BY date) as RN, sml.id, sml.qty_done, sl.usage
                FROM 
                stock_move_line sml
                INNER JOIN stock_location sl 
                ON sml.location_id = sl.id
                WHERE 
                product_id = %s
                AND 
                state = \'done\'
                )
                SELECT
                SUM(a.done)
                AS
                total
                FROM
                (
                SELECT 
                CASE usage
                    when 'internal' then SUM(-qty_done)
                    ELSE
                        SUM(qty_done)
                END
                AS
                done
                FROM
                rn
                WHERE RN < (SELECT RN FROM rn WHERE id= %s)
                GROUP BY usage
                )
                a
                ''', [
                rec.product_id.id, rec.id,
            ])
            start_qty = self._cr.dictfetchall()
            if start_qty[0]['total']:
                rec.balance = start_qty[0]['total'] + rec.qty

    def _compute_price_product(self):
        for rec in self:
            rec.price = 0
            if rec.purchase_line_id.id:
                self._cr.execute('''
                    SELECT price_subtotal
                    FROM purchase_order_line
                    WHERE id = %s
                    ''', [
                    rec.purchase_line_id.id
                ])
                price_subtotal = self._cr.fetchone()
                if price_subtotal is not None:
                    rec.price = price_subtotal[0]
            elif rec.sale_line_id.id:
                self._cr.execute('''
                SELECT price_subtotal
                FROM sale_order_line
                WHERE id = %s
                ''', [
                    rec.sale_line_id.id
                ])
                price_subtotal = self._cr.fetchone()
                if price_subtotal is not None:
                    rec.price = price_subtotal[0]

    def _compute_name_document(self):
        for rec in self:
            if rec.origin:
                rec.document_origin = textwrap.shorten(
                    rec.origin, width=80, placeholder="...")
            else:
                rec.document_origin = "Adjuste de inventario"

    def _compute_price_unit(self):
        for rec in self:
            rec.price_unit = 0
            if rec.purchase_line_id.id:
                self._cr.execute('''
                    SELECT price_unit
                    FROM purchase_order_line
                    WHERE id = %s
                    ''', [
                    rec.purchase_line_id.id
                ])
                price_unit = self._cr.fetchone()
                if price_unit is not None:
                    rec.price_unit = price_unit[0]
            elif rec.sale_line_id.id:
                self._cr.execute('''
                SELECT price_unit
                FROM sale_order_line
                WHERE id = %s
                ''', [
                    rec.sale_line_id.id
                ])
                price_unit = self._cr.fetchone()
                if price_unit is not None:
                    rec.price_unit = price_unit[0]

    def _compute_partner_id(self):
        for rec in self:
            rec.partner_id = None
            if rec.purchase_line_id.id:
                self._cr.execute('''
                    SELECT partner_id
                    FROM purchase_order_line
                    WHERE id = %s
                    ''', [
                    rec.purchase_line_id.id
                ])
                partner = self._cr.fetchone()
                if partner is not None:
                    rec.partner_id = partner[0]
            elif rec.sale_line_id.id:
                rec.partner_id = rec.partner_sale
