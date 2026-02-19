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
from utils.paths import resource_path
from views.lessons_view import LessonDialog
from views.components.rich_text_editor import RichTextEditor

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


# ============================================================================
# CLASES DE ESTILO Y UTILIDADES
# ============================================================================


class StyleHelper:
    """Clase helper para mantener estilos consistentes"""

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
    def card_style():
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
    def button_primary():
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
    def button_success():
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
    def button_danger():
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
    def button_warning():
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
    def badge_active():
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
    def badge_inactive():
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
    def badge_draft():
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


class ModernCard(QFrame):
    """Tarjeta moderna con sombra y efectos"""

    clicked = pyqtSignal(object)

    def __init__(self, modulo, parent=None):
        super().__init__(parent)
        self.modulo = modulo
        self.setup_ui()
        self.setup_shadow()
        self.setup_animations()

    def setup_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def setup_ui(self):
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

        # Header con icono y título
        header = QHBoxLayout()
        header.setSpacing(12)

        # Icono según tipo
        icon_map = {
            "html": "🌐",
            "css": "🎨",
            "javascript": "⚡",
            "php": "🐘",
            "sql": "🗄️",
            "introduccion": "📘",
        }
        icon = icon_map.get(self.modulo.get("modulo", ""), "📚")

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 28px;")
        header.addWidget(icon_label)

        # Título
        titulo = self.modulo.get("titulo", "Sin título")
        if len(titulo) > 40:
            titulo = titulo[:37] + "..."

        title = QLabel(titulo)
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        header.addWidget(title, 1)

        # Badge de tipo
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

        # Descripción
        desc = self.modulo.get("descripcion_larga", "Sin descripción")
        if desc:
            # Limpiar HTML si existe
            import re

            desc = re.sub("<[^<]+?>", "", desc)
            palabras = desc.split()[:15]
            desc = " ".join(palabras) + ("..." if len(palabras) == 15 else "")

        desc_label = QLabel(desc)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #64748b; font-size: 12px; line-height: 1.5;")
        desc_label.setFixedHeight(50)
        layout.addWidget(desc_label)

        # Barra de progreso
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

        # Footer con estadísticas y estado
        footer = QHBoxLayout()
        footer.setSpacing(16)

        # Estadísticas
        stats = [
            f"📚 {self.modulo.get('total_lecciones', 0)} lecciones",
            f"⏱️ {self.modulo.get('duracion', 0)} min",
        ]

        for stat in stats:
            stat_label = QLabel(stat)
            stat_label.setStyleSheet(
                "color: #4361ee; font-size: 11px; font-weight: 500;"
            )
            footer.addWidget(stat_label)

        footer.addStretch()

        # Badge de estado
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

        # Orden
        orden_label = QLabel(f"Orden #{self.modulo.get('orden_global', 1)}")
        orden_label.setStyleSheet("color: #94a3b8; font-size: 10px;")
        orden_label.setAlignment(Qt.AlignRight)
        layout.addWidget(orden_label)

    def mousePressEvent(self, event):
        self.clicked.emit(self.modulo)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(self.pos().x(), self.pos().y() - 2))
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(self.pos().x(), self.pos().y() + 2))
        self.animation.start()
        super().leaveEvent(event)


class EnhancedLessonItem(QWidget):
    """Item de lección con diseño profesional"""

    clicked = pyqtSignal(object)
    edit_clicked = pyqtSignal(object)
    delete_clicked = pyqtSignal(object)

    def __init__(self, leccion, parent=None):
        super().__init__(parent)
        self.leccion = leccion
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(90)
        self.setCursor(Qt.PointingHandCursor)

        # Sombra
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

        # Icono con indicador de ejercicios
        icon_container = QFrame()
        icon_container.setFixedSize(48, 48)
        icon_container.setStyleSheet(
            """
            QFrame {
                background-color: #f1f5f9;
                border-radius: 12px;
            }
        """
        )

        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setAlignment(Qt.AlignCenter)

        icon = "✏️" if self.leccion.get("tiene_ejercicios") else "📖"
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        icon_layout.addWidget(icon_label)

        layout.addWidget(icon_container)

        # Contenido principal
        content = QVBoxLayout()
        content.setSpacing(6)

        # Título
        titulo = self.leccion.get("titulo", "Sin título")
        if len(titulo) > 50:
            titulo = titulo[:47] + "..."

        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        titulo_label.setStyleSheet("color: #1e293b;")
        content.addWidget(titulo_label)

        # Metadata
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(20)

        # Orden
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

        # Tipo
        if self.leccion.get("tipo_contenido"):
            tipo_label = QLabel(f"📄 {self.leccion.get('tipo_contenido')}")
            tipo_label.setStyleSheet("color: #64748b; font-size: 11px;")
            meta_layout.addWidget(tipo_label)

        meta_layout.addStretch()
        content.addLayout(meta_layout)

        layout.addLayout(content, 1)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        # Botón editar
        self.edit_btn = QPushButton("✏️ Editar")
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
        self.delete_btn = QPushButton("🗑️ Eliminar")
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

    def mousePressEvent(self, event):
        if not self.edit_btn.underMouse() and not self.delete_btn.underMouse():
            self.clicked.emit(self.leccion)
        super().mousePressEvent(event)


