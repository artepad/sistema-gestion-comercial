"""
Launcher para Sistema de Gestión Comercial
Ejecuta la aplicación con mensajes informativos
"""

import sys
import os

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=" * 70)
print(" SISTEMA DE GESTION COMERCIAL")
print("=" * 70)

try:
    print("\n[1/2] Cargando modulos...")
    from gestion_comercial.main import main
    print("      OK - Modulos cargados correctamente")

    print("\n[2/2] Iniciando aplicacion...")
    print("=" * 70)
    print()

    # Ejecutar aplicación
    main()

except KeyboardInterrupt:
    print("\n\nAplicacion interrumpida por el usuario")
    sys.exit(0)

except Exception as e:
    print(f"\n\nERROR CRITICO: {e}")
    print("\nDetalles del error:")
    import traceback
    traceback.print_exc()

    print("\n" + "=" * 70)
    print("La aplicacion se cerrara. Presiona Enter para salir...")
    input()
    sys.exit(1)
