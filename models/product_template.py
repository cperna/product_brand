# -*- coding: utf-8 -*-
# Copyright 2026 Carlos Pernalete
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one(
        comodel_name='product.brand',
        string='Brand',
        index=True,
        ondelete='set null',
        help='Select the commercial brand for this product.',
    )

    @api.constrains('brand_id', 'company_id')
    def _check_brand_company(self):
        """Valida que la marca pertenezca a la misma compañía del producto si ambas están definidas."""
        for template in self:
            if template.brand_id and template.brand_id.company_id and template.company_id:
                if template.brand_id.company_id != template.company_id:
                    raise ValidationError(
                        _('The selected brand "%(brand)s" belongs to a different company.',
                          brand=template.brand_id.name)
                    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Many2one(
        related='product_tmpl_id.brand_id',
        string='Brand',
        store=True,
        readonly=True,
        index=True,
    )
