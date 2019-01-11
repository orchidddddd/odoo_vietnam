# -*- coding: utf-8 -*-

from odoo import models, fields, api
class OperationEdit(models.Model):

    _inherit = 'stock.move'

    lot_num = fields.Char()


class button_edit(models.Model):
    _inherit = 'stock.picking'
    """簡化存貨進出"""
    @api.multi
    def button_validate(self):
        for line in self.move_lines:
            for line2 in line.move_line_ids:
                line2.write({
                    'lot_name': line.lot_num,
                    'qty_done': line.quantity_done,
                })

        res=super(button_edit, self).button_validate()
        return res

