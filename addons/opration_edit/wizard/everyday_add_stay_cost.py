from odoo import models, fields, api

class EverydayAddCost(models.Model):
    _name = 'everyday.add.cost'
    _description = '每日增加成本'

    def test(self):
        print('hello odoo')

    #之後做成每日檢查
    def everyday_add_stay_cost(self):
        print('每日增加成本')
        res=self.env['stock.production.lot'].search([])
        print(res)

        for i in res.filtered(lambda x: x.product_qty > 0):
            flag = 0
            print(i.product_id.id)
            bom=self.env['mrp.bom'].search([])
            print(bom)
            for b in bom:
                print(b.product_tmpl_id.id)
                if i.product_id.id == b.product_tmpl_id.id:
                    print('上面的')
                    i.write({
                        'price_ids': [(0, 0, {
                            'cost_change_per_unit':b.bom_cost
                        })]
                    })
                    flag=1
            if flag==0:
                print('下面的')
                i.write({
                    'price_ids': [(0, 0, {
                        'cost_change_per_unit': i.product_id.standard_price
                    })]
                })




            # if len(search_product_ishad_bom)==0:
            #     #如果是產品最初狀態
            #     i.id.write({
            #         'price_ids': [(0, 0, {
            #             'cost_change_per_unit': i.id.product_id.standard_price
            #         })]
            #     })
            # i.id.write({
            #     'price_ids': [(0, 0, {
            #         'cost_change_per_unit':search_product_ishad_bom.bom_cost
            #     })]
            # })