class StatsWidget(QWidget):
    """Widget de estadísticas con diseño de tarjetas"""

    def __init__(self, stats_data, parent=None):
        super().__init__(parent)
        self.stats_data = stats_data
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        stats = [
            ("📚 Lecciones", self.stats_data.get("total_lecciones", 0), "#4361ee"),
            ("📝 Ejercicios", self.stats_data.get("total_ejercicios", 0), "#f72585"),
            ("⏱️ Duración", f"{self.stats_data.get('duracion', 0)} min", "#4cc9f0"),
            ("📊 Progreso", f"{self.stats_data.get('progreso', 0)}%", "#f8961e"),
        ]

        for titulo, valor, color in stats:
            card = QFrame()
            card.setFixedHeight(100)

            # Sombra
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QColor(0, 0, 0, 15))
            shadow.setOffset(0, 2)
            card.setGraphicsEffect(shadow)

            card.setStyleSheet(
                """
                QFrame {
                    background-color: white;
                    border-radius: 12px;
                    border: 1px solid #e9ecef;
                }
            """
            )

            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(8)
            card_layout.setContentsMargins(16, 12, 16, 12)

            titulo_label = QLabel(titulo)
            titulo_label.setStyleSheet("color: #64748b; font-size: 12px;")
            card_layout.addWidget(titulo_label)

            valor_label = QLabel(str(valor))
            valor_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
            valor_label.setStyleSheet(f"color: {color};")
            card_layout.addWidget(valor_label)

            layout.addWidget(card, 1)


class EvaluationConfigCard(QFrame):
    """Tarjeta de configuración de evaluación"""

    def __init__(self, eval_data, parent=None):
        super().__init__(parent)
        self.eval_data = eval_data
        self.setup_ui()

    def setup_ui(self):
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

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

        # Header
        header = QHBoxLayout()

        title = QLabel("⚙️ Configuración de Evaluación")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1e293b;")
        header.addWidget(title)

        header.addStretch()

        # Badge de estado
        if self.eval_data.get("activa"):
            status_badge = QLabel("ACTIVA")
            status_badge.setStyleSheet(StyleHelper.badge_active())
        else:
            status_badge = QLabel("INACTIVA")
            status_badge.setStyleSheet(StyleHelper.badge_inactive())

        header.addWidget(status_badge)

        layout.addLayout(header)

        # Grid de parámetros
        grid = QGridLayout()
        grid.setSpacing(16)

        params = [
            (
                "⏱️ Tiempo límite",
                f"{self.eval_data.get('tiempo_limite', 0)} minutos",
                0,
                0,
            ),
            ("🎯 Puntaje mínimo", f"{self.eval_data.get('puntaje_minimo', 0)}%", 0, 1),
            ("🔄 Intentos máximos", str(self.eval_data.get("max_intentos", 0)), 1, 0),
            ("📊 Total preguntas", str(len(self.eval_data.get("preguntas", []))), 1, 1),
        ]

        for label, value, row, col in params:
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

            grid.addWidget(param_frame, row, col)

        layout.addLayout(grid)


class QuestionItemWidget(QWidget):
    """Widget para item de pregunta con diseño profesional"""

    clicked = pyqtSignal(object)
    edit_clicked = pyqtSignal(object)
    delete_clicked = pyqtSignal(object)

    def __init__(self, pregunta, parent=None):
        super().__init__(parent)
        self.pregunta = pregunta
        self.setup_ui()

    def setup_ui(self):
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

        # Tipo
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

        tipo_icon = {
            "seleccion_multiple": "📝",
            "verdadero_falso": "✓",
            "arrastrar_soltar": "🔄",
        }.get(self.pregunta.get("tipo", ""), "📝")

        icon_label = QLabel(tipo_icon)
        icon_label.setStyleSheet("font-size: 24px;")
        tipo_layout.addWidget(icon_label)

        layout.addWidget(tipo_frame)

        # Contenido
        content = QVBoxLayout()
        content.setSpacing(4)

        pregunta_text = self.pregunta.get("pregunta", "")
        if len(pregunta_text) > 60:
            pregunta_text = pregunta_text[:57] + "..."

        pregunta_label = QLabel(pregunta_text)
        pregunta_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        pregunta_label.setStyleSheet("color: #1e293b;")
        content.addWidget(pregunta_label)

        # Metadata
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)

        puntos_label = QLabel(f"⚡ {self.pregunta.get('puntos', 0)} puntos")
        puntos_label.setStyleSheet("color: #f8961e; font-size: 11px; font-weight: 500;")
        meta_layout.addWidget(puntos_label)

        opciones = self.pregunta.get("opciones", [])
        if opciones:
            total = len(opciones)
            if self.pregunta.get("tipo") == "arrastrar_soltar":
                info = f"🔄 {total} pares"
            elif self.pregunta.get("tipo") == "verdadero_falso":
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

        # Puntos y botones
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

    def mousePressEvent(self, event):
        if not self.edit_btn.underMouse() and not self.delete_btn.underMouse():
            self.clicked.emit(self.pregunta)
        super().mousePressEvent(event)


