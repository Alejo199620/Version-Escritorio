from PyQt6.QtWidgets import (
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
    QAbstractItemView,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import logging

logger = logging.getLogger(__name__)

from utils.paths import resource_path
from views.styles import StyleHelper
from views.exercises_view import ExerciseDialog


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
        else:
            # Si no hay datos, establecer título por defecto
            self.titulo_input.setText(f"Evaluación del Módulo")

    def setup_ui(self):
        self.setStyleSheet(
            f"""
            QDialog {{ background-color: white; }}
            QLineEdit, QComboBox {{
                padding: 10px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 13px;
                background-color: #f8fafc;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: {StyleHelper.PRIMARY_COLOR};
                background-color: white;
            }}
            QLabel {{ font-size: 13px; color: #1e293b; }}
            QSpinBox {{
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 13px;
                background-color: white;
            }}
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #d1d5db;
                border-bottom: 1px solid #d1d5db;
                background-color: #f3f4f6;
                border-top-right-radius: 8px;
            }}
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 30px;
                border-left: 1px solid #d1d5db;
                background-color: #f3f4f6;
                border-bottom-right-radius: 8px;
            }}
            QSpinBox::up-arrow {{
                image: none;
                width: 0; height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-bottom: 6px solid #4b5563;
                margin-top: 2px;
            }}
            QSpinBox::down-arrow {{
                image: none;
                width: 0; height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #4b5563;
                margin-bottom: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: #e5e7eb;
            }}
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("⚙️ Configurar Evaluación")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #1e293b; margin-bottom: 5px;")
        layout.addWidget(title)

        # --- FORMULARIO ---
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Ej: Evaluación Final de Módulo")
        form_layout.addRow("Título de la Evaluación:", self.titulo_input)

        self.num_preguntas_input = QSpinBox()
        self.num_preguntas_input.setRange(1, 50)
        self.num_preguntas_input.setValue(10)
        form_layout.addRow("Número de Preguntas:", self.num_preguntas_input)

        self.tiempo_input = QSpinBox()
        self.tiempo_input.setRange(5, 180)
        self.tiempo_input.setValue(30)
        self.tiempo_input.setSuffix(" minutos")
        form_layout.addRow("Tiempo Límite:", self.tiempo_input)

        self.puntaje_input = QSpinBox()
        self.puntaje_input.setRange(1, 100)
        self.puntaje_input.setValue(70)
        self.puntaje_input.setSuffix("%")
        form_layout.addRow("Puntaje Mínimo:", self.puntaje_input)

        self.intentos_input = QSpinBox()
        self.intentos_input.setRange(1, 10)
        self.intentos_input.setValue(2)
        form_layout.addRow("Intentos Máximos:", self.intentos_input)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo", "borrador"])
        form_layout.addRow("Estado:", self.estado_combo)

        layout.addLayout(form_layout)

        # --- BOTONES ---
        layout.addStretch()
        buttons = QHBoxLayout()
        buttons.setSpacing(15)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setStyleSheet(
            StyleHelper.button_secondary() + 
            "QPushButton { border-radius: 8px; padding: 0 30px; background-color: #ef4444; color: white; }" +
            "QPushButton:hover { background-color: #dc2626; }"
        )
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Guardar Configuración")
        save_btn.setMinimumHeight(45)
        save_btn.setStyleSheet(StyleHelper.button_primary())
        save_btn.clicked.connect(self.accept)

        buttons.addStretch()
        buttons.addWidget(cancel_btn)
        buttons.addWidget(save_btn)
        layout.addLayout(buttons)

    def load_config_data(self):
        """Cargar datos de configuración existente"""

        def safe_int(value, default=0):
            """Convierte cualquier valor numérico (int, float o string '80.00') a int."""
            try:
                return int(float(value))
            except (ValueError, TypeError):
                return default

        self.titulo_input.setText(self.config_data.get("titulo", ""))
        self.num_preguntas_input.setValue(
            safe_int(self.config_data.get("numero_preguntas"), 10)
        )
        self.tiempo_input.setValue(safe_int(self.config_data.get("tiempo_limite"), 30))
        self.puntaje_input.setValue(
            safe_int(self.config_data.get("puntaje_minimo"), 70)
        )
        self.intentos_input.setValue(safe_int(self.config_data.get("max_intentos"), 3))

        index = self.estado_combo.findText(self.config_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

    def get_data(self):
        """Obtener datos del formulario - AHORA INCLUYE TÍTULO"""
        titulo = self.titulo_input.text().strip()
        if not titulo:
            # Si está vacío, usar título por defecto
            titulo = f"Evaluación del Módulo {self.modulo_id}"

        return {
            "titulo": titulo,  # ¡IMPORTANTE! Este campo debe enviarse
            "numero_preguntas": self.num_preguntas_input.value(),
            "tiempo_limite": self.tiempo_input.value(),
            "puntaje_minimo": self.puntaje_input.value(),
            "max_intentos": self.intentos_input.value(),
            "estado": self.estado_combo.currentText(),
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

        # Conectar señales para actualización en tiempo real
        self.api_client.data_changed.connect(self._on_data_changed)
        self.api_client.evaluaciones_changed.connect(self._on_evaluaciones_changed)

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
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
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

        # Contenedor apilado (StackedWidget) para Placeholder / Contenido Real
        self.stack = QStackedWidget()

        # --- PÁGINA 0: PLACEHOLDER PRINCIPAL ---
        self.main_placeholder = self._create_main_placeholder()
        self.stack.addWidget(self.main_placeholder)

        # --- PÁGINA 1: CONTENIDO REAL ---
        self.content_page = QWidget()
        content_layout = QVBoxLayout(self.content_page)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        # Toolbar compacta para la evaluación
        self.eval_toolbar = QFrame()
        self.eval_toolbar.setStyleSheet(
            "background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; padding: 5px;"
        )
        toolbar_layout = QHBoxLayout(self.eval_toolbar)

        self.eval_title_label = QLabel("Título de la Evaluación")
        self.eval_title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.eval_title_label.setStyleSheet("color: #1e293b; border: none;")
        toolbar_layout.addWidget(self.eval_title_label)

        self.eval_stats_label = QLabel("10 preguntas | 30 min")
        self.eval_stats_label.setStyleSheet(
            "color: #64748b; font-size: 13px; border: none;"
        )
        toolbar_layout.addWidget(self.eval_stats_label)

        toolbar_layout.addStretch()

        self.config_btn = QPushButton("⚙️ Configurar")
        self.config_btn.setMinimumHeight(38)
        self.config_btn.setStyleSheet(StyleHelper.button_secondary())
        self.config_btn.clicked.connect(self.configurar_evaluacion)
        toolbar_layout.addWidget(self.config_btn)

        self.new_question_btn = QPushButton("➕ Nueva Pregunta")
        self.new_question_btn.setMinimumHeight(38)
        self.new_question_btn.setStyleSheet(StyleHelper.button_primary())
        self.new_question_btn.clicked.connect(self.nueva_pregunta)
        toolbar_layout.addWidget(self.new_question_btn)

        content_layout.addWidget(self.eval_toolbar)

        # Placeholder interno para cuando NO hay evaluación configurada
        self.no_eval_placeholder = self._create_no_eval_placeholder()
        content_layout.addWidget(self.no_eval_placeholder)

        # Tabla de preguntas (ahora ocupa todo el espacio)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Pregunta", "Tipo", "Puntos", "Acciones"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget { border: none; }
            QTableView { border: none; }
            QTableWidget::item { padding: 8px; }
        """)
        self.table.setColumnWidth(4, 120)
        self.table.verticalHeader().setDefaultSectionSize(54)

        content_layout.addWidget(self.table)

        self.stack.addWidget(self.content_page)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def _create_main_placeholder(self) -> QFrame:
        """Crea el placeholder inicial de la vista"""
        frame = QFrame()
        frame.setStyleSheet(
            "background-color: white; border-radius: 12px; border: 1px dashed #e2e8f0;"
        )

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        icon = QLabel("📝")
        icon.setFont(QFont("Segoe UI", 64))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        text = QLabel("Panel de Gestión de Evaluaciones")
        text.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        text.setStyleSheet("color: #64748b;")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text)

        subtext = QLabel("Seleccione un módulo arriba para ver o configurar su evaluación")
        subtext.setStyleSheet("color: #94a3b8; font-size: 14px;")
        subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtext)

        return frame

    def _create_no_eval_placeholder(self) -> QFrame:
        """Crea el placeholder que se muestra cuando un módulo no tiene evaluación"""
        frame = QFrame()
        frame.setMinimumHeight(300)
        frame.setStyleSheet(
            "background-color: white; border-radius: 12px; border: 1px dashed #e2e8f0;"
        )
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        icon = QLabel("✨")
        icon.setFont(QFont("Segoe UI", 48, QFont.Weight.Bold))
        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

        msg = QLabel("Este módulo aún no tiene una evaluación configurada.")
        msg.setFont(QFont("Segoe UI", 12))
        msg.setStyleSheet("color: #64748b;")
        layout.addWidget(msg, alignment=Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("🚀 Configurar Evaluación Ahora")
        btn.setMinimumSize(250, 45)
        btn.setStyleSheet(StyleHelper.button_primary())
        btn.clicked.connect(self.configurar_evaluacion)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        return frame

    def load_modulos(self):
        """Cargar módulos desde la API"""
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

            self.stack.setCurrentIndex(0)
            self.new_question_btn.setEnabled(False)
        else:
            QMessageBox.warning(
                self, "Error", f"Error al cargar módulos: {result.get('error')}"
            )

    def cambiar_modulo(self, index):
        """Cambiar módulo seleccionado"""
        if index <= 0:
            self.modulo_actual = None
            self.stack.setCurrentIndex(0)
            self.new_question_btn.setEnabled(False)
            return

        self.stack.setCurrentIndex(1)

        modulo_id = self.modulo_combo.currentData()
        self.modulo_actual = next(
            (m for m in self.modulos if m.get("id") == modulo_id), None
        )

        if self.modulo_actual:
            self.load_evaluacion(modulo_id)

    def load_evaluacion(self, modulo_id, force_refresh=False):
        """Cargar evaluación del módulo"""
        logger.debug(f"Cargando evaluación del módulo {modulo_id}...")
        result = self.api_client.get_evaluacion(modulo_id, force_refresh=force_refresh)

        if result["success"]:
            data = result.get("data", {})
            if isinstance(data, dict) and data:
                self.evaluacion_actual = data
                self.mostrar_configuracion(data)
                self.load_preguntas(modulo_id, data.get("id"))
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
        """Mostrar configuración compacta en la toolbar y habilitar tabla"""
        self.eval_toolbar.show()
        self.no_eval_placeholder.hide()
        self.table.show()

        titulo = config.get("titulo", "Evaluación")
        preguntas_count = config.get("numero_preguntas", 0)
        tiempo = config.get("tiempo_limite", 0)
        puntaje = config.get("puntaje_minimo", 0)

        self.eval_title_label.setText(f"📝 {titulo}")
        self.eval_stats_label.setText(
            f"{preguntas_count} Preguntas | {tiempo} min | {puntaje}% p/aprob."
        )

    def mostrar_sin_evaluacion(self):
        """Mostrar placeholder amigable de creación"""
        self.eval_toolbar.hide()
        self.no_eval_placeholder.show()
        self.table.hide()
        self.new_question_btn.setEnabled(False)

    def actualizar_tabla(self, preguntas):
        """Actualizar tabla de preguntas"""
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(len(preguntas))
        self.table.setStyleSheet(
            """
            QTableWidget { border: none; }
            QTableView { border: none; }
            QTableWidget::item { padding: 8px; }
        """
        )
        self.table.setColumnWidth(4, 120)
        self.table.verticalHeader().setDefaultSectionSize(54)
        
        # Validar límite de preguntas
        if self.evaluacion_actual:
            max_preguntas = self.evaluacion_actual.get("numero_preguntas", 10)
            if len(preguntas) >= max_preguntas:
                self.new_question_btn.setEnabled(False)
                self.new_question_btn.setText("Límite Alcanzado")
                self.new_question_btn.setToolTip(f"Ya has alcanzado el límite configurado de {max_preguntas} preguntas.")
            else:
                self.new_question_btn.setEnabled(True)
                self.new_question_btn.setText("➕ Nueva Pregunta")
                self.new_question_btn.setToolTip("")

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

        self.table.setUpdatesEnabled(True)

    def configurar_evaluacion(self):
        """Abrir diálogo de configuración de evaluación"""
        if not self.modulo_actual:
            QMessageBox.warning(self, "Error", "Selecciona un módulo primero")
            return

        dialog = EvaluationConfigDialog(
            self.api_client, self.modulo_actual.get("id"), self.evaluacion_actual, self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            result = self.api_client.update_evaluacion_config(
                self.modulo_actual.get("id"), data
            )

            if result["success"]:
                self.load_evaluacion(self.modulo_actual.get("id"), force_refresh=True)
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def nueva_pregunta(self):
        """Crear nueva pregunta"""
        if not self.modulo_actual or not self.evaluacion_actual:
            QMessageBox.warning(self, "Error", "Primero configura la evaluación")
            return

        dialog = ExerciseDialog(
            self.api_client,
            self.modulo_actual.get("id"),
            self.evaluacion_actual.get("id"),
            None,
            True,
            self,
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            
            # Prevenir error 422 The puntos field must be at least 0.5.
            n_preguntas_config = self.evaluacion_actual.get("numero_preguntas", len(self.preguntas) + 1)
            if n_preguntas_config <= 0:
                n_preguntas_config = 1
            data["puntos"] = round(100.0 / float(n_preguntas_config), 2)

            result = self.api_client.create_pregunta(
                self.modulo_actual.get("id"), self.evaluacion_actual.get("id"), data, silent=True
            )

            if result["success"]:
                # Traer la nueva tabla de red para obtener las ids.
                self.load_evaluacion(self.modulo_actual.get("id"), force_refresh=True)
                # Redisparar la actualización a la nueva tabla, repintar optimísticamente y correr el backend en background.
                self._recalcular_distribucion_puntos()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def editar_pregunta(self, pregunta):
        """Editar pregunta existente"""
        if not self.modulo_actual or not self.evaluacion_actual:
            return

        dialog = ExerciseDialog(
            self.api_client,
            self.modulo_actual.get("id"),
            self.evaluacion_actual.get("id"),
            pregunta,
            True,
            self,
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            result = self.api_client.update_pregunta(
                self.modulo_actual.get("id"),
                self.evaluacion_actual.get("id"),
                pregunta["id"],
                data,
            )

            if result["success"]:
                self.load_evaluacion(self.modulo_actual.get("id"), force_refresh=True)
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def eliminar_pregunta(self, pregunta):
        """Eliminar pregunta"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar esta pregunta?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            result = self.api_client.delete_pregunta(
                self.modulo_actual.get("id"),
                self.evaluacion_actual.get("id"),
                pregunta["id"],
                silent=True
            )

            if result["success"]:
                # Eliminación instantánea de RAM
                self.preguntas = [p for p in self.preguntas if p.get("id") != pregunta["id"]]
                # Redistribuir con las restantes dictaminando nueva interfaz en <10ms y correr el resto en background
                self._recalcular_distribucion_puntos()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def _recalcular_distribucion_puntos(self):
        """Asigna un puntaje parejo 100/N a todas las preguntas de la evaluación basado en su configuración maestra"""
        if not self.preguntas or not self.evaluacion_actual:
            return
            
        # Calcular porcentaje exacto redondeado a 2 decimales usando float dividido el n configurado en Config, no en las cargadas!
        n_preguntas = self.evaluacion_actual.get("numero_preguntas", len(self.preguntas))
        if n_preguntas <= 0:
            n_preguntas = 1
            
        valor_equitativo = round(float(100.0) / float(n_preguntas), 2)
        
        modulo_id = self.modulo_actual.get("id")
        eval_id = self.evaluacion_actual.get("id")
        
        # Actualización de la RAM para que el usuario la vea ya reflejada optimísticamente
        for pre in self.preguntas:
            pre["puntos"] = valor_equitativo
            
        # Repinte instantáneo
        self.actualizar_tabla(self.preguntas)
        
        # Sub-rutina enviada a background thread para realizar N requests PUT sin trabarse
        def _background_sync(preg_list, mod_id, ev_id, val_eq):
            for p in preg_list:
                p_data = {
                    "pregunta": p.get("pregunta"),
                    "tipo": p.get("tipo"),
                    "estado": p.get("estado", "activo"),
                    "puntos": val_eq
                }
                if "opciones" in p:
                    p_data["opciones"] = p["opciones"]
                self.api_client.update_pregunta(mod_id, ev_id, p.get("id"), p_data, silent=True)

        import threading
        hilo_sync = threading.Thread(
            target=_background_sync, 
            args=(list(self.preguntas), modulo_id, eval_id, valor_equitativo)
        )
        hilo_sync.daemon = True
        hilo_sync.start()


    def _on_data_changed(self, data_type: str):
        """Manejador para actualizaciones en tiempo real"""
        if data_type in ["evaluaciones", "modulos"]:
            if self.modulo_actual:
                self.load_evaluacion(self.modulo_actual.get("id"), force_refresh=True)
            elif data_type == "modulos":
                self.load_modulos()

    def _on_evaluaciones_changed(self):
        """Manejador directo para cambios en evaluaciones"""
        if self.modulo_actual:
            self.load_evaluacion(self.modulo_actual.get("id"), force_refresh=True)

    def clear_layout(self, layout):
        """Limpiar un layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
