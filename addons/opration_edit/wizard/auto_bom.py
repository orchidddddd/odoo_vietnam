from odoo import models, fields, api
from odoo.exceptions import UserError

"""將autobom搬進wizard"""
class AutoBom(models.TransientModel):
    _name = 'auto.bom'

    def Auto_bombom(self):
        productlotAuto = self.env['stock.production.lot'].search([])
        for i in productlotAuto.filtered(lambda x:x.product_qty>0):

            bomline = self.env['mrp.bom.line'].search([('product_id', '=', i.product_id.id)])
            print(bomline)
            if len(bomline) != 1:
                print('不只一張bom表')
                raise UserError('要去選擇bom表')
            if len(bomline):
                print(bomline.bom_id.product_tmpl_id.name)
                res= self.env['mrp.production'].create({
                    'product_id' : bomline.bom_id.product_tmpl_id.id,
                    'product_qty' : i.product_qty,
                    'bom_id' : bomline.bom_id.id,
                    'product_uom_id': bomline.bom_id.product_tmpl_id.uom_id.id,
                    })
                res.action_assign()

                lotname = i.name

                lotexist=self.env['stock.production.lot'].search([('name','=',lotname),('product_id','=',res.product_id.id)])
                print(lotexist)
                print(len(lotexist))
                if len(lotexist) == 0:
                    """檢查是否有Lot"""
                    lotexist = self.env['stock.production.lot'].create({
                        'name' :lotname,
                        'product_id' :res.product_id.id
                    })

                produce_wizard = self.env['mrp.product.produce'].with_context({
                    'active_id': res.id,
                    'active_ids': [res.id],
                    }).create({
                    'product_qty': res.product_qty,
                    'lot_id': lotexist.id
                })
                for line in produce_wizard.produce_line_ids:
                        line.qty_done = line.qty_to_consume
                if i.product_id.product_tmpl_id.product_is_auto:
                    produce_wizard.do_produce()
                    res.button_mark_done()

    # def choose_bom_line