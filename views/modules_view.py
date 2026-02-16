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
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
import logging
from utils.paths import resource_path
from views.lessons_view import LessonDialog

# OPTIMIZACIÓN 1: Reducir logging a WARNING (menos escritura en consola)
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class ModuleCard(QFrame):
    """Tarjeta de módulo adaptable - OPTIMIZADA"""

    clicked = pyqtSignal(object)

    def __init__(self, modulo, parent=None):
        super().__init__(parent)
        self.modulo = modulo
        self.setup_ui()

    def setup_ui(self):
        # OPTIMIZACIÓN: Usar fixed height en lugar de min/max
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(140)  # Altura fija en lugar de rango

        self.setStyleSheet(
            """
            ModuleCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
            ModuleCard:hover {
                border: 2px solid #3498db;
                background-color: #f8f9fa;
            }
        """
        )

        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setSpacing(6)  # Reducido de 8 a 6
        layout.setContentsMargins(12, 10, 12, 10)  # Márgenes reducidos

        # Header con título y tipo
        header = QHBoxLayout()
        header.setSpacing(6)

        # OPTIMIZACIÓN: Truncar título si es muy largo
        titulo = self.modulo.get("titulo", "Sin título")
        if len(titulo) > 30:
            titulo = titulo[:27] + "..."

        title = QLabel(titulo)
        title.setFont(
            QFont("Segoe UI", 13, QFont.Bold)
        )  # Fuente ligeramente más pequeña
        title.setStyleSheet("color: #2c3e50;")
        title.setWordWrap(False)  # No wrap para evitar cálculos
        title.setFixedHeight(20)
        header.addWidget(title)

        tipo = QLabel(self.modulo.get("modulo", "html").upper())
        tipo.setStyleSheet(
            """
            background-color: #ecf0f1;
            color: #7f8c8d;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: bold;
        """
        )
        tipo.setFixedHeight(20)
        tipo.setFixedWidth(70)  # Ancho fijo para consistencia
        header.addWidget(tipo)

        layout.addLayout(header)

        # OPTIMIZACIÓN: Descripción más corta
        desc = self.modulo.get("descripcion_larga", "")
        if desc:
            # Tomar solo primeras 8 palabras
            palabras = desc.split()[:8]
            desc = " ".join(palabras) + "..."
        else:
            desc = "Sin descripción"

        desc_label = QLabel(desc)
        desc_label.setWordWrap(False)
        desc_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        desc_label.setFixedHeight(30)
        layout.addWidget(desc_label)

        # Footer con estadísticas
        footer = QHBoxLayout()
        footer.setSpacing(8)

        lecciones = QLabel(f"📚 {self.modulo.get('total_lecciones', 0)}")
        lecciones.setStyleSheet("color: #3498db; font-size: 11px; font-weight: bold;")
        lecciones.setFixedHeight(20)
        footer.addWidget(lecciones)

        footer.addStretch()

        # Estado
        estado = self.modulo.get("estado", "inactivo")
        estado_label = QLabel(estado.upper())

        # OPTIMIZACIÓN: Determinar colores una sola vez
        if estado == "activo":
            bg_color = "#d4edda"
            text_color = "#155724"
        else:
            bg_color = "#f8d7da"
            text_color = "#721c24"

        estado_label.setStyleSheet(
            f"background-color: {bg_color}; color: {text_color}; "
            f"padding: 3px 10px; border-radius: 10px; font-size: 10px; font-weight: bold;"
        )
        estado_label.setFixedHeight(20)
        estado_label.setFixedWidth(70)
        footer.addWidget(estado_label)

        layout.addLayout(footer)

    def mousePressEvent(self, event):
        self.clicked.emit(self.modulo)
        super().mousePressEvent(event)


