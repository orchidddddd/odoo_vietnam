from odoo import models, fields, api
from odoo.exceptions import UserError

class CreatCost(models.Model):
    _inherit = 'mrp.production'
    count_cost=fields.Integer()

    """def Count_cost(self):
        bomline = self.env['mrp.bom.line'].search([('product_id', '=', i.product_id.id)])
        super(CreatCost.self).count_cost=bomline.bom_id.product_tmpl_id.standard_price"""


class AutoBom(models.Model):
    _inherit = 'mrp.production'
    def Auto_bombom(self):
        productlotAuto = self.env['stock.production.lot'].search([])
        for i in productlotAuto.filtered(lambda x:x.product_qty>0):
            print(i.name)
            print(i.product_qty)

            bomline = self.env['mrp.bom.line'].search([('product_id', '=', i.product_id.id)])
            if len(bomline):
                print(bomline.bom_id.product_tmpl_id.name)
                res= self.env['mrp.production'].create({
                    'product_id' : bomline.bom_id.product_tmpl_id.id,
                    'product_qty' : i.product_qty,
                    'bom_id' : bomline.bom_id.id,
                    'product_uom_id': bomline.bom_id.product_tmpl_id.uom_id.id,
                    })
                res.action_assign()

                lotname = res.move_raw_ids.active_move_line_ids.lot_id.name

                lotexist=self.env['stock.production.lot'].search([('name','=',lotname),('product_id','=',res.product_id.id)])

                if len(lotexist)==0:
                    lotexist = self.env['stock.production.lot'].create({
                        'name':lotname,
                        'product_id':res.product_id.id
                    })
                """增加自動生長判斷 true就跳自動生長"""
                if i.product_id.product_tmpl_id.product_is_auto:
                    produce_wizard = self.env['mrp.product.produce'].with_context({
                        'active_id': res.id,
                        'active_ids': [res.id],
                     }).create({
                        'product_qty': res.product_qty,
                        'lot_id':lotexist.id
                    })
                    for line in produce_wizard.produce_line_ids:
                        line.qty_done = line.qty_to_consume
                    produce_wizard.do_produce()
                    res.button_mark_done()


class BomTime(models.Model):
    _inherit = 'mrp.bom.line'
    bom_time = fields.Integer(default = 30)


class DoProduce(models.TransientModel):
    _inherit = "mrp.product.produce"
    """按完生產紐之後 判斷使用者輸入數量是否有相符"""
    @api.multi
    def do_produce(self):
        res=super(DoProduce,self).do_produce()
        amout=0
        for line in self.produce_line_ids:
            amout += line.qty_done
        print("13")
        if self.product_qty !=amout:
            raise UserError("生成數量與完成數量不符")
        else:
            return res

    """將批號以及數量帶入按完生產鈕後跳出的wizard"""
    @api.model
    def default_get(self, fields):
        res = super(DoProduce, self).default_get(fields)
        line_temp=res['produce_line_ids'][0]
        for line in res['produce_line_ids']:
            row=line[2]
            row['qty_done']=row['qty_to_consume']
        print(line_temp[2])
        lot_temp =self.env['stock.production.lot'].browse(line_temp[2]['lot_id'])
        lot_exist=self.env['stock.production.lot'].search([('name','=',lot_temp.name),('product_id','=' ,res['product_id'])])

        if len(lot_exist):
            res['lot_id']=lot_exist.id
        else:
            lot_exist = self.env['stock.production.lot'].create({
                'name': lot_temp.name,
                'product_id': res['product_id']
            })
            res['lot_id'] = lot_exist.id

        return res


