from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QSizePolicy,
    QProgressBar,
)
from PyQt5.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
)
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

logging.basicConfig(level=logging.INFO)  # Cambiado a INFO para ver logs
logger = logging.getLogger(__name__)


class LoadingIndicator(QFrame):
    """Indicador de carga elegante"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loadingIndicator")
        self.setFixedHeight(40)
        self.setStyleSheet(
            """
            QFrame#loadingIndicator {
                background-color: #f8fafc;
                border-radius: 20px;
                border: 1px solid #e2e8f0;
            }
        """
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(10)

        # Barra de progreso circular simulada con puntos animados
        self.dots_container = QWidget()
        self.dots_container.setFixedWidth(60)
        dots_layout = QHBoxLayout(self.dots_container)
        dots_layout.setContentsMargins(0, 0, 0, 0)
        dots_layout.setSpacing(5)

        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setFont(QFont("Segoe UI", 12))
            dot.setStyleSheet("color: #3b82f6;")
            dot.setAlignment(Qt.AlignCenter)
            dots_layout.addWidget(dot)
            self.dots.append(dot)

        # Texto
        self.text_label = QLabel("Actualizando datos...")
        self.text_label.setFont(QFont("Segoe UI", 11))
        self.text_label.setStyleSheet("color: #1e293b;")

        # Tiempo transcurrido
        self.time_label = QLabel("0s")
        self.time_label.setFont(QFont("Segoe UI", 10))
        self.time_label.setStyleSheet("color: #64748b;")
        self.time_label.setAlignment(Qt.AlignRight)

        layout.addWidget(self.dots_container)
        layout.addWidget(self.text_label, 1)
        layout.addWidget(self.time_label)

        self.setLayout(layout)

        # Variables para animación
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate_dots)
        self.animation_step = 0

        # Timer para tiempo transcurrido
        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self._update_elapsed_time)
        self.start_time = None

        # Oculto por defecto
        self.hide()

    def start_loading(self, message="Actualizando datos..."):
        """Iniciar animación de carga"""
        self.text_label.setText(message)
        self.start_time = datetime.now()
        self.time_label.setText("0s")
        self.animation_step = 0
        self.animation_timer.start(300)
        self.elapsed_timer.start(1000)
        self.show()
        logger.info(f"⏳ {message}")

    def stop_loading(self):
        """Detener animación de carga"""
        self.animation_timer.stop()
        self.elapsed_timer.stop()
        self.hide()

        # Resetear colores de puntos
        for dot in self.dots:
            dot.setStyleSheet("color: #3b82f6;")

        if self.start_time:
            elapsed = (datetime.now() - self.start_time).seconds
            logger.info(f"✅ Carga completada en {elapsed}s")

    def _animate_dots(self):
        """Animar los puntos"""
        self.animation_step = (self.animation_step + 1) % 4

        for i, dot in enumerate(self.dots):
            if i < self.animation_step:
                dot.setStyleSheet("color: #3b82f6; font-weight: bold;")
            else:
                dot.setStyleSheet("color: #cbd5e1;")

    def _update_elapsed_time(self):
        """Actualizar tiempo transcurrido"""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).seconds
            self.time_label.setText(f"{elapsed}s")


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
        title_label = QLabel("LECCIONES POR MÓDULO")
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

        # Variables para control de carga
        self.is_visible = False
        self.last_stats = {}
        self.last_modulos = []
        self.loading_timer = QTimer()
        self.loading_timer.setSingleShot(True)
        self.loading_timer.timeout.connect(self._show_loading_indicator)

        # Timer para debounce de actualizaciones
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._process_pending_update)

        self.setup_ui()

        # Conectar señales
        self.conectar_senales()
        self.signals_connected = True

        # Cargar datos iniciales
        self.load_stats(initial_load=True)

        # Auto-refresh cada 5 minutos
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_if_visible)
        self.timer.start(300000)

        # Variables para control
        self.pending_update = False
        self.pending_update_type = None
        self._last_refresh = datetime.now()

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

        # Fecha
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

        # INDICADOR DE CARGA (siempre visible cuando se está actualizando)
        self.loading_indicator = LoadingIndicator()
        main_layout.addWidget(self.loading_indicator)

        # Grid superior
        top_grid = QGridLayout()
        top_grid.setSpacing(20)

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

        # Sección de Lecciones por Módulo
        lecciones_label = QLabel("Lecciones por Módulo")
        lecciones_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        lecciones_label.setStyleSheet("color: #1e293b; margin-top: 10px;")
        main_layout.addWidget(lecciones_label)

        # Tarjeta de módulos
        self.modulos_card = LeccionesPorModuloCard()
        main_layout.addWidget(self.modulos_card)

        # Botón actualizar (opcional, pero útil para recarga manual)
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
        self.refresh_btn.clicked.connect(lambda: self.load_stats(manual_refresh=True))
        button_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def showEvent(self, event):
        """Cuando la pestaña se hace visible"""
        super().showEvent(event)
        self.is_visible = True
        self.refresh_if_needed()

    def hideEvent(self, event):
        """Cuando la pestaña se oculta"""
        super().hideEvent(event)
        self.is_visible = False
        self.loading_indicator.stop_loading()
        self.loading_timer.stop()
        self.update_timer.stop()

    def refresh_if_needed(self):
        """Refrescar si es necesario"""
        if not self.is_visible:
            return

        elapsed = (datetime.now() - self._last_refresh).total_seconds()
        if elapsed > 120:  # 2 minutos
            self.load_stats(background=True)

    def refresh_if_visible(self):
        """Timer refresh"""
        if self.is_visible:
            self.load_stats(background=True)

    def conectar_senales(self):
        """Conectar señales"""
        logger.info("📊 Conectando dashboard a señales")

        # Conectar TODAS las señales relevantes
        self.api_client.usuarios_changed.connect(self.on_usuarios_changed)
        self.api_client.modulos_changed.connect(self.on_modulos_changed)
        self.api_client.lecciones_changed.connect(self.on_lecciones_changed)
        self.api_client.data_changed.connect(self.on_data_changed)

    def on_data_changed(self, data_type):
        """Manejar cambio genérico"""
        logger.info(f"📊 Cambio detectado en: {data_type}")

        if not self.is_visible:
            return

        if data_type == "usuarios":
            self._schedule_update("usuarios", delay=100)
        elif data_type in ["modulos", "lecciones"]:
            self._schedule_update("modulos", delay=200)

    def on_usuarios_changed(self):
        """Cambios en usuarios"""
        logger.info("👥 Usuarios cambiaron - actualizando automáticamente")
        if self.is_visible:
            self._schedule_update("usuarios", delay=100)

    def on_modulos_changed(self):
        """Cambios en módulos"""
        logger.info("📚 Módulos cambiaron - actualizando automáticamente")
        if self.is_visible:
            self._schedule_update("modulos", delay=200)

    def on_lecciones_changed(self):
        """Cambios en lecciones (afecta conteos de módulos)"""
        logger.info("📝 Lecciones cambiaron - actualizando conteos")
        if self.is_visible:
            self._schedule_update("modulos", delay=300)

    def _schedule_update(self, update_type="full", delay=200):
        """Programar actualización"""
        self.pending_update = True
        self.pending_update_type = update_type

        # Mostrar loading inmediatamente para feedback visual
        self.loading_indicator.start_loading(f"Actualizando {update_type}...")

        if not self.update_timer.isActive():
            self.update_timer.start(delay)
            logger.info(f"⏰ Actualización programada en {delay}ms")

    def _process_pending_update(self):
        """Procesar actualización"""
        if not self.pending_update or not self.is_visible:
            self.loading_indicator.stop_loading()
            self.pending_update = False
            return

        logger.info(f"🔄 Procesando actualización: {self.pending_update_type}")

        # Actualizar según tipo
        if self.pending_update_type == "usuarios":
            self._quick_update_usuarios()
        elif self.pending_update_type == "modulos":
            self._quick_update_modulos()
        else:
            self._quick_load()

        self.pending_update = False
        self.pending_update_type = None

    def _quick_update_usuarios(self):
        """Actualizar solo usuarios"""
        logger.info("⚡ Actualizando usuarios...")
        result = self.api_client.get_dashboard_stats()

        if result.get("success"):
            data = result.get("data", {})
            usuarios = data.get("usuarios", {})
            total = usuarios.get("total", 0)
            self.cards["usuarios"].set_value(total)
            logger.info(f"✅ Usuarios actualizados: {total}")

        self.loading_indicator.stop_loading()

    def _quick_update_modulos(self):
        """Actualizar módulos y conteos"""
        logger.info("⚡ Actualizando módulos...")

        # Actualizar número de módulos
        result = self.api_client.get_modulos(force_refresh=True)

        if result.get("success"):
            data = result.get("data", [])
            if isinstance(data, list):
                self.cards["modulos"].set_value(len(data))

                # Actualizar vista de módulos
                modulos_para_mostrar = []
                for modulo in data[:6]:
                    lecciones = modulo.get("lecciones_count", 0)
                    modulos_para_mostrar.append(
                        {
                            "titulo": modulo.get("titulo", ""),
                            "lecciones_count": lecciones,
                            "id": modulo.get("id"),
                        }
                    )

                self.modulos_card.update_data(modulos_para_mostrar)
                logger.info(f"✅ Módulos actualizados: {len(data)}")

        self.loading_indicator.stop_loading()

    def update_date(self):
        """Actualizar fecha"""
        now = datetime.now()

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

        fecha_str = f"{dia_semana} {dia} de {mes}, {año} • {hora}"
        self.date_label.setText(fecha_str)

    def _show_loading_indicator(self):
        """Mostrar loading"""
        if self.is_visible:
            self.loading_indicator.start_loading("Cargando dashboard...")

    def _hide_loading_indicator(self):
        """Ocultar loading"""
        self.loading_timer.stop()
        self.loading_indicator.stop_loading()

    def load_stats(self, initial_load=False, background=False, manual_refresh=False):
        """Cargar estadísticas"""
        if initial_load:
            self._full_load()
        elif manual_refresh:
            self._full_load()
        elif background and self.is_visible:
            self._quick_load()

    def _full_load(self):
        """Carga completa"""
        logger.info("🔄 Carga completa del dashboard")
        self.loading_indicator.start_loading("Cargando dashboard completo...")

        self._last_refresh = datetime.now()
        self.update_date()

        # Cargar estadísticas
        result = self.api_client.get_dashboard_stats(force_refresh=True)

        if result["success"]:
            data = result.get("data", {})
            if isinstance(data, dict):
                usuarios = data.get("usuarios", {})
                contenido = data.get("contenido", {})
                certificaciones = data.get("certificaciones", {})

                self.cards["usuarios"].set_value(usuarios.get("total", 0))
                self.cards["modulos"].set_value(contenido.get("modulos", 0))
                self.cards["certificaciones"].set_value(certificaciones.get("total", 0))

        # Cargar módulos
        self._load_modulos_background()

    def _quick_load(self):
        """Carga rápida"""
        logger.info("⚡ Carga rápida del dashboard")
        self.loading_indicator.start_loading("Actualizando números...")

        result = self.api_client.get_dashboard_stats()

        if result["success"]:
            data = result.get("data", {})
            if isinstance(data, dict):
                usuarios = data.get("usuarios", {})
                contenido = data.get("contenido", {})

                self.cards["usuarios"].set_value(usuarios.get("total", 0))
                self.cards["modulos"].set_value(contenido.get("modulos", 0))

        self.loading_indicator.stop_loading()

    def _load_modulos_background(self):
        """Cargar módulos en segundo plano"""
        self.api_client.get_async(
            "/admin/modulos", self._on_modulos_loaded, force_refresh=True
        )

    def _on_modulos_loaded(self, result):
        """Callback de módulos cargados"""
        if not self.is_visible:
            self.loading_indicator.stop_loading()
            return

        if result and result.get("success"):
            data = result.get("data", [])
            if isinstance(data, list):
                self.modulos = data
                self._load_lecciones_counts_light()
        else:
            self.loading_indicator.stop_loading()

    def _load_lecciones_counts_light(self):
        """Cargar conteos de lecciones"""
        modulos_a_mostrar = self.modulos[:6]

        if not modulos_a_mostrar:
            self.modulos_card.update_data([])
            self.loading_indicator.stop_loading()
            return

        # Verificar si ya tienen conteo
        todos_con_conteo = all("lecciones_count" in m for m in modulos_a_mostrar)

        if todos_con_conteo:
            self.modulos_card.update_data(modulos_a_mostrar)
            self.loading_indicator.stop_loading()
            return

        # Cargar conteos pendientes
        self.modulos_pendientes = len(modulos_a_mostrar)
        self.modulos_completados = 0

        for modulo in modulos_a_mostrar:
            if "lecciones_count" not in modulo:
                self.api_client.get_async(
                    f"/admin/modulos/{modulo['id']}/lecciones",
                    lambda result, m=modulo: self._update_modulo_count(result, m),
                    params={"per_page": 1},
                )
            else:
                self.modulos_completados += 1

    def _update_modulo_count(self, result, modulo):
        """Actualizar conteo de un módulo"""
        if result and result.get("success"):
            data = result.get("data", [])
            modulo["lecciones_count"] = len(data) if isinstance(data, list) else 0
        else:
            modulo["lecciones_count"] = 0

        self.modulos_completados += 1

        if self.modulos_completados >= self.modulos_pendientes:
            self.modulos_card.update_data(self.modulos[:6])
            self.loading_indicator.stop_loading()
