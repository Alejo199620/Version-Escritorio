from PyQt5.QtWidgets import (
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
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor
import logging

from views.components.rich_text_editor import RichTextEditor
from views.exercises_view import ExerciseDialog  # <-- IMPORTANTE: esta importación
from utils.paths import resource_path

logging.basicConfig(level=logging.DEBUG)
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
        self.setCursor(Qt.PointingHandCursor)

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
        pregunta_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
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

    def __init__(self, api_client, modulo_id, lesson_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_id = modulo_id
        self.lesson_data = lesson_data
        self.ejercicios = []
        self.setWindowTitle("Editar Lección" if lesson_data else "Nueva Lección")
        self.setMinimumSize(800, 700)
        self.setup_ui()

        if lesson_data:
            self.load_lesson_data()
            # Si tiene ejercicios, cargarlos después de un pequeño delay
            if lesson_data.get("tiene_ejercicios", False):
                QTimer.singleShot(100, self.cargar_ejercicios)

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
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
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel(
            "📖 " + ("Editar Lección" if self.lesson_data else "Nueva Lección")
        )
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
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
        self.orden_input.setMaximum(100)
        self.orden_input.setValue(1)
        form_layout.addRow("Orden:", self.orden_input)

        layout.addWidget(form_widget)

        # Editor de contenido
        content_label = QLabel("Contenido:")
        content_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(content_label)

        self.editor = RichTextEditor()
        self.editor.setMinimumHeight(200)
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

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar Lección")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        for btn in [
            buttons.button(QDialogButtonBox.Ok),
            buttons.button(QDialogButtonBox.Cancel),
        ]:
            btn.setStyleSheet(
                """
                QPushButton {
                    padding: 10px 30px;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 13px;
                    min-width: 120px;
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
            background-color: #95a5a6;
            color: white;
        """
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def on_ejercicios_changed(self, state):
        """Mostrar/ocultar sección de ejercicios"""
        self.exercises_group.setVisible(state == Qt.Checked)
        if state == Qt.Checked and self.lesson_data:
            self.cargar_ejercicios()

    def cargar_ejercicios(self):
        """Cargar ejercicios de la lección"""
        if not self.lesson_data:
            return

        logger.debug(f"Cargando ejercicios para lección {self.lesson_data['id']}")
        self.exercises_list.clear()

        result = self.api_client.get_ejercicios(self.modulo_id, self.lesson_data["id"])

        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.ejercicios = data
            elif isinstance(data, dict) and "data" in data:
                self.ejercicios = data["data"]
            else:
                self.ejercicios = []

            logger.debug(f"Ejercicios cargados: {len(self.ejercicios)}")

            if not self.ejercicios:
                # Mostrar mensaje si no hay ejercicios
                item = QListWidgetItem("📭 No hay ejercicios creados")
                item.setForeground(QColor("#95a5a6"))
                item.setFlags(Qt.NoItemFlags)
                self.exercises_list.addItem(item)
            else:
                for ejercicio in self.ejercicios:
                    item = QListWidgetItem()
                    widget = ExerciseItemWidget(ejercicio)
                    widget.edit_clicked.connect(self.editar_ejercicio)
                    widget.delete_clicked.connect(self.eliminar_ejercicio)

                    item.setSizeHint(widget.sizeHint())
                    self.exercises_list.addItem(item)
                    self.exercises_list.setItemWidget(item, widget)

    def nuevo_ejercicio(self):
        """Crear nuevo ejercicio"""
        if not self.lesson_data:
            QMessageBox.warning(self, "Error", "Primero debes guardar la lección")
            return

        logger.debug("Abriendo diálogo para nuevo ejercicio")
        dialog = ExerciseDialog(
            self.api_client, self.modulo_id, self.lesson_data["id"], parent=self
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            logger.debug(f"Creando ejercicio con datos: {data}")
            result = self.api_client.create_ejercicio(
                self.modulo_id, self.lesson_data["id"], data
            )

            if result["success"]:
                QMessageBox.information(self, "Éxito", "Ejercicio creado correctamente")
                self.cargar_ejercicios()
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

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data is None:
                return

            result = self.api_client.update_ejercicio(
                self.modulo_id, self.lesson_data["id"], ejercicio["id"], data
            )

            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Ejercicio actualizado correctamente"
                )
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
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            logger.debug(f"Eliminando ejercicio: {ejercicio.get('id')}")
            result = self.api_client.delete_ejercicio(
                self.modulo_id, self.lesson_data["id"], ejercicio["id"]
            )

            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Ejercicio eliminado correctamente"
                )
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
        return {
            "titulo": self.titulo_input.text().strip(),
            "contenido": self.editor.toHtml(),
            "orden": self.orden_input.value(),
            "tiene_editor_codigo": self.editor_check.isChecked(),
            "tiene_ejercicios": self.ejercicios_check.isChecked(),
            "estado": self.estado_combo.currentText(),
        }


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
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
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
        self.load_modulos()

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
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
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

        layout.addLayout(header_layout)

        # Tabla de lecciones
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Título", "Orden", "Ejercicios", "Acciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        self.setLayout(layout)

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
            self.actualizar_tabla([])
            return

        modulo_id = self.modulo_combo.currentData()
        self.modulo_actual = next(
            (m for m in self.modulos if m["id"] == modulo_id), None
        )
        self.load_lecciones(modulo_id)

    def load_lecciones(self, modulo_id):
        """Cargar lecciones del módulo"""
        result = self.api_client.get_lecciones(modulo_id)
        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.lecciones = data
            else:
                self.lecciones = []
            self.actualizar_tabla(self.lecciones)

    def actualizar_tabla(self, lecciones):
        """Actualizar tabla de lecciones"""
        self.table.setRowCount(len(lecciones))

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
            acciones_layout.setContentsMargins(5, 2, 5, 2)

            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.clicked.connect(lambda checked, l=leccion: self.editar_leccion(l))
            acciones_layout.addWidget(edit_btn)

            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(30, 30)
            delete_btn.clicked.connect(
                lambda checked, l=leccion: self.eliminar_leccion(l)
            )
            acciones_layout.addWidget(delete_btn)

            acciones_layout.addStretch()
            self.table.setCellWidget(row, 4, acciones)

    def editar_leccion(self, leccion):
        """Editar lección"""
        if not self.modulo_actual:
            return

        dialog = LessonDialog(self.api_client, self.modulo_actual["id"], leccion, self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_leccion(
                self.modulo_actual["id"], leccion["id"], data
            )
            if result["success"]:
                QMessageBox.information(self, "Éxito", "Lección actualizada")
                self.load_lecciones(self.modulo_actual["id"])
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_leccion(self, leccion):
        """Eliminar lección"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar lección '{leccion.get('titulo')}'?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes and self.modulo_actual:
            result = self.api_client.delete_leccion(
                self.modulo_actual["id"], leccion["id"]
            )
            if result["success"]:
                self.load_lecciones(self.modulo_actual["id"])
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")
