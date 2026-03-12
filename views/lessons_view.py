from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QTextEdit,
    QSpinBox,
    QCheckBox,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QSplitter,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor
import logging

from views.components.toast import ToastNotification
from views.components.rich_text_editor import RichTextEditor
from views.exercises_view import ExerciseDialog  # <-- IMPORTANTE: esta importación
from utils.paths import resource_path
from views.styles import StyleHelper

logger = logging.getLogger(__name__)


class ExerciseItemWidget(QWidget):
    """Widget para mostrar un ejercicio en la lista"""

    clicked = pyqtSignal(object)
    edit_clicked = pyqtSignal(object)
    delete_clicked = pyqtSignal(object)

    def __init__(self, ejercicio, parent=None):
        super().__init__(parent)
        self.ejercicio = ejercicio
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(
            """
            ExerciseItemWidget {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
                margin: 2px;
            }
            ExerciseItemWidget:hover {
                background-color: #f8f9fa;
                border: 2px solid #e67e22;
            }
        """
        )
        self.setFixedHeight(60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        # Icono y tipo
        tipo_icon = {
            "seleccion_multiple": "📝",
            "verdadero_falso": "✓",
            "arrastrar_soltar": "🔄",
        }.get(self.ejercicio.get("tipo", ""), "✏️")

        icon_label = QLabel(tipo_icon)
        icon_label.setFont(QFont("Segoe UI", 16))
        icon_label.setFixedWidth(30)
        layout.addWidget(icon_label)

        # Contenido
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)

        pregunta = self.ejercicio.get("pregunta", "")
        if len(pregunta) > 50:
            pregunta = pregunta[:50] + "..."

        pregunta_label = QLabel(pregunta)
        pregunta_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        pregunta_label.setStyleSheet("color: #2c3e50;")
        content_layout.addWidget(pregunta_label)

        info_label = QLabel(
            f"Tipo: {self.ejercicio.get('tipo', '')} | "
            f"Orden: {self.ejercicio.get('orden', 1)}"
        )
        info_label.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        content_layout.addWidget(info_label)

        layout.addLayout(content_layout, 1)

        # Botones
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(26, 26)
        self.edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #f39c12;
                color: white;
                border-radius: 13px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """
        )
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.ejercicio))
        layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(26, 26)
        self.delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 13px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        self.delete_btn.clicked.connect(
            lambda: self.delete_clicked.emit(self.ejercicio)
        )
        layout.addWidget(self.delete_btn)

    def mousePressEvent(self, event):
        if not self.edit_btn.underMouse() and not self.delete_btn.underMouse():
            self.clicked.emit(self.ejercicio)
        super().mousePressEvent(event)


class LessonDialog(QDialog):
    """Diálogo para crear/editar lecciones con gestión de ejercicios"""

    def __init__(self, api_client, modulo_id, lesson_data=None, parent=None, initial_order=1, taken_orders=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_id = modulo_id
        self.lesson_data = lesson_data
        self.initial_order = initial_order
        self.taken_orders = taken_orders if taken_orders is not None else []
        self.ejercicios = []
        self.pending_exercises = []  # <--- Ejercicios en memoria (staging)
        
        self.setWindowTitle("Editar Lección" if lesson_data else "Nueva Lección")
        self.setMinimumSize(1000, 800)
        self.setup_ui()

        if lesson_data:
            self.load_lesson_data()
            # Si tiene ejercicios, cargarlos después de un pequeño delay
            if lesson_data.get("tiene_ejercicios", False):
                QTimer.singleShot(100, self.cargar_ejercicios)
        else:
            self.orden_input.setValue(self.initial_order)

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QTextEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
                background-color: white;
            }
            QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
                background-color: white;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #d1d5db;
                border-bottom: 1px solid #d1d5db;
                background-color: #f3f4f6;
                border-top-right-radius: 4px;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 30px;
                border-left: 1px solid #d1d5db;
                background-color: #f3f4f6;
                border-bottom-right-radius: 4px;
            }
            QSpinBox::up-arrow {
                image: none;
                width: 0; height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-bottom: 6px solid #4b5563;
                margin-top: 2px;
            }
            QSpinBox::down-arrow {
                image: none;
                width: 0; height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #4b5563;
                margin-bottom: 2px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e5e7eb;
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
            QCheckBox {
                font-size: 13px;
                color: #2c3e50;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:hover {
                border-color: #4361ee;
            }
            QCheckBox::indicator:checked {
                background-color: #4361ee;
                border: 1px solid #4361ee;
            }
        """
        )

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Usar ScrollArea para que quepan todos los campos y botones
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 10)

        # Título
        title = QLabel(
            "📖 " + ("Editar Lección" if self.lesson_data else "Nueva Lección")
        )
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Formulario básico
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(10)

        # Título
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Título de la lección")
        form_layout.addRow("Título:", self.titulo_input)

        # Orden
        self.orden_input = QSpinBox()
        self.orden_input.setMinimum(1)
        self.orden_input.setMaximum(999)
        self.orden_input.setFixedWidth(120)
        self.orden_input.setValue(1)
        form_layout.addRow("Orden:", self.orden_input)

        layout.addWidget(form_widget)

        # Editor de contenido
        content_label = QLabel("Contenido:")
        content_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(content_label)

        self.editor = RichTextEditor()
        self.editor.setMinimumHeight(450)
        layout.addWidget(self.editor, 1)

        # Opciones
        options_group = QGroupBox("Opciones de la Lección")
        options_layout = QHBoxLayout()

        self.editor_check = QCheckBox("Tiene editor de código")
        options_layout.addWidget(self.editor_check)

        self.ejercicios_check = QCheckBox("Tiene ejercicios")
        self.ejercicios_check.stateChanged.connect(self.on_ejercicios_changed)
        options_layout.addWidget(self.ejercicios_check)

        options_layout.addStretch()

        # Estado
        options_layout.addWidget(QLabel("Estado:"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        self.estado_combo.setFixedWidth(100)
        options_layout.addWidget(self.estado_combo)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Sección de ejercicios (visible solo si tiene ejercicios)
        self.exercises_group = QGroupBox("Ejercicios de la Lección")
        exercises_layout = QVBoxLayout()

        # Toolbar de ejercicios
        exercises_toolbar = QHBoxLayout()
        exercises_toolbar.addWidget(QLabel("Gestionar ejercicios:"))

        self.add_exercise_btn = QPushButton("➕ Nuevo Ejercicio")
        self.add_exercise_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 5px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """
        )
        self.add_exercise_btn.clicked.connect(self.nuevo_ejercicio)
        exercises_toolbar.addWidget(self.add_exercise_btn)

        self.refresh_exercises_btn = QPushButton("🔄")
        self.refresh_exercises_btn.setFixedSize(30, 30)
        self.refresh_exercises_btn.setToolTip("Actualizar lista")
        self.refresh_exercises_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )
        self.refresh_exercises_btn.clicked.connect(self.cargar_ejercicios)
        exercises_toolbar.addWidget(self.refresh_exercises_btn)

        exercises_toolbar.addStretch()
        exercises_layout.addLayout(exercises_toolbar)

        # Lista de ejercicios
        self.exercises_list = QListWidget()
        self.exercises_list.setMaximumHeight(200)
        self.exercises_list.setStyleSheet(
            """
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                padding: 5px;
            }
        """
        )
        exercises_layout.addWidget(self.exercises_list)

        self.exercises_group.setLayout(exercises_layout)
        layout.addWidget(self.exercises_group)

        # Inicialmente oculto si no tiene ejercicios
        self.exercises_group.setVisible(False)
        
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # --- BOTONES (FUERA DEL SCROLL PARA VISIBILIDAD) ---
        button_container = QFrame()
        button_container.setFixedHeight(85)
        button_container.setObjectName("dialogButtons")
        button_container.setStyleSheet("""
            #dialogButtons {
                background-color: #ffffff;
                border-top: 1px solid #e5e7eb;
            }
        """)
        
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(30, 0, 30, 0)
        button_layout.setSpacing(15)
        
        # Botón Cancelar
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setFixedHeight(45)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet(
            StyleHelper.button_secondary() + 
            "QPushButton { border-radius: 22px; padding: 0 30px; background-color: #ef4444; color: white; }" +
            "QPushButton:hover { background-color: #dc2626; }"
        )
        self.cancel_btn.clicked.connect(self.reject)
        
        # Botón Guardar
        self.save_btn = QPushButton("Guardar Lección")
        self.save_btn.setFixedHeight(45)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet(
            StyleHelper.button_primary() + 
            "QPushButton { border-radius: 22px; padding: 0 40px; background-color: #4361ee; color: white; }" +
            "QPushButton:hover { background-color: #3f37c9; }"
        )
        self.save_btn.clicked.connect(self._on_save_clicked)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addWidget(button_container)

    def _on_save_clicked(self):
        """Muestra indicador visual antes de guardar"""
        data = self.get_data()
        if data is None:
            return
            
        self.save_btn.setText("⏳ Guardando...")
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.setCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        
        # Le damos un instante a la UI para repintarse antes de congelar en accept
        QTimer.singleShot(50, self.accept)

    def on_ejercicios_changed(self, state):
        """Mostrar/ocultar sección de ejercicios"""
        self.exercises_group.setVisible(state == Qt.CheckState.Checked.value)
        if state == Qt.CheckState.Checked.value and self.lesson_data:
            self.cargar_ejercicios()

    def cargar_ejercicios(self):
        """Cargar ejercicios de la lección"""
        logger.debug(f"Cargando ejercicios. Lesson data: {bool(self.lesson_data)}")
        self.exercises_list.clear()

        # 1. Cargar ejercicios reales de la API (si existen)
        if self.lesson_data:
            result = self.api_client.get_ejercicios(
                self.modulo_id, self.lesson_data["id"], force_refresh=True
            )
            if result["success"]:
                data = result.get("data", [])
                if isinstance(data, list):
                    self.ejercicios = data
                elif isinstance(data, dict) and "data" in data:
                    self.ejercicios = data["data"]
                else:
                    self.ejercicios = []
            else:
                self.ejercicios = []
        else:
            self.ejercicios = []

        # 2. Combinar con ejercicios pendientes (staging)
        # Marcamos los pendientes con un flag especial para visualización
        all_exercises = list(self.ejercicios)
        for pe in self.pending_exercises:
            pe_copy = dict(pe)
            pe_copy["_is_pending"] = True
            all_exercises.append(pe_copy)

        logger.debug(
            f"Total ejercicios: {len(all_exercises)} (API: {len(self.ejercicios)}, Pending: {len(self.pending_exercises)})"
        )

        if not all_exercises:
            # Mostrar mensaje si no hay ejercicios
            item = QListWidgetItem("📭 No hay ejercicios creados")
            item.setForeground(QColor("#95a5a6"))
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.exercises_list.addItem(item)
        else:
            for ejercicio in all_exercises:
                item = QListWidgetItem()
                widget = ExerciseItemWidget(ejercicio)

                # Estilo especial para pendientes
                if ejercicio.get("_is_pending"):
                    widget.setStyleSheet(
                        widget.styleSheet() + "\nQWidget { background-color: #fff9f0; }"
                    )
                    widget.edit_btn.setToolTip(
                        "Disponible después de guardar la lección"
                    )
                    widget.edit_btn.setEnabled(False)

                widget.edit_clicked.connect(self.editar_ejercicio)
                widget.delete_clicked.connect(self.eliminar_ejercicio)

                item.setSizeHint(widget.sizeHint())
                self.exercises_list.addItem(item)
                self.exercises_list.setItemWidget(item, widget)

    def nuevo_ejercicio(self):
        """Crear nuevo ejercicio (soporta staging si la lección es nueva)"""
        logger.debug("Abriendo diálogo para nuevo ejercicio")

        # Pasar ID temporal o real
        lesson_id = self.lesson_data["id"] if self.lesson_data else 0
        dialog = ExerciseDialog(self.api_client, self.modulo_id, lesson_id, parent=self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            if not self.lesson_data:
                # Caso: Lección nueva, guardamos en staging
                logger.debug(f"Agregando ejercicio a staging: {data.get('pregunta')}")
                self.pending_exercises.append(data)
                self.cargar_ejercicios()
                self.exercises_list.scrollToBottom()
                if not self.ejercicios_check.isChecked():
                    self.ejercicios_check.setChecked(True)
                return

            # Caso: Lección existente, guardar directo en API
            logger.debug(f"Creando ejercicio directo en API: {data}")
            result = self.api_client.create_ejercicio(
                self.modulo_id, self.lesson_data["id"], data
            )

            if result["success"]:
                self.cargar_ejercicios()
                self.exercises_list.scrollToBottom()
                # Asegurar que el checkbox esté marcado
                if not self.ejercicios_check.isChecked():
                    self.ejercicios_check.setChecked(True)
            else:
                error_msg = result.get("error", "Error desconocido")
                QMessageBox.critical(
                    self, "Error", f"Error al crear ejercicio:\n{error_msg}"
                )

    def editar_ejercicio(self, ejercicio):
        """Editar ejercicio existente"""
        if not self.lesson_data:
            return

        logger.debug(f"Editando ejercicio: {ejercicio.get('id')}")
        dialog = ExerciseDialog(
            self.api_client, self.modulo_id, self.lesson_data["id"], ejercicio, self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            result = self.api_client.update_ejercicio(
                self.modulo_id, self.lesson_data["id"], ejercicio["id"], data
            )

            if result["success"]:
                self.cargar_ejercicios()
            else:
                error_msg = result.get("error", "Error desconocido")
                QMessageBox.critical(
                    self, "Error", f"Error al actualizar:\n{error_msg}"
                )

    def eliminar_ejercicio(self, ejercicio):
        """Eliminar ejercicio"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar este ejercicio?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            logger.debug(f"Eliminando ejercicio: {ejercicio.get('id')}")
            result = self.api_client.delete_ejercicio(
                self.modulo_id, self.lesson_data["id"], ejercicio["id"]
            )

            if result["success"]:
                self.cargar_ejercicios()
                # Si no quedan ejercicios, podemos desmarcar el checkbox
                if not self.ejercicios:
                    self.ejercicios_check.setChecked(False)
            else:
                error_msg = result.get("error", "Error desconocido")
                QMessageBox.critical(self, "Error", f"Error al eliminar:\n{error_msg}")

    def load_lesson_data(self):
        """Cargar datos de la lección"""
        self.titulo_input.setText(self.lesson_data.get("titulo", ""))
        self.orden_input.setValue(self.lesson_data.get("orden", 1))
        self.editor.setHtml(self.lesson_data.get("contenido", ""))
        self.editor_check.setChecked(self.lesson_data.get("tiene_editor_codigo", False))
        self.ejercicios_check.setChecked(
            self.lesson_data.get("tiene_ejercicios", False)
        )

        index = self.estado_combo.findText(self.lesson_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

    def get_data(self):
        """Obtener datos del formulario"""
        order_val = self.orden_input.value()

        return {
            "titulo": self.titulo_input.text().strip(),
            "contenido": self.editor.toHtml(),
            "orden": order_val,
            "tiene_editor_codigo": self.editor_check.isChecked(),
            "tiene_ejercicios": self.ejercicios_check.isChecked(),
            "estado": self.estado_combo.currentText(),
        }

    def get_pending_exercises(self):
        """Retorna la lista de ejercicios en staging"""
        return self.pending_exercises


# El resto de las clases (LessonDetailView, LessonsView) se mantienen igual...
class LessonDetailView(QWidget):
    """Vista de detalle de lección"""

    def __init__(self, api_client, modulo, leccion, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo = modulo
        self.leccion = leccion
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title = QLabel(f"📖 {self.leccion.get('titulo', 'Lección')}")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        # Contenido
        content = QTextEdit()
        content.setHtml(self.leccion.get("contenido", ""))
        content.setReadOnly(True)
        layout.addWidget(content)


class LessonsView(QWidget):
    """Vista principal de lecciones"""

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.modulos = []
        self.lecciones = []
        self.modulo_actual = None
        self.setup_ui()
        self.toast = ToastNotification(self)
        self.load_modulos()

        # Conectar señales para actualización en tiempo real
        self.api_client.data_changed.connect(self._on_data_changed)

    def setup_ui(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                font-weight: bold;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📖 Lecciones")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Selector de módulo
        header_layout.addWidget(QLabel("Módulo:"))
        self.modulo_combo = QComboBox()
        self.modulo_combo.setMinimumWidth(200)
        self.modulo_combo.currentIndexChanged.connect(self.cambiar_modulo)
        header_layout.addWidget(self.modulo_combo)

        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(36, 36)
        self.refresh_btn.clicked.connect(self.load_modulos)
        header_layout.addWidget(self.refresh_btn)

        self.new_lesson_btn = QPushButton("+ Nueva Lección")
        self.new_lesson_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #059669; }
            QPushButton:disabled { background-color: #9ca3af; }
            """
        )
        self.new_lesson_btn.setEnabled(
            False
        )  # Se activa cuando se selecciona un módulo
        self.new_lesson_btn.clicked.connect(self.nueva_leccion)
        header_layout.addWidget(self.new_lesson_btn)

        layout.addLayout(header_layout)

        # Contenedor apilado (StackedWidget) para Placeholder / Tabla
        self.stack = QStackedWidget()

        # --- PÁGINA 0: PLACEHOLDER ---
        self.placeholder = self._create_placeholder()
        self.stack.addWidget(self.placeholder)

        # --- PÁGINA 1: TABLA ---
        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Título", "Orden", "Ejercicios", "Acciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        table_layout.addWidget(self.table)

        self.stack.addWidget(table_container)
        layout.addWidget(self.stack)

        self.setLayout(layout)

    def _create_placeholder(self) -> QFrame:
        """Crea la vista de placeholder"""
        frame = QFrame()
        frame.setStyleSheet(
            "background-color: white; border-radius: 12px; border: 1px dashed #e2e8f0;"
        )

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        icon = QLabel("📂")
        icon.setFont(QFont("Segoe UI", 64))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        text = QLabel("Seleccione un módulo para gestionar sus lecciones")
        text.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        text.setStyleSheet("color: #64748b;")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text)

        subtext = QLabel("Use el selector superior para comenzar")
        subtext.setStyleSheet("color: #94a3b8; font-size: 14px;")
        subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtext)

        return frame

    def load_modulos(self):
        """Cargar módulos"""
        result = self.api_client.get_modulos()
        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.modulos = data
            else:
                self.modulos = []

            self.modulo_combo.clear()
            self.modulo_combo.addItem("Seleccione un módulo", None)
            for m in self.modulos:
                self.modulo_combo.addItem(m.get("titulo"), m.get("id"))

    def cambiar_modulo(self, index):
        """Cambiar módulo seleccionado"""
        if index <= 0:
            self.modulo_actual = None
            self.lecciones = []
            self.stack.setCurrentIndex(0)
            if hasattr(self, "new_lesson_btn"):
                self.new_lesson_btn.setEnabled(False)
            return

        self.stack.setCurrentIndex(1)

        modulo_id = self.modulo_combo.currentData()
        self.modulo_actual = next(
            (m for m in self.modulos if m["id"] == modulo_id), None
        )
        if hasattr(self, "new_lesson_btn"):
            self.new_lesson_btn.setEnabled(self.modulo_actual is not None)
        self.load_lecciones(modulo_id)

    def load_lecciones(self, modulo_id, force_refresh=False):
        """Cargar lecciones del módulo"""
        result = self.api_client.get_lecciones(modulo_id, force_refresh=force_refresh)
        if result["success"]:
            data = result.get("data", [])
            # Manejar tanto lista simple como respuesta paginada de Laravel
            if isinstance(data, list):
                self.lecciones = data
            elif isinstance(data, dict) and "data" in data:
                self.lecciones = data["data"]
            else:
                self.lecciones = []
            self.actualizar_tabla(self.lecciones)

    def actualizar_tabla(self, lecciones):
        """Actualizar tabla de lecciones"""
        self.table.setRowCount(len(lecciones))
        self.table.setStyleSheet(
            """
            QTableWidget { border: none; }
            QTableView { border: none; }
            QTableWidget::item { padding: 8px; }
        """
        )
        self.table.setColumnWidth(4, 120)
        self.table.verticalHeader().setDefaultSectionSize(54)

        for row, leccion in enumerate(lecciones):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(leccion.get("id", ""))))

            # Título
            self.table.setItem(row, 1, QTableWidgetItem(leccion.get("titulo", "")))

            # Orden
            self.table.setItem(row, 2, QTableWidgetItem(str(leccion.get("orden", ""))))

            # Ejercicios
            tiene_ej = "✅" if leccion.get("tiene_ejercicios") else "❌"
            item = QTableWidgetItem(tiene_ej)
            item.setForeground(
                QColor("#27ae60")
                if leccion.get("tiene_ejercicios")
                else QColor("#e74c3c")
            )
            self.table.setItem(row, 3, item)

            # Acciones
            acciones = QWidget()
            acciones_layout = QHBoxLayout(acciones)
            acciones_layout.setContentsMargins(8, 0, 8, 0)
            acciones_layout.setSpacing(10)
            acciones_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.setToolTip("Editar")
            edit_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #f39c12;
                    color: white;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e67e22;
                }
            """
            )
            edit_btn.clicked.connect(lambda checked, l=leccion: self.editar_leccion(l))
            acciones_layout.addWidget(edit_btn)

            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(30, 30)
            delete_btn.setToolTip("Eliminar")
            delete_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """
            )
            delete_btn.clicked.connect(
                lambda checked, l=leccion: self.eliminar_leccion(l)
            )
            acciones_layout.addWidget(delete_btn)

            acciones_layout.addStretch()
            self.table.setCellWidget(row, 4, acciones)

    def nueva_leccion(self):
        """Crear nueva lección en el módulo seleccionado"""
        if not self.modulo_actual:
            QMessageBox.warning(self, "Aviso", "Selecciona un módulo primero")
            return

        # Calcular siguiente orden de forma robusta
        orders = []
        for l in self.lecciones:
            val = l.get('orden')
            if val is not None:
                try:
                    orders.append(int(val))
                except (ValueError, TypeError):
                    continue
                
        next_order = max(orders) + 1 if orders else 1

        dialog = LessonDialog(self.api_client, self.modulo_actual["id"], lesson_data=None, parent=self, initial_order=next_order, taken_orders=orders)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data is None:
                return
                
            self._desplazar_orden_lecciones(data["orden"])
            
            result = self.api_client.create_leccion(self.modulo_actual["id"], data)
            if result["success"]:
                # Guardar ejercicios pendientes si existen (Cascading Save)
                nueva_leccion_data = result.get("data", {})
                leccion_id = nueva_leccion_data.get("id")
                pending_exercises = dialog.get_pending_exercises()

                if leccion_id and pending_exercises:
                    logger.debug(
                        f"Guardando {len(pending_exercises)} ejercicios pendientes para lección {leccion_id}"
                    )
                    for exercise_data in pending_exercises:
                        self.api_client.create_ejercicio(
                            self.modulo_actual["id"], leccion_id, exercise_data
                        )

                self.load_lecciones(self.modulo_actual["id"], force_refresh=True)
            else:
                err_msg = str(result.get('error', 'Error desconocido'))
                if len(err_msg) > 200:
                    err_msg = err_msg[:200] + "..."
                QMessageBox.critical(self, "Error", f"Error al crear: {err_msg}")

    def editar_leccion(self, leccion):
        """Editar lección"""
        if not self.modulo_actual:
            return

        # Obtener órdenes ocupados excluyendo la lección actual
        orders = [l.get('orden', 0) for l in self.lecciones if l.get('id') != leccion.get('id')]

        dialog = LessonDialog(self.api_client, self.modulo_actual["id"], lesson_data=leccion, parent=self, taken_orders=orders)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data is None:
                return
                
            # Sólo desplazar si cambió el orden y choca con otro
            if data["orden"] != leccion.get("orden"):
                self._desplazar_orden_lecciones(data["orden"], leccion_id_ignorar=leccion["id"])
                
            result = self.api_client.update_leccion(
                self.modulo_actual["id"], leccion["id"], data
            )
            if result["success"]:
                self.load_lecciones(self.modulo_actual["id"], force_refresh=True)
            else:
                err_msg = str(result.get('error', 'Error desconocido'))
                if len(err_msg) > 200:
                    err_msg = err_msg[:200] + "..."
                QMessageBox.critical(self, "Error", f"Error al actualizar: {err_msg}")

    def eliminar_leccion(self, leccion):
        """Eliminar lección"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar lección '{leccion.get('titulo')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes and self.modulo_actual:
            result = self.api_client.delete_leccion(
                self.modulo_actual["id"], leccion["id"]
            )
            if result["success"]:
                self.load_lecciones(self.modulo_actual["id"], force_refresh=True)
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def _desplazar_orden_lecciones(self, orden_objetivo, leccion_id_ignorar=None):
        """Si el orden objetivo está ocupado por otra lección, la mueve al max(orden) + 1"""
        if not self.lecciones:
            return

        leccion_colision = None
        for l in self.lecciones:
            if l.get("id") == leccion_id_ignorar:
                continue
            l_orden = l.get("orden")
            try:
                if l_orden is not None and int(l_orden) == int(orden_objetivo):
                    leccion_colision = l
                    break
            except (ValueError, TypeError):
                continue

        if not leccion_colision:
            return  # No hay colisión

        orders = []
        for l in self.lecciones:
            val = l.get('orden')
            if val is not None:
                try:
                    orders.append(int(val))
                except (ValueError, TypeError):
                    continue

        nuevo_orden_para_antigua = max(orders) + 1 if orders else 1

        update_data = {
            "titulo": leccion_colision.get("titulo", "Sin título"),
            "contenido": leccion_colision.get("contenido", ""),
            "orden": nuevo_orden_para_antigua,
            "tiene_editor_codigo": leccion_colision.get("tiene_editor_codigo", False),
            "tiene_ejercicios": leccion_colision.get("tiene_ejercicios", False),
            "estado": leccion_colision.get("estado", "activo"),
        }
        
        try:
            res = self.api_client.update_leccion(self.modulo_actual["id"], leccion_colision["id"], update_data)
            if res.get("success"):
                self.toast.show_toast(f"La lección '{leccion_colision.get('titulo')}' se movió al orden {nuevo_orden_para_antigua}", "info")
        except Exception as e:
            logger.error(f"Error al desplazar lección: {e}")

    def _on_data_changed(self, data_type: str):
        """Manejador para actualizaciones en tiempo real"""
        if data_type == "lecciones" or data_type == "modulos":
            if self.modulo_actual:
                self.load_lecciones(self.modulo_actual["id"], force_refresh=True)
            else:
                self.load_modulos()
