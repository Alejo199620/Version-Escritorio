"""
Dashboard View — coincide exactamente con vista.png
Diseño limpio, carga en tiempo real.
"""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QFrame,
    QPushButton,
    QSizePolicy,
    QGraphicsDropShadowEffect,
    QScrollArea,
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════
#  Worker para cargar datos en background sin bloquear UI
# ══════════════════════════════════════════════════════════
class DashboardWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client

    def run(self):
        result = {"stats": {}, "modulos": []}
        try:
            stats = self.api_client.get("/admin/dashboard", force_refresh=True)
            if stats.get("success"):
                result["stats"] = stats.get("data", {})

            modulos = self.api_client.get("/admin/modulos", force_refresh=True)
            if modulos.get("success"):
                data = modulos.get("data", [])
                result["modulos"] = data if isinstance(data, list) else []
        except Exception as e:
            logger.error(f"DashboardWorker error: {e}")
        self.finished.emit(result)


# ══════════════════════════════════════════════════════════
#  Tarjeta de estadística (USUARIOS / MÓDULOS / CERTIFICADOS)
# ══════════════════════════════════════════════════════════
class StatCard(QFrame):
    def __init__(self, title: str, color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setStyleSheet("""
            QFrame#statCard {
                background-color: white;
                border-radius: 16px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(130)

        row = QHBoxLayout(self)
        row.setContentsMargins(20, 20, 20, 20)
        row.setSpacing(16)

        # Barra de color lateral
        bar = QFrame()
        bar.setFixedWidth(5)
        bar.setMinimumHeight(70)
        bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
        row.addWidget(bar)

        # Texto
        col = QVBoxLayout()
        col.setSpacing(8)

        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Segoe UI", 10))
        lbl_title.setStyleSheet("color: #94a3b8; letter-spacing: 0.5px;")

        self.lbl_value = QLabel("—")
        self.lbl_value.setFont(QFont("Segoe UI", 34, QFont.Weight.Bold))
        self.lbl_value.setStyleSheet(f"color: {color};")

        col.addWidget(lbl_title)
        col.addWidget(self.lbl_value)
        row.addLayout(col)
        row.addStretch()

    def set_value(self, v):
        self.lbl_value.setText(str(v))


# ══════════════════════════════════════════════════════════
#  Mini-tarjeta de módulo dentro de la sección inferior
# ══════════════════════════════════════════════════════════
class ModuleCard(QFrame):
    def __init__(self, titulo: str, lecciones: int, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: none;
            }
            QFrame:hover {
                background-color: #f8fafc;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 12))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        self.setFixedHeight(95)

        col = QVBoxLayout(self)
        col.setContentsMargins(18, 14, 18, 14)
        col.setSpacing(8)

        t = QLabel(titulo)
        t.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        t.setStyleSheet("color: #1e293b;")
        t.setWordWrap(True)

        l = QLabel(f"{lecciones} lecciones")
        l.setFont(QFont("Segoe UI", 10))
        l.setStyleSheet("color: #64748b;")

        col.addWidget(t)
        col.addStretch()
        col.addWidget(l)


# ══════════════════════════════════════════════════════════
#  Panel "Lecciones por Módulo"
# ══════════════════════════════════════════════════════════
class LeccionesPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("lecPanel")
        self.setStyleSheet("""
            QFrame#lecPanel {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 25, 30, 30)
        outer.setSpacing(20)

        # Título posicionado dentro del cuadro grande
        hdr = QLabel("Lecciones por Módulo")
        hdr.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #1e293b; margin-bottom: 5px;")
        outer.addWidget(hdr)

        # Área de scroll para el grid de módulos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollBar:vertical { width: 6px; background: #f1f5f9; }"
            "QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 3px; }"
        )

        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background: transparent;")
        self.grid = QGridLayout(self.grid_container)
        self.grid.setSpacing(12)
        self.grid.setContentsMargins(0, 0, 0, 0)

        # Placeholder mientras carga
        self.placeholder = QLabel("Cargando módulos...")
        self.placeholder.setFont(QFont("Segoe UI", 10))
        self.placeholder.setStyleSheet("color: #94a3b8;")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.placeholder, 0, 0, 1, 3)

        scroll.setWidget(self.grid_container)
        outer.addWidget(scroll)

    def update_modules(self, modulos: list):
        """Poblar el grid con los módulos recibidos"""
        # Limpiar grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not modulos:
            empty = QLabel("No hay módulos disponibles")
            empty.setFont(QFont("Segoe UI", 10))
            empty.setStyleSheet("color: #94a3b8;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid.addWidget(empty, 0, 0, 1, 3)
            return

        # Ordenar por orden_global
        ordenados = sorted(modulos, key=lambda m: m.get("orden_global", 999))

        for i, modulo in enumerate(ordenados[:12]):
            titulo = modulo.get("titulo", "Módulo")
            count = modulo.get("lecciones_count", modulo.get("total_lecciones", 0))
            card = ModuleCard(titulo, int(count))
            row, col = divmod(i, 3)
            self.grid.addWidget(card, row, col)

        # Rellenar columnas vacías de la última fila para alinear
        total = min(len(ordenados), 12)
        rem = total % 3
        if rem != 0:
            last_row = total // 3
            for c in range(rem, 3):
                spacer = QWidget()
                self.grid.addWidget(spacer, last_row, c)


# ══════════════════════════════════════════════════════════
#  Vista principal del Dashboard
# ══════════════════════════════════════════════════════════
class DashboardView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self._worker = None
        self._is_loading = False

        self._setup_ui()
        self._connect_signals()

        # Carga inicial
        self._load_data()

        # Auto-refresh cada 5 minutos
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_if_visible)
        self._timer.start(300_000)

        # Reloj que actualiza fecha cada minuto
        self._clock = QTimer(self)
        self._clock.timeout.connect(self._update_date)
        self._clock.start(60_000)

    # ── UI ──────────────────────────────────────────────
    def _setup_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(30, 30, 30, 20)
        main.setSpacing(22)

        # ── Header ──────────────────────────────────────
        header = QHBoxLayout()

        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e293b;")

        self._date_lbl = QLabel()
        self._date_lbl.setFont(QFont("Segoe UI", 10))
        self._date_lbl.setStyleSheet("""
            QLabel {
                color: #64748b;
                padding: 6px 14px;
                background-color: #f8fafc;
                border-radius: 18px;
                border: 1px solid #e2e8f0;
            }
        """)
        self._update_date()

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self._date_lbl)
        main.addLayout(header)

        # ── 3 tarjetas de estadísticas ───────────────────
        cards_row = QHBoxLayout()
        cards_row.setSpacing(18)

        self._card_usuarios = StatCard("Usuarios Registrados", "#3b82f6")
        self._card_modulos  = StatCard("Módulos",              "#10b981")
        self._card_certs    = StatCard("Certificados",         "#f59e0b")

        cards_row.addWidget(self._card_usuarios)
        cards_row.addWidget(self._card_modulos)
        cards_row.addWidget(self._card_certs)
        main.addLayout(cards_row)

        # ── Título externo removido (ahora está dentro del panel) ───────────────────

        # ── Panel de módulos ─────────────────────────────
        self._panel = LeccionesPanel()
        main.addWidget(self._panel, stretch=1)

        # ── Botón actualizar ─────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self._btn_refresh = QPushButton("Actualizar Datos")
        self._btn_refresh.setFixedSize(170, 44)
        self._btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_refresh.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover  { background-color: #2563eb; }
            QPushButton:pressed { background-color: #1d4ed8; }
            QPushButton:disabled { background-color: #93c5fd; }
        """)
        self._btn_refresh.clicked.connect(self._load_data)
        btn_row.addWidget(self._btn_refresh)
        main.addLayout(btn_row)

    # ── Señales del api_client ───────────────────────────
    def _connect_signals(self):
        try:
            self.api_client.usuarios_changed.connect(self._on_data_changed)
        except Exception:
            pass
        try:
            self.api_client.modulos_changed.connect(self._on_data_changed)
        except Exception:
            pass
        try:
            self.api_client.lecciones_changed.connect(self._on_data_changed)
        except Exception:
            pass
        try:
            self.api_client.data_changed.connect(self._on_data_changed)
        except Exception:
            pass

    def _on_data_changed(self, *args):
        """Recarga automáticamente cuando cambia data relevante"""
        if self.isVisible():
            self._load_data()

    # ── Carga de datos ───────────────────────────────────
    def _load_data(self):
        if self._is_loading:
            return
        self._is_loading = True
        self._btn_refresh.setEnabled(False)
        self._btn_refresh.setText("Cargando…")

        # Correr en thread para no bloquear UI
        self._worker = DashboardWorker(self.api_client)
        self._worker.finished.connect(self._on_data_loaded)
        self._worker.start()

    def _on_data_loaded(self, result: dict):
        self._is_loading = False
        self._btn_refresh.setEnabled(True)
        self._btn_refresh.setText("Actualizar Datos")

        stats   = result.get("stats", {})
        modulos = result.get("modulos", [])

        # Tarjetas de números
        usuarios = stats.get("usuarios", {})
        contenido = stats.get("contenido", {})
        certs = stats.get("certificaciones", {})

        self._card_usuarios.set_value(usuarios.get("total", 0))
        self._card_modulos.set_value(contenido.get("modulos", len(modulos)))
        self._card_certs.set_value(certs.get("total", 0))

        # Panel de módulos
        self._panel.update_modules(modulos)

        # Actualizar fecha
        self._update_date()

        logger.info(f"✅ Dashboard: {len(modulos)} módulos cargados")

    def _refresh_if_visible(self):
        if self.isVisible():
            self._load_data()

    # ── Fecha ────────────────────────────────────────────
    def _update_date(self):
        now = datetime.now()
        dias  = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
        meses = ["","enero","febrero","marzo","abril","mayo","junio",
                 "julio","agosto","septiembre","octubre","noviembre","diciembre"]
        txt = f"{dias[now.weekday()]} {now.day} de {meses[now.month]}, {now.year} • {now.strftime('%H:%M')}"
        self._date_lbl.setText(txt)

    # ── Eventos de visibilidad ───────────────────────────
    def showEvent(self, event):
        super().showEvent(event)
        self._load_data()

    def hideEvent(self, event):
        super().hideEvent(event)
        if self._worker and self._worker.isRunning():
            self._worker.quit()
