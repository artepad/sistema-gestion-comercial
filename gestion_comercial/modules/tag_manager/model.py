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
        """Generates HTML content for offer tags."""
        promo_texts = ['OFERTA', 'IMPERDIBLE', 'APROVECHA']

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
                .offer-grid {{
                    display: grid; grid-template-columns: 7cm 7cm;
                    grid-template-rows: repeat(2, 9.5cm); gap: 0.3cm;
                    width: 14.6cm; justify-content: center; align-content: start;
                }}
                .offer-label {{
                    display: flex; flex-direction: column;
                    background: #FFD700; border: 3px solid #000;
                    border-radius: 0.2cm; height: 9.5cm; width: 100%;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.15); overflow: hidden;
                }}
                .offer-content {{
                    flex: 1; display: flex; flex-direction: column;
                    align-items: center; justify-content: center;
                    padding: 0.4cm 0.4cm 0.2cm 0.4cm; text-align: center;
                }}
                .offer-footer {{
                    background: #d32f2f; color: white; text-align: center;
                    padding: 0.4cm 0.3cm; font-size: 0.55cm; font-weight: 900;
                    letter-spacing: 1.5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                    flex-shrink: 0;
                }}
                .product-name-offer {{
                    font-weight: 700; color: #000; font-size: 0.55cm;
                    line-height: 1.3; max-height: 2cm; overflow: hidden;
                    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
                    margin-bottom: 0.3cm; font-family: 'Arial', sans-serif;
                }}
                .percentage-product-name {{
                    font-weight: 700; color: #000; font-size: 0.55cm;
                    line-height: 1.3; max-height: 2cm; overflow: hidden;
                    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
                    margin-bottom: 0.3cm; margin-top: 0.5cm; font-family: 'Arial', sans-serif;
                }}
                .price-before {{
                    font-size: 0.50cm; color: #333; text-decoration: line-through;
                    font-weight: 600; margin-bottom: 0.15cm; font-family: 'Arial', sans-serif;
                }}
                .price-now {{
                    font-size: 1.4cm; color: #000; font-weight: 900;
                    font-family: 'Arial Black', 'Arial', sans-serif;
                    margin: 0.2cm 0;
                }}
                .percentage-badge {{
                    font-size: 2cm; color: #000; font-weight: 900;
                    font-family: 'Arial Black', 'Arial', sans-serif;
                    margin: 0.2cm 0;
                }}
                .percentage-price-before {{
                    font-size: 0.45cm; color: #333; text-decoration: line-through;
                    font-weight: 600; margin-bottom: 0.1cm; font-family: 'Arial', sans-serif;
                }}
                .percentage-price-now {{
                    font-size: 1.1cm; color: #000; font-weight: 900;
                    font-family: 'Arial Black', 'Arial', sans-serif;
                    margin: 0.1cm 0;
                }}
                .quantity-offer {{
                    font-size: 1.5cm; color: #000; font-weight: 900;
                    margin: 0.4cm 0; font-family: 'Arial Black', 'Arial', sans-serif;
                }}
                .daily-product {{
                    font-size: 0.60cm; color: #d32f2f; font-weight: bold;
                    text-transform: uppercase; margin-bottom: 0.3cm;
                    font-family: 'Arial', sans-serif;
                }}
                .empty-offer {{
                    border: 2px dashed #bdc3c7 !important; background: #f8f9fa !important;
                    color: #95a5a6; font-style: italic; display: flex;
                    align-items: center; justify-content: center; font-size: 0.45cm;
                }}
                @media print {{
                    body {{ margin: 0; padding: 0.3cm 0; }}
                    .offer-grid {{ page-break-inside: avoid; }}
                    .offer-label {{ page-break-inside: avoid; box-shadow: none; }}
                }}
            </style>
        </head>
        <body>
            <div class="page-title">ETIQUETAS DE OFERTAS</div>
            <div class="offer-grid">
        """

        # Procesar las 4 ofertas
        for offer in offers:
            if offer['type'] == 'normal':
                promo_text = random.choice(promo_texts)
                product_escaped = html_escape.escape(offer['product'])
                price_before = self.format_price_chilean(offer['price_before'])
                price_now = self.format_price_chilean(offer['price_now'])

                html_content += f"""
                <div class="offer-label">
                    <div class="offer-content">
                        <div class="product-name-offer">{product_escaped}</div>
                        <div class="price-before">Antes: ${price_before}</div>
                        <div class="price-now">${price_now}</div>
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
                <div class="offer-label">
                    <div class="offer-content">
                        <div class="percentage-product-name">{product_escaped}</div>
                        <div class="percentage-badge">{percentage}</div>
                        <div class="percentage-price-before">Antes: ${price_before}</div>
                        <div class="percentage-price-now">${price_now}</div>
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
                <div class="offer-label">
                    <div class="offer-content">
                        <div class="product-name-offer">{product_escaped}</div>
                        <div class="quantity-offer">{quantity} x ${price}</div>
                    </div>
                    <div class="offer-footer">{promo_text}</div>
                </div>
                """

            elif offer['type'] == 'daily':
                promo_text = random.choice(promo_texts)
                product_escaped = html_escape.escape(offer['product'])
                price = self.format_price_chilean(offer['price'])

                html_content += f"""
                <div class="offer-label">
                    <div class="offer-content">
                        <div class="daily-product">Producto del Día</div>
                        <div class="product-name-offer">{product_escaped}</div>
                        <div class="price-now">${price}</div>
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
