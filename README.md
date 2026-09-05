# Product Brand (Odoo 19)

Módulo genérico y reutilizable para la gestión de marcas comerciales de productos en Odoo 19 (Community y Enterprise), con integración directa a la tienda en línea (`website_sale`).

---

## 🚀 Características Principales

1. **Modelo de Marca (`product.brand`):**
   - Nombre de marca con soporte multi-idioma (traducible e indexado).
   - Logotipo de marca en alta resolución (campo Image).
   - Descripción enriquecida en formato HTML.
   - Estado activo/archivado lógico (`active`).
   - Contador inteligente de productos (`product_count`) optimizado mediante `_read_group`.
   - Botón inteligente (*stat button*) en el formulario para acceder directamente al catálogo de productos de la marca.
   - Subvista incrustada en pestañas con listado (`<list>`) de productos asociados.

2. **Extensión en Productos (`product.template` y `product.product`):**
   - Campo Many2one `brand_id` en la plantilla de productos.
   - Campo relacionado indexado y almacenado en las variantes (`product.product`).
   - Filtro de búsqueda *"Con Marca"* en el catálogo de productos.
   - Agrupador (*Group by*) por *"Marca"* en la vista de búsqueda.
   - Selector en la vista formulario en datos generales.

3. **Integración con Tienda en Línea (`website_sale`):**
   - Exhibición automática del logotipo de la marca (o badge de texto estilizado si no tiene logo) en la ficha de producto (`/shop/product`).
   - El logo/badge actúa como hipervínculo para filtrar automáticamente todos los productos de esa marca en el catálogo de la tienda (`/shop?brand=ID`).
   - Barra informativa interactiva en `/shop` indicando la marca filtrada activa y botón para limpiar el filtro.

4. **Menús y Accesos:**
   - **Ventas:** *Ventas → Productos → Marcas*.
   - **Inventario:** *Inventario → Productos → Marcas*.
   - **Sitio Web:** *Sitio Web → Comercio Electrónico → Marcas*.

5. **Multi-Empresa y Seguridad:**
   - Campo `company_id` con regla de seguridad `ir.rule` multi-empresa. Las marcas sin empresa son compartidas globalmente entre todas las sucursales.
   - Validación restrictiva que impide asignar marcas de una empresa a productos de otra.
   - Reglas de acceso `ir.model.access.csv` que permiten a visitantes web y usuarios del portal visualizar marcas y logos públicamente.

---

## 📦 Dependencias

Este módulo depende exclusivamente de aplicaciones oficiales de Odoo:
- `product`
- `sale`
- `stock`
- `website_sale`

---

## 🛠️ Instalación

### En entorno local o servidor:

1. Clonar o agregar el módulo en la carpeta de addons (por ejemplo `vendor-addons/` o `custom-addons/`):
   ```bash
   git clone https://github.com/cperna/product_brand.git -b 19.0
   ```

2. Actualizar la lista de aplicaciones en Odoo o instalar vía CLI:
   ```bash
   odoo -c /etc/odoo.conf -i product_brand -d <nombre_bd> --stop-after-init
   ```

3. Reiniciar el servicio de Odoo si aplica.

---

## 🧪 Pruebas Unitarias

Para ejecutar la suite de pruebas automatizadas del módulo:
```bash
odoo -c /etc/odoo.conf -u product_brand --test-enable --stop-after-init -d <nombre_bd>
```

---

## 📄 Licencia y Créditos

- **Autor:** Carlos Pernalete
- **Licencia:** LGPL-3
- **Versión:** 19.0.1.0.0
