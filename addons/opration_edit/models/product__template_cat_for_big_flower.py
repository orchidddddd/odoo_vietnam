from odoo import models, fields, api


class ProductTemplateCateForBigFlower(models.Model):
    _inherit = "product.template"

    product_state = fields.Selection(string="產品分類", selection=[('1', 'one-two flowers'), ('2', 'three-four flowers'), ('3', 'five-six flowers'), ('4', 'seven-eight flowers'), ('5', 'others')], required=False, )
    product_is_auto = fields.Boolean(string="是否為需要自動生長產品", default=True)