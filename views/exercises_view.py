from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
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
    QRadioButton,
    QButtonGroup,
    QListWidget,
    QListWidgetItem,
    QSplitter,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import logging
from utils.paths import resource_path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExerciseDialog(QDialog):
    def __init__(
        self, api_client, modulo_id, leccion_id, exercise_data=None, parent=None
    ):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_id = modulo_id
        self.leccion_id = leccion_id
        self.exercise_data = exercise_data
        self.opciones = []
        self.setWindowTitle("Editar Ejercicio" if exercise_data else "Nuevo Ejercicio")
        self.setMinimumSize(700, 600)
        self.setup_ui()

        if exercise_data:
            self.load_exercise_data()

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
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #3498db;
            }
            QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
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
                background-color: #3498db;
                color: white;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel(
            "✏️ " + ("Editar Ejercicio" if self.exercise_data else "Nuevo Ejercicio")
        )
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Tipo de ejercicio
        tipo_layout = QHBoxLayout()
        tipo_layout.addWidget(QLabel("Tipo:"))

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["seleccion_multiple", "verdadero_falso", "arrastrar_soltar"]
        )
        self.tipo_combo.currentTextChanged.connect(self.cambiar_tipo)
        tipo_layout.addWidget(self.tipo_combo)
        tipo_layout.addStretch()

        layout.addLayout(tipo_layout)

        # Pregunta
        pregunta_label = QLabel("Pregunta:")
        pregunta_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(pregunta_label)

        self.pregunta_input = QTextEdit()
        self.pregunta_input.setPlaceholderText("Escribe la pregunta del ejercicio...")
        self.pregunta_input.setMaximumHeight(100)
        layout.addWidget(self.pregunta_input)

        # Opciones (cambia según el tipo)
        self.opciones_group = QGroupBox("Opciones")
        self.opciones_layout = QVBoxLayout()

        # Toolbar para opciones
        opciones_toolbar = QHBoxLayout()

        self.add_opcion_btn = QPushButton("➕ Agregar Opción")
        self.add_opcion_btn.clicked.connect(self.agregar_opcion)
        opciones_toolbar.addWidget(self.add_opcion_btn)

        self.remove_opcion_btn = QPushButton("🗑️ Eliminar Seleccionada")
        self.remove_opcion_btn.clicked.connect(self.eliminar_opcion)
        opciones_toolbar.addWidget(self.remove_opcion_btn)

        opciones_toolbar.addStretch()
        self.opciones_layout.addLayout(opciones_toolbar)

        # Lista de opciones
        self.opciones_list = QListWidget()
        self.opciones_list.setMaximumHeight(200)
        self.opciones_layout.addWidget(self.opciones_list)

        self.opciones_group.setLayout(self.opciones_layout)
        layout.addWidget(self.opciones_group)

        # Orden y estado
        bottom_layout = QHBoxLayout()

        # Orden
        orden_layout = QHBoxLayout()
        orden_layout.addWidget(QLabel("Orden:"))
        self.orden_input = QSpinBox()
        self.orden_input.setMinimum(1)
        self.orden_input.setMaximum(100)
        self.orden_input.setValue(1)
        self.orden_input.setFixedWidth(80)
        orden_layout.addWidget(self.orden_input)
        bottom_layout.addLayout(orden_layout)

        bottom_layout.addStretch()

        # Estado
        estado_layout = QHBoxLayout()
        estado_layout.addWidget(QLabel("Estado:"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        self.estado_combo.setFixedWidth(100)
        estado_layout.addWidget(self.estado_combo)
        bottom_layout.addLayout(estado_layout)

        layout.addLayout(bottom_layout)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 30px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 30px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.cambiar_tipo(self.tipo_combo.currentText())

    def cambiar_tipo(self, tipo):
        """Cambiar la interfaz según el tipo de ejercicio"""
        if tipo == "verdadero_falso":
            self.add_opcion_btn.setEnabled(False)
            self.remove_opcion_btn.setEnabled(False)
            self.opciones_list.clear()

            # Agregar opciones por defecto
            item1 = QListWidgetItem("Verdadero")
            item1.setData(
                Qt.UserRole, {"texto": "Verdadero", "es_correcta": True, "orden": 1}
            )
            self.opciones_list.addItem(item1)

            item2 = QListWidgetItem("Falso")
            item2.setData(
                Qt.UserRole, {"texto": "Falso", "es_correcta": False, "orden": 2}
            )
            self.opciones_list.addItem(item2)
        else:
            self.add_opcion_btn.setEnabled(True)
            self.remove_opcion_btn.setEnabled(True)

    def agregar_opcion(self):
        """Agregar una nueva opción"""
        dialog = OpcionDialog(self.tipo_combo.currentText())
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            item_text = data["texto"]
            if self.tipo_combo.currentText() == "arrastrar_soltar" and data.get(
                "pareja"
            ):
                item_text = f"{data['texto']} → {data['pareja']}"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, data)

            # Marcar si es correcta
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

    def load_exercise_data(self):
        """Cargar datos del ejercicio"""
        self.pregunta_input.setPlainText(self.exercise_data.get("pregunta", ""))
        self.orden_input.setValue(self.exercise_data.get("orden", 1))

        tipo = self.exercise_data.get("tipo", "seleccion_multiple")
        index = self.tipo_combo.findText(tipo)
        if index >= 0:
            self.tipo_combo.setCurrentIndex(index)

        # Cargar opciones
        opciones = self.exercise_data.get("opciones", [])
        self.opciones_list.clear()

        for opcion in opciones:
            item_text = opcion["texto"]
            if tipo == "arrastrar_soltar" and opcion.get("pareja_arrastre"):
                item_text = f"{opcion['texto']} → {opcion['pareja_arrastre']}"

            item = QListWidgetItem(item_text)
            item.setData(
                Qt.UserRole,
                {
                    "id": opcion.get("id"),
                    "texto": opcion["texto"],
                    "es_correcta": opcion.get("es_correcta", False),
                    "pareja": opcion.get("pareja_arrastre"),
                    "orden": opcion.get("orden", 1),
                },
            )

            if opcion.get("es_correcta"):
                item.setForeground(QColor("#27ae60"))

            self.opciones_list.addItem(item)

        index = self.estado_combo.findText(self.exercise_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

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
            "orden": self.orden_input.value(),
            "estado": self.estado_combo.currentText(),
            "opciones": opciones,
        }


# ... (mantén todos los imports igual) ...


class OpcionDialog(QDialog):
    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.setWindowTitle("Agregar Opción")

        # Tamaño según tipo
        if tipo == "arrastrar_soltar":
            self.setFixedSize(450, 300)
            self.setWindowTitle("Agregar Par (Término → Definición)")
        else:
            self.setFixedSize(400, 200)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        if self.tipo == "arrastrar_soltar":
            # Instrucciones
            instrucciones = QLabel(
                "📌 Crea un par para arrastrar y soltar:\n"
                "El usuario deberá arrastrar el TÉRMINO hasta su DEFINICIÓN"
            )
            instrucciones.setStyleSheet(
                """
                QLabel {
                    background-color: #e3f2fd;
                    color: #1976d2;
                    padding: 12px;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                }
            """
            )
            instrucciones.setWordWrap(True)
            layout.addWidget(instrucciones)

            # Término
            termino_label = QLabel("📝 Término:")
            termino_label.setStyleSheet("font-weight: bold; color: #e67e22;")
            layout.addWidget(termino_label)

            self.texto_input = QLineEdit()
            self.texto_input.setPlaceholderText("Ej: HTML")
            layout.addWidget(self.texto_input)

            layout.addSpacing(10)

            # Definición
            definicion_label = QLabel("📚 Definición:")
            definicion_label.setStyleSheet("font-weight: bold; color: #3498db;")
            layout.addWidget(definicion_label)

            self.pareja_input = QLineEdit()
            self.pareja_input.setPlaceholderText("Ej: HyperText Markup Language")
            layout.addWidget(self.pareja_input)

            # Ejemplo visual
            ejemplo_frame = QFrame()
            ejemplo_frame.setStyleSheet(
                """
                QFrame {
                    background-color: #f8f9fa;
                    border: 2px dashed #3498db;
                    border-radius: 8px;
                    padding: 15px;
                    margin-top: 10px;
                }
            """
            )
            ejemplo_layout = QHBoxLayout(ejemplo_frame)

            ejemplo_termino = QLabel("HTML")
            ejemplo_termino.setStyleSheet(
                """
                QLabel {
                    background-color: #e67e22;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """
            )
            ejemplo_layout.addWidget(ejemplo_termino)

            ejemplo_layout.addWidget(QLabel(" → "))

            ejemplo_def = QLabel("HyperText Markup Language")
            ejemplo_def.setStyleSheet(
                """
                QLabel {
                    background-color: #3498db;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """
            )
            ejemplo_layout.addWidget(ejemplo_def)
            ejemplo_layout.addStretch()

            layout.addWidget(ejemplo_frame)

        elif self.tipo == "seleccion_multiple":
            # Texto de la opción
            layout.addWidget(QLabel("📝 Texto de la opción:"))
            self.texto_input = QLineEdit()
            self.texto_input.setPlaceholderText("Escribe la opción...")
            layout.addWidget(self.texto_input)

            # ¿Es correcta?
            self.correcta_check = QCheckBox("✓ Esta es la respuesta correcta")
            self.correcta_check.setStyleSheet("color: #27ae60; font-weight: bold;")
            layout.addWidget(self.correcta_check)

        else:  # verdadero_falso no debería llegar aquí
            layout.addWidget(QLabel("Texto de la opción:"))
            self.texto_input = QLineEdit()
            layout.addWidget(self.texto_input)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        data = {"texto": self.texto_input.text()}

        if self.tipo == "arrastrar_soltar":
            data["pareja"] = self.pareja_input.text()
            data["es_correcta"] = True  # En arrastrar, todos los pares son correctos
        elif self.tipo == "seleccion_multiple":
            data["es_correcta"] = self.correcta_check.isChecked()
        else:
            data["es_correcta"] = False

        return data


class ExerciseDialog(QDialog):
    def __init__(
        self, api_client, modulo_id, leccion_id, exercise_data=None, parent=None
    ):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_id = modulo_id
        self.leccion_id = leccion_id
        self.exercise_data = exercise_data
        self.opciones = []
        self.setWindowTitle("Editar Ejercicio" if exercise_data else "Nuevo Ejercicio")
        self.setMinimumSize(700, 650)
        self.setup_ui()

        if exercise_data:
            self.load_exercise_data()

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
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #3498db;
            }
            QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
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
                background-color: #3498db;
                color: white;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel(
            "✏️ " + ("Editar Ejercicio" if self.exercise_data else "Nuevo Ejercicio")
        )
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Tipo de ejercicio
        tipo_layout = QHBoxLayout()
        tipo_layout.addWidget(QLabel("Tipo:"))

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["seleccion_multiple", "verdadero_falso", "arrastrar_soltar"]
        )
        self.tipo_combo.currentTextChanged.connect(self.cambiar_tipo)
        tipo_layout.addWidget(self.tipo_combo)
        tipo_layout.addStretch()

        layout.addLayout(tipo_layout)

        # Pregunta
        pregunta_label = QLabel("Pregunta:")
        pregunta_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(pregunta_label)

        self.pregunta_input = QTextEdit()
        self.pregunta_input.setPlaceholderText("Escribe la pregunta del ejercicio...")
        self.pregunta_input.setMaximumHeight(100)
        layout.addWidget(self.pregunta_input)

        # Opciones (cambia según el tipo)
        self.opciones_group = QGroupBox("Opciones")
        self.opciones_layout = QVBoxLayout()

        # Instrucciones según tipo
        self.instrucciones_label = QLabel()
        self.instrucciones_label.setWordWrap(True)
        self.instrucciones_label.setStyleSheet(
            """
            QLabel {
                background-color: #e8f4fd;
                color: #1976d2;
                padding: 10px;
                border-radius: 4px;
                font-size: 12px;
                margin-bottom: 10px;
            }
        """
        )
        self.opciones_layout.addWidget(self.instrucciones_label)

        # Toolbar para opciones
        opciones_toolbar = QHBoxLayout()

        self.add_opcion_btn = QPushButton("➕ Agregar Opción")
        self.add_opcion_btn.clicked.connect(self.agregar_opcion)
        opciones_toolbar.addWidget(self.add_opcion_btn)

        self.remove_opcion_btn = QPushButton("🗑️ Eliminar Seleccionada")
        self.remove_opcion_btn.clicked.connect(self.eliminar_opcion)
        opciones_toolbar.addWidget(self.remove_opcion_btn)

        opciones_toolbar.addStretch()
        self.opciones_layout.addLayout(opciones_toolbar)

        # Lista de opciones
        self.opciones_list = QListWidget()
        self.opciones_list.setMaximumHeight(200)
        self.opciones_layout.addWidget(self.opciones_list)

        self.opciones_group.setLayout(self.opciones_layout)
        layout.addWidget(self.opciones_group)

        # Orden y estado
        bottom_layout = QHBoxLayout()

        # Orden
        orden_layout = QHBoxLayout()
        orden_layout.addWidget(QLabel("Orden:"))
        self.orden_input = QSpinBox()
        self.orden_input.setMinimum(1)
        self.orden_input.setMaximum(100)
        self.orden_input.setValue(1)
        self.orden_input.setFixedWidth(80)
        orden_layout.addWidget(self.orden_input)
        bottom_layout.addLayout(orden_layout)

        bottom_layout.addStretch()

        # Estado
        estado_layout = QHBoxLayout()
        estado_layout.addWidget(QLabel("Estado:"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        self.estado_combo.setFixedWidth(100)
        estado_layout.addWidget(self.estado_combo)
        bottom_layout.addLayout(estado_layout)

        layout.addLayout(bottom_layout)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 30px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        buttons.button(QDialogButtonBox.Cancel).setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 30px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.cambiar_tipo(self.tipo_combo.currentText())

    def cambiar_tipo(self, tipo):
        """Cambiar la interfaz según el tipo de ejercicio"""
        # Actualizar instrucciones
        if tipo == "arrastrar_soltar":
            self.instrucciones_label.setText(
                "📌 Para preguntas de arrastrar y soltar:\n"
                "• Agrega pares de (Término → Definición)\n"
                "• Cada término debe tener su definición correspondiente\n"
                "• El usuario deberá arrastrar cada término hasta su definición"
            )
            self.add_opcion_btn.setEnabled(True)
            self.remove_opcion_btn.setEnabled(True)
            self.opciones_list.clear()

        elif tipo == "verdadero_falso":
            self.instrucciones_label.setText(
                "📌 Para preguntas de Verdadero/Falso:\n"
                "• Se generarán automáticamente las opciones 'Verdadero' y 'Falso'\n"
                "• Marca cuál es la respuesta correcta"
            )
            self.add_opcion_btn.setEnabled(False)
            self.remove_opcion_btn.setEnabled(False)
            self.opciones_list.clear()

            # Agregar opciones por defecto
            item1 = QListWidgetItem("✓ Verdadero")
            item1.setData(
                Qt.UserRole, {"texto": "Verdadero", "es_correcta": True, "orden": 1}
            )
            item1.setForeground(QColor("#27ae60"))
            self.opciones_list.addItem(item1)

            item2 = QListWidgetItem("✗ Falso")
            item2.setData(
                Qt.UserRole, {"texto": "Falso", "es_correcta": False, "orden": 2}
            )
            item2.setForeground(QColor("#e74c3c"))
            self.opciones_list.addItem(item2)

        else:  # seleccion_multiple
            self.instrucciones_label.setText(
                "📌 Para preguntas de selección múltiple:\n"
                "• Agrega todas las opciones posibles\n"
                "• Marca cuál(es) es la respuesta correcta usando el checkbox"
            )
            self.add_opcion_btn.setEnabled(True)
            self.remove_opcion_btn.setEnabled(True)

    def agregar_opcion(self):
        """Agregar una nueva opción"""
        dialog = OpcionDialog(self.tipo_combo.currentText(), self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            if self.tipo_combo.currentText() == "arrastrar_soltar":
                # Para arrastrar y soltar, mostrar como par
                item_text = f"📌 {data['texto']}  →  📚 {data['pareja']}"
                item = QListWidgetItem(item_text)
                item.setForeground(QColor("#e67e22"))

                # Guardar datos
                item.setData(
                    Qt.UserRole,
                    {
                        "texto": data["texto"],
                        "pareja": data["pareja"],
                        "es_correcta": True,
                        "orden": self.opciones_list.count() + 1,
                    },
                )

            elif self.tipo_combo.currentText() == "seleccion_multiple":
                item_text = data["texto"]
                item = QListWidgetItem(item_text)

                if data.get("es_correcta"):
                    item.setForeground(QColor("#27ae60"))
                    item.setIcon(
                        self.style().standardIcon(self.style().SP_DialogApplyButton)
                    )

                item.setData(
                    Qt.UserRole,
                    {
                        "texto": data["texto"],
                        "es_correcta": data["es_correcta"],
                        "orden": self.opciones_list.count() + 1,
                    },
                )

            self.opciones_list.addItem(item)

    def eliminar_opcion(self):
        """Eliminar opción seleccionada"""
        current_row = self.opciones_list.currentRow()
        if current_row >= 0:
            self.opciones_list.takeItem(current_row)

    def load_exercise_data(self):
        """Cargar datos del ejercicio"""
        self.pregunta_input.setPlainText(self.exercise_data.get("pregunta", ""))
        self.orden_input.setValue(self.exercise_data.get("orden", 1))

        tipo = self.exercise_data.get("tipo", "seleccion_multiple")
        index = self.tipo_combo.findText(tipo)
        if index >= 0:
            self.tipo_combo.setCurrentIndex(index)

        # Cargar opciones
        opciones = self.exercise_data.get("opciones", [])
        self.opciones_list.clear()

        for opcion in opciones:
            if tipo == "arrastrar_soltar":
                item_text = (
                    f"📌 {opcion['texto']}  →  📚 {opcion.get('pareja_arrastre', '')}"
                )
                item = QListWidgetItem(item_text)
                item.setForeground(QColor("#e67e22"))
                item.setData(
                    Qt.UserRole,
                    {
                        "id": opcion.get("id"),
                        "texto": opcion["texto"],
                        "pareja": opcion.get("pareja_arrastre"),
                        "es_correcta": True,
                        "orden": opcion.get("orden", 1),
                    },
                )

            elif tipo == "verdadero_falso":
                item_text = "✓ Verdadero" if opcion.get("es_correcta") else "✗ Falso"
                item = QListWidgetItem(item_text)
                if opcion.get("es_correcta"):
                    item.setForeground(QColor("#27ae60"))
                else:
                    item.setForeground(QColor("#e74c3c"))
                item.setData(
                    Qt.UserRole,
                    {
                        "id": opcion.get("id"),
                        "texto": opcion["texto"],
                        "es_correcta": opcion.get("es_correcta", False),
                        "orden": opcion.get("orden", 1),
                    },
                )

            else:  # seleccion_multiple
                item_text = opcion["texto"]
                item = QListWidgetItem(item_text)
                if opcion.get("es_correcta"):
                    item.setForeground(QColor("#27ae60"))
                    item.setIcon(
                        self.style().standardIcon(self.style().SP_DialogApplyButton)
                    )
                item.setData(
                    Qt.UserRole,
                    {
                        "id": opcion.get("id"),
                        "texto": opcion["texto"],
                        "es_correcta": opcion.get("es_correcta", False),
                        "orden": opcion.get("orden", 1),
                    },
                )

            self.opciones_list.addItem(item)

        index = self.estado_combo.findText(self.exercise_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

    def get_data(self):
        """Obtener datos del formulario"""
        opciones = []
        for i in range(self.opciones_list.count()):
            item = self.opciones_list.item(i)
            data = item.data(Qt.UserRole)
            if data:
                data["orden"] = i + 1

                # Adaptar según tipo
                if self.tipo_combo.currentText() == "arrastrar_soltar":
                    opciones.append(
                        {
                            "texto": data["texto"],
                            "pareja_arrastre": data.get("pareja", ""),
                            "es_correcta": True,
                            "orden": i + 1,
                        }
                    )
                else:
                    opciones.append(
                        {
                            "texto": data["texto"],
                            "es_correcta": data.get("es_correcta", False),
                            "orden": i + 1,
                        }
                    )

        return {
            "pregunta": self.pregunta_input.toPlainText(),
            "tipo": self.tipo_combo.currentText(),
            "orden": self.orden_input.value(),
            "estado": self.estado_combo.currentText(),
            "opciones": opciones,
        }


# ... (el resto de la clase ExercisesView se mantiene igual) ...


class ExercisesView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.ejercicios = []
        self.modulos = []
        self.lecciones = []
        self.modulo_actual = None
        self.leccion_actual = None
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
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #ddd;
                font-weight: bold;
            }
            QComboBox, QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                min-width: 200px;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("✏️ Ejercicios")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")

        self.new_btn = QPushButton("➕ Nuevo Ejercicio")
        self.new_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """
        )
        self.new_btn.clicked.connect(self.nuevo_ejercicio)
        self.new_btn.setEnabled(False)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.new_btn)

        layout.addLayout(header_layout)

        # Selectores
        selectors_layout = QHBoxLayout()
        selectors_layout.setSpacing(20)

        # Módulo
        module_layout = QVBoxLayout()
        module_layout.addWidget(QLabel("Módulo:"))
        self.modulo_combo = QComboBox()
        self.modulo_combo.currentIndexChanged.connect(self.cambiar_modulo)
        module_layout.addWidget(self.modulo_combo)
        selectors_layout.addLayout(module_layout)

        # Lección
        lesson_layout = QVBoxLayout()
        lesson_layout.addWidget(QLabel("Lección:"))
        self.leccion_combo = QComboBox()
        self.leccion_combo.currentIndexChanged.connect(self.cambiar_leccion)
        lesson_layout.addWidget(self.leccion_combo)
        selectors_layout.addLayout(lesson_layout)

        selectors_layout.addStretch()

        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setToolTip("Actualizar")
        self.refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 40px;
                max-height: 40px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )
        self.refresh_btn.clicked.connect(self.load_modulos)
        selectors_layout.addWidget(self.refresh_btn)

        layout.addLayout(selectors_layout)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Pregunta", "Tipo", "Orden", "Acciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_modulos(self):
        logger.debug("Cargando módulos...")
        result = self.api_client.get_modulos()

        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.modulos = data
            elif isinstance(data, dict) and "data" in data:
                self.modulos = data["data"]
            else:
                self.modulos = []

            self.modulo_combo.clear()
            self.modulo_combo.addItem("Seleccione un módulo", None)
            for modulo in self.modulos:
                self.modulo_combo.addItem(f"{modulo.get('titulo')}", modulo.get("id"))

            self.leccion_combo.clear()
            self.leccion_combo.addItem("Primero seleccione un módulo", None)
            self.new_btn.setEnabled(False)
        else:
            QMessageBox.warning(
                self, "Error", f"Error al cargar módulos: {result.get('error')}"
            )

    def cambiar_modulo(self, index):
        if index <= 0:
            self.modulo_actual = None
            self.leccion_combo.clear()
            self.leccion_combo.addItem("Seleccione un módulo primero", None)
            self.new_btn.setEnabled(False)
            return

        modulo_id = self.modulo_combo.currentData()
        self.modulo_actual = next(
            (m for m in self.modulos if m.get("id") == modulo_id), None
        )

        if self.modulo_actual:
            self.load_lecciones(modulo_id)

    def load_lecciones(self, modulo_id):
        logger.debug(f"Cargando lecciones del módulo {modulo_id}...")
        result = self.api_client.get_lecciones(modulo_id)

        if result["success"]:
            data = result.get("data", [])
            if isinstance(data, list):
                self.lecciones = data
            elif isinstance(data, dict) and "data" in data:
                self.lecciones = data["data"]
            else:
                self.lecciones = []

            self.leccion_combo.clear()
            self.leccion_combo.addItem("Seleccione una lección", None)
            for leccion in self.lecciones:
                self.leccion_combo.addItem(
                    f"{leccion.get('titulo')}", leccion.get("id")
                )
        else:
            QMessageBox.warning(
                self, "Error", f"Error al cargar lecciones: {result.get('error')}"
            )

    def cambiar_leccion(self, index):
        if index <= 0:
            self.leccion_actual = None
            self.new_btn.setEnabled(False)
            self.ejercicios = []
            self.actualizar_tabla([])
            return

        leccion_id = self.leccion_combo.currentData()
        self.leccion_actual = next(
            (l for l in self.lecciones if l.get("id") == leccion_id), None
        )

        if self.leccion_actual:
            self.new_btn.setEnabled(True)
            self.load_ejercicios(self.modulo_actual.get("id"), leccion_id)

    def load_ejercicios(self, modulo_id, leccion_id):
        logger.debug(f"Cargando ejercicios de la lección {leccion_id}...")
        self.table.setRowCount(0)

        result = self.api_client.get_ejercicios(modulo_id, leccion_id)

        if result["success"]:
            data = result.get("data", [])
            logger.debug(f"Ejercicios recibidos: {data}")

            if isinstance(data, list):
                self.ejercicios = data
            elif isinstance(data, dict) and "data" in data:
                self.ejercicios = data["data"]
            else:
                self.ejercicios = []

            self.actualizar_tabla(self.ejercicios)
        else:
            logger.error(f"Error: {result.get('error')}")
            QMessageBox.warning(
                self, "Error", f"Error al cargar ejercicios: {result.get('error')}"
            )
            self.ejercicios = []
            self.actualizar_tabla([])

    def actualizar_tabla(self, ejercicios):
        self.table.setRowCount(len(ejercicios))

        for row, ejercicio in enumerate(ejercicios):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(ejercicio.get("id", ""))))

            # Pregunta (resumida)
            pregunta = ejercicio.get("pregunta", "")
            if len(pregunta) > 50:
                pregunta = pregunta[:50] + "..."
            self.table.setItem(row, 1, QTableWidgetItem(pregunta))

            # Tipo
            tipo = ejercicio.get("tipo", "")
            tipo_texto = {
                "seleccion_multiple": "Múltiple",
                "verdadero_falso": "V/F",
                "arrastrar_soltar": "Arrastrar",
            }.get(tipo, tipo)

            tipo_item = QTableWidgetItem(tipo_texto)
            if tipo == "seleccion_multiple":
                tipo_item.setForeground(QColor("#3498db"))
            elif tipo == "verdadero_falso":
                tipo_item.setForeground(QColor("#27ae60"))
            elif tipo == "arrastrar_soltar":
                tipo_item.setForeground(QColor("#e67e22"))
            self.table.setItem(row, 2, tipo_item)

            # Orden
            self.table.setItem(
                row, 3, QTableWidgetItem(str(ejercicio.get("orden", "")))
            )

            # Acciones
            acciones = QWidget()
            acciones_layout = QHBoxLayout(acciones)
            acciones_layout.setContentsMargins(5, 2, 5, 2)
            acciones_layout.setSpacing(5)

            # Botón editar
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
            edit_btn.clicked.connect(
                lambda checked, e=ejercicio: self.editar_ejercicio(e)
            )

            # Botón eliminar
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
                lambda checked, e=ejercicio: self.eliminar_ejercicio(e)
            )

            acciones_layout.addWidget(edit_btn)
            acciones_layout.addWidget(delete_btn)
            acciones_layout.addStretch()

            self.table.setCellWidget(row, 4, acciones)

    def nuevo_ejercicio(self):
        if not self.modulo_actual or not self.leccion_actual:
            QMessageBox.warning(self, "Error", "Selecciona un módulo y una lección")
            return

        dialog = ExerciseDialog(
            self.api_client, self.modulo_actual.get("id"), self.leccion_actual.get("id")
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            result = self.api_client.create_ejercicio(
                self.modulo_actual.get("id"), self.leccion_actual.get("id"), data
            )

            if result["success"]:
                QMessageBox.information(self, "Éxito", "Ejercicio creado correctamente")
                self.load_ejercicios(
                    self.modulo_actual.get("id"), self.leccion_actual.get("id")
                )
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def editar_ejercicio(self, ejercicio):
        if not self.modulo_actual or not self.leccion_actual:
            return

        dialog = ExerciseDialog(
            self.api_client,
            self.modulo_actual.get("id"),
            self.leccion_actual.get("id"),
            ejercicio,
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            result = self.api_client.update_ejercicio(
                self.modulo_actual.get("id"),
                self.leccion_actual.get("id"),
                ejercicio["id"],
                data,
            )

            if result["success"]:
                QMessageBox.information(self, "Éxito", "Ejercicio actualizado")
                self.load_ejercicios(
                    self.modulo_actual.get("id"), self.leccion_actual.get("id")
                )
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_ejercicio(self, ejercicio):
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar este ejercicio?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.api_client.delete_ejercicio(
                self.modulo_actual.get("id"),
                self.leccion_actual.get("id"),
                ejercicio["id"],
            )

            if result["success"]:
                self.load_ejercicios(
                    self.modulo_actual.get("id"), self.leccion_actual.get("id")
                )
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")
