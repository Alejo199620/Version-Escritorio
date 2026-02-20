from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGroupBox,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QTextEdit,
    QFrame,
    QSplitter,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QGridLayout,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QDoubleSpinBox,
    QTabWidget,
    QToolButton,
    QMenu,
    QApplication,
    QGraphicsDropShadowEffect,
    QProgressBar,
)
from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    QTimer,
    QSize,
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
)
from PyQt5.QtGui import (
    QFont,
    QColor,
    QPalette,
    QIcon,
    QPixmap,
    QPainter,
    QBrush,
    QLinearGradient,
    QPen,
)
import logging
import re
from utils.paths import resource_path
from views.lessons_view import LessonDialog
from views.components.rich_text_editor import RichTextEditor

# Configuración de logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


# ============================================================================
# CLASE DE UTILIDADES PARA ESTILOS
# ============================================================================


class StyleHelper:
    """
    Clase helper que centraliza la definición de estilos y colores
    para mantener consistencia visual en toda la aplicación.
    """

    # Paleta de colores principal
    PRIMARY_COLOR = "#4361ee"
    SECONDARY_COLOR = "#3f37c9"
    SUCCESS_COLOR = "#4cc9f0"
    DANGER_COLOR = "#f72585"
    WARNING_COLOR = "#f8961e"
    INFO_COLOR = "#4895ef"
    LIGHT_BG = "#f8f9fa"
    DARK_BG = "#212529"
    BORDER_COLOR = "#dee2e6"

    @staticmethod
    def card_style() -> str:
        """Estilo para tarjetas con efecto hover"""
        return """
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
            QFrame:hover {
                border: 2px solid #4361ee;
                background-color: #f8f9fa;
            }
        """

    @staticmethod
    def button_primary() -> str:
        """Estilo para botón principal"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {StyleHelper.SECONDARY_COLOR};
            }}
        """

    @staticmethod
    def button_success() -> str:
        """Estilo para botón de éxito/confirmación"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #3aa8d8;
            }}
        """

    @staticmethod
    def button_danger() -> str:
        """Estilo para botón de peligro/eliminación"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.DANGER_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #d91c72;
            }}
        """

    @staticmethod
    def button_warning() -> str:
        """Estilo para botón de advertencia"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.WARNING_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #e07c0e;
            }}
        """

    @staticmethod
    def badge_active() -> str:
        """Estilo para badge de estado activo"""
        return """
            QLabel {
                background-color: #d1fae5;
                color: #065f46;
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 11px;
                font-weight: bold;
            }
        """

    @staticmethod
    def badge_inactive() -> str:
        """Estilo para badge de estado inactivo"""
        return """
            QLabel {
                background-color: #fee2e2;
                color: #991b1b;
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 11px;
                font-weight: bold;
            }
        """

    @staticmethod
    def badge_draft() -> str:
        """Estilo para badge de estado borrador"""
        return """
            QLabel {
                background-color: #fff3cd;
                color: #856404;
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 11px;
                font-weight: bold;
            }
        """


# ============================================================================
# COMPONENTE: TARJETA DE MÓDULO MODERNA
# ============================================================================


class ModernCard(QFrame):
    """
    Tarjeta interactiva para mostrar información resumida de un módulo.
    Incluye efectos de sombra, animaciones al hover y emite señal al hacer clic.
    """

    clicked = pyqtSignal(object)  # Señal que emite el módulo al hacer clic

    def __init__(self, modulo: dict, parent=None):
        super().__init__(parent)
        self.modulo = modulo
        self._setup_ui()
        self._setup_shadow()
        self._setup_animations()

    def _setup_shadow(self) -> None:
        """Configura el efecto de sombra de la tarjeta"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def _setup_animations(self) -> None:
        """Configura las animaciones de movimiento al hover"""
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario de la tarjeta"""
        self.setObjectName("modernCard")
        self.setFixedHeight(200)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(
            """
            #modernCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #ffffff, stop:1 #fafbfc);
                border-radius: 16px;
                border: 1px solid #edf2f7;
            }
            #modernCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #ffffff, stop:1 #f1f5f9);
                border: 2px solid #4361ee;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 16, 20, 16)

        # --- HEADER: Tipo y título ---
        header = QHBoxLayout()
        header.setSpacing(12)

        # Título del módulo
        titulo = self.modulo.get("titulo", "Sin título")
        if len(titulo) > 40:
            titulo = titulo[:37] + "..."

        title = QLabel(titulo)
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        header.addWidget(title, 1)

        # Badge de tipo de módulo
        tipo_badge = QLabel(self.modulo.get("modulo", "html").upper())
        tipo_badge.setStyleSheet(
            """
            background-color: #e2e8f0;
            color: #475569;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: bold;
        """
        )
        header.addWidget(tipo_badge)

        layout.addLayout(header)

        # --- DESCRIPCIÓN (texto plano sin HTML) ---
        desc = self.modulo.get("descripcion_larga", "Sin descripción")
        if desc:
            # Eliminar etiquetas HTML
            desc = re.sub("<[^<]+?>", "", desc)
            palabras = desc.split()[:15]
            desc = " ".join(palabras) + ("..." if len(palabras) == 15 else "")

        desc_label = QLabel(desc)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #64748b; font-size: 12px; line-height: 1.5;")
        desc_label.setFixedHeight(50)
        layout.addWidget(desc_label)

        # --- BARRA DE PROGRESO ---
        progress_container = QFrame()
        progress_container.setFixedHeight(6)
        progress_container.setStyleSheet(
            "background-color: #e9ecef; border-radius: 3px;"
        )

        progress_layout = QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        progress = QFrame()
        progress.setFixedHeight(6)
        progress.setFixedWidth(int(200 * (self.modulo.get("progreso", 0) / 100)))
        progress.setStyleSheet("background-color: #4361ee; border-radius: 3px;")
        progress_layout.addWidget(progress)
        progress_layout.addStretch()

        layout.addWidget(progress_container)

        # --- FOOTER: Estadísticas y estado ---
        footer = QHBoxLayout()
        footer.setSpacing(16)

        # Estadísticas de lecciones y duración
        stats = [
            f"{self.modulo.get('total_lecciones', 0)} lecciones",
            f"{self.modulo.get('duracion', 0)} min",
        ]

        for stat in stats:
            stat_label = QLabel(stat)
            stat_label.setStyleSheet(
                "color: #4361ee; font-size: 11px; font-weight: 500;"
            )
            footer.addWidget(stat_label)

        footer.addStretch()

        # Badge de estado del módulo
        estado = self.modulo.get("estado", "inactivo")
        estado_label = QLabel(estado.upper())

        if estado == "activo":
            estado_label.setStyleSheet(StyleHelper.badge_active())
        elif estado == "inactivo":
            estado_label.setStyleSheet(StyleHelper.badge_inactive())
        else:
            estado_label.setStyleSheet(StyleHelper.badge_draft())

        footer.addWidget(estado_label)
        layout.addLayout(footer)

        # Orden global del módulo
        orden_label = QLabel(f"Orden #{self.modulo.get('orden_global', 1)}")
        orden_label.setStyleSheet("color: #94a3b8; font-size: 10px;")
        orden_label.setAlignment(Qt.AlignRight)
        layout.addWidget(orden_label)

    def mousePressEvent(self, event) -> None:
        """Maneja el evento de clic en la tarjeta"""
        self.clicked.emit(self.modulo)
        super().mousePressEvent(event)

    def enterEvent(self, event) -> None:
        """Animación al entrar el mouse"""
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(self.pos().x(), self.pos().y() - 2))
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Animación al salir el mouse"""
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(self.pos().x(), self.pos().y() + 2))
        self.animation.start()
        super().leaveEvent(event)


# ============================================================================
# COMPONENTE: ITEM DE LECCIÓN MEJORADO
# ============================================================================


class EnhancedLessonItem(QWidget):
    """
    Widget que representa una lección en la lista con diseño profesional.
    Incluye botones de acción (editar/eliminar) y emite señales para cada acción.
    """

    clicked = pyqtSignal(object)  # Señal al hacer clic en el item
    edit_clicked = pyqtSignal(object)  # Señal al hacer clic en editar
    delete_clicked = pyqtSignal(object)  # Señal al hacer clic en eliminar

    def __init__(self, leccion: dict, parent=None):
        super().__init__(parent)
        self.leccion = leccion
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario del item de lección"""
        self.setFixedHeight(90)
        self.setCursor(Qt.PointingHandCursor)

        # Efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        self.setStyleSheet(
            """
            EnhancedLessonItem {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
            EnhancedLessonItem:hover {
                background-color: #f8fafc;
                border: 2px solid #4361ee;
            }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(16)

        # --- CONTENEDOR DE INDICADOR VISUAL ---
        indicator_container = QFrame()
        indicator_container.setFixedSize(48, 48)
        indicator_container.setStyleSheet(
            """
            QFrame {
                background-color: #f1f5f9;
                border-radius: 12px;
            }
        """
        )

        indicator_layout = QVBoxLayout(indicator_container)
        indicator_layout.setAlignment(Qt.AlignCenter)

        # Indicador si tiene ejercicios
        indicator = "📝" if self.leccion.get("tiene_ejercicios") else "📄"
        indicator_label = QLabel(indicator)
        indicator_label.setStyleSheet("font-size: 24px;")
        indicator_layout.addWidget(indicator_label)

        layout.addWidget(indicator_container)

        # --- CONTENIDO PRINCIPAL ---
        content = QVBoxLayout()
        content.setSpacing(6)

        # Título de la lección
        titulo = self.leccion.get("titulo", "Sin título")
        if len(titulo) > 50:
            titulo = titulo[:47] + "..."

        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        titulo_label.setStyleSheet("color: #1e293b;")
        content.addWidget(titulo_label)

        # --- METADATA: Orden, duración y tipo ---
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(20)

        # Orden de la lección
        orden_frame = QFrame()
        orden_frame.setStyleSheet("background-color: #f1f5f9; border-radius: 4px;")
        orden_layout = QHBoxLayout(orden_frame)
        orden_layout.setContentsMargins(6, 2, 6, 2)

        orden_label = QLabel(f"Orden {self.leccion.get('orden', 1)}")
        orden_label.setStyleSheet("color: #475569; font-size: 11px; font-weight: 500;")
        orden_layout.addWidget(orden_label)
        meta_layout.addWidget(orden_frame)

        # Duración
        if self.leccion.get("duracion"):
            duracion_label = QLabel(f"⏱️ {self.leccion.get('duracion')} min")
            duracion_label.setStyleSheet("color: #64748b; font-size: 11px;")
            meta_layout.addWidget(duracion_label)

        # Tipo de contenido
        if self.leccion.get("tipo_contenido"):
            tipo_label = QLabel(f"📄 {self.leccion.get('tipo_contenido')}")
            tipo_label.setStyleSheet("color: #64748b; font-size: 11px;")
            meta_layout.addWidget(tipo_label)

        meta_layout.addStretch()
        content.addLayout(meta_layout)
        layout.addLayout(content, 1)

        # --- BOTONES DE ACCIÓN ---
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        # Botón editar
        self.edit_btn = QPushButton("Editar")
        self.edit_btn.setFixedHeight(36)
        self.edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: none;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """
        )
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.leccion))
        buttons_layout.addWidget(self.edit_btn)

        # Botón eliminar
        self.delete_btn = QPushButton("Eliminar")
        self.delete_btn.setFixedHeight(36)
        self.delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f1f5f9;
                color: #ef4444;
                border: none;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #fee2e2;
            }
        """
        )
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.leccion))
        buttons_layout.addWidget(self.delete_btn)

        layout.addLayout(buttons_layout)

    def mousePressEvent(self, event) -> None:
        """
        Maneja el evento de clic, ignorando si se hizo clic en los botones.
        """
        if not self.edit_btn.underMouse() and not self.delete_btn.underMouse():
            self.clicked.emit(self.leccion)
        super().mousePressEvent(event)


