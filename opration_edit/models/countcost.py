from odoo import models, fields, api


class LotInherit(models.Model):
    _inherit = "stock.production.lot"

    price_ids = fields.One2many(comodel_name="cost.detail",inverse_name= "lot_id")
    cost_total= fields.Float(compute = "compute_cost", store=True)
    three_days_later = fields.Float()
    seven_days_later = fields.Float()
    fourteen_days_later = fields.Float()

    @api.depends('price_ids')
    def compute_cost(self):
        for line in self:
            sum=0
            for row in line.price_ids:
                sum+=row.cost_change_per_unit
            line.cost_total=sum

    def compute_future_day(self):
        for line in self:
            print('進入計算')
            print(line)
            res=self.env['future.quant.detail'].search([('name','=',line.id),('product_id','=',line.product_id.id)])
            print(res)
            day3=0
            day7=0
            day14=0
            for add in res:
                day3 += add.three_days_later_line
                day7 += add.seven_days_later_line
                day14 += add.fourteen_days_later_line
            line.three_days_later=day3
            line.seven_days_later=day7
            line.fourteen_days_later=day14


class CostDetail(models.Model):
    _name = 'cost.detail'

    name = fields.Char()
    lot_id = fields.Many2one(comodel_name="stock.production.lot")
    cost_change_per_unit = fields.Float()


class CountCostFuntion(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def button_mark_done(self):
        res=super(CountCostFuntion,self).button_mark_done()
        product_lot = 0
        for line in self.finished_move_line_ids:
            product_lot = line.lot_id
            #算前後數量差
            order_qty=product_lot.product_qty-self.product_qty
            #新的成本
            account_new_cost=(order_qty*product_lot.cost_total+self.total_cost)/product_lot.product_qty

            product_lot.write({
                'price_ids': [(0, 0, {
                    #新舊成本相減 存進成本變動
                    'cost_change_per_unit': account_new_cost-product_lot.cost_total
                })]
            })

        return res