class LessonItemWidget(QWidget):
    """Widget para item de lección en la lista - OPTIMIZADO"""

    clicked = pyqtSignal(object)
    edit_clicked = pyqtSignal(object)
    delete_clicked = pyqtSignal(object)

    def __init__(self, leccion, parent=None):
        super().__init__(parent)
        self.leccion = leccion
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(
            """
            LessonItemWidget {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
            }
            LessonItemWidget:hover {
                background-color: #f8f9fa;
                border: 1px solid #3498db;  /* Borde más delgado en hover */
            }
        """
        )
        self.setFixedHeight(60)  # Reducido de 70 a 60
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)  # Márgenes reducidos
        layout.setSpacing(8)

        # Icono y título
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)  # Reducido de 3 a 2

        # OPTIMIZACIÓN: Título truncado
        titulo = self.leccion.get("titulo", "Sin título")
        if len(titulo) > 35:
            titulo = titulo[:32] + "..."

        titulo_label = QLabel(f"📖 {titulo}")
        titulo_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        titulo_label.setStyleSheet("color: #2c3e50;")
        titulo_label.setWordWrap(False)
        titulo_label.setFixedHeight(20)
        title_layout.addWidget(titulo_label)

        # Info adicional (simplificada)
        info_text = f"Orden: {self.leccion.get('orden', 1)}"
        if self.leccion.get("tiene_ejercicios"):
            info_text += " | ✅"
        else:
            info_text += " | ❌"

        info = QLabel(info_text)
        info.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        info.setFixedHeight(15)
        title_layout.addWidget(info)

        layout.addLayout(title_layout, 1)

        # Botones de acción (más pequeños)
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(28, 28)  # Reducido de 32
        self.edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f39c12;
                color: white;
                border-radius: 14px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """
        )
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.leccion))
        layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(28, 28)  # Reducido de 32
        self.delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 14px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.leccion))
        layout.addWidget(self.delete_btn)

    def mousePressEvent(self, event):
        if not self.edit_btn.underMouse() and not self.delete_btn.underMouse():
            self.clicked.emit(self.leccion)
        super().mousePressEvent(event)


class ModuleDialog(QDialog):
    """Diálogo para crear/editar módulo - OPTIMIZADO"""

    def __init__(self, api_client, modulo_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_data = modulo_data
        self.modulos_existentes = []
        self.setWindowTitle("Editar Módulo" if modulo_data else "Nuevo Módulo")
        self.setMinimumSize(650, 550)  # Ligeramente más pequeño
        self.setModal(True)  # Hacer modal para mejor rendimiento

        # OPTIMIZACIÓN: Cargar módulos después de mostrar UI
        QTimer.singleShot(0, self.cargar_modulos_existentes)

        self.setup_ui()

        if modulo_data:
            self.load_data()

    def cargar_modulos_existentes(self):
        """Cargar lista de módulos para mostrar órdenes disponibles"""
        result = self.api_client.get_modulos()
        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.modulos_existentes = data
            elif isinstance(data, dict) and "data" in data:
                self.modulos_existentes = data["data"]

            # Actualizar orden sugerido si es nuevo
            if not self.modulo_data:
                self.orden_spin.setValue(self.obtener_siguiente_orden())

    def setup_ui(self):
        # OPTIMIZACIÓN: Estilos más compactos
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #3498db;
            }
            QLabel {
                font-size: 12px;
                color: #2c3e50;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Reducido de 15
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes reducidos

        # Título
        title = QLabel(
            "📚 " + ("Editar Módulo" if self.modulo_data else "Nuevo Módulo")
        )
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))  # Reducido de 22
        title.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        layout.addWidget(title)

        # Formulario
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(10)  # Reducido de 15
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Título
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Ej: Introducción a HTML")
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
        desc_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        desc_label.setStyleSheet("margin-top: 5px;")
        layout.addWidget(desc_label)

        from views.components.rich_text_editor import RichTextEditor

        self.descripcion_editor = RichTextEditor()
        self.descripcion_editor.setMinimumHeight(150)  # Reducido de 200
        layout.addWidget(self.descripcion_editor)

        # Orden y Estado en horizontal
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        # Orden
        orden_layout = QVBoxLayout()
        orden_layout.addWidget(QLabel("Orden:"))
        self.orden_spin = QSpinBox()
        self.orden_spin.setMinimum(1)
        self.orden_spin.setMaximum(999)
        self.orden_spin.setValue(1)
        orden_layout.addWidget(self.orden_spin)
        bottom_layout.addLayout(orden_layout)

        bottom_layout.addStretch()

        # Estado
        estado_layout = QVBoxLayout()
        estado_layout.addWidget(QLabel("Estado:"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo", "borrador"])
        estado_layout.addWidget(self.estado_combo)
        bottom_layout.addLayout(estado_layout)

        layout.addLayout(bottom_layout)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        # OPTIMIZACIÓN: Botones más compactos
        for btn in [
            buttons.button(QDialogButtonBox.Ok),
            buttons.button(QDialogButtonBox.Cancel),
        ]:
            btn.setStyleSheet(
                """
                QPushButton {
                    padding: 8px 25px;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 12px;
                    min-width: 80px;
                }
            """
            )

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            """
            background-color: #3498db;
            color: white;
        """
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            """
            background-color: #e74c3c;
            color: white;
        """
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def obtener_siguiente_orden(self):
        """Obtener el siguiente orden disponible"""
        if not self.modulos_existentes:
            return 1

        ordenes = [
            m.get("orden_global", 0)
            for m in self.modulos_existentes
            if not self.modulo_data or m["id"] != self.modulo_data.get("id")
        ]
        if not ordenes:
            return 1

        max_orden = max(ordenes)
        return max_orden + 1

    def load_data(self):
        """Cargar datos del módulo existente"""
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

    def get_data(self):
        """Obtener datos del formulario"""
        return {
            "titulo": self.titulo_input.text(),
            "modulo": self.tipo_combo.currentText(),
            "descripcion_larga": self.descripcion_editor.toHtml(),
            "orden_global": self.orden_spin.value(),
            "estado": self.estado_combo.currentText(),
        }


class QuestionItemWidget(QWidget):
    """Widget para item de pregunta en la lista - OPTIMIZADO"""

    clicked = pyqtSignal(object)
    edit_clicked = pyqtSignal(object)
    delete_clicked = pyqtSignal(object)

    def __init__(self, pregunta, parent=None):
        super().__init__(parent)
        self.pregunta = pregunta
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QuestionItemWidget {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
                margin: 1px;
            }
            QuestionItemWidget:hover {
                background-color: #f8f9fa;
                border: 1px solid #3498db;
            }
        """
        )
        self.setFixedHeight(70)  # Reducido de 80
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)  # Márgenes reducidos
        layout.setSpacing(8)

        # Tipo y puntos (más compacto)
        tipo_layout = QVBoxLayout()
        tipo_layout.setSpacing(2)

        tipo_texto = {
            "seleccion_multiple": "📝 Múltiple",
            "verdadero_falso": "✓ V/F",
            "arrastrar_soltar": "🔄 Arrastrar",
        }.get(self.pregunta.get("tipo", ""), "📝")

        tipo_label = QLabel(tipo_texto)
        tipo_label.setStyleSheet("color: #3498db; font-size: 10px; font-weight: bold;")
        tipo_label.setFixedHeight(16)
        tipo_layout.addWidget(tipo_label)

        puntos_label = QLabel(f"⚡ {self.pregunta.get('puntos', 0)} pts")
        puntos_label.setStyleSheet("color: #f39c12; font-size: 9px;")
        puntos_label.setFixedHeight(14)
        tipo_layout.addWidget(puntos_label)

        layout.addLayout(tipo_layout)

        # Pregunta
        question_layout = QVBoxLayout()
        question_layout.setSpacing(2)

        pregunta_text = self.pregunta.get("pregunta", "")
        if len(pregunta_text) > 50:  # Reducido de 60
            pregunta_text = pregunta_text[:47] + "..."

        pregunta_label = QLabel(pregunta_text)
        pregunta_label.setFont(QFont("Segoe UI", 10, QFont.Bold))  # Reducido de 11
        pregunta_label.setStyleSheet("color: #2c3e50;")
        pregunta_label.setWordWrap(False)
        pregunta_label.setFixedHeight(20)
        question_layout.addWidget(pregunta_label)

        # Mostrar resumen de opciones (simplificado)
        opciones = self.pregunta.get("opciones", [])
        if opciones:
            total = len(opciones)
            if self.pregunta.get("tipo") == "arrastrar_soltar":
                opciones_text = f"• {total} pares"
            elif self.pregunta.get("tipo") == "verdadero_falso":
                opciones_text = "• V/F"
            else:
                correctas = sum(1 for o in opciones if o.get("es_correcta", False))
                opciones_text = f"• {correctas}/{total}"

            opciones_info = QLabel(opciones_text)
            opciones_info.setStyleSheet("color: #7f8c8d; font-size: 9px;")
            opciones_info.setFixedHeight(14)
            question_layout.addWidget(opciones_info)

        layout.addLayout(question_layout, 1)

        # Botones de acción (más pequeños)
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(24, 24)  # Reducido de 28
        self.edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f39c12;
                color: white;
                border-radius: 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """
        )
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.pregunta))
        layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(24, 24)  # Reducido de 28
        self.delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.pregunta))
        layout.addWidget(self.delete_btn)

    def mousePressEvent(self, event):
        if not self.edit_btn.underMouse() and not self.delete_btn.underMouse():
            self.clicked.emit(self.pregunta)
        super().mousePressEvent(event)


# Las clases OpcionDialog y QuickQuestionDialog se mantienen IGUAL
# (sin cambios para preservar funcionalidad)


class OpcionDialog(QDialog):
    """Diálogo para agregar opciones de pregunta (SIN CAMBIOS)"""

    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.setWindowTitle("Agregar Opción")
        self.setFixedSize(400, 250 if tipo == "arrastrar_soltar" else 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

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
            layout.addWidget(self.correcta_check)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
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
    """Diálogo rápido para crear/editar preguntas (SIN CAMBIOS)"""

    def __init__(self, api_client, evaluacion_id, question_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.evaluacion_id = evaluacion_id
        self.question_data = question_data
        self.opciones = []
        self.setWindowTitle("Editar Pregunta" if question_data else "Nueva Pregunta")
        self.setMinimumSize(600, 550)
        self.setup_ui()

        if question_data:
            self.load_question_data()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel(
            "❓ " + ("Editar Pregunta" if self.question_data else "Nueva Pregunta")
        )
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        layout.addWidget(title)

        tipo_puntos_layout = QHBoxLayout()

        tipo_layout = QHBoxLayout()
        tipo_layout.addWidget(QLabel("Tipo:"))
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["seleccion_multiple", "verdadero_falso", "arrastrar_soltar"]
        )
        self.tipo_combo.currentTextChanged.connect(self.cambiar_tipo)
        self.tipo_combo.setMinimumWidth(150)
        tipo_layout.addWidget(self.tipo_combo)
        tipo_puntos_layout.addLayout(tipo_layout)
        tipo_puntos_layout.addStretch()

        puntos_layout = QHBoxLayout()
        puntos_layout.addWidget(QLabel("Puntos:"))
        self.puntos_input = QDoubleSpinBox()
        self.puntos_input.setMinimum(0.5)
        self.puntos_input.setMaximum(100)
        self.puntos_input.setValue(10)
        self.puntos_input.setSingleStep(0.5)
        self.puntos_input.setFixedWidth(80)
        puntos_layout.addWidget(self.puntos_input)
        tipo_puntos_layout.addLayout(puntos_layout)

        layout.addLayout(tipo_puntos_layout)

        pregunta_label = QLabel("Pregunta:")
        pregunta_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        layout.addWidget(pregunta_label)

        self.pregunta_input = QTextEdit()
        self.pregunta_input.setPlaceholderText("Escribe la pregunta...")
        self.pregunta_input.setMaximumHeight(80)
        layout.addWidget(self.pregunta_input)

        self.opciones_group = QGroupBox("Opciones de Respuesta")
        opciones_layout = QVBoxLayout()

        toolbar = QHBoxLayout()

        self.add_opcion_btn = QPushButton("➕ Agregar Opción")
        self.add_opcion_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 5px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """
        )
        self.add_opcion_btn.clicked.connect(self.agregar_opcion)
        toolbar.addWidget(self.add_opcion_btn)

        self.remove_opcion_btn = QPushButton("🗑️ Eliminar")
        self.remove_opcion_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        self.remove_opcion_btn.clicked.connect(self.eliminar_opcion)
        toolbar.addWidget(self.remove_opcion_btn)

        toolbar.addStretch()
        opciones_layout.addLayout(toolbar)

        self.opciones_list = QListWidget()
        self.opciones_list.setMaximumHeight(180)
        self.opciones_list.setStyleSheet(
            """
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """
        )
        opciones_layout.addWidget(self.opciones_list)

        self.opciones_group.setLayout(opciones_layout)
        layout.addWidget(self.opciones_group)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar Pregunta")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 25px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 25px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.cambiar_tipo(self.tipo_combo.currentText())

    def cambiar_tipo(self, tipo):
        """Cambiar interfaz según tipo"""
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
        """Agregar nueva opción"""
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
                item.setForeground(QColor("#27ae60"))
                item.setIcon(
                    self.style().standardIcon(self.style().SP_DialogApplyButton)
                )

            self.opciones_list.addItem(item)

    def eliminar_opcion(self):
        """Eliminar opción seleccionada"""
        current_row = self.opciones_list.currentRow()
        if current_row >= 0:
            self.opciones_list.takeItem(current_row)

    def load_question_data(self):
        """Cargar datos de pregunta existente"""
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
                item.setForeground(QColor("#27ae60"))

            self.opciones_list.addItem(item)

    def get_data(self):
        """Obtener datos del formulario"""
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