# ============================================================================
# COMPONENTE: WIDGET DE ESTADÍSTICAS
# ============================================================================


class StatsWidget(QWidget):
    """
    Widget que muestra estadísticas en formato de tarjetas.
    Utilizado para mostrar métricas de módulos y lecciones.
    """

    def __init__(self, stats_data: dict, parent=None):
        super().__init__(parent)
        self.stats_data = stats_data
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario con las estadísticas"""
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Definición de las estadísticas a mostrar
        stats = [
            ("Lecciones", self.stats_data.get("total_lecciones", 0), "#4361ee"),
            # ("Ejercicios", self.stats_data.get("total_ejercicios", 0), "#f72585"),
        ]

        for titulo, valor, color in stats:
            card = self._create_stat_card(titulo, valor, color)
            layout.addWidget(card, 1)

    def _create_stat_card(self, titulo: str, valor, color: str) -> QFrame:
        """
        Crea una tarjeta individual para una estadística.

        Args:
            titulo: Título de la estadística
            valor: Valor a mostrar
            color: Color del texto del valor

        Returns:
            QFrame configurado como tarjeta de estadística
        """
        card = QFrame()
        card.setFixedHeight(100)

        # # Efecto de sombra
        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(10)
        # shadow.setColor(QColor(0, 0, 0, 15))
        # shadow.setOffset(0, 2)
        # card.setGraphicsEffect(shadow)

        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border:none;
                border-radius:0;
            }
        """
        )

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(16, 12, 16, 12)

        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("color: #64748b; font-size: 12px;")
        card_layout.addWidget(titulo_label)

        # Valor
        valor_label = QLabel(str(valor))
        valor_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        valor_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(valor_label)

        return card


# ============================================================================
# COMPONENTE: TARJETA DE CONFIGURACIÓN DE EVALUACIÓN
# ============================================================================


