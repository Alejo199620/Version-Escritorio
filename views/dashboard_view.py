from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QLinearGradient
from datetime import datetime
import locale
import logging
from utils.paths import resource_path

# Configurar locale en español para fechas
try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Linux/Mac
except:
    try:
        locale.setlocale(locale.LC_TIME, "Spanish_Colombia.1252")  # Windows
    except:
        try:
            locale.setlocale(locale.LC_TIME, "es_CO.UTF-8")  # Otra opción
        except:
            pass  # Si falla, usaremos formato manual

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class StatCard(QFrame):
    """Tarjeta de estadística con diseño profesional"""

    def __init__(self, title, value, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setObjectName("statCard")

        self.setStyleSheet(
            """
            QFrame#statCard {
                background-color: white;
                border-radius: 16px;
            }
        """
        )

        # Sombra suave
        self.setGraphicsEffect(self.create_shadow())

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(120)
        self.setMaximumHeight(140)

        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 15, 20, 15)

        # Barra decorativa lateral
        self.color_bar = QFrame()
        self.color_bar.setFixedWidth(4)
        self.color_bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
        layout.addWidget(self.color_bar)

        # Contenido
        content_layout = QVBoxLayout()
        content_layout.setSpacing(8)

        # Título
        title_label = QLabel(title.upper())
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: #7f8c8d; letter-spacing: 0.5px;")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Valor
        self.value_label = QLabel(str(value))
        self.value_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.value_label.setStyleSheet(f"color: {color};")
        self.value_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        content_layout.addWidget(title_label)
        content_layout.addWidget(self.value_label)

        layout.addLayout(content_layout, 1)
        layout.addStretch()

        self.setLayout(layout)

    def create_shadow(self):
        """Crear efecto de sombra"""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        return shadow

    def set_value(self, value):
        self.value_label.setText(str(value))


