import os
import tempfile
import subprocess
import sys
import html as html_escape
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