class EvaluationConfigCard(QFrame):
    """
    Tarjeta de solo lectura que muestra la configuración de una evaluación.
    Presenta los parámetros en formato de grid para fácil lectura.
    """

    def __init__(self, eval_data: dict, parent=None):
        super().__init__(parent)
        self.eval_data = eval_data
        self._setup_ui()
        self._setup_shadow()

    def _setup_shadow(self) -> None:
        """Configura el efecto de sombra de la tarjeta"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario de la tarjeta"""
        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e9ecef;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 20, 24, 20)

        # --- HEADER con título y badge de estado ---
        header = QHBoxLayout()

        title = QLabel("Configuración de Evaluación")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        header.addWidget(title)
        header.addStretch()

        # Badge de estado (solo lectura)
        estado = self.eval_data.get("estado", "inactivo")
        self.status_badge = QLabel(estado.upper())
        self.status_badge.setFixedHeight(32)
        self.status_badge.setAlignment(Qt.AlignCenter)

        if estado == "activo":
            self.status_badge.setStyleSheet(StyleHelper.badge_active())
        elif estado == "inactivo":
            self.status_badge.setStyleSheet(StyleHelper.badge_inactive())
        else:
            self.status_badge.setStyleSheet(StyleHelper.badge_draft())

        header.addWidget(self.status_badge)
        layout.addLayout(header)

        # --- GRID DE PARÁMETROS ---
        grid = QGridLayout()
        grid.setSpacing(16)

        params = [
            (
                "Tiempo límite",
                f"{self.eval_data.get('tiempo_limite', 0)} minutos",
                0,
                0,
            ),
            ("Puntaje mínimo", f"{self.eval_data.get('puntaje_minimo', 0)}%", 0, 1),
            ("Intentos máximos", str(self.eval_data.get("max_intentos", 0)), 1, 0),
            ("Total preguntas", str(len(self.eval_data.get("preguntas", []))), 1, 1),
        ]

        for label, value, row, col in params:
            param_frame = self._create_param_card(label, value)
            grid.addWidget(param_frame, row, col)

        layout.addLayout(grid)

    def _create_param_card(self, label: str, value: str) -> QFrame:
        """
        Crea una tarjeta individual para un parámetro de evaluación.

        Args:
            label: Etiqueta del parámetro
            value: Valor del parámetro

        Returns:
            QFrame configurado como tarjeta de parámetro
        """
        param_frame = QFrame()
        param_frame.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
            }
        """
        )

        param_layout = QVBoxLayout(param_frame)
        param_layout.setSpacing(8)
        param_layout.setContentsMargins(16, 12, 16, 12)

        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #64748b; font-size: 12px;")
        param_layout.addWidget(label_widget)

        value_widget = QLabel(value)
        value_widget.setFont(QFont("Segoe UI", 16, QFont.Bold))
        value_widget.setStyleSheet("color: #1e293b;")
        param_layout.addWidget(value_widget)

        return param_frame


# ============================================================================
# COMPONENTE: ITEM DE PREGUNTA
# ============================================================================


class QuestionItemWidget(QWidget):
    """
    Widget que representa una pregunta en la lista con diseño profesional.
    Incluye información del tipo, texto, puntos y botones de acción.
    """

    clicked = pyqtSignal(object)  # Señal al hacer clic en el item
    edit_clicked = pyqtSignal(object)  # Señal al hacer clic en editar
    delete_clicked = pyqtSignal(object)  # Señal al hacer clic en eliminar

    def __init__(self, pregunta: dict, parent=None):
        super().__init__(parent)
        self.pregunta = pregunta
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario del item de pregunta"""
        self.setFixedHeight(80)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(
            """
            QuestionItemWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e9ecef;
            }
            QuestionItemWidget:hover {
                background-color: #f8fafc;
                border: 2px solid #4361ee;
            }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        # --- CONTENEDOR DE TIPO DE PREGUNTA ---
        tipo_frame = QFrame()
        tipo_frame.setFixedSize(60, 60)
        tipo_frame.setStyleSheet(
            """
            QFrame {
                background-color: #f1f5f9;
                border-radius: 10px;
            }
        """
        )

        tipo_layout = QVBoxLayout(tipo_frame)
        tipo_layout.setAlignment(Qt.AlignCenter)

        # Icono según tipo de pregunta
        tipo_icon = {
            "seleccion_multiple": "📝",
            "verdadero_falso": "✓",
            "arrastrar_soltar": "🔄",
        }.get(self.pregunta.get("tipo", ""), "📝")

        icon_label = QLabel(tipo_icon)
        icon_label.setStyleSheet("font-size: 24px;")
        tipo_layout.addWidget(icon_label)
        layout.addWidget(tipo_frame)

        # --- CONTENIDO PRINCIPAL ---
        content = QVBoxLayout()
        content.setSpacing(4)

        # Texto de la pregunta (truncado si es muy largo)
        pregunta_text = self.pregunta.get("pregunta", "")
        if len(pregunta_text) > 60:
            pregunta_text = pregunta_text[:57] + "..."

        pregunta_label = QLabel(pregunta_text)
        pregunta_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        pregunta_label.setStyleSheet("color: #1e293b;")
        content.addWidget(pregunta_label)

        # --- METADATA: Puntos y estadísticas de opciones ---
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)

        puntos_label = QLabel(f"⚡ {self.pregunta.get('puntos', 0)} puntos")
        puntos_label.setStyleSheet("color: #f8961e; font-size: 11px; font-weight: 500;")
        meta_layout.addWidget(puntos_label)

        opciones = self.pregunta.get("opciones", [])
        if opciones:
            total = len(opciones)
            tipo = self.pregunta.get("tipo")

            if tipo == "arrastrar_soltar":
                info = f"🔄 {total} pares"
            elif tipo == "verdadero_falso":
                info = "✓✓ V/F"
            else:
                correctas = sum(1 for o in opciones if o.get("es_correcta", False))
                info = f"✅ {correctas}/{total} correctas"

            info_label = QLabel(info)
            info_label.setStyleSheet("color: #64748b; font-size: 11px;")
            meta_layout.addWidget(info_label)

        meta_layout.addStretch()
        content.addLayout(meta_layout)
        layout.addLayout(content, 1)

        # --- BOTONES DE ACCIÓN ---
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)

        # Botón editar
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(32, 32)
        self.edit_btn.setToolTip("Editar pregunta")
        self.edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """
        )
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.pregunta))
        actions_layout.addWidget(self.edit_btn)

        # Botón eliminar
        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(32, 32)
        self.delete_btn.setToolTip("Eliminar pregunta")
        self.delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f1f5f9;
                color: #ef4444;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #fee2e2;
            }
        """
        )
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.pregunta))
        actions_layout.addWidget(self.delete_btn)

        layout.addLayout(actions_layout)

    def mousePressEvent(self, event) -> None:
        """
        Maneja el evento de clic, ignorando si se hizo clic en los botones.
        """
        if not self.edit_btn.underMouse() and not self.delete_btn.underMouse():
            self.clicked.emit(self.pregunta)
        super().mousePressEvent(event)


# ============================================================================
# DIÁLOGO: CREACIÓN/EDICIÓN DE MÓDULO
# ============================================================================


class ModuleDialog(QDialog):
    """
    Diálogo para crear o editar un módulo.
    Incluye campos para título, tipo, descripción (con editor enriquecido),
    orden y estado.
    """

    def __init__(self, api_client, modulo_data: dict = None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_data = modulo_data
        self.modulos_existentes = []

        self.setWindowTitle("Editar Módulo" if modulo_data else "Nuevo Módulo")
        self.setMinimumSize(700, 600)
        self.setModal(True)

        # Cargar módulos existentes para calcular orden siguiente
        QTimer.singleShot(0, self._cargar_modulos_existentes)
        self._setup_ui()

        if modulo_data:
            self._load_data()

    def _cargar_modulos_existentes(self) -> None:
        """Carga los módulos existentes para calcular el siguiente orden"""
        result = self.api_client.get_modulos()
        if result["success"]:
            data = result.get("data", [])
            self.modulos_existentes = (
                data
                if isinstance(data, list)
                else data.get("data", []) if isinstance(data, dict) else []
            )
            if not self.modulo_data:
                self.orden_spin.setValue(self._obtener_siguiente_orden())

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario del diálogo"""
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                padding: 10px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 13px;
                background-color: #f8fafc;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #4361ee;
                background-color: white;
            }
            QLabel {
                font-size: 13px;
                color: #1e293b;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título del diálogo
        title = QLabel("Editar Módulo" if self.modulo_data else "Nuevo Módulo")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(title)

        # --- FORMULARIO PRINCIPAL ---
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Campo: Título
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Ej: Introducción a HTML")
        self.titulo_input.textChanged.connect(self._validar_campos)
        form_layout.addRow("Título:", self.titulo_input)

        # Campo: Tipo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["html", "css", "javascript", "php", "sql", "introduccion"]
        )
        form_layout.addRow("Tipo:", self.tipo_combo)

        layout.addWidget(form_widget)

        # --- CAMPO: DESCRIPCIÓN (con editor enriquecido) ---
        desc_label = QLabel("Descripción:")
        desc_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        desc_label.setStyleSheet("margin-top: 10px;")
        layout.addWidget(desc_label)

        self.descripcion_editor = RichTextEditor()
        self.descripcion_editor.setMinimumHeight(200)
        self.descripcion_editor.editor.textChanged.connect(self._validar_campos)
        layout.addWidget(self.descripcion_editor)

        # --- CAMPOS: ORDEN Y ESTADO (en fila) ---
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Orden del módulo
        orden_group = self._create_field_group("Orden del módulo")
        orden_layout = QVBoxLayout(orden_group)

        self.orden_spin = QSpinBox()
        self.orden_spin.setRange(1, 999)
        self.orden_spin.setValue(1)
        orden_layout.addWidget(self.orden_spin)
        bottom_layout.addWidget(orden_group)

        # Estado del módulo
        estado_group = self._create_field_group("Estado del módulo")
        estado_layout = QVBoxLayout(estado_group)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo", "borrador"])
        estado_layout.addWidget(self.estado_combo)
        bottom_layout.addWidget(estado_group)

        layout.addLayout(bottom_layout)

        # --- BOTONES DE ACCIÓN ---
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar Módulo")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            StyleHelper.button_primary() + "padding: 10px 30px;"
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            StyleHelper.button_danger() + "padding: 10px 30px;"
        )

        # Deshabilitar botón OK inicialmente
        self.ok_button = buttons.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Validar campos inicialmente
        self._validar_campos()

    def _create_field_group(self, title: str) -> QFrame:
        """
        Crea un grupo con estilo para campos de formulario.

        Args:
            title: Título del grupo

        Returns:
            QFrame configurado como grupo de campo
        """
        group = QFrame()
        group.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 15px;
            }
        """
        )

        label = QLabel(title)
        label.setFont(QFont("Segoe UI", 12, QFont.Bold))

        layout = QVBoxLayout(group)
        layout.addWidget(label)

        return group

    def _validar_campos(self) -> None:
        """Valida que los campos requeridos no estén vacíos"""
        titulo = self.titulo_input.text().strip()
        descripcion = self.descripcion_editor.toPlainText().strip()

        self.ok_button.setEnabled(bool(titulo and descripcion))

    def _obtener_siguiente_orden(self) -> int:
        """
        Calcula el siguiente orden disponible para un nuevo módulo.

        Returns:
            int: El siguiente número de orden
        """
        if not self.modulos_existentes:
            return 1

        ordenes = [
            m.get("orden_global", 0)
            for m in self.modulos_existentes
            if not self.modulo_data or m["id"] != self.modulo_data.get("id")
        ]
        return max(ordenes) + 1 if ordenes else 1

    def _load_data(self) -> None:
        """Carga los datos del módulo existente en el formulario"""
        self.titulo_input.setText(self.modulo_data.get("titulo", ""))

        index = self.tipo_combo.findText(self.modulo_data.get("modulo", "html"))
        if index >= 0:
            self.tipo_combo.setCurrentIndex(index)

        descripcion = self.modulo_data.get("descripcion_larga", "")
        self.descripcion_editor.setHtml(descripcion)

        self.orden_spin.setValue(self.modulo_data.get("orden_global", 1))

        index = self.estado_combo.findText(self.modulo_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

        self._validar_campos()

    def get_data(self) -> dict:
        """
        Obtiene los datos del formulario.

        Returns:
            dict: Datos del módulo o None si hay errores de validación
        """
        titulo = self.titulo_input.text().strip()
        descripcion_html = self.descripcion_editor.toHtml()
        descripcion_texto = self.descripcion_editor.toPlainText().strip()

        if not titulo or not descripcion_texto:
            QMessageBox.warning(
                self,
                "Campos requeridos",
                "El título y la descripción son obligatorios.",
            )
            return None

        # Usar HTML si tiene formato, si no usar texto plano
        if (
            descripcion_html
            and descripcion_html != "<p></p>"
            and descripcion_html != "<p><br></p>"
            and "<p>" in descripcion_html
        ):
            descripcion = descripcion_html
        else:
            descripcion = descripcion_texto

        return {
            "titulo": titulo,
            "modulo": self.tipo_combo.currentText(),
            "descripcion_larga": descripcion,
            "orden_global": self.orden_spin.value(),
            "estado": self.estado_combo.currentText(),
        }

    def accept(self) -> None:
        """Sobrescribe accept para validar antes de cerrar"""
        data = self.get_data()
        if data is None:
            return
        super().accept()


# ============================================================================
# VISTA: DETALLE DE MÓDULO
# ============================================================================


class ModuleDetailView(QWidget):
    """
    Vista detallada de un módulo con pestañas para lecciones, evaluación e información.
    Se actualiza en tiempo real cuando hay cambios en los datos.
    """

    module_updated = pyqtSignal()  # Señal cuando se actualiza el módulo
    lesson_selected = pyqtSignal(
        object, object
    )  # Señal cuando se selecciona una lección

    def __init__(self, api_client, modulo: dict, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo = modulo
        self.lecciones = []
        self.evaluacion_actual = None
        self._loaded = False
        self._cambiando_estado = False  # Flag para evitar múltiples cambios

        # Elementos para indicadores de carga
        self.loading_eval_label = None
        self.loading_lessons_label = None

        self._setup_ui()

        # Conectar señales del API client para actualización en tiempo real
        self.api_client.evaluaciones_changed.connect(self._on_evaluaciones_changed)
        self.api_client.data_changed.connect(self._on_data_changed)

        QTimer.singleShot(50, self._load_all_data)

    # ============================================================================
    # MANEJADORES DE SEÑALES
    # ============================================================================

    def _on_evaluaciones_changed(self) -> None:
        """Cuando cambian las evaluaciones, recargar automáticamente"""
        logger.debug(
            f"Signal evaluaciones_changed recibida para módulo {self.modulo.get('id')}"
        )
        QTimer.singleShot(300, self._recargar_evaluacion_con_indicador)

    def _on_data_changed(self, data_type: str) -> None:
        """Cuando cambia cualquier dato, verificar si es relevante"""
        if data_type == "evaluaciones":
            logger.debug("Signal data_changed(evaluaciones) recibida")
            QTimer.singleShot(300, self._recargar_evaluacion_con_indicador)
        elif data_type == "lecciones":
            logger.debug("Signal data_changed(lecciones) recibida")
            QTimer.singleShot(300, self._recargar_lecciones_con_indicador)

    # ============================================================================
    # SETUP DE UI
    # ============================================================================

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario principal"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- HEADER CON GRADIENTE ---
        header = self._create_header()
        main_layout.addWidget(header)

        # --- CONTENIDO CON TABS ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: #f8fafc;
            }
        """
        )

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(25)
        content_layout.setContentsMargins(40, 30, 40, 30)

        # Widget de estadísticas
        self.stats_widget = StatsWidget(
            {"total_lecciones": 0, "total_ejercicios": 0, "duracion": 0, "progreso": 0}
        )
        content_layout.addWidget(self.stats_widget)

        # Pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: none;
                background-color: transparent;
                margin-top: 10px;
            }
            QTabBar::tab {
                background-color: white;
                border: 1px solid #e9ecef;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 40px;  /* Aumentado el padding horizontal de 24px a 40px */
                margin-right: 6px;    /* Aumentado ligeramente el margen entre pestañas */
                font-size: 13px;
                font-weight: 500;
                color: #64748b;
                min-width: 100px;    /* Ancho mínimo opcional para consistencia */
            }
            QTabBar::tab:selected {
                color: #4361ee;
                border-bottom: 2px solid #4361ee;
                background-color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #f8fafc;
                color: #1e293b;
            }
        """
        )

        # Crear las pestañas
        self.lessons_tab = self._create_lessons_tab()
        self.eval_tab = self._create_evaluation_tab()
        self.info_tab = self._create_info_tab()

        self.tabs.addTab(self.lessons_tab, "Lecciones")
        self.tabs.addTab(self.eval_tab, "Evaluación")
        self.tabs.addTab(self.info_tab, "Información")

        content_layout.addWidget(self.tabs)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def _create_header(self) -> QFrame:
        """
        Crea el header con gradiente y acciones del módulo.

        Returns:
            QFrame: Header configurado
        """
        header = QFrame()
        header.setFixedHeight(220)
        header.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #1e293b, stop:1 #4361ee);
                border-bottom-left-radius: 40px;
                border-bottom-right-radius: 40px;
            }
        """
        )

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(40, 20, 40, 20)

        # --- NAVEGACIÓN Y ACCIONES ---
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        # Botón editar módulo
        edit_btn = QPushButton("Editar Módulo")
        edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                color: #1e293b;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f8fafc;
            }
        """
        )
        edit_btn.clicked.connect(self._editar_modulo)
        actions_layout.addWidget(edit_btn)

        # Botón eliminar módulo
        delete_btn = QPushButton("Eliminar Módulo")
        delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """
        )
        delete_btn.clicked.connect(self._eliminar_modulo)
        actions_layout.addWidget(delete_btn)

        nav_layout.addLayout(actions_layout)
        header_layout.addLayout(nav_layout)

        # --- INFORMACIÓN DEL MÓDULO ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(30)

        # Título y tipo
        title_info = QVBoxLayout()
        title_info.setSpacing(10)

        tipo_badge = QLabel(self.modulo.get("modulo", "html").upper())
        tipo_badge.setStyleSheet(
            """
            color: rgba(255,255,255,0.9);
            font-size: 12px;
            font-weight: bold;
            background-color: transparent;
            border:none;
            padding:0;
        """
        )
        title_info.addWidget(tipo_badge)

        titulo = self.modulo.get("titulo", "Módulo")
        title_label = QLabel(titulo)
        title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title_label.setStyleSheet(
            """
        color: white;
        background-color: transparent;
        border: none;
        padding: 0;
    """
        )
        title_label.setWordWrap(True)
        title_info.addWidget(title_label)

        info_layout.addLayout(title_info)
        info_layout.addStretch()

        # Badge de estado clickeable
        estado = self.modulo.get("estado", "inactivo")
        self.estado_badge = QLabel(estado.upper())
        self.estado_badge.setCursor(Qt.PointingHandCursor)
        self.estado_badge.setFixedHeight(40)
        self.estado_badge.setAlignment(Qt.AlignCenter)
        self.estado_badge.setToolTip("Haz clic para cambiar el estado del módulo")
        self._actualizar_estado_badge(estado)

        # Conectar evento de clic
        self.estado_badge.mousePressEvent = self._cambiar_estado_click

        info_layout.addWidget(self.estado_badge)
        header_layout.addLayout(info_layout)

        return header

    def _create_lessons_tab(self) -> QWidget:
        """
        Crea la pestaña de lecciones.

        Returns:
            QWidget: Pestaña de lecciones configurada
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 15, 0, 0)

        # Header con título y botón nueva lección
        header = QHBoxLayout()

        lessons_title = QLabel("Lecciones del Módulo")
        lessons_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        lessons_title.setStyleSheet("color: #1e293b;")
        header.addWidget(lessons_title)
        header.addStretch()

        new_lesson_btn = QPushButton("Nueva Lección")
        new_lesson_btn.setStyleSheet(StyleHelper.button_success())
        new_lesson_btn.clicked.connect(self._nueva_leccion)
        header.addWidget(new_lesson_btn)

        layout.addLayout(header)

        # Contenedor de lecciones
        self.lessons_container = QWidget()
        self.lessons_container_layout = QVBoxLayout(self.lessons_container)
        self.lessons_container_layout.setSpacing(12)
        self.lessons_container_layout.setContentsMargins(0, 0, 0, 0)
        self.lessons_container_layout.setAlignment(Qt.AlignTop)

        self.lessons_placeholder = QLabel("Cargando lecciones...")
        self.lessons_placeholder.setStyleSheet(
            "color: #94a3b8; padding: 60px; font-size: 14px;"
        )
        self.lessons_placeholder.setAlignment(Qt.AlignCenter)
        self.lessons_container_layout.addWidget(self.lessons_placeholder)

        layout.addWidget(self.lessons_container)

        return tab

    def _create_evaluation_tab(self) -> QWidget:
        """
        Crea la pestaña de evaluación.

        Returns:
            QWidget: Pestaña de evaluación configurada
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 15, 0, 0)

        # Header con título y botón configurar
        header = QHBoxLayout()

        eval_title = QLabel("Evaluación del Módulo")
        eval_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        eval_title.setStyleSheet("color: #1e293b;")
        header.addWidget(eval_title)
        header.addStretch()

        self.config_eval_btn = QPushButton("Configurar Evaluación")
        self.config_eval_btn.setStyleSheet(StyleHelper.button_primary())
        self.config_eval_btn.clicked.connect(self._configurar_evaluacion)
        header.addWidget(self.config_eval_btn)

        layout.addLayout(header)

        # Contenedor de evaluación
        self.eval_container = QWidget()
        self.eval_container_layout = QVBoxLayout(self.eval_container)
        self.eval_container_layout.setSpacing(15)
        self.eval_container_layout.setContentsMargins(0, 0, 0, 0)

        self.eval_placeholder = QLabel("Cargando evaluación...")
        self.eval_placeholder.setStyleSheet(
            "color: #94a3b8; padding: 60px; font-size: 14px;"
        )
        self.eval_placeholder.setAlignment(Qt.AlignCenter)
        self.eval_container_layout.addWidget(self.eval_placeholder)

        layout.addWidget(self.eval_container)

        return tab

    def _create_info_tab(self) -> QWidget:
        """
        Crea la pestaña de información adicional.

        Returns:
            QWidget: Pestaña de información configurada
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 15, 0, 0)

        # --- DESCRIPCIÓN ---
        desc_group = QFrame()
        desc_group.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e9ecef;
                padding: 20px;
            }
        """
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 10))
        shadow.setOffset(0, 2)
        desc_group.setGraphicsEffect(shadow)

        desc_layout = QVBoxLayout(desc_group)

        desc_title = QLabel("Descripción")
        desc_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        desc_title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        desc_layout.addWidget(desc_title)

        # Limpiar HTML para mostrar
        desc_text = self.modulo.get("descripcion_larga", "Sin descripción")
        desc_text = re.sub("<[^<]+?>", "", desc_text)

        self.desc_label = QLabel(desc_text)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet(
            "color: #475569; line-height: 1.6; font-size: 13px;"
        )
        desc_layout.addWidget(self.desc_label)

        layout.addWidget(desc_group)

        # --- METADATA ADICIONAL ---
        meta_group = QFrame()
        meta_group.setStyleSheet(desc_group.styleSheet())

        meta_layout = QVBoxLayout(meta_group)

        meta_title = QLabel("Información adicional")
        meta_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        meta_title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        meta_layout.addWidget(meta_title)

        grid = QGridLayout()
        grid.setSpacing(15)

        metadata = [
            ("Orden global:", str(self.modulo.get("orden_global", 1)), 0, 0),
            ("Fecha creación:", self.modulo.get("created_at", "No disponible"), 0, 1),
            (
                "Última actualización:",
                self.modulo.get("updated_at", "No disponible"),
                1,
                0,
            ),
            ("ID:", str(self.modulo.get("id", "N/A")), 1, 1),
        ]

        for i, (label, value, row, col) in enumerate(metadata):
            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #64748b; font-size: 12px;")
            grid.addWidget(label_widget, row, col * 2)

            value_widget = QLabel(value)
            value_widget.setStyleSheet(
                "color: #1e293b; font-size: 12px; font-weight: 500;"
            )
            grid.addWidget(value_widget, row, col * 2 + 1)

        meta_layout.addLayout(grid)
        layout.addWidget(meta_group)

        layout.addStretch()

        return tab

    # ============================================================================
    # MÉTODOS DE ACTUALIZACIÓN DE ESTADO
    # ============================================================================

    def _actualizar_estado_badge(self, estado: str) -> None:
        """
        Actualiza el estilo del badge según el estado.

        Args:
            estado: Estado del módulo ("activo" o "inactivo")
        """
        if estado == "activo":
            self.estado_badge.setStyleSheet(
                """
                background-color: #10b981;
                color: white;
                padding: 8px 24px;
                border-radius: 24px;
                font-size: 13px;
                font-weight: bold;
            """
            )
        else:  # inactivo
            self.estado_badge.setStyleSheet(
                """
                background-color: #ef4444;
                color: white;
                padding: 8px 24px;
                border-radius: 24px;
                font-size: 13px;
                font-weight: bold;
            """
            )

    def _cambiar_estado_click(self, event) -> None:
        """
        Maneja el clic en el badge para cambiar el estado.
        """
        if self._cambiando_estado:
            return

        self._cambiando_estado = True

        estado_actual = self.modulo.get("estado", "inactivo")
        nuevo_estado = "inactivo" if estado_actual == "activo" else "activo"

        reply = QMessageBox.question(
            self,
            "Cambiar estado",
            f"¿Cambiar estado del módulo de '{estado_actual}' a '{nuevo_estado}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            self._cambiar_estado_modulo(nuevo_estado)
        else:
            self._cambiando_estado = False

    def _cambiar_estado_modulo(self, nuevo_estado: str) -> None:
        """
        Realiza la petición a la API para cambiar el estado.

        Args:
            nuevo_estado: Nuevo estado a establecer
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:
            result = self.api_client.update_modulo(
                self.modulo["id"], {"estado": nuevo_estado}
            )

            if result["success"]:
                self.modulo["estado"] = nuevo_estado
                self._actualizar_estado_badge(nuevo_estado)

                QApplication.restoreOverrideCursor()
                QMessageBox.information(
                    self, "Éxito", f"Estado cambiado a '{nuevo_estado}' correctamente"
                )

                self.module_updated.emit()
            else:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error al cambiar estado:\n{result.get('error', 'Error desconocido')}",
                )
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")
        finally:
            self._cambiando_estado = False

    # ============================================================================
    # MÉTODOS DE CARGA Y ACTUALIZACIÓN
    # ============================================================================

    def _recargar_evaluacion_con_indicador(self) -> None:
        """Recarga la evaluación mostrando un indicador visual"""
        # Limpiar indicador anterior si existe
        if self.loading_eval_label and not self.loading_eval_label.isHidden():
            self.loading_eval_label.deleteLater()

        self.loading_eval_label = QLabel("Cargando evaluación...")
        self.loading_eval_label.setAlignment(Qt.AlignCenter)
        self.loading_eval_label.setStyleSheet(
            """
            QLabel {
                color: #4361ee;
                padding: 60px;
                font-size: 16px;
                font-weight: bold;
                background-color: white;
                border-radius: 16px;
                border: 2px dashed #4361ee;
            }
        """
        )

        self._clear_layout(self.eval_container_layout)
        self.eval_container_layout.addWidget(self.loading_eval_label)
        QApplication.processEvents()

        QTimer.singleShot(300, self._do_load_evaluacion)

    def _do_load_evaluacion(self) -> None:
        """Carga la evaluación forzando refresco"""
        self._load_evaluacion()

    def _recargar_lecciones_con_indicador(self) -> None:
        """Recarga las lecciones mostrando un indicador visual"""
        if self.loading_lessons_label and not self.loading_lessons_label.isHidden():
            self.loading_lessons_label.deleteLater()

        self.loading_lessons_label = QLabel("Cargando lecciones...")
        self.loading_lessons_label.setAlignment(Qt.AlignCenter)
        self.loading_lessons_label.setStyleSheet(
            """
            QLabel {
                color: #10b981;
                padding: 40px;
                font-size: 14px;
                background-color: #f0fdf4;
                border-radius: 12px;
                border: 2px dashed #10b981;
            }
        """
        )

        self._clear_layout(self.lessons_container_layout)
        self.lessons_container_layout.addWidget(self.loading_lessons_label)
        QApplication.processEvents()
        # Llamar directamente a _load_lecciones sin timer adicional
        self._load_lecciones()

        QTimer.singleShot(300, self._do_load_lecciones)

    def _do_load_lecciones(self) -> None:
        """Carga las lecciones forzando refresco"""
        self._load_lecciones()

    def _load_all_data(self) -> None:
        """Carga todos los datos del módulo"""
        if self._loaded:
            return

        self._recargar_lecciones_con_indicador()
        self._recargar_evaluacion_con_indicador()

        self._loaded = True

    def _update_stats(self) -> None:
        """Actualiza las estadísticas del módulo"""
        stats = {
            "total_lecciones": len(self.lecciones),
        }

        new_stats_widget = StatsWidget(stats)

        # Buscar el contenedor de estadísticas en el layout
        if hasattr(self, "stats_widget") and self.stats_widget:
            # Obtener el layout padre
            parent_layout = self.stats_widget.parent().layout()
            if parent_layout:
                # Encontrar el índice del widget actual
                index = parent_layout.indexOf(self.stats_widget)
                if index >= 0:
                    # Eliminar el widget antiguo
                    old_widget = self.stats_widget
                    parent_layout.removeWidget(old_widget)
                    old_widget.deleteLater()

                    # Insertar el nuevo en la misma posición
                    parent_layout.insertWidget(index, new_stats_widget)
                    self.stats_widget = new_stats_widget
                else:
                    # Si no se encuentra el índice, agregar al final
                    parent_layout.addWidget(new_stats_widget)
                    self.stats_widget = new_stats_widget
        else:
            # Si no existe, guardar referencia
            self.stats_widget = new_stats_widget
            # Aquí deberías agregarlo al layout si es necesario

    def _load_lecciones(self) -> None:
        """Carga las lecciones del módulo desde la API"""
        # Limpiar referencias
        if hasattr(self, "loading_lessons_label") and self.loading_lessons_label:
            self.loading_lessons_label = None

        self._clear_layout(self.lessons_container_layout)

        result = self.api_client.get_lecciones(self.modulo["id"], force_refresh=True)

        if result["success"]:
            data = result.get("data", [])
            self.lecciones = (
                data
                if isinstance(data, list)
                else data.get("data", []) if isinstance(data, dict) else []
            )

            self._update_stats()

            if not self.lecciones:
                empty_label = QLabel("No hay lecciones creadas en este módulo")
                empty_label.setStyleSheet(
                    "color: #94a3b8; padding: 60px; font-size: 14px;"
                )
                empty_label.setAlignment(Qt.AlignCenter)
                self.lessons_container_layout.addWidget(empty_label)
            else:
                lecciones_ordenadas = sorted(
                    self.lecciones, key=lambda x: x.get("orden", 999)
                )
                for leccion in lecciones_ordenadas:
                    item = EnhancedLessonItem(leccion)
                    item.clicked.connect(self._abrir_leccion)
                    item.edit_clicked.connect(self._editar_leccion)
                    item.delete_clicked.connect(self._eliminar_leccion)
                    self.lessons_container_layout.addWidget(item)
        else:
            error_label = QLabel(f"Error al cargar lecciones: {result.get('error')}")
            error_label.setStyleSheet("color: #ef4444; padding: 40px; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            self.lessons_container_layout.addWidget(error_label)
            self.lecciones = []

        self.lessons_container_layout.addStretch()
        QApplication.processEvents()

    def _load_evaluacion(self) -> None:
        """Carga la evaluación del módulo desde la API"""
        if hasattr(self, "loading_eval_label") and self.loading_eval_label:
            self.loading_eval_label = None

        self._clear_layout(self.eval_container_layout)

        result = self.api_client.get_evaluacion(self.modulo["id"], force_refresh=True)

        if result["success"] and result.get("data"):
            # Hay evaluación configurada
            self.evaluacion_actual = result["data"]
            eval_data = self.evaluacion_actual

            # Tarjeta de configuración
            config_card = EvaluationConfigCard(eval_data, self)
            self.eval_container_layout.addWidget(config_card)

            # Botón para agregar preguntas
            add_question_btn = QPushButton("Agregar Pregunta")
            add_question_btn.setFixedHeight(50)
            add_question_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: white;
                    color: #4361ee;
                    border: 2px dashed #4361ee;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #f0f4ff;
                }
            """
            )
            add_question_btn.clicked.connect(self._agregar_pregunta)
            self.eval_container_layout.addWidget(add_question_btn)

            # Preguntas existentes
            preguntas = eval_data.get("preguntas", [])
            if preguntas:
                preguntas_title = QLabel(f"Preguntas ({len(preguntas)})")
                preguntas_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
                preguntas_title.setStyleSheet(
                    "color: #1e293b; margin-top: 20px; margin-bottom: 10px;"
                )
                self.eval_container_layout.addWidget(preguntas_title)

                for pregunta in preguntas:
                    item = QuestionItemWidget(pregunta)
                    item.edit_clicked.connect(self._editar_pregunta)
                    item.delete_clicked.connect(self._eliminar_pregunta)
                    self.eval_container_layout.addWidget(item)
            else:
                no_preguntas_label = QLabel("No hay preguntas creadas aún")
                no_preguntas_label.setStyleSheet(
                    "color: #94a3b8; padding: 40px; font-size: 14px;"
                )
                no_preguntas_label.setAlignment(Qt.AlignCenter)
                self.eval_container_layout.addWidget(no_preguntas_label)

        else:
            # No hay evaluación configurada
            self.evaluacion_actual = None

            empty_frame = QFrame()
            empty_frame.setStyleSheet(
                """
                QFrame {
                    background-color: white;
                    border-radius: 16px;
                    border: 1px solid #e9ecef;
                    padding: 40px;
                }
            """
            )

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setColor(QColor(0, 0, 0, 10))
            shadow.setOffset(0, 2)
            empty_frame.setGraphicsEffect(shadow)

            empty_layout = QVBoxLayout(empty_frame)
            empty_layout.setSpacing(20)
            empty_layout.setAlignment(Qt.AlignCenter)

            icon_label = QLabel("📝")
            icon_label.setStyleSheet("font-size: 48px;")
            empty_layout.addWidget(icon_label)

            text_label = QLabel("No hay evaluación configurada")
            text_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
            text_label.setStyleSheet("color: #1e293b;")
            empty_layout.addWidget(text_label)

            hint_label = QLabel("Configura una evaluación para este módulo")
            hint_label.setStyleSheet("color: #64748b; font-size: 13px;")
            empty_layout.addWidget(hint_label)

            config_now_btn = QPushButton("Configurar Ahora")
            config_now_btn.setFixedHeight(45)
            config_now_btn.setStyleSheet(StyleHelper.button_primary())
            config_now_btn.clicked.connect(self._configurar_evaluacion)
            empty_layout.addWidget(config_now_btn)

            self.eval_container_layout.addWidget(empty_frame)

        self.eval_container_layout.addStretch()

    # ============================================================================
    # CONFIGURACIÓN DE EVALUACIÓN
    # ============================================================================

    def _configurar_evaluacion(self) -> None:
        """Configura la evaluación del módulo"""
        from views.evaluations_view import EvaluationConfigDialog

        dialog = EvaluationConfigDialog(
            self.api_client,
            self.modulo["id"],
            self.evaluacion_actual,
            self,
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                if "titulo" not in data or not data["titulo"]:
                    data["titulo"] = f"Evaluación del Módulo {self.modulo['id']}"

                result = self.api_client.update_evaluacion_config(
                    self.modulo["id"], data
                )

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Evaluación configurada correctamente"
                    )

                    self._recargar_evaluacion_con_indicador()
                    self.module_updated.emit()
                else:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.critical(
                        self, "Error", f"Error al configurar: {result.get('error')}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    # ============================================================================
    # GESTIÓN DE PREGUNTAS
    # ============================================================================

    def _agregar_pregunta(self) -> None:
        """Agrega una nueva pregunta a la evaluación"""
        if not self.evaluacion_actual:
            QMessageBox.warning(
                self,
                "Configuración requerida",
                "Debes configurar la evaluación antes de agregar preguntas.",
            )
            return

        dialog = QuickQuestionDialog(
            self.api_client, self.evaluacion_actual.get("id"), None, self
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.create_pregunta(
                    self.modulo["id"], self.evaluacion_actual.get("id"), data
                )

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Pregunta creada correctamente"
                    )

                    self._recargar_evaluacion_con_indicador()
                else:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.critical(
                        self, "Error", f"Error al crear: {result.get('error')}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    def _eliminar_pregunta(self, pregunta: dict) -> None:
        """
        Elimina una pregunta existente.

        Args:
            pregunta: Datos de la pregunta a eliminar
        """
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar esta pregunta?\n\n"
            f"Pregunta: {pregunta.get('pregunta', '')[:50]}...\n\n"
            f"Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.delete_pregunta(
                    self.modulo["id"],
                    self.evaluacion_actual.get("id"),
                    pregunta["id"],
                )

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Pregunta eliminada correctamente"
                    )

                    self._recargar_evaluacion_con_indicador()
                else:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.critical(
                        self, "Error", f"Error al eliminar: {result.get('error')}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    def _editar_pregunta(self, pregunta: dict) -> None:
        """
        Edita una pregunta existente.

        Args:
            pregunta: Datos de la pregunta a editar
        """
        dialog = QuickQuestionDialog(
            self.api_client, self.evaluacion_actual.get("id"), pregunta, self
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.update_pregunta(
                    self.modulo["id"],
                    self.evaluacion_actual.get("id"),
                    pregunta["id"],
                    data,
                )

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Pregunta actualizada correctamente"
                    )

                    self._recargar_evaluacion_con_indicador()
                else:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.critical(
                        self, "Error", f"Error al actualizar: {result.get('error')}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    def _update_pregunta_opciones(self, pregunta_id: int, opciones: list) -> None:
        """
        Actualiza las opciones de una pregunta.

        Args:
            pregunta_id: ID de la pregunta
            opciones: Lista de opciones actualizadas
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:
            result = self.api_client.update_pregunta_opciones(
                self.modulo["id"],
                self.evaluacion_actual.get("id"),
                pregunta_id,
                opciones,
            )

            if result["success"]:
                QApplication.restoreOverrideCursor()
                QMessageBox.information(
                    self, "Éxito", "Opciones actualizadas correctamente"
                )
                self._recargar_evaluacion_con_indicador()
            else:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error al actualizar opciones: {result.get('error')}",
                )
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    # ============================================================================
    # GESTIÓN DE LECCIONES
    # ============================================================================

    def _nueva_leccion(self) -> None:
        """Crea una nueva lección"""
        dialog = LessonDialog(self.api_client, self.modulo["id"], parent=self)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.create_leccion(self.modulo["id"], data)

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Lección creada correctamente"
                    )

                    self._recargar_lecciones_con_indicador()
                    QTimer.singleShot(500, self._update_stats)
                    self.module_updated.emit()
                else:
                    QApplication.restoreOverrideCursor()
                    error_msg = result.get("error", "Error desconocido")
                    if "errors" in result:
                        error_msg += "\n" + "\n".join(result["errors"])
                    QMessageBox.critical(
                        self, "Error", f"Error al crear lección:\n{error_msg}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    def _editar_leccion(self, leccion: dict) -> None:
        """
        Edita una lección existente.

        Args:
            leccion: Datos de la lección a editar
        """
        dialog = LessonDialog(self.api_client, self.modulo["id"], leccion, self)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.update_leccion(
                    self.modulo["id"], leccion["id"], data
                )

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Lección actualizada correctamente"
                    )

                    self._recargar_lecciones_con_indicador()
                    QTimer.singleShot(500, self._update_stats)
                    self.module_updated.emit()
                else:
                    QApplication.restoreOverrideCursor()
                    error_msg = result.get("error", "Error desconocido")
                    if "errors" in result:
                        error_msg += "\n" + "\n".join(result["errors"])
                    QMessageBox.critical(
                        self, "Error", f"Error al actualizar:\n{error_msg}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    def _eliminar_leccion(self, leccion: dict) -> None:
        """
        Elimina una lección existente.

        Args:
            leccion: Datos de la lección a eliminar
        """
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar la lección '{leccion.get('titulo')}'?\n\n"
            f"Esta acción eliminará TODOS los ejercicios asociados.\n"
            f"No se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.delete_leccion(
                    self.modulo["id"], leccion["id"]
                )

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Lección eliminada correctamente"
                    )

                    self.lecciones = []
                    self._recargar_lecciones_con_indicador()
                    QTimer.singleShot(500, self._update_stats)
                    self.module_updated.emit()
                else:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Error al eliminar lección:\n{result.get('error')}",
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    # ============================================================================
    # GESTIÓN DE MÓDULOS
    # ============================================================================

    def _editar_modulo(self) -> None:
        """Edita el módulo actual"""
        dialog = ModuleDialog(self.api_client, self.modulo, self)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.update_modulo(self.modulo["id"], data)

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Módulo actualizado correctamente"
                    )

                    self.modulo.update(data)
                    self.module_updated.emit()

                    QTimer.singleShot(300, self._load_all_data)
                else:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Error al actualizar módulo: {result.get('error')}",
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    def _eliminar_modulo(self) -> None:
        """Elimina el módulo actual"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar el módulo '{self.modulo.get('titulo')}'?\n\n"
            f"Esta acción eliminará TODAS las lecciones, ejercicios y evaluaciones asociadas.\n"
            f"NO SE PUEDE DESHACER.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.delete_modulo(self.modulo["id"])

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Módulo eliminado correctamente"
                    )

                    self.module_updated.emit()
                else:
                    QApplication.restoreOverrideCursor()
                    error_msg = result.get("error", "Error desconocido")
                    if "errors" in result:
                        error_msg += "\n" + "\n".join(result["errors"])
                    QMessageBox.critical(
                        self, "Error", f"Error al eliminar módulo:\n{error_msg}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error: {str(e)}")

    # ============================================================================
    # MÉTODOS UTILITARIOS
    # ============================================================================

    def _clear_layout(self, layout) -> None:
        """
        Limpia un layout de manera segura.

        Args:
            layout: Layout a limpiar
        """
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                try:
                    widget.blockSignals(True)
                    widget.hide()
                    widget.setParent(None)
                    widget.deleteLater()
                except:
                    pass
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self._clear_layout(sublayout)

        QApplication.processEvents()

    def _abrir_leccion(self, leccion: dict) -> None:
        """
        Abre la vista detallada de una lección.

        Args:
            leccion: Datos de la lección a abrir
        """
        self.lesson_selected.emit(self.modulo, leccion)


# ============================================================================
# VISTA PRINCIPAL: GESTIÓN DE MÓDULOS
# ============================================================================


class ModulesView(QWidget):
    """
    Vista principal que muestra la lista de módulos y permite gestionarlos.
    Incluye búsqueda, creación, edición y eliminación de módulos.
    """

    lesson_selected = pyqtSignal(
        object, object
    )  # Señal cuando se selecciona una lección

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.modulos = []
        self.modulo_actual = None
        self.current_detail_view = None
        self.placeholder = None

        self._setup_ui()

        QTimer.singleShot(0, self._load_modulos)

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario principal"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- HEADER SUPERIOR ---
        header = self._create_header()
        main_layout.addWidget(header)

        # --- SPLITTER PRINCIPAL ---
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(
            """
            QSplitter::handle {
                background-color: #e9ecef;
                width: 1px;
            }
        """
        )

        # Panel izquierdo - Lista de módulos
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)

        # Panel derecho
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("background-color: #f8fafc;")
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        self._create_placeholder()
        splitter.addWidget(self.right_panel)

        splitter.setSizes([450, 850])
        main_layout.addWidget(splitter)

    def _create_header(self) -> QFrame:
        """
        Crea el header superior con título, búsqueda y acciones.

        Returns:
            QFrame: Header configurado
        """
        header = QFrame()
        header.setFixedHeight(90)
        header.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-bottom: 1px solid #e9ecef;
            }
        """
        )

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 0, 40, 0)

        # Título
        title = QLabel("Gestión de Módulos")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Buscador
        search_container = QFrame()
        search_container.setFixedSize(350, 45)
        search_container.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border: 1px solid #e9ecef;
                border-radius: 22px;
            }
        """
        )

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(16, 0, 16, 0)

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 16px;")
        search_layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar módulos por título...")
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                border: none;
                background-color: transparent;
                font-size: 14px;
            }
            QLineEdit:focus {
                outline: none;
            }
        """
        )
        self.search_input.textChanged.connect(self._filtrar_modulos)
        search_layout.addWidget(self.search_input)

        header_layout.addWidget(search_container)

        # Botón refrescar
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(45, 45)
        refresh_btn.setToolTip("Refrescar lista de módulos")
        refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f8fafc;
                color: #4361ee;
                border: 1px solid #e9ecef;
                border-radius: 22px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """
        )
        refresh_btn.clicked.connect(self._refrescar_modulos)
        header_layout.addWidget(refresh_btn)

        # Botón nuevo módulo
        self.new_btn = QPushButton("➕ Nuevo Módulo")
        self.new_btn.setFixedHeight(45)
        self.new_btn.setStyleSheet(
            StyleHelper.button_primary() + "padding: 0 25px; font-size: 14px;"
        )
        self.new_btn.clicked.connect(self._nuevo_modulo)
        header_layout.addWidget(self.new_btn)

        return header

    def _create_left_panel(self) -> QWidget:
        """
        Crea el panel izquierdo con la lista de módulos.

        Returns:
            QWidget: Panel izquierdo configurado
        """
        left_panel = QWidget()
        left_panel.setMinimumWidth(400)
        left_panel.setMaximumWidth(550)
        left_panel.setStyleSheet("background-color: #f8fafc;")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Header del panel izquierdo
        left_header = QWidget()
        left_header.setFixedHeight(70)
        left_header.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e9ecef;
            }
        """
        )

        left_header_layout = QHBoxLayout(left_header)
        left_header_layout.setContentsMargins(25, 0, 25, 0)

        modules_count = QLabel("Módulos")
        modules_count.setFont(QFont("Segoe UI", 16, QFont.Bold))
        modules_count.setStyleSheet("color: #1e293b;")
        left_header_layout.addWidget(modules_count)
        left_header_layout.addStretch()

        self.count_label = QLabel("0")
        self.count_label.setStyleSheet(
            """
            color: #64748b;
            background-color: #f1f5f9;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
        """
        )
        left_header_layout.addWidget(self.count_label)

        left_layout.addWidget(left_header)

        # Lista scrollable de módulos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        self.modulos_container = QWidget()
        self.modulos_layout = QVBoxLayout(self.modulos_container)
        self.modulos_layout.setSpacing(12)
        self.modulos_layout.setContentsMargins(20, 20, 20, 20)
        self.modulos_layout.setAlignment(Qt.AlignTop)

        self.loading_label = QLabel("Cargando módulos...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet(
            "color: #94a3b8; padding: 60px; font-size: 14px;"
        )
        self.modulos_layout.addWidget(self.loading_label)

        scroll.setWidget(self.modulos_container)
        left_layout.addWidget(scroll)

        return left_panel

    def _create_placeholder(self) -> None:
        """Crea el placeholder para cuando no hay módulo seleccionado"""
        if self.placeholder is not None:
            try:
                self.placeholder.deleteLater()
            except:
                pass
            self.placeholder = None

        self.placeholder = QFrame()
        self.placeholder.setStyleSheet("background-color: transparent;")

        placeholder_layout = QVBoxLayout(self.placeholder)
        placeholder_layout.setSpacing(30)
        placeholder_layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel("📚")
        icon_label.setStyleSheet("font-size: 120px; color: #cbd5e1;")
        placeholder_layout.addWidget(icon_label)

        text_label = QLabel("Selecciona un módulo")
        text_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        text_label.setStyleSheet("color: #94a3b8;")
        placeholder_layout.addWidget(text_label)

        hint_label = QLabel(
            "Haz clic en cualquier módulo de la lista para ver sus detalles"
        )
        hint_label.setStyleSheet("color: #94a3b8; font-size: 14px;")
        placeholder_layout.addWidget(hint_label)

        create_btn = QPushButton("Crear Nuevo Módulo")
        create_btn.setFixedHeight(50)
        create_btn.setStyleSheet(
            StyleHelper.button_primary() + "padding: 0 40px; font-size: 14px;"
        )
        create_btn.clicked.connect(self._nuevo_modulo)
        placeholder_layout.addWidget(create_btn)

        self.right_layout.addWidget(self.placeholder)

    def _show_placeholder(self) -> None:
        """Muestra el placeholder en el panel derecho"""
        self._clear_layout_safe(self.right_layout)
        self._create_placeholder()
        if self.placeholder:
            self.placeholder.show()

    def _clear_layout_safe(self, layout) -> None:
        """
        Limpia un layout de manera segura.

        Args:
            layout: Layout a limpiar
        """
        if layout is None:
            return

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                widget = child.widget()
                widget.hide()
                try:
                    widget.deleteLater()
                except:
                    pass

        QApplication.processEvents()

    def _load_modulos(self, force_refresh: bool = False) -> None:
        """
        Carga la lista de módulos desde la API.

        Args:
            force_refresh: Si es True, fuerza la recarga ignorando caché
        """
        self._clear_layout_safe(self.modulos_layout)

        if force_refresh:
            self.api_client.invalidate_cache_type("modulos")

        result = self.api_client.get_modulos(force_refresh=force_refresh)

        if result["success"]:
            data = result.get("data", [])
            self.modulos = (
                data
                if isinstance(data, list)
                else data.get("data", []) if isinstance(data, dict) else []
            )
            self.count_label.setText(str(len(self.modulos)))
            self._mostrar_modulos(self.modulos)

            if self.modulo_actual:
                modulo_existe = any(
                    m.get("id") == self.modulo_actual.get("id") for m in self.modulos
                )
                if not modulo_existe:
                    self.modulo_actual = None
                    QTimer.singleShot(0, self._show_placeholder)
        else:
            error_label = QLabel(f"Error: {result.get('error')}")
            error_label.setStyleSheet("color: #ef4444; padding: 40px; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            self.modulos_layout.addWidget(error_label)

    def _mostrar_modulos(self, modulos: list) -> None:
        """
        Muestra los módulos en el panel izquierdo.

        Args:
            modulos: Lista de módulos a mostrar
        """
        self._clear_layout(self.modulos_layout)

        if not modulos:
            empty_label = QLabel("No hay módulos creados")
            empty_label.setStyleSheet("color: #94a3b8; padding: 60px; font-size: 14px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.modulos_layout.addWidget(empty_label)

            create_btn = QPushButton("Crear Primer Módulo")
            create_btn.setFixedHeight(45)
            create_btn.setStyleSheet(StyleHelper.button_primary())
            create_btn.clicked.connect(self._nuevo_modulo)
            self.modulos_layout.addWidget(create_btn)
        else:
            modulos_ordenados = sorted(
                modulos, key=lambda x: x.get("orden_global", 999)
            )
            for modulo in modulos_ordenados:
                card = ModernCard(modulo)
                card.clicked.connect(self._mostrar_detalle_modulo)
                self.modulos_layout.addWidget(card)

        self.modulos_layout.addStretch()

    def _filtrar_modulos(self) -> None:
        """Filtra los módulos según el texto de búsqueda"""
        texto = self.search_input.text().lower()
        if not texto:
            self._mostrar_modulos(self.modulos)
            return

        filtrados = [m for m in self.modulos if texto in m.get("titulo", "").lower()]
        self._mostrar_modulos(filtrados)

    def _mostrar_detalle_modulo(self, modulo: dict) -> None:
        """
        Muestra la vista detallada del módulo seleccionado.

        Args:
            modulo: Datos del módulo a mostrar
        """
        self.modulo_actual = modulo

        self._clear_layout(self.right_layout)

        self.current_detail_view = ModuleDetailView(self.api_client, modulo)
        self.current_detail_view.module_updated.connect(self._on_module_updated)
        self.current_detail_view.lesson_selected.connect(self._abrir_leccion)
        self.right_layout.addWidget(self.current_detail_view)

    def _abrir_leccion(self, modulo: dict, leccion: dict) -> None:
        """
        Abre la vista de lección.

        Args:
            modulo: Datos del módulo
            leccion: Datos de la lección
        """
        self.lesson_selected.emit(modulo, leccion)

    def _on_module_updated(self) -> None:
        """Manejador cuando se actualiza un módulo"""
        self.api_client.invalidate_cache_type("modulos")
        self._load_modulos(force_refresh=True)
        QTimer.singleShot(100, self._delayed_module_selection)

    def _delayed_module_selection(self) -> None:
        """Selecciona el módulo después de un pequeño retraso"""
        if self.modulo_actual:
            modulo_actualizado = None
            for modulo in self.modulos:
                if modulo.get("id") == self.modulo_actual.get("id"):
                    modulo_actualizado = modulo
                    break

            if modulo_actualizado:
                self._mostrar_detalle_modulo(modulo_actualizado)
            else:
                self.modulo_actual = None
                self._show_placeholder()

    def _refrescar_modulos(self) -> None:
        """Refresca manualmente la lista de módulos"""
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self._load_modulos(force_refresh=True)
        QApplication.restoreOverrideCursor()

        QMessageBox.information(
            self, "Actualizado", "Lista de módulos actualizada correctamente"
        )

    def _nuevo_modulo(self) -> None:
        """Crea un nuevo módulo"""
        dialog = ModuleDialog(self.api_client, parent=self)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.create_modulo(data)
                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Módulo creado correctamente"
                    )

                    self._load_modulos(force_refresh=True)

                    nuevo_modulo = None
                    if result.get("data") and isinstance(result["data"], dict):
                        nuevo_modulo = result["data"]
                    elif self.modulos:
                        nuevo_modulo = self.modulos[-1]

                    if nuevo_modulo:
                        self._mostrar_detalle_modulo(nuevo_modulo)
                    else:
                        self._show_placeholder()
                else:
                    QApplication.restoreOverrideCursor()
                    error_msg = result.get("error", "Error desconocido")
                    if "errors" in result:
                        error_msg += "\n" + "\n".join(result["errors"])
                    QMessageBox.critical(
                        self, "Error", f"Error al crear módulo:\n{error_msg}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error inesperado", f"Error:\n{str(e)}")

    def _clear_layout(self, layout) -> None:
        """
        Limpia un layout de manera segura y completa.

        Args:
            layout: Layout a limpiar
        """
        if layout is None:
            return

        for i in reversed(range(layout.count())):
            child = layout.takeAt(i)
            if child.widget():
                widget = child.widget()
                try:
                    widget.deleteLater()
                except:
                    pass

        QApplication.processEvents()


# ============================================================================
# DIÁLOGO: CREACIÓN/EDICIÓN RÁPIDA DE PREGUNTAS
# ============================================================================


class OpcionDialog(QDialog):
    """
    Diálogo para agregar opciones de respuesta a una pregunta.
    Se adapta según el tipo de pregunta.
    """

    def __init__(self, tipo: str, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.setWindowTitle("Agregar Opción")
        self.setFixedSize(450, 300 if tipo == "arrastrar_soltar" else 250)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario del diálogo"""
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4361ee;
            }
            QLabel {
                font-size: 13px;
                color: #1e293b;
            }
            QCheckBox {
                font-size: 13px;
                color: #1e293b;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        # Título
        title = QLabel("Agregar Nueva Opción")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(title)

        # Texto de la opción
        layout.addWidget(QLabel("Texto de la opción:"))
        self.texto_input = QLineEdit()
        self.texto_input.setPlaceholderText("Escribe la opción...")
        layout.addWidget(self.texto_input)

        # Campo adicional para arrastrar/soltar
        if self.tipo == "arrastrar_soltar":
            layout.addWidget(QLabel("Pareja (definición):"))
            self.pareja_input = QLineEdit()
            self.pareja_input.setPlaceholderText("Ej: HyperText Markup Language")
            layout.addWidget(self.pareja_input)

        # Checkbox para respuesta correcta (solo selección múltiple)
        if self.tipo == "seleccion_multiple":
            self.correcta_check = QCheckBox("Es la respuesta correcta")
            self.correcta_check.setStyleSheet("margin-top: 10px;")
            layout.addWidget(self.correcta_check)

        layout.addStretch()

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Agregar")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            StyleHelper.button_success() + "padding: 8px 25px;"
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            StyleHelper.button_danger() + "padding: 8px 25px;"
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self) -> dict:
        """
        Obtiene los datos de la opción.

        Returns:
            dict: Datos de la opción
        """
        data = {
            "texto": self.texto_input.text(),
            "es_correcta": (
                self.correcta_check.isChecked()
                if hasattr(self, "correcta_check")
                else False
            ),
        }
        if self.tipo == "arrastrar_soltar":
            data["pareja"] = self.pareja_input.text()
        return data


