# -*- coding: utf-8 -*-
# Copyright 2026 Carlos Pernalete
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, fields, models


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'
    _order = 'sequence, name'

    name = fields.Char(
        string='Brand Name',
        required=True,
        index=True,
        translate=True,
    )
    logo = fields.Image(
        string='Logo',
        max_width=1024,
        max_height=1024,
    )
    description = fields.Html(
        string='Description',
        translate=True,
        sanitize=True,
    )
    product_ids = fields.One2many(
        comodel_name='product.template',
        inverse_name='brand_id',
        string='Products',
    )
    product_count = fields.Integer(
        string='Number of Products',
        compute='_compute_product_count',
        store=False,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        index=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        index=True,
        default=lambda self: self.env.company,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )

    @api.depends('product_ids')
    def _compute_product_count(self):
        """Calcula el número de productos asociados a cada marca usando _read_group."""
        count_data = dict(self.env['product.template']._read_group(
            domain=[('brand_id', 'in', self.ids)],
            groupby=['brand_id'],
            aggregates=['__count'],
        ))
        for brand in self:
            brand.product_count = count_data.get(brand, 0)

    def action_view_products(self):
        """Retorna la acción de ventana para ver los productos asociados a la marca."""
        self.ensure_one()
        return {
            'name': _('Products - %(brand)s', brand=self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('brand_id', '=', self.id)],
            'context': {
                'default_brand_id': self.id,
            },
        }
