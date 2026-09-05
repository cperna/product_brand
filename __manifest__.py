# -*- coding: utf-8 -*-
# Copyright 2026 Carlos Pernalete
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Product Brand',
    'version': '19.0.1.0.0',
    'category': 'Sales/Products',
    'summary': 'Manage product brands, logos and integrate with eCommerce store',
    'description': """
Product Brand for Odoo 19
=========================
A generic and reusable module to manage commercial product brands across Odoo:
* Brand model (product.brand) with logo, rich-text description, active state and product counter.
* Smart button in brand form to quickly view associated products.
* Product extension (product.template & product.product) with brand selector, search filters and grouping.
* eCommerce integration (website_sale): display brand logo or badge on product details page (/shop/product).
* Interactive eCommerce filtering: clicking brand logo/badge filters catalog products in /shop?brand=ID.
* Dedicated menus in Sales, Inventory and Website eCommerce catalogs.
* Multi-company security rules and public read access for eCommerce store visitors.
    """,
    'author': 'Carlos Pernalete',
    'website': 'https://github.com/cperna/product_brand',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'sale',
        'stock',
        'website_sale',
    ],
    'data': [
        'security/product_brand_security.xml',
        'security/ir.model.access.csv',
        'views/product_brand_views.xml',
        'views/product_template_views.xml',
        'views/website_sale_templates.xml',
        'views/menu_views.xml',
        'data/product_brand_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
