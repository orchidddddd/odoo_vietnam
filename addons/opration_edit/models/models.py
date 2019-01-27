# -*- coding: utf-8 -*-

from odoo import models, fields, api
class OperationEdit(models.Model):

    _inherit = 'stock.move'

    lot_num = fields.Char(default=lambda self: self._get_default_lot_num())

    def _get_default_lot_num(self):
        temp = self.picking_id.picking_type_id.name
        if temp == False:
            return self.env['ir.sequence'].next_by_code('stock.customized.lot')
        else:
            return True


class button_edit(models.Model):
    _inherit = 'stock.picking'
    """簡化存貨進出"""
    @api.multi
    def button_validate(self):
        print('簡化部分')
        for line in self.move_lines:
            print(line.picking_id.picking_type_id.code)
            if line.picking_id.picking_type_id.code == 'incoming':
                print('屬於入庫')
                for line2 in line.move_line_ids:
                    line2.write({
                        'lot_name': line.lot_num,
                        'qty_done': line.quantity_done,
                    })

        print(self.env['stock.production.lot'].search([('name','=',line.lot_num)]))
        res=super(button_edit, self).button_validate()
        return res

