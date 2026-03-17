import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFontDatabase, QPalette, QColor
from PyQt6.QtCore import Qt


def apply_light_palette(app: QApplication):
    """Fuerza siempre el tema claro, sin importar la configuración del sistema."""
    palette = QPalette()

    # --- Colores base blancos/claros ---
    white   = QColor("#ffffff")
    light   = QColor("#f8f9fa")  # fondo de ventanas/widgets
    mid     = QColor("#e9ecef")
    dark    = QColor("#dee2e6")
    text    = QColor("#1e293b")  # texto principal
    dimtext = QColor("#64748b")  # texto secundario/deshabilitado

    # --- Selección: azul claro con texto negro ---
    highlight     = QColor("#bfdbfe")  # azul claro suave
    highlightText = QColor("#1e293b")  # texto oscuro sobre azul

    # Window / base
    palette.setColor(QPalette.ColorRole.Window,          light)
    palette.setColor(QPalette.ColorRole.WindowText,      text)
    palette.setColor(QPalette.ColorRole.Base,            white)
    palette.setColor(QPalette.ColorRole.AlternateBase,   light)
    palette.setColor(QPalette.ColorRole.ToolTipBase,     white)
    palette.setColor(QPalette.ColorRole.ToolTipText,     text)

    # Text
    palette.setColor(QPalette.ColorRole.Text,            text)
    palette.setColor(QPalette.ColorRole.PlaceholderText, dimtext)
    palette.setColor(QPalette.ColorRole.BrightText,      text)

    # Buttons
    palette.setColor(QPalette.ColorRole.Button,          light)
    palette.setColor(QPalette.ColorRole.ButtonText,      text)

    # Borders / mid tones
    palette.setColor(QPalette.ColorRole.Mid,             mid)
    palette.setColor(QPalette.ColorRole.Midlight,        mid)
    palette.setColor(QPalette.ColorRole.Dark,            dark)
    palette.setColor(QPalette.ColorRole.Shadow,          QColor("#adb5bd"))
    palette.setColor(QPalette.ColorRole.Light,           white)

    # Selection (azul claro, texto oscuro legible)
    palette.setColor(QPalette.ColorRole.Highlight,       highlight)
    palette.setColor(QPalette.ColorRole.HighlightedText, highlightText)

    # Links
    palette.setColor(QPalette.ColorRole.Link,            QColor("#2563eb"))
    palette.setColor(QPalette.ColorRole.LinkVisited,     QColor("#7c3aed"))

    # Disabled state (apenas más tenue)
    for role in [
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ]:
        palette.setColor(QPalette.ColorGroup.Disabled, role, dimtext)

    app.setPalette(palette)

    # Refuerzo a nivel global de stylesheet para tablas, listas e inputs
    app.setStyleSheet("""
        QTableView::item:selected,
        QListWidget::item:selected,
        QListView::item:selected,
        QTreeView::item:selected {
            background-color: #bfdbfe;
            color: #1e293b;
        }
        QTableView::item:selected:active,
        QListWidget::item:selected:active,
        QListView::item:selected:active {
            background-color: #93c5fd;
            color: #1e293b;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #bfdbfe;
            color: #1e293b;
        }
    """)


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


def load_custom_fonts():
    """Registra las fuentes personalizadas embebidas en assets/fonts."""
    fonts_base = resource_path(os.path.join("assets", "fonts"))
    registered = 0
    for root, dirs, files in os.walk(fonts_base):
        for filename in files:
            if filename.lower().endswith((".ttf", ".otf")):
                font_path = os.path.join(root, filename)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    registered += 1
                else:
                    print(f"[WARNING] No se pudo cargar la fuente: {filename}")
    print(f"[OK] {registered} fuentes personalizadas registradas.")


class AdminApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")

        # Forzar siempre tema claro con selección azul visible
        apply_light_palette(self.app)

        # Registrar fuentes personalizadas
        load_custom_fonts()
        self.app.setApplicationName("Varchate Admin")

        # === CORREGIR RUTA DEL ICONO Y EVITAR DISTORSIÓN ===
        icon_path = resource_path(os.path.join("assets", "icons", "logo.ico"))

        if os.path.exists(icon_path):
            try:
                # Cargar el pixmap primero para verificar
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    print(
                        f"[INFO] Dimensiones originales: {pixmap.width()}x{pixmap.height()}"
                    )

                    # Crear un pixmap con fondo transparente del tamaño del icono estándar
                    # pero mantener la proporción del logo
                    target_size = 256  # Tamaño estándar para iconos
                    final_pixmap = QPixmap(target_size, target_size)
                    final_pixmap.fill(Qt.GlobalColor.transparent)  # Fondo transparente

                    # Calcular posición para centrar el logo
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
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
                    painter.end()

                    # Establecer el icono con el pixmap procesado
                    self.app.setWindowIcon(QIcon(final_pixmap))
                    print(
                        f"[OK] Icono cargado y centrado correctamente desde: {icon_path}"
                    )
                else:
                    print(f"[WARNING] El archivo {icon_path} está corrupto")
                    # Fallback a carga simple
                    self.app.setWindowIcon(QIcon(icon_path))
            except Exception as e:
                print(f"[WARNING] Error al procesar el icono: {str(e)}")
                # Fallback a carga simple
                self.app.setWindowIcon(QIcon(icon_path))
        else:
            print(f"[WARNING] No se encontró el icono en: {icon_path}")

        # Inicializar API client
        self.api_client = APIClient()

        # Mostrar ventana de login
        self.login_window = LoginWindow(self.api_client)
        self.login_window.show()

    def run(self):
        return self.app.exec()


if __name__ == "__main__":
    app = AdminApplication()
    sys.exit(app.run())
