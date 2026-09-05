# -*- coding: utf-8 -*-
# Copyright 2026 Carlos Pernalete
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route


class WebsiteSaleBrand(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values, **kwargs):
        """Inyecta el filtro de marca en el dominio de búsqueda de la tienda."""
        domain = super()._get_search_domain(search, category, attrib_values, **kwargs)
        brand_val = kwargs.get('brand') or request.httprequest.args.get('brand')
        if brand_val:
            try:
                brand_id = int(brand_val)
                domain += [('brand_id', '=', brand_id)]
            except (ValueError, TypeError):
                pass
        return domain

    @route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        """Extiende la tienda para pasar la marca activa al contexto de renderizado."""
        response = super().shop(
            page=page, category=category, search=search,
            min_price=min_price, max_price=max_price, ppg=ppg, **post
        )
        brand_val = post.get('brand') or request.httprequest.args.get('brand')
        if brand_val and hasattr(response, 'qcontext'):
            try:
                brand_id = int(brand_val)
                brand = request.env['product.brand'].sudo().browse(brand_id).exists()
                if brand:
                    response.qcontext['active_brand'] = brand
            except (ValueError, TypeError):
                pass
        return response
