"""
Test con autenticación real para reproducir el crash de "Configurar Evaluación"
"""
import sys, traceback
sys.path.insert(0, r"c:\Users\Henry\Desktop\admin-python - copia")

import os
os.environ.setdefault("API_URL", "http://localhost:8000/api")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
app = QApplication(sys.argv)

from controllers.api_client import APIClient

api = APIClient()
print("Haciendo login...")
login_result = api.login("alejo29.c@gmail.com", "Password123")
print(f"Login result: success={login_result.get('success')}")

if not login_result.get("success"):
    print("❌ Login falló")
    sys.exit(1)

# Obtener módulos
mods_result = api.get_modulos()
if not mods_result.get("success"):
    print("❌ get_modulos falló")
    sys.exit(1)

modulos = mods_result.get("data", [])
if not modulos:
    print("❌ No hay módulos")
    sys.exit(1)

modulo = modulos[0]
print(f"Módulo: {modulo.get('id')} - {modulo.get('titulo')}")

# Obtener evaluación
print("\nLlamando get_evaluacion...")
try:
    result = api.get_evaluacion(modulo["id"], force_refresh=True)
    print(f"get_evaluacion result: success={result.get('success')}, data type={type(result.get('data'))}")
    print(f"Response keys: {list(result.keys())}")
    if result.get("data"):
        print(f"Eval data keys: {list(result['data'].keys()) if isinstance(result['data'], dict) else result['data']}")
except Exception as e:
    print(f"\n❌ CRASH en get_evaluacion: {e}")
    traceback.print_exc()
    sys.exit(1)

# Ahora abrir el EvaluationConfigDialog
print("\nAbriendo EvaluationConfigDialog...")
try:
    from views.evaluations_view import EvaluationConfigDialog
    eval_data = result.get("data")
    dlg = EvaluationConfigDialog(api, modulo["id"], eval_data)
    print("Dialog creado OK")
    
    # No hacemos exec() para que no se quede esperando
    dlg.show()
    QTimer.singleShot(1000, app.quit)  # Cerrar en 1 segundo
    app.exec()
    print("Dialog cerrado OK")
    
except Exception as e:
    print(f"\n❌ CRASH en EvaluationConfigDialog: {e}")
    traceback.print_exc()

print("\n✅ Test completado")
sys.exit(0)