class LeccionesPorModuloCard(QFrame):
    """Tarjeta especial para mostrar lecciones por módulo"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modulosCard")

        self.setStyleSheet(
            """
            QFrame#modulosCard {
                background-color: white;
                border-radius: 16px;
            }
        """
        )

        self.setGraphicsEffect(self.create_shadow())
        self.setMinimumHeight(180)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title_layout = QHBoxLayout()
        title_label = QLabel("LECCIONES POR MÓDULO")  # Sin icono
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # Grid de módulos
        self.modulos_grid = QGridLayout()
        self.modulos_grid.setSpacing(12)
        self.modulos_grid.setVerticalSpacing(12)
        self.modulos_grid.setHorizontalSpacing(12)
        layout.addLayout(self.modulos_grid)

        self.setLayout(layout)

        # Datos de ejemplo
        self.modulos_data = []

    def create_shadow(self):
        """Crear efecto de sombra"""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        return shadow

    def update_data(self, modulos):
        """Actualizar datos de módulos"""
        # Limpiar grid
        self.clear_layout(self.modulos_grid)

        # Ordenar por orden_global
        modulos_ordenados = sorted(modulos, key=lambda x: x.get("orden_global", 999))

        # Mostrar hasta 6 módulos (2 filas de 3)
        for i, modulo in enumerate(modulos_ordenados[:6]):
            titulo = modulo.get("titulo", "Módulo")
            lecciones = modulo.get("lecciones_count", 0)

            # Crear item de módulo
            item = self.create_modulo_item(titulo, lecciones)
            row = i // 3
            col = i % 3
            self.modulos_grid.addWidget(item, row, col)

    def create_modulo_item(self, titulo, lecciones):
        """Crear item individual de módulo"""
        item = QFrame()
        item.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
            }
            QFrame:hover {
                background-color: #e9ecef;
            }
        """
        )
        item.setFixedHeight(70)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(12, 8, 12, 8)

        # Contenido
        content_layout = QVBoxLayout()
        content_layout.setSpacing(4)

        titulo_label = QLabel(titulo[:20] + "..." if len(titulo) > 20 else titulo)
        titulo_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        titulo_label.setStyleSheet("color: #2c3e50;")

        lecciones_label = QLabel(f"{lecciones} lecciones")
        lecciones_label.setFont(QFont("Segoe UI", 10))
        lecciones_label.setStyleSheet("color: #7f8c8d;")

        content_layout.addWidget(titulo_label)
        content_layout.addWidget(lecciones_label)

        layout.addLayout(content_layout)
        layout.addStretch()

        return item

    def clear_layout(self, layout):
        """Limpiar layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class DashboardView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.cards = {}
        self.modulos = []
        self.setup_ui()
        self.load_stats()

        # Auto-refresh cada 30 segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_stats)
        self.timer.start(30000)

    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Fecha en español (Colombia)
        self.date_label = QLabel()
        self.date_label.setFont(QFont("Segoe UI", 11))
        self.date_label.setStyleSheet(
            """
            QLabel {
                color: #64748b;
                padding: 8px 16px;
                background-color: #f8fafc;
                border-radius: 20px;
            }
        """
        )
        self.update_date()

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.date_label)

        main_layout.addLayout(header_layout)

        # Grid superior - 3 tarjetas principales
        top_grid = QGridLayout()
        top_grid.setSpacing(20)

        # Tarjetas (sin iconos en el título, solo texto)
        cards_data = [
            ("usuarios", "USUARIOS REGISTRADOS", "#3b82f6"),
            ("modulos", "MÓDULOS", "#10b981"),
            ("certificaciones", "CERTIFICADOS", "#f59e0b"),
        ]

        positions = [(0, 0), (0, 1), (0, 2)]

        for i, (key, title_text, color) in enumerate(cards_data):
            card = StatCard(title_text, "0", color)
            self.cards[key] = card
            row, col = positions[i]
            top_grid.addWidget(card, row, col)

        main_layout.addLayout(top_grid)

        # Sección de Lecciones por Módulo (sin icono)
        lecciones_label = QLabel("Lecciones por Módulo")
        lecciones_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        lecciones_label.setStyleSheet("color: #1e293b; margin-top: 10px;")
        main_layout.addWidget(lecciones_label)

        # Tarjeta de módulos
        self.modulos_card = LeccionesPorModuloCard()
        main_layout.addWidget(self.modulos_card)

        # Botón actualizar
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.refresh_btn = QPushButton("Actualizar Datos")
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """
        )
        self.refresh_btn.clicked.connect(self.load_stats)
        button_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_date(self):
        """Actualizar fecha en formato Colombia"""
        now = datetime.now()

        # Diccionario de meses en español
        meses = {
            1: "enero",
            2: "febrero",
            3: "marzo",
            4: "abril",
            5: "mayo",
            6: "junio",
            7: "julio",
            8: "agosto",
            9: "septiembre",
            10: "octubre",
            11: "noviembre",
            12: "diciembre",
        }

        # Diccionario de días de la semana en español
        dias = {
            0: "lunes",
            1: "martes",
            2: "miércoles",
            3: "jueves",
            4: "viernes",
            5: "sábado",
            6: "domingo",
        }

        dia_semana = dias[now.weekday()]
        dia = now.day
        mes = meses[now.month]
        año = now.year
        hora = (
            now.strftime("%I:%M %p").lower().replace("am", "a.m.").replace("pm", "p.m.")
        )

        # Formato: "viernes 14 de febrero, 2025 • 03:30 p.m."
        fecha_str = f"{dia_semana} {dia} de {mes}, {año} • {hora}"

        self.date_label.setText(fecha_str)

    def load_stats(self):
        """Cargar estadísticas desde la API"""
        # Mostrar loading
        for card in self.cards.values():
            card.set_value("...")

        # Cargar estadísticas del dashboard
        result = self.api_client.get_dashboard_stats()

        # Cargar módulos para lecciones por módulo
        modulos_result = self.api_client.get_modulos()

        if result["success"]:
            data = result.get("data", {})
            self.update_date()

            if isinstance(data, dict):
                usuarios = data.get("usuarios", {})
                contenido = data.get("contenido", {})
                certificaciones = data.get("certificaciones", {})

                # Actualizar tarjetas principales
                self.cards["usuarios"].set_value(usuarios.get("total", 0))
                self.cards["modulos"].set_value(contenido.get("modulos", 0))
                self.cards["certificaciones"].set_value(certificaciones.get("total", 0))

                logger.debug(f"Datos actualizados: {data}")
        else:
            # Datos de ejemplo para desarrollo
            self.cards["usuarios"].set_value(156)
            self.cards["modulos"].set_value(12)
            self.cards["certificaciones"].set_value(89)

            logger.warning(f"Usando datos de ejemplo: {result.get('error')}")

        # Cargar módulos para lecciones por módulo
        if modulos_result["success"]:
            data = modulos_result.get("data", [])
            if isinstance(data, list):
                self.modulos = data
            elif isinstance(data, dict) and "data" in data:
                self.modulos = data["data"]
            else:
                self.modulos = []

            # Contar lecciones por módulo
            for modulo in self.modulos:
                # Si no viene el conteo, obtener lecciones
                if "lecciones_count" not in modulo:
                    lecciones_result = self.api_client.get_lecciones(modulo["id"])
                    if lecciones_result["success"]:
                        lecciones_data = lecciones_result.get("data", [])
                        if isinstance(lecciones_data, list):
                            modulo["lecciones_count"] = len(lecciones_data)
                        else:
                            modulo["lecciones_count"] = 0
                    else:
                        modulo["lecciones_count"] = 0

            self.modulos_card.update_data(self.modulos)
