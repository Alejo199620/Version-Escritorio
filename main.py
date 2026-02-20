import sys
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap
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

        # === CORREGIR RUTA DEL ICONO Y EVITAR DISTORSIÓN ===
        icon_path = resource_path(os.path.join("assets", "icons", "logo.ico"))

        if os.path.exists(icon_path):
            try:
                # Cargar el pixmap primero para verificar
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    print(
                        f"📐 Dimensiones originales: {pixmap.width()}x{pixmap.height()}"
                    )

                    # Crear un pixmap con fondo transparente del tamaño del icono estándar
                    # pero mantener la proporción del logo
                    target_size = 256  # Tamaño estándar para iconos
                    final_pixmap = QPixmap(target_size, target_size)
                    final_pixmap.fill(Qt.transparent)  # Fondo transparente

                    # Calcular posición para centrar el logo
                    from PyQt5.QtGui import QPainter

                    painter = QPainter(final_pixmap)

                    # Escalar manteniendo aspecto y centrar
                    if pixmap.width() > pixmap.height():
                        # Logo más ancho que alto
                        new_width = target_size - 40  # Dejar margen
                        new_height = int(pixmap.height() * new_width / pixmap.width())
                        x_offset = (target_size - new_width) // 2
                        y_offset = (target_size - new_height) // 2
                    else:
                        # Logo más alto que ancho
                        new_height = target_size - 40
                        new_width = int(pixmap.width() * new_height / pixmap.height())
                        x_offset = (target_size - new_width) // 2
                        y_offset = (target_size - new_height) // 2

                    # Escalar y dibujar
                    scaled_pixmap = pixmap.scaled(
                        new_width,
                        new_height,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                    painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
                    painter.end()

                    # Establecer el icono con el pixmap procesado
                    self.app.setWindowIcon(QIcon(final_pixmap))
                    print(
                        f"✅ Icono cargado y centrado correctamente desde: {icon_path}"
                    )
                else:
                    print(f"⚠️ El archivo {icon_path} está corrupto")
                    # Fallback a carga simple
                    self.app.setWindowIcon(QIcon(icon_path))
            except Exception as e:
                print(f"⚠️ Error al procesar el icono: {str(e)}")
                # Fallback a carga simple
                self.app.setWindowIcon(QIcon(icon_path))
        else:
            print(f"⚠️ No se encontró el icono en: {icon_path}")

        # Inicializar API client
        self.api_client = APIClient()

        # Mostrar ventana de login
        self.login_window = LoginWindow(self.api_client)
        self.login_window.show()

    def run(self):
        return self.app.exec_()


if __name__ == "__main__":
    app = AdminApplication()
    sys.exit(app.run())
