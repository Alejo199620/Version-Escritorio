from PyQt6.QtWidgets import (
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
    QAbstractItemView,
    QDoubleSpinBox,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import logging
from utils.paths import resource_path
from views.styles import StyleHelper

logger = logging.getLogger(__name__)


class OpcionDialog(QDialog):
    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.setWindowTitle("Agregar Opción")

        # Tamaño según tipo
        if tipo == "arrastrar_soltar":
            self.setMinimumSize(450, 300)
            self.resize(450, 300)
            self.setWindowTitle("Agregar Par (Término → Definición)")
        else:
            self.setMinimumSize(400, 200)
            self.resize(400, 200)

        self.setWindowFlags(
            self.windowFlags() 
            | Qt.WindowType.WindowMinimizeButtonHint 
            | Qt.WindowType.WindowMaximizeButtonHint 
            | Qt.WindowType.WindowCloseButtonHint
        )

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
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        data = {"texto": self.texto_input.text()}

        if self.tipo == "arrastrar_soltar":
            data["pareja_arrastre"] = self.pareja_input.text()
            data["es_correcta"] = 1  # 1 en lugar de True
        elif self.tipo == "seleccion_multiple":
            data["es_correcta"] = 1 if self.correcta_check.isChecked() else 0
        else:
            data["es_correcta"] = 0

        return data


class ExerciseDialog(QDialog):
    """
    Diálogo universal para crear o editar contenido interactivo (Ejercicios o Preguntas).
    Diseño unificado con StyleHelper para garantizar consistencia visual.
    """

    def __init__(
        self,
        api_client,
        modulo_id,
        content_id,
        exercise_data=None,
        is_evaluation=False,
        parent=None,
    ):
        super().__init__(parent)
        self.api_client = api_client
        self.modulo_id = modulo_id
        # content_id puede ser leccion_id o evaluacion_id
        self.content_id = content_id
        self.exercise_data = exercise_data
        self.is_evaluation = is_evaluation
        self.opciones = []
        self.puntos_input = None
        self.orden_input = None

        self.setWindowTitle(
            "Pregunta de Evaluación" if is_evaluation else "Ejercicio de Lección"
        )
        self.setMinimumSize(750, 700)
        self.setWindowFlags(
            self.windowFlags() 
            | Qt.WindowType.WindowMinimizeButtonHint 
            | Qt.WindowType.WindowMaximizeButtonHint 
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setup_ui()

        if exercise_data:
            self.load_exercise_data()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog { background-color: #f0f0f0; }
            QLabel { font-size: 14px; }
            QLineEdit, QTextEdit, QComboBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
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
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-bottom: 6px solid #4b5563;
                margin-top: 2px;
            }
            QSpinBox::down-arrow {
                image: none;
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #4b5563;
                margin-bottom: 2px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e5e7eb;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Filtros/Header
        header = QHBoxLayout()
        header.addWidget(QLabel("Tipo de pregunta:"))
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(
            ["seleccion_multiple", "verdadero_falso", "arrastrar_soltar"]
        )
        self.tipo_combo.currentTextChanged.connect(self.cambiar_tipo)
        header.addWidget(self.tipo_combo)

        if self.is_evaluation:
            # Los puntos ahora se auto-calculan equitativamente en 100/N
            pass

        else:
            header.addWidget(QLabel("Orden:"))
            self.orden_input = QSpinBox()
            self.orden_input.setRange(1, 999)
            header.addWidget(self.orden_input)

        header.addStretch()
        layout.addLayout(header)

        # Enunciado
        layout.addWidget(QLabel("Pregunta/Enunciado:"))
        self.pregunta_input = QTextEdit()
        self.pregunta_input.setPlaceholderText(
            "Escriba aquí el enunciado del ejercicio..."
        )
        self.pregunta_input.setMaximumHeight(100)
        layout.addWidget(self.pregunta_input)

        # Opciones Estándar (Multiple Choice / Drag & Drop)
        self.opciones_group = QGroupBox("Opciones / Respuestas")
        self.opciones_layout = QVBoxLayout()

        self.instrucciones_label = QLabel()
        self.instrucciones_label.setWordWrap(True)
        self.instrucciones_label.setStyleSheet("color: #666; font-style: italic;")
        self.opciones_layout.addWidget(self.instrucciones_label)

        self.edit_opciones_container = QWidget()
        btn_layout = QHBoxLayout(self.edit_opciones_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        self.add_opcion_btn = QPushButton("➕ Agregar Opción")
        self.add_opcion_btn.clicked.connect(self.agregar_opcion)
        btn_layout.addWidget(self.add_opcion_btn)

        self.remove_opcion_btn = QPushButton("🗑️ Eliminar Seleccionada")
        self.remove_opcion_btn.clicked.connect(self.eliminar_opcion)
        btn_layout.addWidget(self.remove_opcion_btn)
        btn_layout.addStretch()
        self.opciones_layout.addWidget(self.edit_opciones_container)

        self.opciones_list = QListWidget()
        self.opciones_layout.addWidget(self.opciones_list)

        self.opciones_group.setLayout(self.opciones_layout)
        layout.addWidget(self.opciones_group)

        # Opciones Verdadero / Falso (Radio Buttons)
        self.vf_group = QGroupBox("Seleccione la Respuesta Correcta")
        vf_layout = QVBoxLayout()
        vf_layout.setSpacing(15)
        vf_layout.setContentsMargins(20, 20, 20, 20)

        self.vf_radio_v = QRadioButton("✓ Verdadero")
        self.vf_radio_v.setStyleSheet("font-weight: bold; color: #059669; font-size: 16px;")
        
        self.vf_radio_f = QRadioButton("✗ Falso")
        self.vf_radio_f.setStyleSheet("font-weight: bold; color: #dc2626; font-size: 16px;")

        vf_layout.addWidget(self.vf_radio_v)
        vf_layout.addWidget(self.vf_radio_f)
        self.vf_group.setLayout(vf_layout)
        layout.addWidget(self.vf_group)

        # Footer
        footer = QHBoxLayout()
        footer.addWidget(QLabel("Estado:"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        footer.addWidget(self.estado_combo)
        footer.addStretch()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        footer.addWidget(buttons)
        layout.addLayout(footer)

        self.cambiar_tipo(self.tipo_combo.currentText())

    def cambiar_tipo(self, tipo):
        """Actualizar UI según el tipo de contenido"""
        if tipo == "arrastrar_soltar":
            self.instrucciones_label.setText(
                "Crea pares de (Término → Definición). El usuario deberá emparejarlos."
            )
            self.opciones_group.show()
            self.vf_group.hide()
            self.add_opcion_btn.setEnabled(True)
        elif tipo == "verdadero_falso":
            self.instrucciones_label.setText(
                "Indique si el enunciado anterior es Verdadero o Falso."
            )
            self.opciones_group.hide()
            self.vf_group.show()
        else:
            self.instrucciones_label.setText(
                "Añade opciones y marca la(s) correcta(s) usando el checkbox del diálogo."
            )
            self.opciones_group.show()
            self.vf_group.hide()
            self.add_opcion_btn.setEnabled(True)


    def agregar_opcion(self):
        dialog = OpcionDialog(self.tipo_combo.currentText(), self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            text = data["texto"]
            if self.tipo_combo.currentText() == "arrastrar_soltar":
                text = f"{text} → {data['pareja_arrastre']}"

            item = QListWidgetItem(text)
            if data["es_correcta"]:
                item.setText(f"✅ {text}")
                item.setForeground(QColor("#27ae60"))

            item.setData(Qt.ItemDataRole.UserRole, data)
            self.opciones_list.addItem(item)

    def eliminar_opcion(self):
        for item in self.opciones_list.selectedItems():
            self.opciones_list.takeItem(self.opciones_list.row(item))

    def load_exercise_data(self):
        data = self.exercise_data
        self.pregunta_input.setText(data.get("pregunta", ""))
        self.tipo_combo.setCurrentText(data.get("tipo", "seleccion_multiple"))
        self.estado_combo.setCurrentText(data.get("estado", "activo"))

        if self.is_evaluation:
            pass # Puntos se calculan automáticos.

        elif self.orden_input:
            self.orden_input.setValue(int(data.get("orden", 1)))

        self.opciones_list.clear()
        tipo = data.get("tipo", "")
        
        if tipo == "verdadero_falso":
            for opt in data.get("opciones", []):
                es_v = str(opt.get("texto", "")).lower() == "verdadero"
                if es_v and opt.get("es_correcta"):
                    self.vf_radio_v.setChecked(True)
                elif not es_v and opt.get("es_correcta"):
                    self.vf_radio_f.setChecked(True)
        else:
            for opt in data.get("opciones", []):
                text = opt.get("texto", "")
                if tipo == "arrastrar_soltar":
                    text = f"{text} → {opt.get('pareja_arrastre', '')}"

                item = QListWidgetItem(text)
                if opt.get("es_correcta"):
                    item.setText(f"✅ {text}")
                    item.setForeground(QColor("#27ae60"))
                item.setData(Qt.ItemDataRole.UserRole, opt)
                self.opciones_list.addItem(item)

    def get_data(self):
        opciones = []
        tipo = self.tipo_combo.currentText()
        res_correcta = None

        if tipo == "verdadero_falso":
            es_v_correcta = 1 if self.vf_radio_v.isChecked() else 0
            res_correcta = "verdadero" if self.vf_radio_v.isChecked() else "falso"
            opciones = [
                {
                    "texto": "Verdadero",
                    "es_correcta": es_v_correcta,
                    "orden": 1,
                },
                {
                    "texto": "Falso",
                    "es_correcta": 1 - es_v_correcta,
                    "orden": 2,
                },
            ]
        else:
            for i in range(self.opciones_list.count()):
                item = self.opciones_list.item(i)
                opt_data = item.data(Qt.ItemDataRole.UserRole)
                if opt_data:
                    opt_data["orden"] = i + 1
                    opciones.append(opt_data)

        data = {
            "pregunta": self.pregunta_input.toPlainText().strip(),
            "tipo": tipo,
            "estado": self.estado_combo.currentText(),
            "opciones": opciones,
        }

        if res_correcta:
            data["respuesta_correcta"] = res_correcta

        if self.is_evaluation:
            # Por defecto asignamos 1.0 para evitar el error 422 (min 0.5) 
            # El valor real será recalculado por las vistas (EvaluationsView/ModulesView)
            data["puntos"] = 1.0
        elif self.orden_input:
            data["orden"] = self.orden_input.value()

        return data


# ============================================================================
# VISTA PRINCIPAL DE EJERCICIOS
# ============================================================================


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
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")

        self.add_ejercicio_btn = QPushButton("➕ Nuevo Ejercicio")
        self.add_ejercicio_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        self.add_ejercicio_btn.clicked.connect(self.agregar_ejercicio)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_ejercicio_btn)

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
            ["ID", "Pregunta", "Tipo", "Orden", "Acciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table_layout.addWidget(self.table)

        self.stack.addWidget(table_container)
        
        # --- PÁGINA 2: PLACEHOLDER VACÍO ---
        self.empty_placeholder = self._create_empty_placeholder()
        self.stack.addWidget(self.empty_placeholder)

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

        icon = QLabel("✏️")
        icon.setFont(QFont("Segoe UI", 64))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        text = QLabel("Seleccione un módulo y lección para gestionar ejercicios")
        text.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        text.setStyleSheet("color: #64748b;")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text)

        subtext = QLabel("Use los selectores superiores para comenzar")
        subtext.setStyleSheet("color: #94a3b8; font-size: 14px;")
        subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtext)

        return frame

    def _create_empty_placeholder(self) -> QFrame:
        """Crea la vista para cuando no hay ejercicios en la lección"""
        frame = QFrame()
        frame.setStyleSheet(
            "background-color: white; border-radius: 12px; border: 1px dashed #e2e8f0;"
        )

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        icon = QLabel("📭")
        icon.setFont(QFont("Segoe UI", 64))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        text = QLabel("No se han agregado ejercicios a esta lección")
        text.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        text.setStyleSheet("color: #64748b;")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text)

        subtext = QLabel("Ve a la sección 'Lecciones', edita esta lección y agrega los ejercicios desde allí.")
        subtext.setStyleSheet("color: #94a3b8; font-size: 15px;")
        subtext.setWordWrap(True)
        subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtext)

        return frame

    def load_modulos(self):
        logger.debug("Cargando módulos...")
        # Intentar obtener de caché primero para respuesta instantánea
        result = self.api_client.get_modulos()

        if result["success"]:
            data = result.get("data", [])
            self.modulos = (
                data
                if isinstance(data, list)
                else data.get("data", []) if isinstance(data, dict) else []
            )

            current_modulo_id = self.modulo_combo.currentData()

            self.modulo_combo.setUpdatesEnabled(False)
            self.modulo_combo.blockSignals(True)
            self.modulo_combo.clear()
            self.modulo_combo.addItem("Seleccione un módulo", None)
            
            new_index = 0
            for i, modulo in enumerate(self.modulos):
                self.modulo_combo.addItem(f"{modulo.get('titulo')}", modulo.get("id"))
                if current_modulo_id == modulo.get("id"):
                    new_index = i + 1

            self.modulo_combo.setCurrentIndex(new_index)
            self.modulo_combo.blockSignals(False)
            self.modulo_combo.setUpdatesEnabled(True)

            if new_index == 0:
                self.leccion_combo.clear()
                self.leccion_combo.addItem("Primero seleccione un módulo", None)
        else:
            QMessageBox.warning(
                self, "Error", f"Error al cargar módulos: {result.get('error')}"
            )

    def cambiar_modulo(self, index):
        if index <= 0:
            self.modulo_actual = None
            self.leccion_combo.clear()
            self.leccion_combo.addItem("Seleccione un módulo primero", None)
            return

        modulo_id = self.modulo_combo.currentData()
        self.modulo_actual = next(
            (m for m in self.modulos if m.get("id") == modulo_id), None
        )

        if self.modulo_actual:
            self.load_lecciones(modulo_id)
            self.stack.setCurrentIndex(0)

    def load_lecciones(self, modulo_id):
        logger.debug(f"Cargando lecciones del módulo {modulo_id}...")
        result = self.api_client.get_lecciones(modulo_id)

        if result["success"]:
            data = result.get("data", [])
            self.lecciones = (
                data
                if isinstance(data, list)
                else data.get("data", []) if isinstance(data, dict) else []
            )

            self.leccion_combo.setUpdatesEnabled(False)
            self.leccion_combo.clear()
            self.leccion_combo.addItem("Seleccione una lección", None)
            for leccion in self.lecciones:
                self.leccion_combo.addItem(
                    f"{leccion.get('titulo')}", leccion.get("id")
                )
            self.leccion_combo.setUpdatesEnabled(True)
        else:
            QMessageBox.warning(
                self, "Error", f"Error al cargar lecciones: {result.get('error')}"
            )

    def cambiar_leccion(self, index):
        if index <= 0:
            self.leccion_actual = None
            self.ejercicios = []
            self.stack.setCurrentIndex(0)
            return

        self.stack.setCurrentIndex(1)

        leccion_id = self.leccion_combo.currentData()
        self.leccion_actual = next(
            (l for l in self.lecciones if l.get("id") == leccion_id), None
        )

        if self.modulo_actual:
            self.load_ejercicios(self.modulo_actual.get("id"), leccion_id)

    def load_ejercicios(self, modulo_id, leccion_id, force_refresh=False):
        """Cargar ejercicios de la lección"""
        logger.debug(f"Cargando ejercicios de la lección {leccion_id}...")

        result = self.api_client.get_ejercicios(
            modulo_id, leccion_id, force_refresh=force_refresh
        )

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
        if not ejercicios and self.leccion_actual:
            self.stack.setCurrentIndex(2)
            return
            
        self.stack.setCurrentIndex(1)
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(len(ejercicios))
        self.table.setStyleSheet(
            """
            QTableWidget { border: none; }
            QTableView { border: none; }
            QTableWidget::item { padding: 8px; }
        """
        )
        self.table.setColumnWidth(4, 120)
        self.table.verticalHeader().setDefaultSectionSize(54)

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
            acciones_layout.setContentsMargins(8, 0, 8, 0)
            acciones_layout.setSpacing(10)
            acciones_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

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

        self.table.setUpdatesEnabled(True)

    def agregar_ejercicio(self):
        if not self.modulo_actual or not self.leccion_actual:
            QMessageBox.warning(
                self, "Aviso", "Primero debe seleccionar un módulo y una lección."
            )
            return

        dialog = ExerciseDialog(
            self.api_client,
            self.modulo_actual.get("id"),
            self.leccion_actual.get("id"),
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            result = self.api_client.create_ejercicio(
                self.modulo_actual.get("id"),
                self.leccion_actual.get("id"),
                data,
            )

            if result["success"]:
                self.load_ejercicios(
                    self.modulo_actual.get("id"),
                    self.leccion_actual.get("id"),
                    force_refresh=True,
                )
            else:
                QMessageBox.critical(self, "Error", f"Error al crear: {result.get('error')}")

    def editar_ejercicio(self, ejercicio):
        if not self.modulo_actual or not self.leccion_actual:
            return

        dialog = ExerciseDialog(
            self.api_client,
            self.modulo_actual.get("id"),
            self.leccion_actual.get("id"),
            ejercicio,
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            result = self.api_client.update_ejercicio(
                self.modulo_actual.get("id"),
                self.leccion_actual.get("id"),
                ejercicio["id"],
                data,
            )

            if result["success"]:
                self.load_ejercicios(
                    self.modulo_actual.get("id"),
                    self.leccion_actual.get("id"),
                    force_refresh=True,
                )
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_ejercicio(self, ejercicio):
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar este ejercicio?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            result = self.api_client.delete_ejercicio(
                self.modulo_actual.get("id"),
                self.leccion_actual.get("id"),
                ejercicio["id"],
            )

            if result["success"]:
                self.load_ejercicios(
                    self.modulo_actual.get("id"),
                    self.leccion_actual.get("id"),
                    force_refresh=True,
                )
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def _on_data_changed(self, data_type: str):
        """Manejador para actualizaciones en tiempo real"""
        if data_type == "modulos":
            self.load_modulos()

        if data_type in ["ejercicios", "lecciones"]:
            if self.modulo_actual and self.leccion_actual:
                self.load_ejercicios(
                    self.modulo_actual.get("id"),
                    self.leccion_actual.get("id"),
                    force_refresh=True,
                )
            elif data_type == "lecciones" and self.modulo_actual:
                self.cambiar_modulo(self.modulo_combo.currentIndex())