class ModuleDialog(QDialog):
    """Diálogo para crear/editar módulo con diseño moderno"""

    def __init__(self, api_client, modulo_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_data = modulo_data
        self.modulos_existentes = []
        self.setWindowTitle("Editar Módulo" if modulo_data else "Nuevo Módulo")
        self.setMinimumSize(700, 600)
        self.setModal(True)

        QTimer.singleShot(0, self.cargar_modulos_existentes)
        self.setup_ui()

        if modulo_data:
            self.load_data()

    def cargar_modulos_existentes(self):
        result = self.api_client.get_modulos()
        if result["success"]:
            data = result.get("data", [])
            self.modulos_existentes = (
                data
                if isinstance(data, list)
                else data.get("data", []) if isinstance(data, dict) else []
            )
            if not self.modulo_data:
                self.orden_spin.setValue(self.obtener_siguiente_orden())

    def setup_ui(self):
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

        # Título
        title = QLabel(
            "📚 " + ("Editar Módulo" if self.modulo_data else "Nuevo Módulo")
        )
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(title)

        # Formulario
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Título
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Ej: Introducción a HTML")
        self.titulo_input.textChanged.connect(self.validar_campos)
        form_layout.addRow("Título:", self.titulo_input)

        # Tipo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["html", "css", "javascript", "php", "sql", "introduccion"]
        )
        form_layout.addRow("Tipo:", self.tipo_combo)

        layout.addWidget(form_widget)

        # Descripción
        desc_label = QLabel("📝 Descripción:")
        desc_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        desc_label.setStyleSheet("margin-top: 10px;")
        layout.addWidget(desc_label)

        from views.components.rich_text_editor import RichTextEditor

        self.descripcion_editor = RichTextEditor()
        self.descripcion_editor.setMinimumHeight(200)
        self.descripcion_editor.editor.textChanged.connect(self.validar_campos)
        layout.addWidget(self.descripcion_editor)

        # Orden y Estado
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # Orden
        orden_group = QFrame()
        orden_group.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 15px;
            }
        """
        )
        orden_layout = QVBoxLayout(orden_group)

        orden_label = QLabel("Orden del módulo")
        orden_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        orden_layout.addWidget(orden_label)

        self.orden_spin = QSpinBox()
        self.orden_spin.setRange(1, 999)
        self.orden_spin.setValue(1)
        orden_layout.addWidget(self.orden_spin)

        bottom_layout.addWidget(orden_group)

        # Estado
        estado_group = QFrame()
        estado_group.setStyleSheet(orden_group.styleSheet())
        estado_layout = QVBoxLayout(estado_group)

        estado_label = QLabel("Estado del módulo")
        estado_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        estado_layout.addWidget(estado_label)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo", "borrador"])
        estado_layout.addWidget(self.estado_combo)

        bottom_layout.addWidget(estado_group)

        layout.addLayout(bottom_layout)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar Módulo")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            StyleHelper.button_primary() + "padding: 10px 30px;"
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            StyleHelper.button_danger() + "padding: 10px 30px;"
        )

        # Deshabilitar el botón OK inicialmente
        self.ok_button = buttons.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        # Validar campos inicialmente
        self.validar_campos()

    def validar_campos(self):
        """Validar que los campos requeridos no estén vacíos"""
        titulo = self.titulo_input.text().strip()
        descripcion = self.descripcion_editor.toPlainText().strip()

        # Habilitar botón solo si ambos campos tienen contenido
        self.ok_button.setEnabled(bool(titulo and descripcion))

    def obtener_siguiente_orden(self):
        if not self.modulos_existentes:
            return 1
        ordenes = [
            m.get("orden_global", 0)
            for m in self.modulos_existentes
            if not self.modulo_data or m["id"] != self.modulo_data.get("id")
        ]
        return max(ordenes) + 1 if ordenes else 1

    def load_data(self):
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

        # Validar después de cargar datos
        self.validar_campos()

    def get_data(self):
        """Obtener datos del formulario"""
        titulo = self.titulo_input.text().strip()
        descripcion_html = self.descripcion_editor.toHtml()
        descripcion_texto = self.descripcion_editor.toPlainText().strip()

        # Si no hay título o descripción, mostrar error
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

    def accept(self):
        """Sobrescribir accept para validar antes de cerrar"""
        data = self.get_data()
        if data is None:
            return  # No cerrar el diálogo si hay error
        super().accept()


class ModuleDetailView(QWidget):
    """Vista de detalle de módulo con diseño profesional"""

    module_updated = pyqtSignal()
    lesson_selected = pyqtSignal(object, object)

    def __init__(self, api_client, modulo, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo = modulo
        self.lecciones = []
        self.evaluacion_actual = None
        self._loaded = False
        self.setup_ui()

        QTimer.singleShot(50, self.load_all_data)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header con gradiente
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

        # Navegación
        nav_layout = QHBoxLayout()

        back_btn = QPushButton("← Volver a Módulos")
        back_btn.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """
        )
        back_btn.clicked.connect(self.cancelar)
        nav_layout.addWidget(back_btn)

        nav_layout.addStretch()

        # Acciones
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        edit_btn = QPushButton("✏️ Editar Módulo")
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
        edit_btn.clicked.connect(self.editar_modulo)
        actions_layout.addWidget(edit_btn)

        # Botón eliminar
        delete_btn = QPushButton("🗑️ Eliminar Módulo")
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
        delete_btn.clicked.connect(self.eliminar_modulo)
        actions_layout.addWidget(delete_btn)

        nav_layout.addLayout(actions_layout)
        header_layout.addLayout(nav_layout)

        # Info del módulo
        info_layout = QHBoxLayout()
        info_layout.setSpacing(30)

        # Título y tipo
        title_info = QVBoxLayout()
        title_info.setSpacing(10)

        tipo_badge = QLabel(self.modulo.get("modulo", "html").upper())
        tipo_badge.setStyleSheet(
            """
            background-color: rgba(255,255,255,0.2);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            max-width: 100px;
        """
        )
        title_info.addWidget(tipo_badge)

        titulo = self.modulo.get("titulo", "Módulo")
        title_label = QLabel(titulo)
        title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setWordWrap(True)
        title_info.addWidget(title_label)

        info_layout.addLayout(title_info)
        info_layout.addStretch()

        # Estado
        estado = self.modulo.get("estado", "inactivo")
        estado_badge = QLabel(estado.upper())
        if estado == "activo":
            estado_badge.setStyleSheet(
                """
                background-color: #10b981;
                color: white;
                padding: 8px 24px;
                border-radius: 24px;
                font-size: 13px;
                font-weight: bold;
            """
            )
        elif estado == "inactivo":
            estado_badge.setStyleSheet(
                """
                background-color: #ef4444;
                color: white;
                padding: 8px 24px;
                border-radius: 24px;
                font-size: 13px;
                font-weight: bold;
            """
            )
        else:
            estado_badge.setStyleSheet(
                """
                background-color: #f59e0b;
                color: white;
                padding: 8px 24px;
                border-radius: 24px;
                font-size: 13px;
                font-weight: bold;
            """
            )

        info_layout.addWidget(estado_badge)

        header_layout.addLayout(info_layout)
        main_layout.addWidget(header)

        # Contenido con tabs
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

        # Stats
        self.stats_widget = StatsWidget(
            {"total_lecciones": 0, "total_ejercicios": 0, "duracion": 0, "progreso": 0}
        )
        content_layout.addWidget(self.stats_widget)

        # Tabs
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
                padding: 12px 24px;
                margin-right: 4px;
                font-size: 13px;
                font-weight: 500;
                color: #64748b;
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

        # Tab Lecciones
        self.lessons_tab = QWidget()
        lessons_layout = QVBoxLayout(self.lessons_tab)
        lessons_layout.setSpacing(20)
        lessons_layout.setContentsMargins(0, 15, 0, 0)

        # Header de lecciones
        lessons_header = QHBoxLayout()

        lessons_title = QLabel("📚 Lecciones del Módulo")
        lessons_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        lessons_title.setStyleSheet("color: #1e293b;")
        lessons_header.addWidget(lessons_title)

        lessons_header.addStretch()

        new_lesson_btn = QPushButton("➕ Nueva Lección")
        new_lesson_btn.setStyleSheet(StyleHelper.button_success())
        new_lesson_btn.clicked.connect(self.nueva_leccion)
        lessons_header.addWidget(new_lesson_btn)

        lessons_layout.addLayout(lessons_header)

        # Contenedor de lecciones
        self.lessons_container = QWidget()
        self.lessons_container_layout = QVBoxLayout(self.lessons_container)
        self.lessons_container_layout.setSpacing(12)
        self.lessons_container_layout.setContentsMargins(0, 0, 0, 0)
        self.lessons_container_layout.setAlignment(Qt.AlignTop)

        self.lessons_placeholder = QLabel("📭 Cargando lecciones...")
        self.lessons_placeholder.setStyleSheet(
            "color: #94a3b8; padding: 60px; font-size: 14px;"
        )
        self.lessons_placeholder.setAlignment(Qt.AlignCenter)
        self.lessons_container_layout.addWidget(self.lessons_placeholder)

        lessons_layout.addWidget(self.lessons_container)

        # Tab Evaluación
        self.eval_tab = QWidget()
        eval_layout = QVBoxLayout(self.eval_tab)
        eval_layout.setSpacing(20)
        eval_layout.setContentsMargins(0, 15, 0, 0)

        # Header de evaluación
        eval_header = QHBoxLayout()

        eval_title = QLabel("📝 Evaluación del Módulo")
        eval_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        eval_title.setStyleSheet("color: #1e293b;")
        eval_header.addWidget(eval_title)

        eval_header.addStretch()

        self.config_eval_btn = QPushButton("⚙️ Configurar Evaluación")
        self.config_eval_btn.setStyleSheet(StyleHelper.button_primary())
        self.config_eval_btn.clicked.connect(self.configurar_evaluacion)
        eval_header.addWidget(self.config_eval_btn)

        eval_layout.addLayout(eval_header)

        # Contenedor de evaluación
        self.eval_container = QWidget()
        self.eval_container_layout = QVBoxLayout(self.eval_container)
        self.eval_container_layout.setSpacing(15)
        self.eval_container_layout.setContentsMargins(0, 0, 0, 0)

        self.eval_placeholder = QLabel("📭 Cargando evaluación...")
        self.eval_placeholder.setStyleSheet(
            "color: #94a3b8; padding: 60px; font-size: 14px;"
        )
        self.eval_placeholder.setAlignment(Qt.AlignCenter)
        self.eval_container_layout.addWidget(self.eval_placeholder)

        eval_layout.addWidget(self.eval_container)

        # Tab Información
        self.info_tab = QWidget()
        info_layout = QVBoxLayout(self.info_tab)
        info_layout.setSpacing(20)
        info_layout.setContentsMargins(0, 15, 0, 0)

        # Descripción
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

        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 10))
        shadow.setOffset(0, 2)
        desc_group.setGraphicsEffect(shadow)

        desc_layout = QVBoxLayout(desc_group)

        desc_title = QLabel("📄 Descripción")
        desc_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        desc_title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        desc_layout.addWidget(desc_title)

        # Limpiar HTML para mostrar
        desc_text = self.modulo.get("descripcion_larga", "Sin descripción")
        import re

        desc_text = re.sub("<[^<]+?>", "", desc_text)

        self.desc_label = QLabel(desc_text)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet(
            "color: #475569; line-height: 1.6; font-size: 13px;"
        )
        desc_layout.addWidget(self.desc_label)

        info_layout.addWidget(desc_group)

        # Metadata
        meta_group = QFrame()
        meta_group.setStyleSheet(desc_group.styleSheet())

        meta_layout = QVBoxLayout(meta_group)

        meta_title = QLabel("📊 Información adicional")
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
        info_layout.addWidget(meta_group)

        info_layout.addStretch()

        self.tabs.addTab(self.lessons_tab, "📚 Lecciones")
        self.tabs.addTab(self.eval_tab, "📝 Evaluación")
        self.tabs.addTab(self.info_tab, "ℹ️ Información")

        content_layout.addWidget(self.tabs)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def eliminar_modulo(self):
        """Eliminar el módulo actual"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar el módulo '{self.modulo.get('titulo')}'?\n"
            "Esta acción eliminará TODAS las lecciones, ejercicios y evaluaciones asociadas.\n"
            "No se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # Mostrar indicador de carga
            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.delete_modulo(self.modulo["id"])

                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Módulo eliminado correctamente"
                    )
                    # Volver a la lista de módulos
                    self.module_updated.emit()  # Esto actualizará la vista principal
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
                QMessageBox.critical(self, "Error", f"Error inesperado:\n{str(e)}")

    def load_all_data(self):
        """Cargar todos los datos del módulo"""
        if self._loaded:
            return

        # Cargar lecciones
        self.load_lecciones()

        # Cargar evaluación
        self.load_evaluacion()

        # Actualizar estadísticas después de cargar datos
        QTimer.singleShot(100, self.update_stats)

        self._loaded = True

    def update_stats(self):
        """Actualizar estadísticas del módulo"""
        stats = {
            "total_lecciones": len(self.lecciones),
            "total_ejercicios": sum(
                1 for l in self.lecciones if l.get("tiene_ejercicios", False)
            ),
            "duracion": sum(l.get("duracion", 0) for l in self.lecciones),
            "progreso": 0,
        }

        # Crear nuevo widget de estadísticas
        new_stats_widget = StatsWidget(stats)

        # Buscar el contenedor de estadísticas en el layout
        # Asumiendo que stats_widget está en content_layout (el layout del contenido)
        if hasattr(self, "stats_widget") and self.stats_widget:
            # Obtener el layout padre
            parent = self.stats_widget.parent()
            if parent and parent.layout():
                layout = parent.layout()
                # Reemplazar el widget
                index = layout.indexOf(self.stats_widget)
                if index >= 0:
                    layout.removeWidget(self.stats_widget)
                    self.stats_widget.deleteLater()
                    layout.insertWidget(index, new_stats_widget)
                    self.stats_widget = new_stats_widget
                else:
                    # Si no se encuentra el índice, agregar al final
                    layout.addWidget(new_stats_widget)
                    self.stats_widget = new_stats_widget
            else:
                # No hay padre, probablemente estamos en inicialización
                # Solo guardar el nuevo widget
                self.stats_widget = new_stats_widget
        else:
            # Primera vez que se crea
            self.stats_widget = new_stats_widget

    def load_lecciones(self):
        """Cargar lecciones del módulo"""
        # Limpiar el layout actual
        self.clear_layout(self.lessons_container_layout)

        # Mostrar indicador de carga
        loading_label = QLabel("🔄 Cargando lecciones...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("color: #94a3b8; padding: 40px; font-size: 14px;")
        self.lessons_container_layout.addWidget(loading_label)

        # Procesar eventos para mostrar el indicador
        QApplication.processEvents()

        # Hacer la petición a la API
        result = self.api_client.get_lecciones(self.modulo["id"], force_refresh=True)

        if result["success"]:
            data = result.get("data", [])
            self.lecciones = (
                data
                if isinstance(data, list)
                else data.get("data", []) if isinstance(data, dict) else []
            )

            # Limpiar de nuevo antes de agregar los items
            self.clear_layout(self.lessons_container_layout)

            if not self.lecciones:
                empty_label = QLabel("📭 No hay lecciones creadas en este módulo")
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
                    item.clicked.connect(self.abrir_leccion)
                    item.edit_clicked.connect(self.editar_leccion)
                    item.delete_clicked.connect(self.eliminar_leccion)
                    self.lessons_container_layout.addWidget(item)
        else:
            # Limpiar y mostrar error
            self.clear_layout(self.lessons_container_layout)
            error_label = QLabel(f"❌ Error al cargar lecciones: {result.get('error')}")
            error_label.setStyleSheet("color: #ef4444; padding: 40px; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            self.lessons_container_layout.addWidget(error_label)
            self.lecciones = []

        self.lessons_container_layout.addStretch()

        # Forzar actualización de la interfaz
        QApplication.processEvents()

    def load_evaluacion(self):
        self.clear_layout(self.eval_container_layout)

        result = self.api_client.get_evaluacion(self.modulo["id"])

        if result["success"] and result.get("data"):
            self.evaluacion_actual = result["data"]
            eval_data = self.evaluacion_actual

            # Tarjeta de configuración
            config_card = EvaluationConfigCard(eval_data)
            self.eval_container_layout.addWidget(config_card)

            # Botón agregar pregunta
            add_question_btn = QPushButton("➕ Agregar Pregunta")
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
            add_question_btn.clicked.connect(self.agregar_pregunta)
            self.eval_container_layout.addWidget(add_question_btn)

            # Preguntas
            preguntas = eval_data.get("preguntas", [])
            if preguntas:
                preguntas_title = QLabel(f"📋 Preguntas ({len(preguntas)})")
                preguntas_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
                preguntas_title.setStyleSheet(
                    "color: #1e293b; margin-top: 20px; margin-bottom: 10px;"
                )
                self.eval_container_layout.addWidget(preguntas_title)

                for pregunta in preguntas:
                    item = QuestionItemWidget(pregunta)
                    item.clicked.connect(self.editar_pregunta)
                    item.edit_clicked.connect(self.editar_pregunta)
                    item.delete_clicked.connect(self.eliminar_pregunta)
                    self.eval_container_layout.addWidget(item)
        else:
            # No hay evaluación configurada
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

            # Sombra
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

            config_now_btn = QPushButton("⚙️ Configurar Ahora")
            config_now_btn.setFixedHeight(45)
            config_now_btn.setStyleSheet(StyleHelper.button_primary())
            config_now_btn.clicked.connect(self.configurar_evaluacion)
            empty_layout.addWidget(config_now_btn)

            self.eval_container_layout.addWidget(empty_frame)

        self.eval_container_layout.addStretch()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Métodos de acción
    def abrir_leccion(self, leccion):
        self.lesson_selected.emit(self.modulo, leccion)

    def editar_leccion(self, leccion):
        """Editar lección existente"""
        dialog = LessonDialog(self.api_client, self.modulo["id"], leccion, self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            # Mostrar cursor de espera
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

                    # Forzar recarga completa
                    self.load_lecciones()
                    QTimer.singleShot(200, self.update_stats)
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
                QMessageBox.critical(self, "Error", f"Error inesperado:\n{str(e)}")

    def eliminar_leccion(self, leccion):
        """Eliminar lección"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar la lección '{leccion.get('titulo')}'?\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # Mostrar cursor de espera
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

                    # Forzar recarga completa de lecciones
                    self.lecciones = []  # Limpiar lista actual
                    self.load_lecciones()  # Recargar desde la API
                    QTimer.singleShot(200, self.update_stats)  # Actualizar estadísticas
                    self.module_updated.emit()  # Notificar a la vista principal
                else:
                    QApplication.restoreOverrideCursor()
                    error_msg = result.get("error", "Error desconocido")
                    QMessageBox.critical(
                        self, "Error", f"Error al eliminar lección:\n{error_msg}"
                    )
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, "Error", f"Error inesperado:\n{str(e)}")

    def editar_modulo(self):
        dialog = ModuleDialog(self.api_client, self.modulo, self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_modulo(self.modulo["id"], data)
            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Módulo actualizado correctamente"
                )
                self.module_updated.emit()  # Actualizar vista principal
                # Recargar datos del módulo
                self.modulo.update(data)
                # Actualizar UI
                self.load_all_data()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def nueva_leccion(self):
        """Crear nueva lección"""
        dialog = LessonDialog(self.api_client, self.modulo["id"], parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            result = self.api_client.create_leccion(self.modulo["id"], data)
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Lección creada correctamente")
                self.load_lecciones()
                # Usar QTimer para actualizar stats después de que se hayan cargado las lecciones
                QTimer.singleShot(200, self.update_stats)
                self.module_updated.emit()  # Actualizar vista principal
            else:
                error_msg = result.get("error", "Error desconocido")
                if "errors" in result:
                    error_msg += "\n" + "\n".join(result["errors"])
                QMessageBox.critical(
                    self, "Error", f"Error al crear lección:\n{error_msg}"
                )

    def configurar_evaluacion(self):
        from views.evaluations_view import EvaluationConfigDialog

        dialog = EvaluationConfigDialog(
            self.api_client, self.modulo["id"], self.evaluacion_actual, self
        )
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_evaluacion_config(self.modulo["id"], data)
            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Evaluación configurada correctamente"
                )
                self.load_evaluacion()
                self.module_updated.emit()  # Actualizar vista principal
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def agregar_pregunta(self):
        if not self.evaluacion_actual:
            QMessageBox.warning(
                self,
                "Configuración requerida",
                "Debes configurar la evaluación antes de agregar preguntas.",
            )
            return

        dialog = QuickQuestionDialog(
            self.api_client, self.evaluacion_actual.get("id"), parent=self
        )
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.create_pregunta(
                self.modulo["id"], self.evaluacion_actual.get("id"), data
            )
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Pregunta creada correctamente")
                self.load_evaluacion()
                self.module_updated.emit()  # Actualizar vista principal
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def editar_pregunta(self, pregunta):
        if not self.evaluacion_actual:
            return
        dialog = QuickQuestionDialog(
            self.api_client, self.evaluacion_actual.get("id"), pregunta, self
        )
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_pregunta(
                self.modulo["id"],
                self.evaluacion_actual.get("id"),
                pregunta["id"],
                data,
            )
            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Pregunta actualizada correctamente"
                )
                self.load_evaluacion()
                self.module_updated.emit()  # Actualizar vista principal
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_pregunta(self, pregunta):
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de eliminar esta pregunta?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.api_client.delete_pregunta(
                self.modulo["id"], self.evaluacion_actual.get("id"), pregunta["id"]
            )
            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Pregunta eliminada correctamente"
                )
                self.load_evaluacion()
                self.module_updated.emit()  # Actualizar vista principal
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def cancelar(self):
        self.module_updated.emit()