class QuickQuestionDialog(QDialog):
    """
    Diálogo para crear o editar preguntas de forma rápida.
    Soporta diferentes tipos de preguntas y gestión de opciones.
    """

    def __init__(
        self, api_client, evaluacion_id: int, question_data: dict = None, parent=None
    ):
        super().__init__(parent)
        self.api_client = api_client
        self.evaluacion_id = evaluacion_id
        self.question_data = question_data
        self.opciones = []

        self.setWindowTitle("Editar Pregunta" if question_data else "Nueva Pregunta")
        self.setMinimumSize(700, 650)
        self._setup_ui()

        if question_data:
            self._load_question_data()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario del diálogo"""
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 10px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 13px;
                background-color: #f8fafc;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #4361ee;
                background-color: white;
            }
            QLabel {
                font-size: 13px;
                color: #1e293b;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("Editar Pregunta" if self.question_data else "Nueva Pregunta")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(title)

        # --- TIPO Y PUNTOS (en fila) ---
        tipo_puntos_layout = QHBoxLayout()
        tipo_puntos_layout.setSpacing(20)

        # Tipo de pregunta
        tipo_group = self._create_field_group("Tipo de pregunta")
        tipo_group_layout = QVBoxLayout(tipo_group)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["seleccion_multiple", "verdadero_falso", "arrastrar_soltar"]
        )
        self.tipo_combo.currentTextChanged.connect(self._cambiar_tipo)
        tipo_group_layout.addWidget(self.tipo_combo)

        tipo_puntos_layout.addWidget(tipo_group)

        # Puntos
        puntos_group = self._create_field_group("Puntos")
        puntos_group_layout = QVBoxLayout(puntos_group)

        self.puntos_input = QDoubleSpinBox()
        self.puntos_input.setRange(0.5, 100)
        self.puntos_input.setValue(10)
        self.puntos_input.setSingleStep(0.5)
        puntos_group_layout.addWidget(self.puntos_input)

        tipo_puntos_layout.addWidget(puntos_group)
        layout.addLayout(tipo_puntos_layout)

        # --- PREGUNTA ---
        pregunta_group = self._create_field_group("Pregunta")
        pregunta_layout = QVBoxLayout(pregunta_group)

        self.pregunta_input = QTextEdit()
        self.pregunta_input.setPlaceholderText("Escribe la pregunta...")
        self.pregunta_input.setMaximumHeight(100)
        pregunta_layout.addWidget(self.pregunta_input)

        layout.addWidget(pregunta_group)

        # --- OPCIONES ---
        self.opciones_group = QGroupBox("Opciones de Respuesta")
        opciones_layout = QVBoxLayout()

        # Toolbar para opciones
        toolbar = QHBoxLayout()

        self.add_opcion_btn = QPushButton("Agregar Opción")
        self.add_opcion_btn.setStyleSheet(StyleHelper.button_success())
        self.add_opcion_btn.clicked.connect(self._agregar_opcion)
        toolbar.addWidget(self.add_opcion_btn)

        self.remove_opcion_btn = QPushButton("Eliminar Seleccionada")
        self.remove_opcion_btn.setStyleSheet(StyleHelper.button_danger())
        self.remove_opcion_btn.clicked.connect(self._eliminar_opcion)
        toolbar.addWidget(self.remove_opcion_btn)

        toolbar.addStretch()
        opciones_layout.addLayout(toolbar)

        # Lista de opciones
        self.opciones_list = QListWidget()
        self.opciones_list.setMaximumHeight(200)
        self.opciones_list.setStyleSheet(
            """
            QListWidget {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f1f5f9;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #e1f5fe;
            }
        """
        )
        opciones_layout.addWidget(self.opciones_list)

        self.opciones_group.setLayout(opciones_layout)
        layout.addWidget(self.opciones_group)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar Pregunta")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            StyleHelper.button_primary() + "padding: 10px 35px; font-size: 14px;"
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            StyleHelper.button_danger() + "padding: 10px 35px; font-size: 14px;"
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._cambiar_tipo(self.tipo_combo.currentText())

    def _create_field_group(self, title: str) -> QFrame:
        """
        Crea un grupo con estilo para campos de formulario.

        Args:
            title: Título del grupo

        Returns:
            QFrame configurado como grupo de campo
        """
        group = QFrame()
        group.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 15px;
            }
        """
        )

        label = QLabel(title)
        label.setFont(QFont("Segoe UI", 12, QFont.Bold))

        layout = QVBoxLayout(group)
        layout.addWidget(label)

        return group

    def _cambiar_tipo(self, tipo: str) -> None:
        """
        Cambia la interfaz según el tipo de pregunta seleccionado.

        Args:
            tipo: Tipo de pregunta
        """
        if tipo == "verdadero_falso":
            self.add_opcion_btn.setEnabled(False)
            self.remove_opcion_btn.setEnabled(False)
            self.opciones_list.clear()

            item1 = QListWidgetItem("✓ Verdadero")
            item1.setData(
                Qt.UserRole, {"texto": "Verdadero", "es_correcta": True, "orden": 1}
            )
            self.opciones_list.addItem(item1)

            item2 = QListWidgetItem("✗ Falso")
            item2.setData(
                Qt.UserRole, {"texto": "Falso", "es_correcta": False, "orden": 2}
            )
            self.opciones_list.addItem(item2)
        else:
            self.add_opcion_btn.setEnabled(True)
            self.remove_opcion_btn.setEnabled(True)

    def _agregar_opcion(self) -> None:
        """Abre el diálogo para agregar una nueva opción"""
        dialog = OpcionDialog(self.tipo_combo.currentText(), self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            item_text = data["texto"]
            if self.tipo_combo.currentText() == "arrastrar_soltar" and data.get(
                "pareja"
            ):
                item_text = f"{data['texto']} → {data['pareja']}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, data)

            if data.get("es_correcta"):
                item.setForeground(QColor("#10b981"))
                item.setFont(QFont("Segoe UI", 10, QFont.Bold))

            self.opciones_list.addItem(item)

    def _eliminar_opcion(self) -> None:
        """Elimina la opción seleccionada de la lista"""
        current_row = self.opciones_list.currentRow()
        if current_row >= 0:
            self.opciones_list.takeItem(current_row)

    def _load_question_data(self) -> None:
        """Carga los datos de la pregunta existente en el formulario"""
        self.pregunta_input.setPlainText(self.question_data.get("pregunta", ""))
        self.puntos_input.setValue(float(self.question_data.get("puntos", 10)))

        tipo = self.question_data.get("tipo", "seleccion_multiple")
        index = self.tipo_combo.findText(tipo)
        if index >= 0:
            self.tipo_combo.setCurrentIndex(index)

        opciones = self.question_data.get("opciones", [])
        self.opciones_list.clear()

        for opcion in opciones:
            item_text = opcion["texto"]
            if tipo == "arrastrar_soltar" and opcion.get("pareja_arrastre"):
                item_text = f"{opcion['texto']} → {opcion['pareja_arrastre']}"

            item = QListWidgetItem(item_text)
            item.setData(
                Qt.UserRole,
                {
                    "texto": opcion["texto"],
                    "es_correcta": opcion.get("es_correcta", False),
                    "pareja": opcion.get("pareja_arrastre"),
                    "orden": opcion.get("orden", 1),
                },
            )

            if opcion.get("es_correcta"):
                item.setForeground(QColor("#10b981"))

            self.opciones_list.addItem(item)

    def get_data(self) -> dict:
        """
        Obtiene los datos de la pregunta del formulario.

        Returns:
            dict: Datos de la pregunta
        """
        opciones = []
        for i in range(self.opciones_list.count()):
            item = self.opciones_list.item(i)
            data = item.data(Qt.UserRole)
            if data:
                data["orden"] = i + 1
                opciones.append(data)

        return {
            "pregunta": self.pregunta_input.toPlainText(),
            "tipo": self.tipo_combo.currentText(),
            "puntos": self.puntos_input.value(),
            "opciones": opciones,
        }
