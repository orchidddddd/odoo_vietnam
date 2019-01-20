from odoo import models, fields, api


class InheritStockMove(models.Model):
    _inherit = "stock.move"

    #記得要打開
    def _action_done(self):
        res=super(InheritStockMove,self)._action_done()
        print('move的action_done')
        print(self.move_line_ids.state)
        self.env['stock.move.line'].search([('id','=',self.move_line_ids.id)]).update_qty123()
        return res

class InheritStockQuant(models.Model):
    _inherit = "stock.move.line"

    future_quant_detail_ids = fields.One2many(comodel_name="future.quant.detail", inverse_name="detail_id")

    def update_qty123(self):
        if self.location_id.usage != 'internal' and self.location_dest_id.usage != 'internal':
            return True
        if self.location_id.usage == 'internal' and self.location_dest_id.usage == 'internal':
            return True
        if self.qty_done == 0:
            return True
        print(self.product_qty)
        # if self.location_id.usage=='supplier':
        #     if self.future_quant_detail_ids_flag is False:
        #         print('進入flag判斷')
        #         return True
        #
        # self.write({
        #     ' future_quant_detail_ids_flag': True
        # })

        quantity = self.qty_done
        if self.location_id.usage == 'internal':
            quantity = -self.qty_done
        print(quantity)
        # if self.location_id.usage not in ['internal', 'transit']:
        #     return self
        print('寫入')
        source = self.env['mrp.bom.line']

        detial = []
        time_sheet = []
        init_source = source.search([('product_id', '=', self.product_id.id)])
        print(init_source)
        # for init_source_line in init_source:
        #     i=0
        #     source+=init_source_line[i]
        #     i+=1
        print(source)
        final_source = 0
        while len(init_source) != 0:
            source += init_source
            print(source)
            tmp = source.search([('product_id', '=', init_source.bom_id.product_tmpl_id.id)])
            if len(tmp) == 0:
                final_source = init_source.bom_id
                print('進入是否為最終產品判斷')
                break
            else:
                init_source = tmp
        lot_temp = self.lot_id.name
        # print(lot_temp)
        # if self.lot_id.id is False:
        #     print('有進入沒有批次號判斷')
        #     lot_temp = self.move_id.lot_num
        #     print(self.move_id.lot_num)


        if len(init_source) == 0:
            # if len(self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.id)])):
            #     return True
            print('進入直接是最終產品部分')
            self.write({
                'future_quant_detail_ids': [(0, 0, {
                    'name': lot_temp,
                    'product_id': self.product_id.id,
                    'three_days_later_line': quantity,
                    'seven_days_later_line': quantity,
                    'fourteen_days_later_line': quantity,
                })]
            })
            print('source=0')
            print(self.lot_id.id)
            print(self.product_id.id)
            print(quantity)
            print(quantity)
            print(quantity)
            self.env['stock.production.lot'].search([('name', '=', self.lot_id.name)]).compute_future_day()

        else:
            days = 0
            print(self)
            print(self.lot_id.id)
            print(self.move_id.lot_num)
            print(lot_temp)
            for row in source:
                days += row.bom_id.bom_time
                for line in range(0, int(row.bom_id.bom_time)):
                    time_sheet.append(row.product_id.id)

                detial.append((0, 0, {
                    'name': lot_temp,
                    'product_id': row.product_id.id,
                    'three_days_later_line': 0,
                    'seven_days_later_line': 0,
                    'fourteen_days_later_line': 0,
                }))
                print('正常情況寫入')
                print(detial)
                print(self.lot_id.id)
                print(self.product_id.id)
                print(quantity)
                print(quantity)
                print(quantity)

            detial.append((0, 0, {
                'name': lot_temp,
                'product_id': final_source.product_tmpl_id.id,
                'three_days_later_line': 0,
                'seven_days_later_line': 0,
                'fourteen_days_later_line': 0,
            }))
            print('最終產品寫入')
            print(detial)
            print(self.lot_id.id)
            print(self.product_id.id)
            print(quantity)
            print(quantity)
            print(quantity)

            if len(time_sheet) < 14:
                for line in range(0, 14 - len(time_sheet)):
                    time_sheet.append(final_source.product_tmpl_id.id)

            print(time_sheet)

            for line in detial:
                if line[2]['product_id'] == time_sheet[2]:
                    line[2]['three_days_later_line'] = quantity
                if line[2]['product_id'] == time_sheet[6]:
                    line[2]['seven_days_later_line'] = quantity
                if line[2]['product_id'] == time_sheet[13]:
                    line[2]['fourteen_days_later_line'] = quantity

            self.write({
                'future_quant_detail_ids': detial,
            })

            print("最後寫入部分")
            print(self.env['stock.production.lot'].search([('name','=',self.lot_id.name)]))
            print(self.lot_id.name)
            self.env['stock.production.lot'].search([('name','=',self.lot_id.name)]).compute_future_day()
            # self.env['stock.production.lot'].compute_future_day()
        return True

class FutureQuantDetail(models.Model):
    _name = 'future.quant.detail'
    _description = '為了顯示未來預期數量'

    name = fields.Char(string='lot名稱')
    detail_id = fields.Many2one(comodel_name="stock.move.line")
    product_id = fields.Many2one(comodel_name='product.product')
    three_days_later_line = fields.Float()
    seven_days_later_line = fields.Float()
    fourteen_days_later_line = fields.Float()