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
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
import logging
from utils.paths import resource_path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserDialog(QDialog):
    def __init__(self, api_client, user_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = user_data
        self.setWindowTitle("Editar Usuario" if user_data else "Nuevo Usuario")
        self.setFixedSize(400, 450)
        self.setup_ui()

        if user_data:
            self.load_user_data()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel(
            "👤 " + ("Editar Usuario" if self.user_data else "Nuevo Usuario")
        )
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Nombre
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")
        form_layout.addRow("Nombre:", self.nombre_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("correo@ejemplo.com")
        form_layout.addRow("Email:", self.email_input)

        # Contraseña (solo para nuevos)
        if not self.user_data:
            self.password_input = QLineEdit()
            self.password_input.setPlaceholderText("Mínimo 8 caracteres")
            self.password_input.setEchoMode(QLineEdit.Password)
            form_layout.addRow("Contraseña:", self.password_input)

        # Rol
        self.rol_combo = QComboBox()
        self.rol_combo.addItems(["aprendiz", "administrador"])
        form_layout.addRow("Rol:", self.rol_combo)

        # Estado
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        form_layout.addRow("Estado:", self.estado_combo)

        layout.addLayout(form_layout)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Guardar")
        buttons.button(QDialogButtonBox.Cancel).setText("Cancelar")

        buttons.button(QDialogButtonBox.Ok).setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
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
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def load_user_data(self):
        self.nombre_input.setText(self.user_data.get("nombre", ""))
        self.email_input.setText(self.user_data.get("email", ""))

        index = self.rol_combo.findText(self.user_data.get("rol", "aprendiz"))
        if index >= 0:
            self.rol_combo.setCurrentIndex(index)

        index = self.estado_combo.findText(self.user_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

    def get_data(self):
        data = {
            "nombre": self.nombre_input.text(),
            "email": self.email_input.text(),
            "rol": self.rol_combo.currentText(),
            "estado": self.estado_combo.currentText(),
        }

        if not self.user_data and hasattr(self, "password_input"):
            data["password"] = self.password_input.text()

        return data


class UsersView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.usuarios = []
        self.setup_ui()
        self.load_usuarios()

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
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("👥 Usuarios")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")

        self.new_btn = QPushButton("➕ Nuevo")
        self.new_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        self.new_btn.clicked.connect(self.nuevo_usuario)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.new_btn)

        layout.addLayout(header_layout)

        # Filtros
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar nombre o email...")
        self.search_input.textChanged.connect(self.filtrar_usuarios)

        self.rol_filter = QComboBox()
        self.rol_filter.addItems(["Todos", "administrador", "aprendiz"])
        self.rol_filter.currentTextChanged.connect(self.filtrar_usuarios)

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
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )
        self.refresh_btn.clicked.connect(self.load_usuarios)

        filters_layout.addWidget(self.search_input, 1)
        filters_layout.addWidget(self.rol_filter)
        filters_layout.addWidget(self.refresh_btn)

        layout.addLayout(filters_layout)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Email", "Rol", "Acciones"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.table)

        # Estadísticas
        self.stats_label = QLabel("Cargando...")
        self.stats_label.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 5px;")
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def load_usuarios(self):
        self.stats_label.setText("🔄 Cargando usuarios...")
        logger.debug("Cargando usuarios desde API...")

        result = self.api_client.get_usuarios()
        logger.debug(f"Resultado API: {result}")

        if result["success"]:
            data = result.get("data", [])
            logger.debug(f"Datos recibidos: {data}")

            if isinstance(data, list):
                self.usuarios = data
            elif isinstance(data, dict) and "data" in data:
                self.usuarios = data["data"]
            else:
                self.usuarios = []

            self.filtrar_usuarios()
            self.stats_label.setText(f"📊 Total: {len(self.usuarios)} usuarios")
        else:
            logger.error(f"Error: {result.get('error')}")
            QMessageBox.warning(
                self, "Error", f"Error al cargar usuarios: {result.get('error')}"
            )
            self.usuarios = []
            self.actualizar_tabla([])

    def filtrar_usuarios(self):
        search = self.search_input.text().lower()
        rol = self.rol_filter.currentText()

        filtrados = []
        for u in self.usuarios:
            if (
                search
                and search not in u.get("nombre", "").lower()
                and search not in u.get("email", "").lower()
            ):
                continue
            if rol != "Todos" and u.get("rol") != rol:
                continue
            filtrados.append(u)

        self.actualizar_tabla(filtrados)

    def actualizar_tabla(self, usuarios):
        self.table.setRowCount(len(usuarios))

        for row, usuario in enumerate(usuarios):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(usuario.get("id", ""))))

            # Nombre
            self.table.setItem(row, 1, QTableWidgetItem(usuario.get("nombre", "")))

            # Email
            self.table.setItem(row, 2, QTableWidgetItem(usuario.get("email", "")))

            # Rol con color
            rol_item = QTableWidgetItem(usuario.get("rol", ""))
            if usuario.get("rol") == "administrador":
                rol_item.setForeground(QColor("#e74c3c"))
                rol_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            else:
                rol_item.setForeground(QColor("#3498db"))
            self.table.setItem(row, 3, rol_item)

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
            edit_btn.clicked.connect(lambda checked, u=usuario: self.editar_usuario(u))

            # Botón estado
            estado_btn = QPushButton("🔄" if usuario.get("estado") == "activo" else "⏸️")
            estado_btn.setFixedSize(30, 30)
            estado_btn.setToolTip("Cambiar estado")
            estado_btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {'#2ecc71' if usuario.get('estado') == 'activo' else '#e74c3c'};
                    color: white;
                    border-radius: 4px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {'#27ae60' if usuario.get('estado') == 'activo' else '#c0392b'};
                }}
            """
            )
            estado_btn.clicked.connect(lambda checked, u=usuario: self.toggle_estado(u))

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
                lambda checked, u=usuario: self.eliminar_usuario(u)
            )

            acciones_layout.addWidget(edit_btn)
            acciones_layout.addWidget(estado_btn)
            acciones_layout.addWidget(delete_btn)
            acciones_layout.addStretch()

            self.table.setCellWidget(row, 4, acciones)

    def nuevo_usuario(self):
        dialog = UserDialog(self.api_client)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            if not data.get("password"):
                QMessageBox.warning(self, "Error", "La contraseña es requerida")
                return

            result = self.api_client.create_usuario(data)

            if result["success"]:
                QMessageBox.information(self, "Éxito", "Usuario creado correctamente")
                self.load_usuarios()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def editar_usuario(self, usuario):
        dialog = UserDialog(self.api_client, usuario)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            result = self.api_client.update_usuario(usuario["id"], data)

            if result["success"]:
                QMessageBox.information(self, "Éxito", "Usuario actualizado")
                self.load_usuarios()
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")

    def toggle_estado(self, usuario):
        nuevo = "inactivar" if usuario["estado"] == "activo" else "activar"
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿{nuevo} usuario {usuario['nombre']}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.api_client.toggle_usuario_status(usuario["id"])
            if result["success"]:
                self.load_usuarios()

    def eliminar_usuario(self, usuario):
        if usuario["email"] == self.api_client.user.get("email"):
            QMessageBox.warning(self, "Error", "No puedes eliminarte a ti mismo")
            return

        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar usuario {usuario['nombre']}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.api_client.delete_usuario(usuario["id"])
            if result["success"]:
                self.load_usuarios()
