from odoo import models, tools, fields


def _query(with_clause="", fields={}, groupby="", from_clause=""):
    return """
    SELECT aml.move_name, aml.date, aml.debit, aml.credit, aml.balance, a.code, a.name, aml.journal_id, a.id
        FROM account_move_line aml
        INNER JOIN account_account a
        ON a.id = aml.account_id
        GROUP BY
        a.id,
        a.name,
        a.code,
        aml.move_name,
        aml.date,
        aml.journal_id,
        aml.debit,
        aml.credit,
        aml.balance
    """


class FinancialGlobalReportWiz(models.Model):
    _name = 'financial.global.report'
    _description = 'Wizard to creates financial reports of account_moves'
    _auto = False

    id = fields.Many2one('account.account', readonly=True)
    name = fields.Char(readonly=True)
    code = fields.Char(readonly=True)
    move_name = fields.Char(readonly=True)
    date = fields.Date(readonly=True)
    journal_id = fields.Many2one('account.journal', readonly=True)
    debit = fields.Float(readonly=True)
    credit = fields.Float(readonly=True)
    balance = fields.Float(readonly=True)

    # account_from = fields.Many2one('account.account', required=True)
    # account_to = fields.Many2one('account.account', required=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, _query())
        )