class ModuleDetailView(QWidget):
    """Vista de detalle de módulo - OPTIMIZADA con carga lazy"""

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

        # OPTIMIZACIÓN: Cargar datos después de mostrar UI
        QTimer.singleShot(50, self.load_all_data)

    def setup_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; }"
        )

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(15)  # Reducido de 20
        self.layout.setContentsMargins(20, 20, 20, 20)  # Márgenes reducidos

        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

        # Header con título
        header = QHBoxLayout()
        header.setSpacing(10)  # Reducido de 15

        # OPTIMIZACIÓN: Título truncado
        titulo = self.modulo.get("titulo", "Módulo")
        if len(titulo) > 40:
            titulo = titulo[:37] + "..."

        title = QLabel(f"📚 {titulo}")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))  # Reducido de 28
        title.setStyleSheet("color: #2c3e50;")
        title.setWordWrap(False)
        title.setFixedHeight(35)
        header.addWidget(title)

        # Estado
        estado = self.modulo.get("estado", "inactivo")
        self.estado_label = QLabel(estado.upper())
        if estado == "activo":
            bg = "#d4edda"
            color = "#155724"
        else:
            bg = "#f8d7da"
            color = "#721c24"

        self.estado_label.setStyleSheet(
            f"background-color: {bg}; color: {color}; padding: 4px 12px; "
            f"border-radius: 16px; font-size: 11px; font-weight: bold;"
        )
        self.estado_label.setFixedHeight(24)
        header.addWidget(self.estado_label)

        self.layout.addLayout(header)

        # Botones de acción
        actions_top = QHBoxLayout()
        actions_top.setSpacing(8)

        self.edit_btn = QPushButton("✏️ Editar")
        self.edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 6px 15px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        self.edit_btn.clicked.connect(self.editar_modulo)
        actions_top.addWidget(self.edit_btn)

        self.new_lesson_btn = QPushButton("➕ Nueva")
        self.new_lesson_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 6px 15px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """
        )
        self.new_lesson_btn.clicked.connect(self.nueva_leccion)
        actions_top.addWidget(self.new_lesson_btn)

        actions_top.addStretch()
        self.layout.addLayout(actions_top)

        # Placeholders (se reemplazarán cuando carguen los datos)
        self.desc_placeholder = QLabel("Cargando descripción...")
        self.desc_placeholder.setStyleSheet("color: #95a5a6; padding: 10px;")
        self.layout.addWidget(self.desc_placeholder)

        self.lessons_placeholder = QLabel("📖 Cargando lecciones...")
        self.lessons_placeholder.setStyleSheet("color: #95a5a6; padding: 10px;")
        self.layout.addWidget(self.lessons_placeholder)

        self.eval_placeholder = QLabel("📝 Cargando evaluación...")
        self.eval_placeholder.setStyleSheet("color: #95a5a6; padding: 10px;")
        self.layout.addWidget(self.eval_placeholder)

        # Botón cancelar
        self.cancel_btn = QPushButton("Volver")
        self.cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 25px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """
        )
        self.cancel_btn.clicked.connect(self.cancelar)
        self.layout.addWidget(self.cancel_btn, 0, Qt.AlignRight)

        self.layout.addStretch()

    def load_all_data(self):
        """Cargar todos los datos (lazy loading)"""
        if self._loaded:
            return
        self._loaded = True

        # Cargar descripción
        desc = self.modulo.get("descripcion_larga", "Sin descripción")
        self.desc_placeholder.setText(desc[:150] + "..." if len(desc) > 150 else desc)
        self.desc_placeholder.setStyleSheet("color: #2c3e50;")

        # Cargar lecciones
        self.load_lecciones()

        # Cargar evaluación
        self.load_evaluacion()

    def load_lecciones(self):
        """Cargar lecciones del módulo"""
        self.lessons_placeholder.deleteLater()

        result = self.api_client.get_lecciones(self.modulo["id"])

        # Crear contenedor de lecciones
        lessons_container = QVBoxLayout()
        lessons_container.setSpacing(5)

        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.lecciones = data
            elif isinstance(data, dict) and "data" in data:
                self.lecciones = data["data"]
            else:
                self.lecciones = []

            # OPTIMIZACIÓN: Título de sección
            section_title = QLabel("📖 Lecciones")
            section_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
            section_title.setStyleSheet("color: #2c3e50; margin-top: 5px;")
            lessons_container.addWidget(section_title)

            if not self.lecciones:
                empty = QLabel("No hay lecciones creadas.")
                empty.setStyleSheet("color: #95a5a6; font-size: 12px; padding: 10px;")
                lessons_container.addWidget(empty)
            else:
                # OPTIMIZACIÓN: Mostrar solo primeras 10 para rendimiento
                for leccion in self.lecciones[:10]:
                    item = LessonItemWidget(leccion)
                    item.clicked.connect(self.abrir_leccion)
                    item.edit_clicked.connect(self.editar_leccion)
                    item.delete_clicked.connect(self.eliminar_leccion)
                    lessons_container.addWidget(item)

                if len(self.lecciones) > 10:
                    more = QLabel(f"... y {len(self.lecciones) - 10} más")
                    more.setStyleSheet("color: #7f8c8d; font-size: 11px; padding: 5px;")
                    lessons_container.addWidget(more)

        # Insertar después del placeholder
        self.layout.insertLayout(4, lessons_container)

    def load_evaluacion(self):
        """Cargar información de evaluación"""
        self.eval_placeholder.deleteLater()

        result = self.api_client.get_evaluacion(self.modulo["id"])

        eval_frame = QFrame()
        eval_frame.setStyleSheet(
            "background-color: #f8f9fa; border-radius: 10px; padding: 12px; margin-top: 5px;"
        )
        eval_layout = QVBoxLayout(eval_frame)
        eval_layout.setSpacing(10)

        # Título
        title = QLabel("📝 Evaluación")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        eval_layout.addWidget(title)

        if result["success"] and result.get("data"):
            self.evaluacion_actual = result["data"]
            eval_data = self.evaluacion_actual

            # Información compacta
            info = QLabel(
                f"⏱️ {eval_data.get('tiempo_limite', 0)}min | "
                f"🎯 {eval_data.get('puntaje_minimo', 0)}% | "
                f"🔄 {eval_data.get('max_intentos', 0)} intentos"
            )
            info.setStyleSheet("color: #2c3e50; font-size: 11px;")
            eval_layout.addWidget(info)

            # Botones
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(8)

            config_btn = QPushButton("⚙️ Configurar")
            config_btn.setStyleSheet(
                "background-color: #9b59b6; color: white; padding: 4px 12px; border-radius: 15px; font-size: 11px;"
            )
            config_btn.clicked.connect(self.configurar_evaluacion)
            btn_layout.addWidget(config_btn)

            add_btn = QPushButton("➕ Pregunta")
            add_btn.setStyleSheet(
                "background-color: #27ae60; color: white; padding: 4px 12px; border-radius: 15px; font-size: 11px;"
            )
            add_btn.clicked.connect(self.agregar_pregunta)
            btn_layout.addWidget(add_btn)

            btn_layout.addStretch()
            eval_layout.addLayout(btn_layout)

            # Preguntas
            preguntas = eval_data.get("preguntas", [])
            if preguntas:
                q_label = QLabel(f"Preguntas ({len(preguntas)}):")
                q_label.setStyleSheet(
                    "font-weight: bold; color: #2c3e50; font-size: 12px; margin-top: 5px;"
                )
                eval_layout.addWidget(q_label)

                # OPTIMIZACIÓN: Mostrar solo primeras 3
                for pregunta in preguntas[:3]:
                    item = QuestionItemWidget(pregunta)
                    item.clicked.connect(self.editar_pregunta)
                    eval_layout.addWidget(item)

                if len(preguntas) > 3:
                    more = QLabel(f"... y {len(preguntas) - 3} más")
                    more.setStyleSheet("color: #7f8c8d; font-size: 10px;")
                    eval_layout.addWidget(more)
        else:
            eval_layout.addWidget(QLabel("No hay configuración"))
            config_btn = QPushButton("⚙️ Configurar")
            config_btn.setStyleSheet(
                "background-color: #9b59b6; color: white; padding: 4px 12px; border-radius: 15px; font-size: 11px;"
            )
            config_btn.clicked.connect(self.configurar_evaluacion)
            eval_layout.addWidget(config_btn)

        # Insertar después de lecciones
        self.layout.insertWidget(5, eval_frame)

    # Los métodos de acción se mantienen IGUALES
    def abrir_leccion(self, leccion):
        self.lesson_selected.emit(self.modulo, leccion)

    def editar_leccion(self, leccion):
        dialog = LessonDialog(self.api_client, self.modulo["id"], leccion, self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_leccion(
                self.modulo["id"], leccion["id"], data
            )
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Lección actualizada")
                self.load_lecciones()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_leccion(self, leccion):
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar lección '{leccion.get('titulo')}'?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.api_client.delete_leccion(self.modulo["id"], leccion["id"])
            if result["success"]:
                self.load_lecciones()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def editar_modulo(self):
        dialog = ModuleDialog(self.api_client, self.modulo, self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_modulo(self.modulo["id"], data)
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Módulo actualizado")
                self.module_updated.emit()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def nueva_leccion(self):
        dialog = LessonDialog(self.api_client, self.modulo["id"], parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.create_leccion(self.modulo["id"], data)
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Lección creada")
                self.load_lecciones()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def configurar_evaluacion(self):
        from views.evaluations_view import EvaluationConfigDialog

        config_actual = None
        if hasattr(self, "evaluacion_actual") and self.evaluacion_actual:
            config_actual = self.evaluacion_actual

        dialog = EvaluationConfigDialog(
            self.api_client, self.modulo["id"], config_actual, self
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_evaluacion_config(self.modulo["id"], data)
            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Evaluación configurada correctamente"
                )
                self.load_evaluacion()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def agregar_pregunta(self):
        if not hasattr(self, "evaluacion_actual") or not self.evaluacion_actual:
            reply = QMessageBox.question(
                self,
                "Configurar Evaluación",
                "No hay configuración de evaluación. ¿Deseas configurarla ahora?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.configurar_evaluacion()
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
                QMessageBox.information(self, "Éxito", "Pregunta actualizada")
                self.load_evaluacion()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_pregunta(self, pregunta):
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "¿Eliminar esta pregunta?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.api_client.delete_pregunta(
                self.modulo["id"], self.evaluacion_actual.get("id"), pregunta["id"]
            )

            if result["success"]:
                self.load_evaluacion()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def toggle_estado(self):
        nuevo_estado = "inactivo" if self.modulo.get("estado") == "activo" else "activo"
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Cambiar estado a {nuevo_estado}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            data = {"estado": nuevo_estado}
            result = self.api_client.update_modulo(self.modulo["id"], data)
            if result["success"]:
                self.modulo["estado"] = nuevo_estado
                self.module_updated.emit()
                self.activate_btn.setText(
                    "Activar" if nuevo_estado != "activo" else "Desactivar"
                )
                if nuevo_estado == "activo":
                    bg = "#27ae60"
                else:
                    bg = "#e74c3c"
                self.activate_btn.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: {bg};
                        color: white;
                        padding: 8px 25px;
                        border-radius: 20px;
                        font-weight: bold;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {'#229954' if nuevo_estado == 'activo' else '#c0392b'};
                    }}
                """
                )
                if nuevo_estado == "activo":
                    bg = "#d4edda"
                    color = "#155724"
                else:
                    bg = "#f8d7da"
                    color = "#721c24"
                self.estado_label.setStyleSheet(
                    f"background-color: {bg}; color: {color}; padding: 4px 12px; "
                    f"border-radius: 16px; font-size: 11px; font-weight: bold;"
                )
                self.estado_label.setText(nuevo_estado.upper())
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def cancelar(self):
        self.module_updated.emit()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class ModulesView(QWidget):
    """Vista principal de módulos - OPTIMIZADA"""

    lesson_selected = pyqtSignal(object, object)

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.modulos = []
        self.modulo_actual = None
        self.setup_ui()

        # OPTIMIZACIÓN: Cargar después de mostrar UI
        QTimer.singleShot(0, self.load_modulos)

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel izquierdo
        left_panel = QWidget()
        left_panel.setMinimumWidth(250)  # Reducido de 300
        left_panel.setMaximumWidth(350)  # Reducido de 400
        left_panel.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
                border-right: 1px solid #dee2e6;
            }
        """
        )

        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)  # Reducido de 15
        left_layout.setContentsMargins(10, 15, 10, 15)  # Márgenes reducidos

        # Header
        header = QHBoxLayout()

        title = QLabel("📚 Módulos")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))  # Reducido de 20
        title.setStyleSheet("color: #2c3e50;")
        header.addWidget(title)

        header.addStretch()

        self.new_btn = QPushButton("➕")
        self.new_btn.setFixedSize(36, 36)  # Reducido de 44
        self.new_btn.setToolTip("Nuevo Módulo")
        self.new_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 18px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        self.new_btn.clicked.connect(self.nuevo_modulo)
        header.addWidget(self.new_btn)

        left_layout.addLayout(header)

        # Buscador
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar...")
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #dee2e6;
                border-radius: 20px;
                background-color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        )
        self.search_input.textChanged.connect(self.filtrar_modulos)
        left_layout.addWidget(self.search_input)

        # Lista de módulos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; }"
        )

        self.modulos_container = QWidget()
        self.modulos_container.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.modulos_layout = QVBoxLayout(self.modulos_container)
        self.modulos_layout.setSpacing(8)
        self.modulos_layout.setAlignment(Qt.AlignTop)

        # Placeholder de carga
        self.loading_label = QLabel("Cargando módulos...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: #95a5a6; padding: 20px;")
        self.modulos_layout.addWidget(self.loading_label)

        scroll.setWidget(self.modulos_container)
        left_layout.addWidget(scroll)

        main_layout.addWidget(left_panel)

        # Panel derecho
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet("background-color: white;")

        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        self.placeholder = QLabel("Selecciona un módulo")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: #95a5a6; font-size: 14px;")
        self.right_layout.addWidget(self.placeholder)

        main_layout.addWidget(self.right_panel, 1)

    def load_modulos(self):
        """Cargar lista de módulos"""
        # Remover placeholder de carga
        self.clear_layout(self.modulos_layout)

        result = self.api_client.get_modulos()

        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.modulos = data
            elif isinstance(data, dict) and "data" in data:
                self.modulos = data["data"]
            else:
                self.modulos = []

            self.mostrar_modulos(self.modulos)
        else:
            error_label = QLabel(f"Error: {result.get('error')}")
            error_label.setStyleSheet("color: #e74c3c; padding: 20px;")
            error_label.setAlignment(Qt.AlignCenter)
            self.modulos_layout.addWidget(error_label)

    def mostrar_modulos(self, modulos):
        """Mostrar módulos en el panel izquierdo"""
        self.clear_layout(self.modulos_layout)

        if not modulos:
            empty_label = QLabel("No hay módulos creados.")
            empty_label.setStyleSheet("color: #95a5a6; font-size: 13px; padding: 20px;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.modulos_layout.addWidget(empty_label)
        else:
            # OPTIMIZACIÓN: Ordenar y limitar
            modulos_ordenados = sorted(
                modulos, key=lambda x: x.get("orden_global", 999)
            )[
                :30
            ]  # Máximo 30 para rendimiento

            for modulo in modulos_ordenados:
                card = ModuleCard(modulo)
                card.clicked.connect(self.mostrar_detalle_modulo)
                self.modulos_layout.addWidget(card)

            if len(modulos) > 30:
                more_label = QLabel(f"... y {len(modulos) - 30} más")
                more_label.setStyleSheet(
                    "color: #7f8c8d; font-size: 11px; padding: 5px;"
                )
                more_label.setAlignment(Qt.AlignCenter)
                self.modulos_layout.addWidget(more_label)

        self.modulos_layout.addStretch()

    def filtrar_modulos(self):
        """Filtrar módulos por búsqueda"""
        texto = self.search_input.text().lower()
        if not texto:
            self.mostrar_modulos(self.modulos)
            return

        filtrados = [m for m in self.modulos if texto in m.get("titulo", "").lower()]
        self.mostrar_modulos(filtrados[:30])

    def mostrar_detalle_modulo(self, modulo):
        """Mostrar detalle del módulo seleccionado"""
        self.modulo_actual = modulo

        self.clear_layout(self.right_layout)

        detail_view = ModuleDetailView(self.api_client, modulo)
        detail_view.module_updated.connect(self.load_modulos)
        detail_view.lesson_selected.connect(self.abrir_leccion)
        self.right_layout.addWidget(detail_view)

    def abrir_leccion(self, modulo, leccion):
        """Abrir vista de lección"""
        self.lesson_selected.emit(modulo, leccion)

    def nuevo_modulo(self):
        """Crear nuevo módulo"""
        dialog = ModuleDialog(self.api_client, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.create_modulo(data)
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Módulo creado")
                self.load_modulos()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def clear_layout(self, layout):
        """Limpiar layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
