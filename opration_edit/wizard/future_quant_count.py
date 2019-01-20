from odoo import models, fields, api


class InheritStockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self):
        res=super(InheritStockMove,self)._action_done()
        print('move的action_done')
        print(self.move_line_ids.state)
        self.env['stock.move.line'].search([('id','=',self.move_line_ids.id)]).update_qty123()
        return res

class InheritStockQuant(models.Model):
    _inherit = "stock.move.line"

    future_quant_detail_ids = fields.One2many(comodel_name="future.quant.detail", inverse_name="detail_id")
    # qty_done = fields.Float(inverse='update_qty123')
    future_quant_detail_ids_flag=fields.Boolean(default=False)
    # state = fields.Selection(related='move_id.state', store=True , inverse='test')
    # done_move=fields.Boolean(inverse='test')
    # move_id= fields.Many2one(inverse='test2')

    def test(self):
        # if self.state=='done':
        print('開始執行')
        self.env['stock.production.lot'].search([('name','=',self.lot_id.name)]).compute_future_day()
        print('執行完畢')

    def test2(self):
        print(self.move_id)
        self.update_qty123()


    def update_qty123(self):
        if self.location_id.usage != 'internal' and self.location_dest_id.usage != 'internal':
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
        final_source = 0
        while len(init_source) != 0:

            source += init_source
            print(source)
            tmp = source.search([('product_id', '=', init_source.bom_id.product_tmpl_id.id)])
            if len(tmp) == 0:
                final_source = init_source.bom_id
                break
            else:
                init_source = tmp
        lot_temp = self.lot_id.id
        # print(lot_temp)
        # if self.lot_id.id is False:
        #     print('有進入沒有批次號判斷')
        #     lot_temp = self.move_id.lot_num
        #     print(self.move_id.lot_num)


        if len(source) == 0:
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
            print(self.env['stock.production.lot'].search([('id','=',self.lot_id.id)]))
            self.env['stock.production.lot'].search([('id','=',self.lot_id.id)]).compute_future_day()
            # self.env['stock.production.lot'].compute_future_day()
        return True

    # def _action_done(self):
    #     res=super(InheritStockQuant,self)._action_done()
    #     # print('進入done')
    #     # self.update_qty123()
    #     print(self.state)
    #     print(self.lot_id)
    #     return res
    #
    # def write(self, vals):
    #     res = super(InheritStockQuant, self).write(vals)
    #     print('進入write')
    #     print(self.state)
    #     print(self.lot_id)
    #     return res


    # @api.model
    # def create(self, vals):
    #     print(987)
    #     res = super(InheritStockQuant,self).create(vals)
    #     if res.location_id.usage != 'internal' and res.location_dest_id.usage !='internal':
    #         return res
    #     quantity=res.qty_done
    #     if res.location_id.usage == 'internal':
    #         quantity = -res.qty_done
    #     print(quantity)
    #     # if res.location_id.usage not in ['internal', 'transit']:
    #     #     return res
    #     print('寫入')
    #     source = self.env['mrp.bom.line']
    #
    #     detial = []
    #     time_sheet = []
    #     init_source = source.search([('product_id', '=', res.product_id.id)])
    #     final_source = 0
    #     while len(init_source) !=0:
    #
    #         source += init_source
    #         print(source)
    #         tmp = source.search([('product_id', '=', init_source.bom_id.product_tmpl_id.id)])
    #         if len(tmp) == 0:
    #             final_source = init_source.bom_id
    #             break
    #         else:
    #             init_source = tmp
    #     if len(source) == 0:
    #         res.write({
    #             'future_quant_detail_ids':[(0,0,{
    #                 'name': res.lot_id.name,
    #                 'product_id': res.product_id.id,
    #                 'three_days_later_line': quantity,
    #                 'seven_days_later_line': quantity,
    #                 'fourteen_days_later_line': quantity,
    #             })]
    #         })
    #
    #     else:
    #         days = 0
    #         for row in source:
    #             days += row.bom_id.bom_time
    #             for line in range(0, int(row.bom_id.bom_time)):
    #                 time_sheet.append(row.product_id.id)
    #
    #             detial.append((0, 0, {
    #                 'name': res.lot_id.name,
    #                 'product_id': row.product_id.id,
    #                 'three_days_later_line': 0,
    #                 'seven_days_later_line': 0,
    #                 'fourteen_days_later_line': 0,
    #             }))
    #
    #         detial.append((0, 0, {
    #             'name': res.lot_id.name,
    #             'product_id': final_source.product_tmpl_id.id,
    #             'three_days_later_line': 0,
    #             'seven_days_later_line': 0,
    #             'fourteen_days_later_line': 0,
    #         }))
    #
    #         if len(time_sheet) < 14:
    #             for line in range(0, 14-len(time_sheet)):
    #                 time_sheet.append(final_source.product_tmpl_id.id)
    #
    #         print(time_sheet)
    #
    #         for line in detial:
    #             if line[2]['product_id'] == time_sheet[2]:
    #                 line[2]['three_days_later_line'] = quantity
    #             if line[2]['product_id'] == time_sheet[6]:
    #                 line[2]['seven_days_later_line'] = quantity
    #             if line[2]['product_id'] == time_sheet[13]:
    #                 line[2]['fourteen_days_later_line'] = quantity
    #
    #         res.write({
    #             'future_quant_detail_ids': detial
    #         })
    #
    #         res.lot_id.compute_future_day()











                # day3 = 0
                # day7 = 0
                # day14 =0
                # days += row.bom_id.bom_time
                # if days >= 3:
                #     day3 = res.quantity
                # if days > 3 and days <= 7:
                #     day7 = res.quantity
                # if days > 7 and days <=14:
                #     day14 = res.quantity



            # tmp_day = 0
            # for line in range(0,len(detial)):


                # tmp_day += detial[line]['day']
                # if tmp_day > 3:
                #     detial[line]['three_days_later_line'] = res.quantity
                # if tmp_day > 3 and tmp_day <= 7:
                #     detial[line]['seven_days_later_line'] = res.quantity
                # if tmp_day > 7 and tmp_day <=14:
                #     detial[line]['fourteen_days_later_line'] = res.quantity


