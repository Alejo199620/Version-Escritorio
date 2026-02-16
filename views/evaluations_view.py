from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
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
    QDoubleSpinBox,
    QCheckBox,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from utils.paths import resource_path


class EvaluationConfigDialog(QDialog):
    """Diálogo para configurar los parámetros generales de una evaluación"""

    def __init__(self, api_client, modulo_id, config_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_id = modulo_id
        self.config_data = config_data
        self.setWindowTitle("Configuración de Evaluación")
        self.setMinimumSize(500, 550)
        self.setup_ui()

        if config_data:
            self.load_config_data()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
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
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("⚙️ Configuración de Evaluación")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Título
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Ej: Evaluación Final de HTML")
        form_layout.addRow("Título:", self.titulo_input)

        # Descripción
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setPlaceholderText("Descripción de la evaluación...")
        self.descripcion_input.setMaximumHeight(80)
        form_layout.addRow("Descripción:", self.descripcion_input)

        # Número de preguntas
        self.num_preguntas_input = QSpinBox()
        self.num_preguntas_input.setMinimum(1)
        self.num_preguntas_input.setMaximum(50)
        self.num_preguntas_input.setValue(10)
        form_layout.addRow("N° Preguntas:", self.num_preguntas_input)

        # Tiempo límite
        tiempo_layout = QHBoxLayout()
        self.tiempo_input = QSpinBox()
        self.tiempo_input.setMinimum(5)
        self.tiempo_input.setMaximum(180)
        self.tiempo_input.setValue(30)
        tiempo_layout.addWidget(self.tiempo_input)
        tiempo_layout.addWidget(QLabel("minutos"))
        tiempo_layout.addStretch()
        form_layout.addRow("Tiempo límite:", tiempo_layout)

        # Puntaje mínimo
        puntaje_layout = QHBoxLayout()
        self.puntaje_input = QDoubleSpinBox()
        self.puntaje_input.setMinimum(0)
        self.puntaje_input.setMaximum(100)
        self.puntaje_input.setValue(70)
        self.puntaje_input.setSuffix("%")
        puntaje_layout.addWidget(self.puntaje_input)
        puntaje_layout.addStretch()
        form_layout.addRow("Puntaje mínimo:", puntaje_layout)

        # Máximo de intentos
        self.intentos_input = QSpinBox()
        self.intentos_input.setMinimum(1)
        self.intentos_input.setMaximum(10)
        self.intentos_input.setValue(3)
        form_layout.addRow("Máx. intentos:", self.intentos_input)

        # Estado
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        form_layout.addRow("Estado:", self.estado_combo)

        layout.addLayout(form_layout)

        # Resumen
        summary_group = QGroupBox("📊 Resumen")
        summary_layout = QVBoxLayout(summary_group)

        self.summary_label = QLabel("Completa los campos para ver el resumen")
        self.summary_label.setStyleSheet("color: #7f8c8d; padding: 10px;")
        self.summary_label.setWordWrap(True)
        summary_layout.addWidget(self.summary_label)

        layout.addWidget(summary_group)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar Configuración")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        for btn in [
            buttons.button(QDialogButtonBox.Ok),
            buttons.button(QDialogButtonBox.Cancel),
        ]:
            btn.setStyleSheet(
                """
                QPushButton {
                    padding: 12px 30px;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 14px;
                    min-width: 150px;
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

        # Conectar señales para actualizar resumen
        self.tiempo_input.valueChanged.connect(self.actualizar_resumen)
        self.puntaje_input.valueChanged.connect(self.actualizar_resumen)
        self.intentos_input.valueChanged.connect(self.actualizar_resumen)
        self.num_preguntas_input.valueChanged.connect(self.actualizar_resumen)

        self.actualizar_resumen()

    def actualizar_resumen(self):
        """Actualizar el resumen de la configuración"""
        tiempo = self.tiempo_input.value()
        puntaje = self.puntaje_input.value()
        intentos = self.intentos_input.value()
        preguntas = self.num_preguntas_input.value()

        self.summary_label.setText(
            f"📝 Configuración:\n\n"
            f"• {preguntas} preguntas\n"
            f"• {tiempo} minutos de duración\n"
            f"• {puntaje}% mínimo para aprobar\n"
            f"• {intentos} intentos máximos"
        )

    def load_config_data(self):
        """Cargar datos de configuración existente"""
        self.titulo_input.setText(self.config_data.get("titulo", ""))
        self.descripcion_input.setPlainText(self.config_data.get("descripcion", ""))
        self.num_preguntas_input.setValue(self.config_data.get("numero_preguntas", 10))
        self.tiempo_input.setValue(self.config_data.get("tiempo_limite", 30))
        self.puntaje_input.setValue(float(self.config_data.get("puntaje_minimo", 70)))
        self.intentos_input.setValue(self.config_data.get("max_intentos", 3))

        index = self.estado_combo.findText(self.config_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

        self.actualizar_resumen()

    def get_data(self):
        """Obtener datos del formulario"""
        return {
            "titulo": self.titulo_input.text(),
            "descripcion": self.descripcion_input.toPlainText(),
            "numero_preguntas": self.num_preguntas_input.value(),
            "tiempo_limite": self.tiempo_input.value(),
            "puntaje_minimo": self.puntaje_input.value(),
            "max_intentos": self.intentos_input.value(),
            "estado": self.estado_combo.currentText(),
        }


class OpcionEvaluacionDialog(QDialog):
    """Diálogo mejorado para agregar opciones según el tipo de pregunta - MISMO ESTILO QUE EJERCICIOS"""

    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.setWindowTitle("Agregar Opción")

        # Tamaño según tipo
        if tipo == "arrastrar_soltar":
            self.setFixedSize(450, 320)
            self.setWindowTitle("➕ Agregar Par (Término → Definición)")
        elif tipo == "seleccion_multiple":
            self.setFixedSize(400, 220)
        else:
            self.setFixedSize(400, 150)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        if self.tipo == "arrastrar_soltar":
            # Instrucciones
            instrucciones = QLabel(
                "📌 **CREAR PAR PARA ARRASTRAR Y SOLTAR**\n"
                "El usuario deberá relacionar el término con su definición."
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
            termino_label = QLabel("📝 **TÉRMINO / CONCEPTO:**")
            termino_label.setStyleSheet(
                "font-weight: bold; color: #e67e22; font-size: 12px;"
            )
            layout.addWidget(termino_label)

            self.texto_input = QLineEdit()
            self.texto_input.setPlaceholderText("Ej: HTML, CSS, JavaScript...")
            self.texto_input.setStyleSheet("border: 2px solid #e67e22;")
            layout.addWidget(self.texto_input)

            layout.addSpacing(10)

            # Definición
            definicion_label = QLabel("📚 **DEFINICIÓN / DESCRIPCIÓN:**")
            definicion_label.setStyleSheet(
                "font-weight: bold; color: #3498db; font-size: 12px;"
            )
            layout.addWidget(definicion_label)

            self.pareja_input = QLineEdit()
            self.pareja_input.setPlaceholderText("Ej: HyperText Markup Language...")
            self.pareja_input.setStyleSheet("border: 2px solid #3498db;")
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

            ejemplo_flecha = QLabel("  →  ")
            ejemplo_flecha.setStyleSheet(
                "font-size: 16px; font-weight: bold; color: #2c3e50;"
            )
            ejemplo_layout.addWidget(ejemplo_flecha)

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
            # Instrucciones
            instrucciones = QLabel("📝 Agrega una opción para la pregunta")
            instrucciones.setStyleSheet(
                "color: #2c3e50; font-style: italic; margin-bottom: 5px;"
            )
            layout.addWidget(instrucciones)

            # Texto de la opción
            layout.addWidget(QLabel("Texto de la opción:"))
            self.texto_input = QLineEdit()
            self.texto_input.setPlaceholderText("Escribe la opción...")
            layout.addWidget(self.texto_input)

            # ¿Es correcta?
            self.correcta_check = QCheckBox("✓ Esta es la respuesta correcta")
            self.correcta_check.setStyleSheet(
                "color: #27ae60; font-weight: bold; margin-top: 10px;"
            )
            layout.addWidget(self.correcta_check)

        elif self.tipo == "verdadero_falso":
            # Para V/F, no se usa este diálogo, pero por si acaso
            layout.addWidget(QLabel("Esta opción no aplica para Verdadero/Falso"))
            self.texto_input = QLineEdit()
            self.texto_input.hide()

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        """Obtener los datos ingresados"""
        data = {
            "texto": self.texto_input.text() if hasattr(self, "texto_input") else ""
        }

        if self.tipo == "arrastrar_soltar":
            data["pareja"] = self.pareja_input.text()
            data["es_correcta"] = True  # En arrastrar, todos los pares son correctos
        elif self.tipo == "seleccion_multiple":
            data["es_correcta"] = (
                self.correcta_check.isChecked()
                if hasattr(self, "correcta_check")
                else False
            )
        else:
            data["es_correcta"] = False

        return data


class QuestionDialog(QDialog):
    """Diálogo para crear/editar preguntas - MISMO ESTILO QUE EJERCICIOS"""

    def __init__(self, api_client, evaluacion_id, question_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.evaluacion_id = evaluacion_id
        self.question_data = question_data
        self.opciones = []
        self.setWindowTitle("Editar Pregunta" if question_data else "Nueva Pregunta")
        self.setMinimumSize(650, 600)
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

        # Título
        title = QLabel(
            "❓ " + ("Editar Pregunta" if self.question_data else "Nueva Pregunta")
        )
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        layout.addWidget(title)

        # Tipo y puntos
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

        # Pregunta
        pregunta_label = QLabel("Pregunta:")
        pregunta_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        layout.addWidget(pregunta_label)

        self.pregunta_input = QTextEdit()
        self.pregunta_input.setPlaceholderText("Escribe la pregunta...")
        self.pregunta_input.setMaximumHeight(80)
        layout.addWidget(self.pregunta_input)

        # Opciones
        self.opciones_group = QGroupBox("Opciones de Respuesta")
        opciones_layout = QVBoxLayout()

        # Instrucciones según tipo (se actualizará dinámicamente)
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
        opciones_layout.addWidget(self.instrucciones_label)

        # Toolbar de opciones
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

        # Lista de opciones
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

        # Botones
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
        """Cambiar interfaz según tipo de pregunta - MISMO ESTILO QUE EJERCICIOS"""
        # Actualizar instrucciones
        if tipo == "arrastrar_soltar":
            self.instrucciones_label.setText(
                "📌 **ARRASTRAR Y SOLTAR:**\n"
                "• Agrega pares de (Término → Definición)\n"
                "• Cada término debe tener su definición correspondiente\n"
                "• El usuario deberá relacionar cada término con su definición"
            )
            self.add_opcion_btn.setEnabled(True)
            self.remove_opcion_btn.setEnabled(True)
            self.opciones_list.clear()

        elif tipo == "verdadero_falso":
            self.instrucciones_label.setText(
                "📌 **VERDADERO / FALSO:**\n"
                "• Las opciones se generan automáticamente\n"
                "• Selecciona cuál es la respuesta correcta"
            )
            self.add_opcion_btn.setEnabled(False)
            self.remove_opcion_btn.setEnabled(False)
            self.opciones_list.clear()

            # Agregar opciones por defecto
            item1 = QListWidgetItem("✓ **Verdadero**")
            item1.setData(
                Qt.UserRole, {"texto": "Verdadero", "es_correcta": True, "orden": 1}
            )
            item1.setForeground(QColor("#27ae60"))
            item1.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.opciones_list.addItem(item1)

            item2 = QListWidgetItem("✗ **Falso**")
            item2.setData(
                Qt.UserRole, {"texto": "Falso", "es_correcta": False, "orden": 2}
            )
            item2.setForeground(QColor("#e74c3c"))
            item2.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.opciones_list.addItem(item2)

        else:  # seleccion_multiple
            self.instrucciones_label.setText(
                "📌 **SELECCIÓN MÚLTIPLE:**\n"
                "• Agrega todas las opciones posibles\n"
                "• Marca cuál(es) es la respuesta correcta usando el checkbox"
            )
            self.add_opcion_btn.setEnabled(True)
            self.remove_opcion_btn.setEnabled(True)

    def agregar_opcion(self):
        """Agregar nueva opción - MISMO ESTILO QUE EJERCICIOS"""
        dialog = OpcionEvaluacionDialog(self.tipo_combo.currentText(), self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            if self.tipo_combo.currentText() == "arrastrar_soltar":
                # Para arrastrar y soltar, mostrar como par con formato especial
                item_text = f"📌 **{data['texto']}**  →  📚 **{data['pareja']}**"
                item = QListWidgetItem(item_text)
                item.setForeground(QColor("#e67e22"))
                item.setFont(QFont("Segoe UI", 10, QFont.Bold))

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
                    item.setText(f"✓ {item_text}")

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

    def load_question_data(self):
        """Cargar datos de pregunta existente"""
        self.pregunta_input.setPlainText(self.question_data.get("pregunta", ""))
        self.puntos_input.setValue(float(self.question_data.get("puntos", 10)))

        tipo = self.question_data.get("tipo", "seleccion_multiple")
        index = self.tipo_combo.findText(tipo)
        if index >= 0:
            self.tipo_combo.setCurrentIndex(index)

        # Cargar opciones
        opciones = self.question_data.get("opciones", [])
        self.opciones_list.clear()

        for opcion in opciones:
            if tipo == "arrastrar_soltar":
                item_text = f"📌 **{opcion['texto']}**  →  📚 **{opcion.get('pareja_arrastre', '')}**"
                item = QListWidgetItem(item_text)
                item.setForeground(QColor("#e67e22"))
                item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                item.setData(
                    Qt.UserRole,
                    {
                        "texto": opcion["texto"],
                        "pareja": opcion.get("pareja_arrastre"),
                        "es_correcta": True,
                        "orden": opcion.get("orden", 1),
                    },
                )

            elif tipo == "verdadero_falso":
                item_text = (
                    "✓ **Verdadero**" if opcion.get("es_correcta") else "✗ **Falso**"
                )
                item = QListWidgetItem(item_text)
                if opcion.get("es_correcta"):
                    item.setForeground(QColor("#27ae60"))
                else:
                    item.setForeground(QColor("#e74c3c"))
                item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                item.setData(
                    Qt.UserRole,
                    {
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
                    item.setText(f"✓ {item_text}")
                item.setData(
                    Qt.UserRole,
                    {
                        "texto": opcion["texto"],
                        "es_correcta": opcion.get("es_correcta", False),
                        "orden": opcion.get("orden", 1),
                    },
                )

            self.opciones_list.addItem(item)

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
            "puntos": self.puntos_input.value(),
            "opciones": opciones,
        }


class EvaluationsView(QWidget):
    """Vista principal de evaluaciones"""

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.modulos = []
        self.modulo_actual = None
        self.evaluacion_actual = None
        self.preguntas = []
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
            QFrame {
                background-color: white;
                border-radius: 5px;
                border: 1px solid #ddd;
                padding: 15px;
            }
            QLabel#configLabel {
                font-size: 14px;
                color: #2c3e50;
                padding: 5px;
            }
        """
        )

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("📝 Evaluaciones")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")

        header_layout.addWidget(title)
        header_layout.addStretch()

        # Selector de módulo
        module_selector = QHBoxLayout()
        module_selector.addWidget(QLabel("Módulo:"))

        self.modulo_combo = QComboBox()
        self.modulo_combo.currentIndexChanged.connect(self.cambiar_modulo)
        self.modulo_combo.setMinimumWidth(250)
        module_selector.addWidget(self.modulo_combo)

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
        module_selector.addWidget(self.refresh_btn)

        header_layout.addLayout(module_selector)

        main_layout.addLayout(header_layout)

        # Splitter para dividir configuración y preguntas
        splitter = QSplitter(Qt.Vertical)

        # Panel de configuración
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        # Config header
        config_header = QHBoxLayout()
        config_header.addWidget(QLabel("⚙️ Configuración"))
        config_header.addStretch()

        self.config_btn = QPushButton("⚙️ Configurar Evaluación")
        self.config_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        self.config_btn.clicked.connect(self.configurar_evaluacion)
        config_header.addWidget(self.config_btn)

        config_layout.addLayout(config_header)

        # Info de configuración
        self.config_frame = QFrame()
        self.config_frame_layout = QVBoxLayout(self.config_frame)

        self.config_info = QLabel("No hay configuración de evaluación para este módulo")
        self.config_info.setObjectName("configLabel")
        self.config_info.setAlignment(Qt.AlignCenter)
        self.config_info.setStyleSheet("color: #7f8c8d; padding: 20px;")
        self.config_frame_layout.addWidget(self.config_info)

        config_layout.addWidget(self.config_frame)

        splitter.addWidget(config_widget)

        # Panel de preguntas
        questions_widget = QWidget()
        questions_layout = QVBoxLayout(questions_widget)
        questions_layout.setContentsMargins(0, 0, 0, 0)

        # Questions header
        questions_header = QHBoxLayout()
        questions_header.addWidget(QLabel("❓ Preguntas"))
        questions_header.addStretch()

        self.new_question_btn = QPushButton("➕ Nueva Pregunta")
        self.new_question_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """
        )
        self.new_question_btn.clicked.connect(self.nueva_pregunta)
        self.new_question_btn.setEnabled(False)
        questions_header.addWidget(self.new_question_btn)

        questions_layout.addLayout(questions_header)

        # Tabla de preguntas
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Pregunta", "Tipo", "Puntos", "Acciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        questions_layout.addWidget(self.table)

        splitter.addWidget(questions_widget)

        # Set initial sizes (30% config, 70% questions)
        splitter.setSizes([200, 500])

        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    def load_modulos(self):
        """Cargar lista de módulos"""
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

            self.mostrar_sin_evaluacion()
            self.new_question_btn.setEnabled(False)
        else:
            QMessageBox.warning(
                self, "Error", f"Error al cargar módulos: {result.get('error')}"
            )

    def cambiar_modulo(self, index):
        """Cambiar módulo seleccionado"""
        if index <= 0:
            self.modulo_actual = None
            self.mostrar_sin_evaluacion()
            self.new_question_btn.setEnabled(False)
            return

        modulo_id = self.modulo_combo.currentData()
        self.modulo_actual = next(
            (m for m in self.modulos if m.get("id") == modulo_id), None
        )

        if self.modulo_actual:
            self.load_evaluacion(modulo_id)

    def load_evaluacion(self, modulo_id):
        """Cargar evaluación del módulo"""
        logger.debug(f"Cargando evaluación del módulo {modulo_id}...")
        result = self.api_client.get_evaluacion(modulo_id)

        if result["success"]:
            data = result.get("data", {})
            if isinstance(data, dict) and data:
                self.evaluacion_actual = data
                self.mostrar_configuracion(data)
                self.load_preguntas(modulo_id, data.get("id"))
                self.new_question_btn.setEnabled(True)
            else:
                self.evaluacion_actual = None
                self.mostrar_sin_evaluacion()
                self.new_question_btn.setEnabled(False)
                self.preguntas = []
                self.actualizar_tabla([])
        else:
            logger.error(f"Error: {result.get('error')}")
            self.evaluacion_actual = None
            self.mostrar_sin_evaluacion()
            self.new_question_btn.setEnabled(False)

    def load_preguntas(self, modulo_id, evaluacion_id):
        """Cargar preguntas de la evaluación"""
        logger.debug(f"Cargando preguntas de evaluación {evaluacion_id}...")

        # Usar los datos de la evaluación
        if self.evaluacion_actual and "preguntas" in self.evaluacion_actual:
            self.preguntas = self.evaluacion_actual["preguntas"]
        else:
            self.preguntas = []

        self.actualizar_tabla(self.preguntas)

    def mostrar_configuracion(self, config):
        """Mostrar configuración en el panel"""
        # Limpiar frame
        self.clear_layout(self.config_frame_layout)

        # Crear grid de información
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(10)
        grid_layout.setHorizontalSpacing(20)

        row = 0
        grid_layout.addWidget(QLabel("📌 Título:"), row, 0)
        titulo_label = QLabel(config.get("titulo", "N/A"))
        titulo_label.setStyleSheet("font-weight: bold;")
        titulo_label.setWordWrap(True)
        grid_layout.addWidget(titulo_label, row, 1)

        row += 1
        grid_layout.addWidget(QLabel("📝 Descripción:"), row, 0)
        desc_label = QLabel(config.get("descripcion", "N/A"))
        desc_label.setWordWrap(True)
        grid_layout.addWidget(desc_label, row, 1)

        row += 1
        grid_layout.addWidget(QLabel("🔢 Preguntas:"), row, 0)
        grid_layout.addWidget(QLabel(str(config.get("numero_preguntas", 0))), row, 1)

        row += 1
        grid_layout.addWidget(QLabel("⏱️ Tiempo:"), row, 0)
        grid_layout.addWidget(
            QLabel(f"{config.get('tiempo_limite', 0)} minutos"), row, 1
        )

        row += 1
        grid_layout.addWidget(QLabel("🎯 Puntaje mínimo:"), row, 0)
        grid_layout.addWidget(QLabel(f"{config.get('puntaje_minimo', 0)}%"), row, 1)

        row += 1
        grid_layout.addWidget(QLabel("🔄 Intentos máximos:"), row, 0)
        grid_layout.addWidget(QLabel(str(config.get("max_intentos", 0))), row, 1)

        row += 1
        grid_layout.addWidget(QLabel("📊 Estado:"), row, 0)
        estado_label = QLabel(config.get("estado", "inactivo"))
        if config.get("estado") == "activo":
            estado_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            estado_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        grid_layout.addWidget(estado_label, row, 1)

        grid_layout.setColumnStretch(1, 1)
        self.config_frame_layout.addLayout(grid_layout)
        self.config_frame_layout.addStretch()

    def mostrar_sin_evaluacion(self):
        """Mostrar mensaje de sin configuración"""
        self.clear_layout(self.config_frame_layout)
        self.config_info = QLabel("No hay configuración de evaluación para este módulo")
        self.config_info.setObjectName("configLabel")
        self.config_info.setAlignment(Qt.AlignCenter)
        self.config_info.setStyleSheet("color: #7f8c8d; padding: 20px;")
        self.config_frame_layout.addWidget(self.config_info)
        self.config_frame_layout.addStretch()

    def actualizar_tabla(self, preguntas):
        """Actualizar tabla de preguntas"""
        self.table.setRowCount(len(preguntas))

        for row, pregunta in enumerate(preguntas):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(pregunta.get("id", ""))))

            # Pregunta (resumida)
            texto = pregunta.get("pregunta", "")
            if len(texto) > 50:
                texto = texto[:50] + "..."
            self.table.setItem(row, 1, QTableWidgetItem(texto))

            # Tipo
            tipo = pregunta.get("tipo", "")
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

            # Puntos
            self.table.setItem(
                row, 3, QTableWidgetItem(str(pregunta.get("puntos", "")))
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
                lambda checked, p=pregunta: self.editar_pregunta(p)
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
                lambda checked, p=pregunta: self.eliminar_pregunta(p)
            )

            acciones_layout.addWidget(edit_btn)
            acciones_layout.addWidget(delete_btn)
            acciones_layout.addStretch()

            self.table.setCellWidget(row, 4, acciones)

    def configurar_evaluacion(self):
        """Abrir diálogo de configuración de evaluación"""
        if not self.modulo_actual:
            QMessageBox.warning(self, "Error", "Selecciona un módulo primero")
            return

        dialog = EvaluationConfigDialog(
            self.api_client, self.modulo_actual.get("id"), self.evaluacion_actual, self
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            result = self.api_client.update_evaluacion_config(
                self.modulo_actual.get("id"), data
            )

            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Configuración guardada correctamente"
                )
                self.load_evaluacion(self.modulo_actual.get("id"))
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def nueva_pregunta(self):
        """Crear nueva pregunta"""
        if not self.modulo_actual or not self.evaluacion_actual:
            QMessageBox.warning(self, "Error", "Primero configura la evaluación")
            return

        dialog = QuestionDialog(
            self.api_client, self.evaluacion_actual.get("id"), parent=self
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            result = self.api_client.create_pregunta(
                self.modulo_actual.get("id"), self.evaluacion_actual.get("id"), data
            )

            if result["success"]:
                QMessageBox.information(self, "Éxito", "Pregunta creada correctamente")
                self.load_evaluacion(self.modulo_actual.get("id"))
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def editar_pregunta(self, pregunta):
        """Editar pregunta existente"""
        if not self.modulo_actual or not self.evaluacion_actual:
            return

        dialog = QuestionDialog(
            self.api_client, self.evaluacion_actual.get("id"), pregunta, self
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            result = self.api_client.update_pregunta(
                self.modulo_actual.get("id"),
                self.evaluacion_actual.get("id"),
                pregunta["id"],
                data,
            )

            if result["success"]:
                QMessageBox.information(self, "Éxito", "Pregunta actualizada")
                self.load_evaluacion(self.modulo_actual.get("id"))
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_pregunta(self, pregunta):
        """Eliminar pregunta"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar esta pregunta?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.api_client.delete_pregunta(
                self.modulo_actual.get("id"),
                self.evaluacion_actual.get("id"),
                pregunta["id"],
            )

            if result["success"]:
                self.load_evaluacion(self.modulo_actual.get("id"))
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def clear_layout(self, layout):
        """Limpiar un layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
