import os
import tempfile
import subprocess
import sys
import html as html_escape
import random
from datetime import datetime

class TagManagerModel:
    def generate_html(self, products):
        """Generates HTML content for the tags."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Etiquetas de Precios - {datetime.now().strftime('%d/%m/%Y')}</title>
            <style>
                @page {{ margin: 0.5cm; size: A4 portrait; }}
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                    background: white; color: black;
                    print-color-adjust: exact; -webkit-print-color-adjust: exact;
                    display: flex; flex-direction: column; align-items: center;
                    min-height: 100vh; justify-content: flex-start; padding: 0.5cm 0;
                }}
                .page-title {{
                    text-align: center; font-size: 23px; font-weight: bold;
                    margin-bottom: 0.8cm; margin-top: 0.8cm; color: #2c3e50;
                    letter-spacing: 2px; text-transform: uppercase;
                }}
                .price-grid {{
                    display: grid; grid-template-columns: 7cm 7cm;
                    grid-template-rows: repeat(7, 3.4cm); gap: 0.3cm;
                    width: 14.6cm; justify-content: center; align-content: start;
                }}
                .price-label {{
                    display: flex; flex-direction: column; align-items: center;
                    justify-content: center; background: white;
                    border: 2px solid #2c3e50; border-radius: 0.2cm;
                    padding: 0.4cm; text-align: center; height: 3.4cm; width: 100%;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden;
                }}
                .price-text {{
                    font-weight: 900; color: #2c3e50; margin-bottom: 0.3cm;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1); line-height: 1.1;
                }}
                .product-name {{
                    font-weight: bold; color: #34495e;
                    text-align: center; line-height: 1.3; max-width: 100%;
                    word-wrap: break-word; hyphens: auto; overflow: hidden;
                    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
                }}
                .empty-label {{
                    border: 2px dashed #bdc3c7 !important; background: #f8f9fa !important;
                    color: #95a5a6; font-style: italic; font-size: 0.38cm;
                }}
                @media print {{
                    body {{ margin: 0; padding: 0.3cm 0; }}
                    .price-grid {{ page-break-inside: avoid; }}
                    .price-label {{ page-break-inside: avoid; box-shadow: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="page-title">ETIQUETAS DE PRECIOS</div>
            <div class="price-grid">
        """
        
        products_to_show = products[:14]
        
        for product in products_to_show:
            price_formatted = self.format_price_chilean(product['price'])
            price_text = f"${price_formatted}"
            price_font_size = self.calculate_price_font_size(price_text)
            product_name_escaped = html_escape.escape(product['name'])
            name_font_size = self.calculate_product_name_font_size(product['name'])

            html_content += f"""
                <div class="price-label">
                    <div class="price-text" style="font-size: {price_font_size};">
                        {price_text}
                    </div>
                    <div class="product-name" style="font-size: {name_font_size};">
                        {product_name_escaped}
                    </div>
                </div>
            """
            
        for i in range(len(products_to_show), 14):
            html_content += """
                <div class="price-label empty-label">
                    <div>Espacio<br>disponible</div>
                </div>
            """
            
        html_content += "</div></body></html>"
        return html_content

    def format_price_chilean(self, price):
        try:
            return f"{int(round(price)):,}".replace(",", ".")
        except (ValueError, OverflowError):
            return str(int(price))

    def calculate_price_font_size(self, price_text):
        length = len(price_text)
        if length <= 4: return "1.2cm"
        elif length <= 6: return "1.1cm"
        elif length <= 8: return "1.0cm"
        elif length <= 10: return "0.90cm"
        elif length <= 12: return "0.80cm"
        elif length <= 14: return "0.8cm"
        else: return "0.7cm"

    def calculate_product_name_font_size(self, product_name):
        """Calcula el tamaño de fuente del nombre del producto según su longitud."""
        length = len(product_name)
        if length <= 20: return "0.48cm"      # Nombres cortos
        elif length <= 35: return "0.43cm"    # Nombres medianos
        elif length <= 50: return "0.38cm"    # Nombres largos
        elif length <= 70: return "0.35cm"    # Nombres muy largos
        elif length <= 90: return "0.32cm"    # Nombres extra largos (Igenix ejemplo)
        else: return "0.30cm"                 # Nombres excepcionalmente largos

    def print_tags(self, products):
        if not products: return False, "No hay productos válidos."
        
        try:
            html_content = self.generate_html(products)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name
                
            if sys.platform.startswith('win'):
                os.startfile(temp_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', temp_path])
            else:
                subprocess.run(['xdg-open', temp_path])
                
            return True, temp_path
        except Exception as e:
            return False, str(e)
            
    def cleanup_temp_file(self, path):
        try:
            if os.path.exists(path): os.unlink(path)
        except Exception: pass

    def generate_offer_html(self, offers):
        """Generates HTML content for offer tags with modern design."""
        promo_texts = ['OFERTA', 'IMPERDIBLE', 'APROVECHA', 'NO TE LO PIERDAS']

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Etiquetas de Ofertas - {datetime.now().strftime('%d/%m/%Y')}</title>
            <style>
                @page {{ margin: 0.5cm; size: A4 portrait; }}
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                    background: white; color: #1a1a2e;
                    print-color-adjust: exact; -webkit-print-color-adjust: exact;
                    display: flex; flex-direction: column; align-items: center;
                    min-height: 100vh; justify-content: flex-start; padding: 0.5cm 0;
                }}
                .page-title {{
                    text-align: center; font-size: 22px; font-weight: 800;
                    margin-bottom: 0.8cm; margin-top: 0.8cm; color: #1a1a2e;
                    letter-spacing: 3px; text-transform: uppercase;
                }}
                .offer-grid {{
                    display: grid; grid-template-columns: 7cm 7cm;
                    grid-template-rows: repeat(2, 9.5cm); gap: 0.4cm;
                    width: 14.8cm; justify-content: center; align-content: start;
                }}

                /* --- Etiqueta base --- */
                .offer-label {{
                    display: flex; flex-direction: column;
                    background: #ffffff;
                    border: none; border-radius: 0;
                    height: 9.5cm; width: 100%;
                    overflow: hidden; position: relative;
                }}
                .offer-header {{
                    padding: 0.3cm 0.5cm; flex-shrink: 0;
                    display: flex; align-items: center; justify-content: space-between;
                }}
                .offer-header-label {{
                    font-size: 0.32cm; font-weight: 800; letter-spacing: 2px;
                    text-transform: uppercase; color: white;
                }}
                .offer-header-badge {{
                    font-size: 0.28cm; font-weight: 700; color: white;
                    opacity: 0.85; letter-spacing: 1px;
                }}
                .offer-content {{
                    flex: 1; display: flex; flex-direction: column;
                    align-items: center; justify-content: center;
                    padding: 0.3cm 0.5cm; text-align: center;
                }}
                .offer-footer {{
                    padding: 0.35cm 0.5cm; flex-shrink: 0;
                    text-align: center; font-size: 0.50cm; font-weight: 900;
                    letter-spacing: 2px; color: white;
                }}

                /* --- Colores por tipo --- */
                .type-normal .offer-header {{ background: #c0392b; }}
                .type-normal .offer-footer {{ background: #c0392b; }}
                .type-normal {{ border-left: 5px solid #c0392b; border-right: 5px solid #c0392b; }}

                .type-percentage .offer-header {{ background: #e67e22; }}
                .type-percentage .offer-footer {{ background: #e67e22; }}
                .type-percentage {{ border-left: 5px solid #e67e22; border-right: 5px solid #e67e22; }}

                .type-quantity .offer-header {{ background: #8e44ad; }}
                .type-quantity .offer-footer {{ background: #8e44ad; }}
                .type-quantity {{ border-left: 5px solid #8e44ad; border-right: 5px solid #8e44ad; }}

                .type-daily .offer-header {{ background: #2980b9; }}
                .type-daily .offer-footer {{ background: #2980b9; }}
                .type-daily {{ border-left: 5px solid #2980b9; border-right: 5px solid #2980b9; }}

                /* --- Tipografía --- */
                .product-name-offer {{
                    font-weight: 700; color: #2c3e50; font-size: 0.50cm;
                    line-height: 1.35; max-height: 1.8cm; overflow: hidden;
                    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
                    margin-bottom: 0.25cm; letter-spacing: 0.3px;
                }}
                .price-before {{
                    font-size: 0.42cm; color: #95a5a6; text-decoration: line-through;
                    font-weight: 600; margin-bottom: 0.15cm;
                }}
                .price-now {{
                    font-size: 1.5cm; color: #1a1a2e; font-weight: 900;
                    font-family: 'Arial Black', 'Impact', sans-serif;
                    line-height: 1;
                }}
                .price-symbol {{
                    font-size: 0.8cm; vertical-align: super; font-weight: 800;
                }}

                /* Porcentaje */
                .pct-badge {{
                    font-size: 1.8cm; color: #e67e22; font-weight: 900;
                    font-family: 'Arial Black', 'Impact', sans-serif;
                    line-height: 1; margin-bottom: 0.1cm;
                }}
                .pct-label {{
                    font-size: 0.32cm; color: #e67e22; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.2cm;
                }}
                .pct-prices {{
                    display: flex; align-items: baseline; gap: 0.4cm;
                    margin-top: 0.15cm;
                }}
                .pct-price-before {{
                    font-size: 0.42cm; color: #95a5a6; text-decoration: line-through;
                    font-weight: 600;
                }}
                .pct-price-now {{
                    font-size: 1.1cm; color: #1a1a2e; font-weight: 900;
                    font-family: 'Arial Black', 'Impact', sans-serif;
                }}

                /* Cantidad */
                .qty-display {{
                    display: flex; align-items: baseline; gap: 0.2cm;
                    margin: 0.2cm 0;
                }}
                .qty-number {{
                    font-size: 1.8cm; color: #8e44ad; font-weight: 900;
                    font-family: 'Arial Black', 'Impact', sans-serif;
                    line-height: 1;
                }}
                .qty-x {{
                    font-size: 0.8cm; color: #8e44ad; font-weight: 800;
                }}
                .qty-price {{
                    font-size: 1.3cm; color: #1a1a2e; font-weight: 900;
                    font-family: 'Arial Black', 'Impact', sans-serif;
                    line-height: 1;
                }}

                /* Producto del Día */
                .daily-badge {{
                    font-size: 0.38cm; color: #2980b9; font-weight: 800;
                    text-transform: uppercase; letter-spacing: 3px;
                    border: 2px solid #2980b9; padding: 0.12cm 0.4cm;
                    margin-bottom: 0.35cm;
                }}
                .daily-price {{
                    font-size: 1.5cm; color: #1a1a2e; font-weight: 900;
                    font-family: 'Arial Black', 'Impact', sans-serif;
                    line-height: 1; margin-top: 0.2cm;
                }}

                /* Vacío */
                .empty-offer {{
                    border: 2px dashed #dee2e6 !important; background: #f8f9fa !important;
                    color: #adb5bd; font-style: italic; display: flex;
                    align-items: center; justify-content: center; font-size: 0.40cm;
                }}

                @media print {{
                    body {{ margin: 0; padding: 0.3cm 0; }}
                    .offer-grid {{ page-break-inside: avoid; }}
                    .offer-label {{ page-break-inside: avoid; }}
                }}
            </style>
        </head>
        <body>
            <div class="page-title">ETIQUETAS DE OFERTAS</div>
            <div class="offer-grid">
        """

        type_headers = {
            'normal': 'Oferta Especial',
            'percentage': 'Descuento',
            'quantity': 'Oferta por Cantidad',
            'daily': 'Destacado del Día',
        }

        for offer in offers:
            if offer['type'] == 'normal':
                promo_text = random.choice(promo_texts)
                product_escaped = html_escape.escape(offer['product'])
                price_before = self.format_price_chilean(offer['price_before'])
                price_now = self.format_price_chilean(offer['price_now'])

                html_content += f"""
                <div class="offer-label type-normal">
                    <div class="offer-header">
                        <span class="offer-header-label">{type_headers['normal']}</span>
                    </div>
                    <div class="offer-content">
                        <div class="product-name-offer">{product_escaped}</div>
                        <div class="price-before">Antes: ${price_before}</div>
                        <div class="price-now"><span class="price-symbol">$</span>{price_now}</div>
                    </div>
                    <div class="offer-footer">{promo_text}</div>
                </div>
                """

            elif offer['type'] == 'percentage':
                promo_text = random.choice(promo_texts)
                product_escaped = html_escape.escape(offer['product'])
                percentage = offer['percentage']
                price_before = self.format_price_chilean(offer['price_before'])
                price_now = self.format_price_chilean(offer['price_now'])

                html_content += f"""
                <div class="offer-label type-percentage">
                    <div class="offer-header">
                        <span class="offer-header-label">{type_headers['percentage']}</span>
                        <span class="offer-header-badge">{percentage} OFF</span>
                    </div>
                    <div class="offer-content">
                        <div class="product-name-offer">{product_escaped}</div>
                        <div class="pct-badge">{percentage}</div>
                        <div class="pct-label">de descuento</div>
                        <div class="pct-prices">
                            <span class="pct-price-before">${price_before}</span>
                            <span class="pct-price-now"><span class="price-symbol">$</span>{price_now}</span>
                        </div>
                    </div>
                    <div class="offer-footer">{promo_text}</div>
                </div>
                """

            elif offer['type'] == 'quantity':
                promo_text = random.choice(promo_texts)
                product_escaped = html_escape.escape(offer['product'])
                quantity = offer['quantity']
                price = self.format_price_chilean(offer['price'])

                html_content += f"""
                <div class="offer-label type-quantity">
                    <div class="offer-header">
                        <span class="offer-header-label">{type_headers['quantity']}</span>
                    </div>
                    <div class="offer-content">
                        <div class="product-name-offer">{product_escaped}</div>
                        <div class="qty-display">
                            <span class="qty-number">{quantity}</span>
                            <span class="qty-x">x</span>
                            <span class="qty-price"><span class="price-symbol">$</span>{price}</span>
                        </div>
                    </div>
                    <div class="offer-footer">{promo_text}</div>
                </div>
                """

            elif offer['type'] == 'daily':
                promo_text = random.choice(promo_texts)
                product_escaped = html_escape.escape(offer['product'])
                price = self.format_price_chilean(offer['price'])

                html_content += f"""
                <div class="offer-label type-daily">
                    <div class="offer-header">
                        <span class="offer-header-label">{type_headers['daily']}</span>
                    </div>
                    <div class="offer-content">
                        <div class="daily-badge">Producto del Día</div>
                        <div class="product-name-offer">{product_escaped}</div>
                        <div class="daily-price"><span class="price-symbol">$</span>{price}</div>
                    </div>
                    <div class="offer-footer">{promo_text}</div>
                </div>
                """

            elif offer['type'] == 'empty':
                html_content += """
                <div class="offer-label empty-offer">
                    <div>Espacio<br>disponible</div>
                </div>
                """

        html_content += "</div></body></html>"
        return html_content

    def print_offers(self, offers):
        """Prints offer tags to HTML and opens in browser."""
        if not offers or all(o['type'] == 'empty' for o in offers):
            return False, "No hay ofertas válidas."

        try:
            html_content = self.generate_offer_html(offers)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name

            if sys.platform.startswith('win'):
                os.startfile(temp_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', temp_path])
            else:
                subprocess.run(['xdg-open', temp_path])

            return True, temp_path
        except Exception as e:
            return False, str(e)
