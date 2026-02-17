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
    QFrame,
    QScrollArea,
    QProgressBar,
    QApplication,  # Añadido
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter, QPen
import logging
import re
import requests
from io import BytesIO
from utils.paths import resource_path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ProcessingMessage(QMessageBox):
    """Mensaje de procesamiento que se cierra automáticamente"""

    def __init__(self, text="Procesando...", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Procesando")
        self.setText(text)
        self.setStandardButtons(QMessageBox.NoButton)
        self.setModal(True)

    def closeEvent(self, event):
        """Manejar evento de cierre"""
        event.accept()

    def close(self):
        """Cerrar el mensaje"""
        self.done(0)
        super().close()


class AvatarSelector(QDialog):
    """Diálogo para seleccionar avatar desde la API"""

    def __init__(self, api_client, current_avatar=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.current_avatar = current_avatar
        self.selected_avatar = current_avatar
        self.avatars = []
        self.setWindowTitle("Seleccionar Avatar")
        self.setFixedSize(600, 500)
        self.setup_ui()
        self.cargar_avatars()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton#selectBtn {
                background-color: #3498db;
                color: white;
            }
            QPushButton#selectBtn:hover {
                background-color: #2980b9;
            }
            QPushButton#cancelBtn {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton#cancelBtn:hover {
                background-color: #c0392b;
            }
            QFrame.avatar-frame {
                border: 2px solid #ddd;
                border-radius: 50px;
                padding: 5px;
                background-color: white;
            }
            QFrame.avatar-frame:hover {
                border-color: #3498db;
                background-color: #f0f8ff;
            }
            QFrame.avatar-frame.selected {
                border: 4px solid #2ecc71;
                background-color: #f0fff0;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title = QLabel("Selecciona un avatar")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Área de scroll para avatares
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        scroll_widget = QWidget()
        self.avatars_layout = QHBoxLayout(scroll_widget)
        self.avatars_layout.setSpacing(20)
        self.avatars_layout.setAlignment(Qt.AlignCenter)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        select_btn = QPushButton("Seleccionar")
        select_btn.setObjectName("selectBtn")
        select_btn.setFixedSize(120, 40)
        select_btn.setCursor(Qt.PointingHandCursor)
        select_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setFixedSize(120, 40)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(select_btn)
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

    def cargar_avatars(self):
        """Cargar avatares desde la API"""
        try:
            # Llamar al endpoint de avatares
            result = self.api_client.get("/admin/usuarios/avatars")

            if result.get("success"):
                self.avatars = result.get("data", [])

                # Crear frames para cada avatar
                for avatar in self.avatars:
                    self.crear_frame_avatar(avatar)
            else:
                # Si falla, crear avatares por defecto
                self.crear_avatars_default()

        except Exception as e:
            logger.error(f"Error cargando avatares: {e}")
            self.crear_avatars_default()

    def crear_frame_avatar(self, avatar):
        """Crear frame para un avatar"""
        frame = QFrame()
        frame.setObjectName("avatar-frame")
        frame.setProperty("class", "avatar-frame")
        frame.setFixedSize(120, 140)
        frame.setCursor(Qt.PointingHandCursor)

        if self.current_avatar and avatar.get("id") == self.current_avatar.get("id"):
            frame.setProperty("class", "avatar-frame selected")

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(5)

        # Contenedor de la imagen
        img_container = QLabel()
        img_container.setFixedSize(100, 100)
        img_container.setAlignment(Qt.AlignCenter)
        img_container.setStyleSheet("border: none;")

        # Cargar imagen del avatar
        if avatar.get("url"):
            try:
                response = requests.get(avatar["url"], timeout=5)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    pixmap = pixmap.scaled(
                        90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    img_container.setPixmap(pixmap)
                else:
                    self.mostrar_iniciales(img_container, avatar.get("nombre", "AV"))
            except:
                self.mostrar_iniciales(img_container, avatar.get("nombre", "AV"))
        else:
            self.mostrar_iniciales(img_container, avatar.get("nombre", "AV"))

        layout.addWidget(img_container)

        # Nombre del avatar
        nombre = QLabel(avatar.get("nombre", "Avatar"))
        nombre.setAlignment(Qt.AlignCenter)
        nombre.setStyleSheet("font-size: 12px; color: #2c3e50; font-weight: bold;")
        layout.addWidget(nombre)

        # Hacer clickeable
        frame.mousePressEvent = lambda e, a=avatar: self.seleccionar_avatar(a, frame)

        self.avatars_layout.addWidget(frame)

    def mostrar_iniciales(self, label, texto):
        """Mostrar iniciales en el avatar"""
        inicial = texto[0].upper() if texto else "A"

        pixmap = QPixmap(90, 90)
        pixmap.fill(QColor("#3498db"))

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Segoe UI", 36, QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, inicial)
        painter.end()

        label.setPixmap(pixmap)

    def crear_avatars_default(self):
        """Crear avatares por defecto si la API falla"""
        avatars_default = [
            {"id": 1, "nombre": "Avatar 1", "color": "#3498db"},
            {"id": 2, "nombre": "Avatar 2", "color": "#e74c3c"},
            {"id": 3, "nombre": "Avatar 3", "color": "#2ecc71"},
            {"id": 4, "nombre": "Avatar 4", "color": "#f39c12"},
            {"id": 5, "nombre": "Avatar 5", "color": "#9b59b6"},
        ]

        for avatar in avatars_default:
            frame = QFrame()
            frame.setObjectName("avatar-frame")
            frame.setProperty("class", "avatar-frame")
            frame.setFixedSize(120, 140)
            frame.setCursor(Qt.PointingHandCursor)

            layout = QVBoxLayout(frame)
            layout.setAlignment(Qt.AlignCenter)

            # Círculo con color
            img_label = QLabel()
            img_label.setFixedSize(90, 90)
            img_label.setAlignment(Qt.AlignCenter)

            pixmap = QPixmap(90, 90)
            pixmap.fill(QColor(avatar["color"]))

            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.white))
            painter.setFont(QFont("Segoe UI", 36, QFont.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, avatar["nombre"][0])
            painter.end()

            img_label.setPixmap(pixmap)
            layout.addWidget(img_label)

            # Nombre
            nombre = QLabel(avatar["nombre"])
            nombre.setAlignment(Qt.AlignCenter)
            nombre.setStyleSheet("font-size: 12px; color: #2c3e50; font-weight: bold;")
            layout.addWidget(nombre)

            frame.mousePressEvent = lambda e, a=avatar: self.seleccionar_avatar(
                a, frame
            )

            self.avatars_layout.addWidget(frame)

    def seleccionar_avatar(self, avatar, frame):
        """Seleccionar un avatar"""
        # Quitar selección anterior
        for i in range(self.avatars_layout.count()):
            f = self.avatars_layout.itemAt(i).widget()
            if f:
                f.setProperty("class", "avatar-frame")
                f.style().polish(f)

        # Marcar como seleccionado
        frame.setProperty("class", "avatar-frame selected")
        frame.style().polish(frame)

        self.selected_avatar = avatar

    def get_selected_avatar(self):
        """Obtener avatar seleccionado"""
        return self.selected_avatar


class UserDialog(QDialog):
    def __init__(self, api_client, user_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = user_data
        self.selected_avatar = None
        self.setWindowTitle("Editar Usuario" if user_data else "Nuevo Usuario")
        self.setFixedSize(550, 700)
        self.setup_ui()

        # Timer para validación en tiempo real
        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.validate_all_fields)

        if user_data:
            self.load_user_data()
            if user_data.get("avatar"):
                self.selected_avatar = user_data["avatar"]
        else:
            self.set_default_avatar()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            QLineEdit.valid {
                border: 2px solid #2ecc71;
                background-color: #f0fff0;
            }
            QLineEdit.invalid {
                border: 2px solid #e74c3c;
                background-color: #fff5f5;
            }
            QLabel.error {
                color: #e74c3c;
                font-size: 11px;
                padding-left: 10px;
            }
            QLabel.success {
                color: #2ecc71;
                font-size: 11px;
                padding-left: 10px;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
            QFrame#avatarFrame {
                border: 2px solid #3498db;
                border-radius: 60px;
                padding: 5px;
                background-color: white;
            }
            QFrame#avatarFrame:hover {
                border-color: #2980b9;
                background-color: #f0f8ff;
                cursor: pointer;
            }
            QPushButton#changeAvatarBtn {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton#changeAvatarBtn:hover {
                background-color: #2980b9;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 3px;
                text-align: center;
                height: 8px;
            }
            QProgressBar::chunk {
                border-radius: 3px;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(35, 25, 35, 25)

        # Título
        title = QLabel(" " + ("Editar Usuario" if self.user_data else "Nuevo Usuario"))
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Avatar (clickeable)
        self.avatar_frame = QFrame()
        self.avatar_frame.setObjectName("avatarFrame")
        self.avatar_frame.setFixedSize(100, 100)
        self.avatar_frame.setCursor(Qt.PointingHandCursor)
        self.avatar_frame.mousePressEvent = self.seleccionar_avatar

        avatar_layout = QVBoxLayout(self.avatar_frame)
        avatar_layout.setAlignment(Qt.AlignCenter)

        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(80, 80)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet("border: none;")

        avatar_layout.addWidget(self.avatar_label)

        avatar_container = QHBoxLayout()
        avatar_container.addStretch()
        avatar_container.addWidget(self.avatar_frame)
        avatar_container.addStretch()

        layout.addLayout(avatar_container)

        # Botón cambiar avatar
        change_avatar_btn = QPushButton("Cambiar Avatar")
        change_avatar_btn.setObjectName("changeAvatarBtn")
        change_avatar_btn.setFixedHeight(30)
        change_avatar_btn.setCursor(Qt.PointingHandCursor)
        change_avatar_btn.clicked.connect(self.seleccionar_avatar)

        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(change_avatar_btn)
        btn_container.addStretch()
        layout.addLayout(btn_container)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Nombre
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo (mínimo 3 caracteres)")
        self.nombre_input.textChanged.connect(self.on_text_changed)
        form_layout.addRow("Nombre:", self.nombre_input)

        self.nombre_error = QLabel("")
        self.nombre_error.setProperty("class", "error")
        form_layout.addRow("", self.nombre_error)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("correo@ejemplo.com")
        self.email_input.textChanged.connect(self.on_text_changed)
        form_layout.addRow("Email:", self.email_input)

        self.email_error = QLabel("")
        self.email_error.setProperty("class", "error")
        form_layout.addRow("", self.email_error)

        # Contraseña (solo para nuevos)
        if not self.user_data:
            self.password_input = QLineEdit()
            self.password_input.setPlaceholderText(
                "Mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número"
            )
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.textChanged.connect(self.on_text_changed)
            form_layout.addRow("Contraseña:", self.password_input)

            # Barra de fortaleza
            self.password_strength = QProgressBar()
            self.password_strength.setRange(0, 100)
            self.password_strength.setValue(0)
            self.password_strength.setTextVisible(False)
            form_layout.addRow("", self.password_strength)

            self.password_error = QLabel("")
            self.password_error.setProperty("class", "error")
            form_layout.addRow("", self.password_error)

            # Confirmar contraseña
            self.password_confirm_input = QLineEdit()
            self.password_confirm_input.setPlaceholderText("Repite la contraseña")
            self.password_confirm_input.setEchoMode(QLineEdit.Password)
            self.password_confirm_input.textChanged.connect(self.on_text_changed)
            form_layout.addRow("Confirmar:", self.password_confirm_input)

            self.password_confirm_error = QLabel("")
            self.password_confirm_error.setProperty("class", "error")
            form_layout.addRow("", self.password_confirm_error)

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
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.save_btn = QPushButton("Guardar")
        self.save_btn.setFixedHeight(45)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """
        )
        self.save_btn.clicked.connect(self.validate_and_accept)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 25px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        self.save_btn.setEnabled(False)

    def set_default_avatar(self):
        """Establecer avatar por defecto con iniciales"""
        nombre = self.nombre_input.text() or "NU"
        palabras = nombre.split()
        iniciales = ""
        for palabra in palabras[:2]:
            if palabra:
                iniciales += palabra[0].upper()

        if not iniciales:
            iniciales = "NU"

        pixmap = QPixmap(80, 80)
        pixmap.fill(QColor("#3498db"))

        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Segoe UI", 24, QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, iniciales)
        painter.end()

        self.avatar_label.setPixmap(pixmap)

    def seleccionar_avatar(self, event=None):
        """Abrir selector de avatar"""
        dialog = AvatarSelector(
            self.api_client, current_avatar=self.selected_avatar, parent=self
        )

        if dialog.exec_() == QDialog.Accepted:
            self.selected_avatar = dialog.get_selected_avatar()
            self.actualizar_avatar()

    def actualizar_avatar(self):
        """Actualizar la vista del avatar"""
        if self.selected_avatar:
            if self.selected_avatar.get("url"):
                try:
                    response = requests.get(self.selected_avatar["url"], timeout=5)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        pixmap = pixmap.scaled(
                            80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        self.avatar_label.setPixmap(pixmap)
                        return
                except:
                    pass

        # Si no se puede cargar, mostrar iniciales
        self.set_default_avatar()

    def on_text_changed(self):
        """Manejar cambios en tiempo real"""
        self.validation_timer.start(500)

        sender = self.sender()
        if sender == self.nombre_input:
            self.validate_nombre(show_error=False)
        elif sender == self.email_input:
            self.validate_email(show_error=False)
        elif sender == self.password_input:
            self.validate_password(show_error=False)
            self.update_password_strength()
        elif sender == self.password_confirm_input:
            self.validate_password_confirm(show_error=False)

    def validate_all_fields(self):
        """Validar todos los campos"""
        nombre_valido = self.validate_nombre(show_error=False)
        email_valido = self.validate_email(show_error=False)

        if self.user_data:
            todos_validos = nombre_valido and email_valido
        else:
            password_valida = self.validate_password(show_error=False)
            password_confirm_valida = self.validate_password_confirm(show_error=False)
            todos_validos = (
                nombre_valido
                and email_valido
                and password_valida
                and password_confirm_valida
            )

        self.save_btn.setEnabled(todos_validos)

    def validate_nombre(self, show_error=True):
        """Validar nombre"""
        nombre = self.nombre_input.text().strip()

        if not nombre:
            if show_error:
                self.nombre_input.setProperty("class", "invalid")
                self.nombre_error.setText("El nombre es requerido")
                self.nombre_error.setProperty("class", "error")
            return False
        elif len(nombre) < 3:
            if show_error:
                self.nombre_input.setProperty("class", "invalid")
                self.nombre_error.setText("Mínimo 3 caracteres")
                self.nombre_error.setProperty("class", "error")
            return False
        else:
            self.nombre_input.setProperty("class", "valid")
            self.nombre_error.setText("Válido")
            self.nombre_error.setProperty("class", "success")
            return True

        self.style().polish(self.nombre_input)
        self.style().polish(self.nombre_error)

    def validate_email(self, show_error=True):
        """Validar email"""
        email = self.email_input.text().strip()

        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not email:
            if show_error:
                self.email_input.setProperty("class", "invalid")
                self.email_error.setText("El email es requerido")
                self.email_error.setProperty("class", "error")
            return False
        elif not re.match(patron, email):
            if show_error:
                self.email_input.setProperty("class", "invalid")
                self.email_error.setText("Formato de email inválido")
                self.email_error.setProperty("class", "error")
            return False
        else:
            self.email_input.setProperty("class", "valid")
            self.email_error.setText("Válido")
            self.email_error.setProperty("class", "success")
            return True

        self.style().polish(self.email_input)
        self.style().polish(self.email_error)

    def validate_password(self, show_error=True):
        """Validar contraseña"""
        if self.user_data:
            return True

        password = self.password_input.text()

        if not password:
            if show_error:
                self.password_input.setProperty("class", "invalid")
                self.password_error.setText("La contraseña es requerida")
                self.password_error.setProperty("class", "error")
            return False

        errores = []

        if len(password) < 8:
            errores.append("• Mínimo 8 caracteres")
        if not re.search(r"[A-Z]", password):
            errores.append("• Al menos una mayúscula")
        if not re.search(r"[a-z]", password):
            errores.append("• Al menos una minúscula")
        if not re.search(r"[0-9]", password):
            errores.append("• Al menos un número")

        if errores:
            if show_error:
                self.password_input.setProperty("class", "invalid")
                self.password_error.setText("Requisitos:\n" + "\n".join(errores))
                self.password_error.setProperty("class", "error")
            return False
        else:
            self.password_input.setProperty("class", "valid")
            self.password_error.setText("Válida")
            self.password_error.setProperty("class", "success")
            return True

        self.style().polish(self.password_input)
        self.style().polish(self.password_error)

    def update_password_strength(self):
        """Actualizar barra de fortaleza"""
        password = self.password_input.text()
        strength = 0

        if len(password) >= 8:
            strength += 25
        if re.search(r"[A-Z]", password):
            strength += 25
        if re.search(r"[a-z]", password):
            strength += 25
        if re.search(r"[0-9]", password):
            strength += 25

        self.password_strength.setValue(strength)

        # Cambiar color según fortaleza
        if strength <= 25:
            self.password_strength.setStyleSheet(
                "QProgressBar::chunk { background-color: #e74c3c; }"
            )
        elif strength <= 50:
            self.password_strength.setStyleSheet(
                "QProgressBar::chunk { background-color: #f39c12; }"
            )
        elif strength <= 75:
            self.password_strength.setStyleSheet(
                "QProgressBar::chunk { background-color: #3498db; }"
            )
        else:
            self.password_strength.setStyleSheet(
                "QProgressBar::chunk { background-color: #2ecc71; }"
            )

    def validate_password_confirm(self, show_error=True):
        """Validar confirmación de contraseña"""
        if self.user_data:
            return True

        password = self.password_input.text()
        confirm = self.password_confirm_input.text()

        if not confirm:
            if show_error:
                self.password_confirm_input.setProperty("class", "invalid")
                self.password_confirm_error.setText("Confirma la contraseña")
                self.password_confirm_error.setProperty("class", "error")
            return False
        elif password != confirm:
            if show_error:
                self.password_confirm_input.setProperty("class", "invalid")
                self.password_confirm_error.setText("No coinciden")
                self.password_confirm_error.setProperty("class", "error")
            return False
        else:
            self.password_confirm_input.setProperty("class", "valid")
            self.password_confirm_error.setText("Coinciden")
            self.password_confirm_error.setProperty("class", "success")
            return True

        self.style().polish(self.password_confirm_input)
        self.style().polish(self.password_confirm_error)

    def validate_and_accept(self):
        """Validar y aceptar"""
        nombre_valido = self.validate_nombre(show_error=True)
        email_valido = self.validate_email(show_error=True)

        if not nombre_valido or not email_valido:
            return

        if not self.user_data:
            password_valida = self.validate_password(show_error=True)
            password_confirm_valida = self.validate_password_confirm(show_error=True)

            if not password_valida or not password_confirm_valida:
                return

        self.accept()

    def load_user_data(self):
        """Cargar datos del usuario"""
        self.nombre_input.setText(self.user_data.get("nombre", ""))
        self.email_input.setText(self.user_data.get("email", ""))

        index = self.rol_combo.findText(self.user_data.get("rol", "aprendiz"))
        if index >= 0:
            self.rol_combo.setCurrentIndex(index)

        index = self.estado_combo.findText(self.user_data.get("estado", "activo"))
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

        # Validar después de cargar
        self.nombre_input.textChanged.emit(self.nombre_input.text())
        self.email_input.textChanged.emit(self.email_input.text())

        # Actualizar avatar
        self.actualizar_avatar()

    def get_data(self):
        """Obtener datos del formulario"""
        data = {
            "nombre": self.nombre_input.text().strip(),
            "email": self.email_input.text().strip().lower(),
            "rol": self.rol_combo.currentText(),
            "estado": self.estado_combo.currentText(),
        }

        # Incluir avatar si está seleccionado
        if self.selected_avatar:
            data["avatar_id"] = self.selected_avatar.get("id")

        if not self.user_data and hasattr(self, "password_input"):
            data["password"] = self.password_input.text()
        elif hasattr(self, "password_input") and self.password_input.text():
            data["password"] = self.password_input.text()

        return data


class UsersView(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.usuarios = []
        self.usuarios_filtrados = []

        # Variables de paginación
        self.pagina_actual = 1
        self.items_por_pagina = 10
        self.total_paginas = 1

        self.setup_ui()

        # Conectar señal de actualización automática
        self.api_client.usuarios_changed.connect(self.on_usuarios_changed)

        # Cargar datos iniciales
        self.cargar_usuarios(force_refresh=True)

    def setup_ui(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px 8px;
                vertical-align: middle;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #3498db;
                font-weight: bold;
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                padding: 10px 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
            }
            QPushButton {
                font-size: 13px;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        title = QLabel("Gestión Usuarios")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")

        self.new_btn = QPushButton("+ Nuevo Usuario")
        self.new_btn.setFixedHeight(45)
        self.new_btn.setCursor(Qt.PointingHandCursor)
        self.new_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        )
        self.new_btn.clicked.connect(self.nuevo_usuario)

        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.setFixedSize(45, 45)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setToolTip("Actualizar")
        self.refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """
        )
        self.refresh_btn.clicked.connect(
            lambda: self.cargar_usuarios(force_refresh=True)
        )

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.new_btn)
        header_layout.addWidget(self.refresh_btn)

        layout.addLayout(header_layout)

        # Filtros
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(15)

        # Búsqueda
        search_container = QWidget()
        search_container.setFixedHeight(45)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre o email...")
        self.search_input.setFixedHeight(45)
        self.search_input.textChanged.connect(self.filtrar_usuarios)
        search_layout.addWidget(self.search_input)

        # Filtro rol
        self.rol_filter = QComboBox()
        self.rol_filter.setFixedHeight(45)
        self.rol_filter.setMinimumWidth(150)
        self.rol_filter.addItems(["Todos los roles", "administrador", "aprendiz"])
        self.rol_filter.currentTextChanged.connect(self.filtrar_usuarios)

        filters_layout.addWidget(search_container, 2)
        filters_layout.addWidget(self.rol_filter, 1)

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
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

        # Controles de paginación
        pagination_layout = QHBoxLayout()
        pagination_layout.setSpacing(10)

        # Botones de paginación
        self.first_btn = QPushButton("◀◀")
        self.first_btn.setFixedSize(40, 35)
        self.first_btn.setCursor(Qt.PointingHandCursor)
        self.first_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """
        )
        self.first_btn.clicked.connect(self.ir_primera_pagina)

        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(40, 35)
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """
        )
        self.prev_btn.clicked.connect(self.pagina_anterior)

        self.page_label = QLabel("Página 1 de 1")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet(
            "font-size: 13px; color: #2c3e50; font-weight: bold;"
        )

        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(40, 35)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """
        )
        self.next_btn.clicked.connect(self.pagina_siguiente)

        self.last_btn = QPushButton("▶▶")
        self.last_btn.setFixedSize(40, 35)
        self.last_btn.setCursor(Qt.PointingHandCursor)
        self.last_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """
        )
        self.last_btn.clicked.connect(self.ir_ultima_pagina)

        # Selector de items por página
        items_label = QLabel("Mostrar:")
        items_label.setStyleSheet("color: #2c3e50;")

        self.items_per_page = QComboBox()
        self.items_per_page.setFixedHeight(35)
        self.items_per_page.setFixedWidth(80)
        self.items_per_page.addItems(["10", "20", "50", "100"])
        self.items_per_page.setCurrentText(str(self.items_por_pagina))
        self.items_per_page.currentTextChanged.connect(self.cambiar_items_por_pagina)

        pagination_layout.addStretch()
        pagination_layout.addWidget(self.first_btn)
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addWidget(self.last_btn)
        pagination_layout.addSpacing(20)
        pagination_layout.addWidget(items_label)
        pagination_layout.addWidget(self.items_per_page)
        pagination_layout.addStretch()

        layout.addLayout(pagination_layout)

        # Estadísticas
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(5, 10, 5, 5)

        self.stats_label = QLabel("Cargando...")
        self.stats_label.setStyleSheet("color: #7f8c8d; font-size: 13px;")

        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()

        layout.addWidget(stats_container)

        self.setLayout(layout)

    def on_usuarios_changed(self):
        """Este método se ejecuta automáticamente cuando hay cambios en usuarios"""
        logger.debug("Usuarios cambiaron - actualizando vista...")
        self.stats_label.setText("Actualizando...")
        QTimer.singleShot(100, lambda: self.cargar_usuarios(force_refresh=True))

    def cargar_usuarios(self, force_refresh=False):
        """Cargar usuarios desde la API"""
        self.stats_label.setText("Cargando usuarios...")
        logger.debug(f"Cargando usuarios desde API... (force_refresh={force_refresh})")

        result = self.api_client.get_usuarios(force_refresh=force_refresh)
        logger.debug(f"Resultado API: {result}")

        if result["success"]:
            data = result.get("data", [])
            logger.debug(
                f"Datos recibidos: {len(data) if isinstance(data, list) else 'dict'} usuarios"
            )

            if isinstance(data, list):
                self.usuarios = data
            elif isinstance(data, dict) and "data" in data:
                self.usuarios = data["data"]
            else:
                self.usuarios = []

            self.filtrar_usuarios()
            self.stats_label.setText(f"{len(self.usuarios)} usuarios cargados")
            QTimer.singleShot(2000, self.actualizar_stats_normal)
        else:
            logger.error(f"Error: {result.get('error')}")
            QMessageBox.warning(
                self, "Error", f"Error al cargar usuarios: {result.get('error')}"
            )
            self.usuarios = []
            self.usuarios_filtrados = []
            self.actualizar_tabla()

    def actualizar_stats_normal(self):
        """Restaurar estadísticas normales"""
        total_filtrados = len(self.usuarios_filtrados)
        if total_filtrados > 0:
            inicio = (self.pagina_actual - 1) * self.items_por_pagina + 1
            fin = min(inicio + self.items_por_pagina - 1, total_filtrados)
            self.stats_label.setText(
                f"Mostrando {inicio}-{fin} de {total_filtrados} usuarios (Total: {len(self.usuarios)})"
            )
        else:
            self.stats_label.setText("No se encontraron usuarios")

    def filtrar_usuarios(self):
        search = self.search_input.text().lower()
        rol = self.rol_filter.currentText()

        self.usuarios_filtrados = []
        for u in self.usuarios:
            if search:
                nombre = u.get("nombre", "").lower()
                email = u.get("email", "").lower()
                if search not in nombre and search not in email:
                    continue

            if rol != "Todos los roles" and u.get("rol") != rol:
                continue

            self.usuarios_filtrados.append(u)

        self.pagina_actual = 1
        self.calcular_total_paginas()
        self.actualizar_tabla()
        self.actualizar_controles_paginacion()

    def calcular_total_paginas(self):
        total_items = len(self.usuarios_filtrados)
        self.total_paginas = max(
            1, (total_items + self.items_por_pagina - 1) // self.items_por_pagina
        )
        if self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas

    def obtener_pagina_actual(self):
        inicio = (self.pagina_actual - 1) * self.items_por_pagina
        fin = inicio + self.items_por_pagina
        return self.usuarios_filtrados[inicio:fin]

    def actualizar_tabla(self):
        usuarios_pagina = self.obtener_pagina_actual()
        self.table.setRowCount(len(usuarios_pagina))

        for row, usuario in enumerate(usuarios_pagina):
            # ID
            id_item = QTableWidgetItem(str(usuario.get("id", "")))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, id_item)

            # Nombre
            nombre_item = QTableWidgetItem(usuario.get("nombre", ""))
            nombre_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row, 1, nombre_item)

            # Email
            email_item = QTableWidgetItem(usuario.get("email", ""))
            email_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(row, 2, email_item)

            # Rol
            rol_item = QTableWidgetItem(usuario.get("rol", ""))
            rol_item.setTextAlignment(Qt.AlignCenter)
            rol_item.setFont(QFont("Segoe UI", 11))
            if usuario.get("rol") == "administrador":
                rol_item.setForeground(QColor("#e74c3c"))
                rol_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            else:
                rol_item.setForeground(QColor("#3498db"))
            self.table.setItem(row, 3, rol_item)

            # Acciones
            acciones = QWidget()
            acciones.setFixedHeight(50)
            acciones_layout = QHBoxLayout(acciones)
            acciones_layout.setContentsMargins(5, 0, 5, 0)
            acciones_layout.setSpacing(8)
            acciones_layout.setAlignment(Qt.AlignCenter)

            # Botón editar
            edit_btn = QPushButton("Editar")
            edit_btn.setFixedSize(70, 32)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setToolTip("Editar usuario")
            edit_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """
            )
            edit_btn.clicked.connect(lambda checked, u=usuario: self.editar_usuario(u))

            # Botón estado
            estado_btn = QPushButton()
            estado_btn.setFixedSize(32, 32)
            estado_btn.setCursor(Qt.PointingHandCursor)

            if usuario.get("estado") == "activo":
                estado_btn.setText("●")
                estado_btn.setToolTip("Activo - Click para inactivar")
                estado_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #2ecc71;
                        color: white;
                        border-radius: 16px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #27ae60;
                    }
                """
                )
            else:
                estado_btn.setText("●")
                estado_btn.setToolTip("Inactivo - Click para activar")
                estado_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border-radius: 16px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """
                )

            estado_btn.clicked.connect(lambda checked, u=usuario: self.toggle_estado(u))

            # Botón eliminar
            delete_btn = QPushButton("✕")
            delete_btn.setFixedSize(32, 32)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setToolTip("Eliminar usuario")
            delete_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
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

            self.table.setCellWidget(row, 4, acciones)
            self.table.setRowHeight(row, 60)

        self.actualizar_stats_normal()
        self.page_label.setText(f"Página {self.pagina_actual} de {self.total_paginas}")

    def actualizar_controles_paginacion(self):
        self.first_btn.setEnabled(self.pagina_actual > 1)
        self.prev_btn.setEnabled(self.pagina_actual > 1)
        self.next_btn.setEnabled(self.pagina_actual < self.total_paginas)
        self.last_btn.setEnabled(self.pagina_actual < self.total_paginas)

    def ir_primera_pagina(self):
        if self.pagina_actual > 1:
            self.pagina_actual = 1
            self.actualizar_tabla()
            self.actualizar_controles_paginacion()

    def ir_ultima_pagina(self):
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual = self.total_paginas
            self.actualizar_tabla()
            self.actualizar_controles_paginacion()

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.actualizar_tabla()
            self.actualizar_controles_paginacion()

    def pagina_siguiente(self):
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.actualizar_tabla()
            self.actualizar_controles_paginacion()

    def cambiar_items_por_pagina(self, value):
        self.items_por_pagina = int(value)
        self.pagina_actual = 1
        self.calcular_total_paginas()
        self.actualizar_tabla()
        self.actualizar_controles_paginacion()

    def nuevo_usuario(self):
        dialog = UserDialog(self.api_client)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            if not data.get("password"):
                QMessageBox.warning(self, "Error", "La contraseña es requerida")
                return

            # Crear y mostrar mensaje de procesamiento
            msg = ProcessingMessage("Creando usuario...", self)
            msg.show()

            # Forzar actualización de eventos
            QApplication.processEvents()

            # Procesar directamente sin QTimer
            self._procesar_nuevo_usuario(data, msg)

    def _procesar_nuevo_usuario(self, data, msg):
        """Procesar creación de usuario"""
        try:
            result = self.api_client.create_usuario(data)

            # Cerrar mensaje de procesamiento
            msg.close()
            QApplication.processEvents()

            if result["success"]:
                email_verified = result.get("email_verified", False)

                if not email_verified:
                    QMessageBox.information(
                        self,
                        "Éxito",
                        "Usuario creado correctamente\n\n"
                        "Se ha enviado un email de verificación a:\n"
                        f"{data['email']}\n\n"
                        "El usuario debe verificar su email para poder acceder.",
                    )
                else:
                    QMessageBox.information(
                        self, "Éxito", "Usuario creado correctamente"
                    )
            else:
                error_msg = result.get("error", "Error desconocido")

                if result.get("validation_errors"):
                    error_msg = "\n".join(result["validation_errors"])
                elif "email" in error_msg.lower():
                    if (
                        "already" in error_msg.lower()
                        or "registrado" in error_msg.lower()
                    ):
                        error_msg = "El email ya está registrado en el sistema"

                QMessageBox.critical(
                    self, "Error", f"Error al crear usuario:\n{error_msg}"
                )
        except Exception as e:
            msg.close()
            QApplication.processEvents()
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def editar_usuario(self, usuario):
        dialog = UserDialog(self.api_client, usuario)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            # Crear y mostrar mensaje de procesamiento
            msg = ProcessingMessage("Actualizando usuario...", self)
            msg.show()

            # Forzar actualización de eventos
            QApplication.processEvents()

            # Procesar directamente sin QTimer
            self._procesar_editar_usuario(usuario["id"], data, msg)

    def _procesar_editar_usuario(self, usuario_id, data, msg):
        """Procesar edición de usuario"""
        try:
            result = self.api_client.update_usuario(usuario_id, data)

            # Cerrar mensaje de procesamiento
            msg.close()
            QApplication.processEvents()

            if result["success"]:
                if "email" in data and data["email"] != self._get_original_email(
                    usuario_id
                ):
                    QMessageBox.information(
                        self,
                        "Éxito",
                        "Usuario actualizado correctamente\n\n"
                        "Se ha enviado un nuevo email de verificación porque el email cambió.",
                    )
                else:
                    QMessageBox.information(
                        self, "Éxito", "Usuario actualizado correctamente"
                    )
            else:
                error_msg = result.get("error", "Error desconocido")
                if result.get("validation_errors"):
                    error_msg = "\n".join(result["validation_errors"])
                QMessageBox.critical(
                    self, "Error", f"Error al actualizar:\n{error_msg}"
                )
        except Exception as e:
            msg.close()
            QApplication.processEvents()
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def _get_original_email(self, usuario_id):
        """Obtener email original del usuario"""
        for usuario in self.usuarios:
            if usuario.get("id") == usuario_id:
                return usuario.get("email")
        return None

    def toggle_estado(self, usuario):
        nuevo = "inactivar" if usuario["estado"] == "activo" else "activar"
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Estás seguro de {nuevo} al usuario {usuario['nombre']}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # Crear y mostrar mensaje de procesamiento
            msg = ProcessingMessage("Cambiando estado...", self)
            msg.show()

            # Forzar actualización de eventos
            QApplication.processEvents()

            # Procesar directamente sin QTimer
            self._procesar_cambio_estado(usuario, msg)

    def _procesar_cambio_estado(self, usuario, msg):
        """Procesar cambio de estado"""
        try:
            result = self.api_client.toggle_usuario_status(usuario["id"])

            # Cerrar mensaje de procesamiento
            msg.close()
            QApplication.processEvents()

            if result["success"]:
                estado_text = (
                    "inactivado" if usuario["estado"] == "activo" else "activado"
                )
                QMessageBox.information(
                    self, "Éxito", f"Usuario {estado_text} correctamente"
                )
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")
        except Exception as e:
            msg.close()
            QApplication.processEvents()
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

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
            # Crear y mostrar mensaje de procesamiento
            msg = ProcessingMessage("Eliminando usuario...", self)
            msg.show()

            # Forzar actualización de eventos
            QApplication.processEvents()

            # Procesar directamente sin QTimer
            self._procesar_eliminar_usuario(usuario["id"], msg)

    def _procesar_eliminar_usuario(self, usuario_id, msg):
        """Procesar eliminación de usuario"""
        try:
            result = self.api_client.delete_usuario(usuario_id)

            # Cerrar mensaje de procesamiento
            msg.close()
            QApplication.processEvents()

            if result["success"]:
                QMessageBox.information(
                    self, "Éxito", "Usuario eliminado correctamente"
                )
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")
        except Exception as e:
            msg.close()
            QApplication.processEvents()
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