class FutureQuantDetail(models.Model):
    _name = 'future.quant.detail'
    _description = '為了顯示未來預期數量'

    name = fields.Char(string='lot名稱')
    detail_id = fields.Many2one(comodel_name="stock.move.line")
    product_id = fields.Many2one(comodel_name='product.product')
    three_days_later_line = fields.Float()
    seven_days_later_line = fields.Float()
    fourteen_days_later_line = fields.Float()
# class InheritStockQuant(models.Model):
#     _inherit = "stock.quant"
#
#     three_days_later = fields.Float()
#     seven_days_later = fields.Float()
#     fourteen_days_later = fields.Float()
#     future_quant_detail_ids = fields.One2many(comodel_name="future.quant.detail", inverse_name= "detail_id")
#
#
#
#
#
#
#
# class FutureQuantDetail(models.Model):
#     _name = 'future.quant.detail'
#     _description = '為了顯示未來預期數量'
#
#     name = fields.Char()
#     detail_id = fields.Many2one(comodel_name="stock.quant")
#     product_id = fields.Integer()
#     three_days_later_line = fields.Float()
#     seven_days_later_line = fields.Float()
#     fourteen_days_later_line = fields.Float()
#
#     def write_detail(self):
#         quant_temp = self.env['stock.quant'].search([])
#         print(quant_temp)
#         for quant_line in quant_temp:
#             three_day_quantity=0
#             seven_day_quantity=0
#             fourteen_day_quantity=0
#             bom_time=0
#             count = 0
#             flag=0
#             flag_for_high_level_product=0
#             product_id_temp = quant_line.product_id #暫存產品id
#             print(product_id_temp)
#             quantity = quant_line.quantity
#             print(quantity)
#
#
#             if quantity > 0:
#                 print('大於零')
#                 while flag==0:
#                     res = self.env['mrp.bom.line'].search([])
#                     print(product_id_temp)
#                     for bom_line in res:
#                         if bom_line.product_id.id== product_id_temp.id:
#                             break
#                     print(bom_line)
#                     bom_res=self.env['mrp.bom'].search([])
#                     for bom in bom_res:
#                         if bom.id == bom_line.bom_id.id:
#                             break
#                     print(bom)
#                     bom_time = bom_time+bom.bom_time
#                     print(bom_time)
#                     if count==0:
#                         if bom_time < 3:
#                             three_day_quantity = 0
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 3 and bom_time < 7:
#                             three_day_quantity = +quantity
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 7 and bom_time <= 14:
#                             three_day_quantity = quantity
#                             seven_day_quantity = +quantity
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 14:
#                             three_day_quantity = +quantity
#                             seven_day_quantity = +quantity
#                             fourteen_day_quantity = +quantity
#                         bom_time=0
#                     elif bom_time<3:
#                         three_day_quantity=0
#                         seven_day_quantity=0
#                         fourteen_day_quantity=0
#                     elif bom_time>=3 and bom_time<7:
#                         three_day_quantity = 0
#                         seven_day_quantity = +quantity
#                         fourteen_day_quantity = 0
#                     elif bom_time>=7 and bom_time<=14:
#                         three_day_quantity = 0
#                         seven_day_quantity = 0
#                         fourteen_day_quantity = quantity
#                     elif bom_time>=14:
#                         three_day_quantity = 0
#                         seven_day_quantity = 0
#                         fourteen_day_quantity = 0
#                     quant_line.write({
#                             'future_quant_detail_ids': [(0, 0, {
#                             'product_id':bom_line.product_id.id,
#                             'three_days_later_line':three_day_quantity,
#                             'seven_days_later_line':seven_day_quantity,
#                             'fourteen_days_later_line':fourteen_day_quantity
#                             })]
#                     })
#
#                     try:
#                         print('進入try')
#                         try_func_res=self.env['mrp.bom.line'].search([])
#                         for i in try_func_res:
#                             print(i.product_id.id)
#                             print(bom.product_tmpl_id.id)
#                             if i.product_id.id == bom.product_tmpl_id.id:
#                                 product_id_temp = i.product_id
#                                 count = 1
#                                 break
#                             flag = 1
#                             flag_for_high_level_product=1
#                             print(flag)
#                             product_id_temp = quant_line.product_id
#                             print(product_id_temp)
#                     except:
#                         print('出事了')
#                         flag=1
#                         product_id_temp=quant_line.product_id
#                     else:
#                         print('沒事')
#                 if flag_for_high_level_product==1:
#                     print('大於零部分最高層級')
#                     print(bom_time)
#                     high_level_res=self.env['mrp.bom'].search([])
#                     for high_level_line in high_level_res:
#                         if high_level_line.product_tmpl_id.id == bom.product_tmpl_id.id:
#                             bom_time+=high_level_line.bom_time
#                             break
#                     if count==0:
#                         if bom_time < 3:
#                             three_day_quantity = 0
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 3 and bom_time < 7:
#                             three_day_quantity = +quantity
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 7 and bom_time <= 14:
#                             three_day_quantity = quantity
#                             seven_day_quantity = +quantity
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 14:
#                             three_day_quantity = +quantity
#                             seven_day_quantity = +quantity
#                             fourteen_day_quantity = +quantity
#                         bom_time=0
#                     elif bom_time<3:
#                         three_day_quantity=0
#                         seven_day_quantity=0
#                         fourteen_day_quantity=0
#                     elif bom_time>=3 and bom_time<7:
#                         three_day_quantity = 0
#                         seven_day_quantity = +quantity
#                         fourteen_day_quantity = 0
#                     elif bom_time>=7 and bom_time<=14:
#                         three_day_quantity = 0
#                         seven_day_quantity = 0
#                         fourteen_day_quantity = quantity
#                     elif bom_time>=14:
#                         three_day_quantity = 0
#                         seven_day_quantity = 0
#                         fourteen_day_quantity = 0
#                     quant_line.write({
#                         'future_quant_detail_ids': [(0, 0, {
#                             'product_id':  bom.product_tmpl_id.id,
#                             'three_days_later_line': three_day_quantity,
#                             'seven_days_later_line': seven_day_quantity,
#                             'fourteen_days_later_line': fourteen_day_quantity
#                         })]
#                     })
#                     product_id_temp = quant_line.product_id
#
#             flag=0
#             flag_for_high_level_product =0
#             if quantity < 0:
#                 print('小於零的部分')
#                 while flag==0:
#                     minus_bom_line_res = self.env['mrp.bom.line'].search([])
#                     for minus_bom_line in minus_bom_line_res:
#                         if minus_bom_line.product_id.id == product_id_temp.id:
#                             print(minus_bom_line.product_id.id)
#                             break
#
#                     minus_bom_res = self.env['mrp.bom'].search([])
#                     for minus_bom in minus_bom_res:
#                         if minus_bom.id ==  minus_bom_line.bom_id.id:
#                             print(minus_bom.id)
#                             break
#                     bom_time = bom_time+minus_bom.bom_time
#                     print(bom_time)
#
#                     if count==0:
#                         if bom_time < 3:
#                             three_day_quantity = 0
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 3 and bom_time < 7:
#                             three_day_quantity = quantity
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 7 and bom_time <= 14:
#                             three_day_quantity = 0
#                             seven_day_quantity = quantity
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 14:
#                             three_day_quantity = 0
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = quantity
#                         print('count部分')
#                         bom_time = 0
#                     elif bom_time<3:
#                         three_day_quantity = 0
#                         seven_day_quantity = 0
#                         fourteen_day_quantity = 0
#                         print('小於3部分')
#                     elif bom_time >= 3 and bom_time < 7:
#                         three_day_quantity = 0
#                         seven_day_quantity = quantity
#                         fourteen_day_quantity = 0
#                         print('3-7之間')
#                     elif bom_time>=7 and bom_time<=14:
#                         three_day_quantity = 0
#                         seven_day_quantity = quantity
#                         fourteen_day_quantity = 0
#                         print('7-14之間')
#                     elif bom_time>=14:
#                         three_day_quantity = 0
#                         seven_day_quantity = 0
#                         fourteen_day_quantity = quantity
#                         print('14以上')
#                     quant_line.write({
#                         'future_quant_detail_ids': [(0, 0, {
#                             'product_id': minus_bom_line.product_id.id,
#                             'three_days_later_line': three_day_quantity,
#                             'seven_days_later_line': seven_day_quantity,
#                             'fourteen_days_later_line': fourteen_day_quantity
#                         })]
#                     })
#                     print('寫入資料')
#                     print(minus_bom_line.product_id.id)
#                     print(three_day_quantity)
#                     print(seven_day_quantity)
#                     print(fourteen_day_quantity)
#
#                     minus_func_res = self.env['mrp.bom.line'].search([])
#                     print('進入確定是否為最高層級')
#                     for i in minus_func_res:
#                         print(i.product_id.id)
#                         print(minus_bom.product_tmpl_id.id)
#                         if i.product_id.id == minus_bom.product_tmpl_id.id:
#                             product_id_temp = i.product_id
#                             count = 1
#                             break
#                         flag = 1
#                         flag_for_high_level_product = 1
#                         print(flag)
#                         product_id_temp = quant_line.product_id
#                         print(product_id_temp)
#
#                     if flag_for_high_level_product == 1:
#                         print('小於零部分最高層級')
#                         print(bom_time)
#                         minus_high_level_res=self.env['mrp.bom'].search([])
#                         for minus_high_level_line in minus_high_level_res:
#                             if minus_high_level_line.product_tmpl_id.id == minus_bom.product_tmpl_id.id:
#                                 bom_time+=minus_high_level_line.bom_time
#                                 print(bom_time)
#                                 break
#
#                         if bom_time < 3:
#                             three_day_quantity = 0
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 3 and bom_time < 7:
#                             three_day_quantity = 0
#                             seven_day_quantity = quantity
#                             fourteen_day_quantity = 0
#                         elif bom_time >= 7 and bom_time <= 14:
#                             three_day_quantity = 0
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = quantity
#                         elif bom_time >= 14:
#                             three_day_quantity = 0
#                             seven_day_quantity = 0
#                             fourteen_day_quantity = 0
#
#                         quant_line.write({
#                             'future_quant_detail_ids': [(0, 0, {
#                                 'product_id': minus_bom.product_tmpl_id.id,
#                                 'three_days_later_line': three_day_quantity,
#                                 'seven_days_later_line': seven_day_quantity,
#                                 'fourteen_days_later_line': fourteen_day_quantity
#                             })]
#                         })
#                         print('寫入資料')
#                         print(minus_bom_line.product_id.id)
#                         print(three_day_quantity)
#                         print(seven_day_quantity)
#                         print(fourteen_day_quantity)