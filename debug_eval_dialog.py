"""
Reproduce crash: abre EvaluationConfigDialog directamente para ver el error exacto
"""
import sys, traceback
sys.path.insert(0, r"c:\Users\Henry\Desktop\admin-python - copia")

from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)

try:
    from views.evaluations_view import EvaluationConfigDialog

    class FakeApi:
        pass

    # Simular sin config_data (caso nuevo)
    print("-- Abriendo EvaluationConfigDialog sin config_data...")
    dlg = EvaluationConfigDialog(FakeApi(), modulo_id=1, config_data=None)
    print("-- Dialog creado OK, ejecutando...")
    dlg.exec()
    print("-- exec() completado OK")

except Exception as e:
    print(f"\n❌ CRASH: {e}")
    traceback.print_exc()

sys.exit(0)
