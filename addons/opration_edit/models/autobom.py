from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

class BomTime(models.Model):
    _inherit = 'mrp.bom'
    bom_time = fields.Float(default = 5.0)

class BomCost(models.Model):
    _inherit = 'mrp.bom'
    bom_cost = fields.Integer()


class CreatCost(models.Model):

    _inherit = 'mrp.production'
    count_cost =fields.Float(string="換盆成本")
    past_cost = fields.Float(string="過往成本")
    per_unit_cost = fields.Float(string="每株成本")
    total_cost = fields.Float(string="總成本")

    #綁在檢查可用
    @api.multi
    def action_assign(self):
        res = super(CreatCost, self).action_assign()
        self.get_cost_change_per_unit()
        return res

    #自動生產不會呼叫 看要不要綁到do_produce() 在auto_bom 86行有呼叫
    # @api.multi
    # def open_produce_product(self):
    #     res = super(CreatCost, self).open_produce_product()
    #     self.get_cost_change_per_unit()
    #     return res

    # """取得生產產品過往單價"""
    def get_cost_change_per_unit(self):
        """計算換盆成本"""
        print('計算換盆成本')
        res = self.env['mrp.production'].search([])
        print(res)
        for mo_line in res:
            print(self)
            bom_temp = self.env['mrp.bom'].search([('id', '=', mo_line.bom_id.id)])
            print(bom_temp)
            self.count_cost = bom_temp.bom_cost * bom_temp.bom_time * mo_line.product_qty
        """取得產品過往單價 """
        print('取得產品過往單價')
        print(self.move_raw_ids)
        for line in self.move_raw_ids:
            # if len(line.active_move_line_ids[0].lot_id) == 0:
            #     print('QQ')
            #     return True
            print(line.active_move_line_ids)
            temp = line.active_move_line_ids[0].lot_id
            if len(line.active_move_line_ids) != 1:
                raise UserError("批號只能有一筆")
            if len(temp.price_ids) == 0:
                """先增加一筆過往紀錄"""
                temp.write({
                    'price_ids': [(0, 0, {
                        'cost_change_per_unit': temp.product_id.standard_price
                    })]
                })
            self.per_unit_cost = temp.cost_total
            """計算過往成本 """
            self.past_cost = self.product_qty*self.per_unit_cost
            self.total_cost = self.count_cost + self.past_cost


    # @api.multi
    # def open_produce_product(self):
    #     res = super(CreatCost, self).action_assign()
    #     self.get_cost_change_per_unit()
    #     return res


class AutoBom(models.Model):
    _inherit = 'mrp.production'
    # def Auto_bombom(self):
    #     productlotAuto = self.env['stock.production.lot'].search([])
    #     for i in productlotAuto.filtered(lambda x:x.product_qty>0):
    #         print(i.name)
    #         print(i.product_qty)
    #
    #         bomline = self.env['mrp.bom.line'].search([('product_id', '=', i.product_id.id)])
    #         if len(bomline):
    #             print(bomline.bom_id.product_tmpl_id.name)
    #             res= self.env['mrp.production'].create({
    #                 'product_id' : bomline.bom_id.product_tmpl_id.id,
    #                 'product_qty' : i.product_qty,
    #                 'bom_id' : bomline.bom_id.id,
    #                 'product_uom_id': bomline.bom_id.product_tmpl_id.uom_id.id,
    #                 })
    #             res.action_assign()
    #
    #             lotname = res.move_raw_ids.active_move_line_ids.lot_id.name
    #
    #             lotexist=self.env['stock.production.lot'].search([('name','=',lotname),('product_id','=',res.product_id.id)])
    #
    #             if len(lotexist)==0:
    #                 lotexist = self.env['stock.production.lot'].create({
    #                     'name':lotname,
    #                     'product_id':res.product_id.id
    #                 })
    #             """增加自動生長判斷 true就跳自動生長"""
    #             if i.product_id.product_tmpl_id.product_is_auto:
    #                 produce_wizard = self.env['mrp.product.produce'].with_context({
    #                     'active_id': res.id,
    #                     'active_ids': [res.id],
    #                  }).create({
    #                     'product_qty': res.product_qty,
    #                     'lot_id':lotexist.id
    #                 })
    #                 for line in produce_wizard.produce_line_ids:
    #                     line.qty_done = line.qty_to_consume
    #                 if i.product_id.product_tmpl_id.product_is_auto:
    #                     produce_wizard.do_produce()
    #                     res.button_mark_done()

class DoProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    """將批號以及數量帶入按完生產鈕後跳出的wizard"""
    @api.model
    def default_get(self, fields):
        res = super(DoProduce, self).default_get(fields)
        print(res)
        """判斷produce_line_ids是否存在 避免系統錯誤"""
        if self._context and self._context.get('active_id'):
            # print(res['produce_line_ids'])
            if 'produce_line_ids' in fields:
                print(res['produce_line_ids'])
                line_temp = res['produce_line_ids'][0]
                #print(line_temp)

                for line in res['produce_line_ids']:
                    #print(line)
                    row = line[2]
                    #print(row)
                    row['qty_done'] = row['qty_to_consume']
                    #print(row['qty_done'])
                    #print(line)
                print(line_temp[2])
                #print(res)
                if 'lot_id' not in line_temp[2]:
                    raise UserError("請先將產品設定批號以及其數量")
                lot_temp = self.env['stock.production.lot'].browse(line_temp[2]['lot_id'])
                #print(lot_temp)
                lot_exist = self.env['stock.production.lot'].search([('name', '=', lot_temp.name), ('product_id', '=', res['product_id'])])
                #print(lot_exist)

                if len(lot_exist):
                    res['lot_id'] = lot_exist.id
                else:
                    lot_exist = self.env['stock.production.lot'].create({
                        'name': lot_temp.name,
                        'product_id': res['product_id']
                    })
                    res['lot_id'] = lot_exist.id
                #print(res)
        return res


    """按完生產紐之後 判斷使用者輸入數量是否有相符"""
    @api.multi
    def do_produce(self):
        res = super(DoProduce, self).do_produce()
        amout = 0
        for line in self.produce_line_ids:
            amout += line.qty_done
        print("13")
        if self.product_qty != amout:
            raise UserError("生成數量與完成數量不符")
        else:
            return res