class ModulesView(QWidget):
    """Vista principal de módulos con diseño profesional"""

    lesson_selected = pyqtSignal(object, object)

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.modulos = []
        self.modulo_actual = None
        self.current_detail_view = None
        self.placeholder = None
        self.setup_ui()

        QTimer.singleShot(0, self.load_modulos)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header superior
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
        title = QLabel("📚 Gestión de Módulos")
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
        self.search_input.textChanged.connect(self.filtrar_modulos)
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
        refresh_btn.clicked.connect(self.refrescar_modulos)
        header_layout.addWidget(refresh_btn)

        # Botón nuevo módulo
        self.new_btn = QPushButton("➕ Nuevo Módulo")
        self.new_btn.setFixedHeight(45)
        self.new_btn.setStyleSheet(
            StyleHelper.button_primary() + "padding: 0 25px; font-size: 14px;"
        )
        self.new_btn.clicked.connect(self.nuevo_modulo)
        header_layout.addWidget(self.new_btn)

        main_layout.addWidget(header)

        # Splitter principal
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

        self.loading_label = QLabel("📚 Cargando módulos...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet(
            "color: #94a3b8; padding: 60px; font-size: 14px;"
        )
        self.modulos_layout.addWidget(self.loading_label)

        scroll.setWidget(self.modulos_container)
        left_layout.addWidget(scroll)

        splitter.addWidget(left_panel)

        # Panel derecho
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("background-color: #f8fafc;")

        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        # Crear placeholder
        self.create_placeholder()

        splitter.addWidget(self.right_panel)

        # Ajustar tamaños del splitter
        splitter.setSizes([450, 850])

        main_layout.addWidget(splitter)

    def create_placeholder(self):
        """Crear el placeholder para cuando no hay módulo seleccionado"""
        # Si ya existe un placeholder, lo marcamos para eliminar pero no lo eliminamos ahora
        if self.placeholder is not None:
            # Desconectar señales si las hay
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

        # Icono grande
        icon_label = QLabel("📚")
        icon_label.setStyleSheet("font-size: 120px; color: #cbd5e1;")
        placeholder_layout.addWidget(icon_label)

        # Texto
        text_label = QLabel("Selecciona un módulo")
        text_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        text_label.setStyleSheet("color: #94a3b8;")
        placeholder_layout.addWidget(text_label)

        hint_label = QLabel(
            "Haz clic en cualquier módulo de la lista para ver sus detalles"
        )
        hint_label.setStyleSheet("color: #94a3b8; font-size: 14px;")
        placeholder_layout.addWidget(hint_label)

        # Botón para crear nuevo
        create_btn = QPushButton("➕ Crear Nuevo Módulo")
        create_btn.setFixedHeight(50)
        create_btn.setStyleSheet(
            StyleHelper.button_primary() + "padding: 0 40px; font-size: 14px;"
        )
        create_btn.clicked.connect(self.nuevo_modulo)
        placeholder_layout.addWidget(create_btn)

        # Añadir al layout del panel derecho
        self.right_layout.addWidget(self.placeholder)

    def show_placeholder(self):
        """Mostrar el placeholder"""
        # Limpiar el layout actual de manera segura
        self.clear_layout_safe(self.right_layout)

        # Crear y mostrar nuevo placeholder
        self.create_placeholder()
        if self.placeholder:
            self.placeholder.show()

    def clear_layout_safe(self, layout):
        """Limpiar layout de manera segura"""
        if layout is None:
            return

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                widget = child.widget()
                # Ocultar el widget primero
                widget.hide()
                # Desconectar señales
                try:
                    widget.deleteLater()
                except:
                    pass

        # Forzar actualización
        QApplication.processEvents()

    def clear_layout(self, layout):
        """Versión anterior - mantener por compatibilidad pero usar la segura"""
        self.clear_layout_safe(layout)

    def load_modulos(self, force_refresh=False):
        """Cargar lista de módulos"""
        self.clear_layout_safe(self.modulos_layout)

        # Si force_refresh es True, invalidar caché
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
            self.mostrar_modulos(self.modulos)

            # Si hay un módulo seleccionado, verificar que todavía existe
            if self.modulo_actual:
                modulo_existe = any(
                    m.get("id") == self.modulo_actual.get("id") for m in self.modulos
                )
                if not modulo_existe:
                    # El módulo ya no existe, limpiar selección
                    self.modulo_actual = None
                    # Usar QTimer para evitar problemas de recursión
                    QTimer.singleShot(0, self.show_placeholder)
        else:
            error_label = QLabel(f"❌ Error: {result.get('error')}")
            error_label.setStyleSheet("color: #ef4444; padding: 40px; font-size: 14px;")
            error_label.setAlignment(Qt.AlignCenter)
            self.modulos_layout.addWidget(error_label)

    def mostrar_modulos(self, modulos):
        """Mostrar módulos en el panel izquierdo"""
        self.clear_layout(self.modulos_layout)

        if not modulos:
            empty_label = QLabel("📭 No hay módulos creados")
            empty_label.setStyleSheet("color: #94a3b8; padding: 60px; font-size: 14px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.modulos_layout.addWidget(empty_label)

            # Botón para crear
            create_btn = QPushButton("➕ Crear Primer Módulo")
            create_btn.setFixedHeight(45)
            create_btn.setStyleSheet(StyleHelper.button_primary())
            create_btn.clicked.connect(self.nuevo_modulo)
            self.modulos_layout.addWidget(create_btn)
        else:
            modulos_ordenados = sorted(
                modulos, key=lambda x: x.get("orden_global", 999)
            )
            for modulo in modulos_ordenados:
                card = ModernCard(modulo)
                card.clicked.connect(self.mostrar_detalle_modulo)
                self.modulos_layout.addWidget(card)

        self.modulos_layout.addStretch()

    def filtrar_modulos(self):
        """Filtrar módulos por búsqueda"""
        texto = self.search_input.text().lower()
        if not texto:
            self.mostrar_modulos(self.modulos)
            return

        filtrados = [m for m in self.modulos if texto in m.get("titulo", "").lower()]
        self.mostrar_modulos(filtrados)

    def mostrar_detalle_modulo(self, modulo):
        """Mostrar detalle del módulo seleccionado"""
        self.modulo_actual = modulo

        # Limpiar el layout del panel derecho completamente
        self.clear_layout(self.right_layout)

        # Crear y mostrar la vista de detalle
        self.current_detail_view = ModuleDetailView(self.api_client, modulo)
        self.current_detail_view.module_updated.connect(self.on_module_updated)
        self.current_detail_view.lesson_selected.connect(self.abrir_leccion)
        self.right_layout.addWidget(self.current_detail_view)

    def abrir_leccion(self, modulo, leccion):
        """Abrir vista de lección"""
        self.lesson_selected.emit(modulo, leccion)

    def on_module_updated(self):
        """Manejador cuando se actualiza un módulo"""
        # Invalidar caché
        self.api_client.invalidate_cache_type("modulos")

        # Recargar la lista de módulos
        self.load_modulos(force_refresh=True)

        # Usar QTimer para evitar problemas de sincronización
        QTimer.singleShot(100, self._delayed_module_selection)

    def _delayed_module_selection(self):
        """Seleccionar módulo después de un pequeño retraso"""
        # Si hay un módulo seleccionado, mantenerlo seleccionado
        if self.modulo_actual:
            # Buscar el módulo actualizado en la lista
            modulo_actualizado = None
            for modulo in self.modulos:
                if modulo.get("id") == self.modulo_actual.get("id"):
                    modulo_actualizado = modulo
                    break

            if modulo_actualizado:
                # Actualizar la vista de detalle
                self.mostrar_detalle_modulo(modulo_actualizado)
            else:
                # El módulo fue eliminado, mostrar placeholder
                self.modulo_actual = None
                self.show_placeholder()

    def refrescar_modulos(self):
        """Refrescar manualmente la lista de módulos"""
        # Mostrar indicador de carga
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Recargar módulos forzando refresco
        self.load_modulos(force_refresh=True)

        QApplication.restoreOverrideCursor()

        # Mostrar mensaje
        QMessageBox.information(
            self, "Actualizado", "Lista de módulos actualizada correctamente"
        )

    def nuevo_modulo(self):
        """Crear nuevo módulo"""
        dialog = ModuleDialog(self.api_client, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            # Mostrar indicador de carga
            QApplication.setOverrideCursor(Qt.WaitCursor)

            try:
                result = self.api_client.create_modulo(data)
                if result["success"]:
                    QApplication.restoreOverrideCursor()
                    QMessageBox.information(
                        self, "Éxito", "Módulo creado correctamente"
                    )

                    # Recargar lista de módulos forzando refresco
                    self.load_modulos(force_refresh=True)

                    # Buscar el nuevo módulo (el último creado o el que viene en la respuesta)
                    nuevo_modulo = None
                    if result.get("data") and isinstance(result["data"], dict):
                        nuevo_modulo = result["data"]
                    elif self.modulos:
                        # Tomar el último módulo de la lista (asumiendo que es el nuevo)
                        nuevo_modulo = self.modulos[-1]

                    if nuevo_modulo:
                        # Seleccionar automáticamente el nuevo módulo
                        self.mostrar_detalle_modulo(nuevo_modulo)
                    else:
                        # Si no podemos obtener el módulo, mostrar placeholder
                        self.show_placeholder()
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
                QMessageBox.critical(self, "Error", f"Error inesperado:\n{str(e)}")

    def clear_layout(self, layout):
        """Limpiar layout de manera segura y completa"""
        if layout is None:
            return

        # Invertir el orden para eliminar desde el final
        for i in reversed(range(layout.count())):
            child = layout.takeAt(i)
            if child.widget():
                widget = child.widget()
                # Desconectar todas las señales
                try:
                    widget.deleteLater()
                except:
                    pass

        # Forzar recolección de basura y actualización
        QApplication.processEvents()


# ============================================================================
# CLASES PARA PREGUNTAS
# ============================================================================


class OpcionDialog(QDialog):
    """Diálogo para agregar opciones de pregunta"""

    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.setWindowTitle("Agregar Opción")
        self.setFixedSize(450, 300 if tipo == "arrastrar_soltar" else 250)
        self.setup_ui()

    def setup_ui(self):
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
        title = QLabel("➕ Agregar Nueva Opción")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(title)

        # Texto
        layout.addWidget(QLabel("Texto de la opción:"))
        self.texto_input = QLineEdit()
        self.texto_input.setPlaceholderText("Escribe la opción...")
        layout.addWidget(self.texto_input)

        if self.tipo == "arrastrar_soltar":
            layout.addWidget(QLabel("Pareja (definición):"))
            self.pareja_input = QLineEdit()
            self.pareja_input.setPlaceholderText("Ej: HyperText Markup Language")
            layout.addWidget(self.pareja_input)

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

    def get_data(self):
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
    """Diálogo rápido para crear/editar preguntas"""

    def __init__(self, api_client, evaluacion_id, question_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.evaluacion_id = evaluacion_id
        self.question_data = question_data
        self.opciones = []
        self.setWindowTitle("Editar Pregunta" if question_data else "Nueva Pregunta")
        self.setMinimumSize(700, 650)
        self.setup_ui()

        if question_data:
            self.load_question_data()

    def setup_ui(self):
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
        title = QLabel(
            "❓ " + ("Editar Pregunta" if self.question_data else "Nueva Pregunta")
        )
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #1e293b; margin-bottom: 10px;")
        layout.addWidget(title)

        # Tipo y puntos
        tipo_puntos_layout = QHBoxLayout()
        tipo_puntos_layout.setSpacing(20)

        # Tipo
        tipo_group = QFrame()
        tipo_group.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 15px;
            }
        """
        )
        tipo_group_layout = QVBoxLayout(tipo_group)

        tipo_label = QLabel("Tipo de pregunta")
        tipo_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        tipo_group_layout.addWidget(tipo_label)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["seleccion_multiple", "verdadero_falso", "arrastrar_soltar"]
        )
        self.tipo_combo.currentTextChanged.connect(self.cambiar_tipo)
        tipo_group_layout.addWidget(self.tipo_combo)

        tipo_puntos_layout.addWidget(tipo_group)

        # Puntos
        puntos_group = QFrame()
        puntos_group.setStyleSheet(tipo_group.styleSheet())
        puntos_group_layout = QVBoxLayout(puntos_group)

        puntos_label = QLabel("Puntos")
        puntos_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        puntos_group_layout.addWidget(puntos_label)

        self.puntos_input = QDoubleSpinBox()
        self.puntos_input.setRange(0.5, 100)
        self.puntos_input.setValue(10)
        self.puntos_input.setSingleStep(0.5)
        puntos_group_layout.addWidget(self.puntos_input)

        tipo_puntos_layout.addWidget(puntos_group)

        layout.addLayout(tipo_puntos_layout)

        # Pregunta
        pregunta_group = QFrame()
        pregunta_group.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 15px;
            }
        """
        )
        pregunta_layout = QVBoxLayout(pregunta_group)

        pregunta_label = QLabel("Pregunta")
        pregunta_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        pregunta_layout.addWidget(pregunta_label)

        self.pregunta_input = QTextEdit()
        self.pregunta_input.setPlaceholderText("Escribe la pregunta...")
        self.pregunta_input.setMaximumHeight(100)
        pregunta_layout.addWidget(self.pregunta_input)

        layout.addWidget(pregunta_group)

        # Opciones
        self.opciones_group = QGroupBox("Opciones de Respuesta")
        opciones_layout = QVBoxLayout()

        # Toolbar
        toolbar = QHBoxLayout()

        self.add_opcion_btn = QPushButton("➕ Agregar Opción")
        self.add_opcion_btn.setStyleSheet(StyleHelper.button_success())
        self.add_opcion_btn.clicked.connect(self.agregar_opcion)
        toolbar.addWidget(self.add_opcion_btn)

        self.remove_opcion_btn = QPushButton("🗑️ Eliminar Seleccionada")
        self.remove_opcion_btn.setStyleSheet(StyleHelper.button_danger())
        self.remove_opcion_btn.clicked.connect(self.eliminar_opcion)
        toolbar.addWidget(self.remove_opcion_btn)

        toolbar.addStretch()
        opciones_layout.addLayout(toolbar)

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

        self.cambiar_tipo(self.tipo_combo.currentText())

    def cambiar_tipo(self, tipo):
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

    def agregar_opcion(self):
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

    def eliminar_opcion(self):
        current_row = self.opciones_list.currentRow()
        if current_row >= 0:
            self.opciones_list.takeItem(current_row)

    def load_question_data(self):
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

    def get_data(self):
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
