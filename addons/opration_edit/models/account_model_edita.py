from odoo import models, fields, api


class AccountAddBranch(models.Model):
    _inherit = "account.journal"

    account_add_branch = fields.Char(string="分行")
