# -*- coding: utf-8 -*-
# Copyright 2026 Carlos Pernalete
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import base64
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestProductBrand(TransactionCase):
    """Pruebas unitarias para el modelo product.brand y su integración con productos."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Pixel PNG 1x1 válido en base64 para pruebas de carga de logo
        cls.dummy_logo = b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='

        cls.brand_a = cls.env['product.brand'].create({
            'name': 'Brand Alpha',
            'description': '<p>Description of Brand Alpha</p>',
            'logo': cls.dummy_logo,
        })
        cls.brand_b = cls.env['product.brand'].create({
            'name': 'Brand Beta',
            'description': '<p>Description of Brand Beta</p>',
        })

        cls.product_1 = cls.env['product.template'].create({
            'name': 'Test Product 1',
            'brand_id': cls.brand_a.id,
        })
        cls.product_2 = cls.env['product.template'].create({
            'name': 'Test Product 2',
            'brand_id': cls.brand_a.id,
        })
        cls.product_3 = cls.env['product.template'].create({
            'name': 'Test Product 3',
            'brand_id': cls.brand_b.id,
        })

    def test_01_brand_creation(self):
        """Verifica la creación correcta de marcas y sus campos básicos."""
        self.assertEqual(self.brand_a.name, 'Brand Alpha')
        self.assertTrue(self.brand_a.active)
        self.assertTrue(bool(self.brand_a.logo))
        self.assertIn('Description of Brand Alpha', self.brand_a.description)

    def test_02_product_association_and_related(self):
        """Verifica la asociación de marca en template y la sincronización con product.product."""
        self.assertEqual(self.product_1.brand_id, self.brand_a)
        # Verificar campo relacionado en las variantes (product.product)
        variant = self.product_1.product_variant_ids[0]
        self.assertEqual(variant.brand_id, self.brand_a)

    def test_03_product_count_computation(self):
        """Verifica el cálculo de product_count y actualización dinámica."""
        self.assertEqual(self.brand_a.product_count, 2)
        self.assertEqual(self.brand_b.product_count, 1)

        # Crear un nuevo producto para Brand Beta
        self.env['product.template'].create({
            'name': 'Test Product 4',
            'brand_id': self.brand_b.id,
        })
        self.brand_b.invalidate_recordset(['product_count'])
        self.assertEqual(self.brand_b.product_count, 2)

        # Desvincular product_1 de Brand Alpha
        self.product_1.brand_id = False
        self.brand_a.invalidate_recordset(['product_count'])
        self.assertEqual(self.brand_a.product_count, 1)

    def test_04_action_view_products(self):
        """Verifica que la acción del botón inteligente retorne la vista y dominio correctos."""
        action = self.brand_a.action_view_products()
        self.assertEqual(action['res_model'], 'product.template')
        self.assertEqual(action['domain'], [('brand_id', '=', self.brand_a.id)])
        self.assertEqual(action['context']['default_brand_id'], self.brand_a.id)

    def test_05_brand_archiving(self):
        """Verifica el archivado lógico de marcas."""
        self.brand_a.active = False
        archived_brand = self.env['product.brand'].with_context(active_test=False).search([
            ('id', '=', self.brand_a.id)
        ])
        self.assertFalse(archived_brand.active)
        active_brands = self.env['product.brand'].search([('id', '=', self.brand_a.id)])
        self.assertFalse(active_brands)

    def test_06_multi_company_validation(self):
        """Valida que una marca de una empresa distinta no pueda asignarse a un producto de otra empresa."""
        company_other = self.env['res.company'].create({'name': 'Other Company'})
        brand_other = self.env['product.brand'].create({
            'name': 'Other Company Brand',
            'company_id': company_other.id,
        })
        product_main = self.env['product.template'].create({
            'name': 'Main Company Product',
            'company_id': self.env.company.id,
        })
        with self.assertRaises(ValidationError):
            product_main.brand_id = brand_other.id
