import sys
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


# === AGREGAR ESTA FUNCIÓN AL INICIO ===
def resource_path(relative_path):
    """Obtiene la ruta correcta para recursos en desarrollo y producción"""
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Cargar variables de entorno - USANDO RESOURCE_PATH
env_path = resource_path(".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()  # Intentar carga normal

# Importar después de cargar las variables
from views.login_window import LoginWindow
from controllers.api_client import APIClient


class AdminApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        self.app.setApplicationName("Varchate Admin")

        # === AGREGAR ICONO DE LA APLICACIÓN ===
        icon_path = resource_path(os.path.join("assets", "logo.png"))
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
            print(f"Icono cargado desde: {icon_path}")
        else:
            print(f"⚠️ No se encontró el icono en: {icon_path}")

        # Inicializar API client
        self.api_client = APIClient()

        # Mostrar ventana de login
        self.login_window = LoginWindow(self.api_client)
        self.login_window.show()

    def run(self):
        return self.app.exec_()  # Nota: exec_() con guión bajo


if __name__ == "__main__":
    app = AdminApplication()
    sys.exit(app.run())
