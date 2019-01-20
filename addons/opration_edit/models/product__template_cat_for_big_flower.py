from odoo import models, fields, api


class ProductTemplateCateForBigFlower(models.Model):
    _inherit = "product.template"

    product_state = fields.Selection(string="產品分類", selection=[('1', '1-2'),
                                                               ('2', '3-4'),
                                                               ('3', '5-6'),
                                                               ('4', '7-8'),
                                                               ('5', '9-10'),
                                                               ('6', '11-'),
                                                               ('7', 'Mature'),
                                                               ('8', 'Stalk'),
                                                               ('9', 'Bud'),
                                                               ('10','History')], required=False, )
    product_is_auto = fields.Boolean(string="是否為需要自動生長產品", default=True)