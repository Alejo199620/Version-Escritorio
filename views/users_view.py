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
    QFrame,
    QScrollArea,
    QProgressBar,
    QApplication,
    QAbstractItemView,
    QFileDialog,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPixmap, QPainter, QPen
from views.components.toast import ToastNotification
import logging
import re
import requests
import os
from io import BytesIO
from utils.paths import resource_path

logger = logging.getLogger(__name__)


def avatar_id_to_name(avatar_id):
    """Convierte un ID de avatar a un nombre legible"""
    if not avatar_id:
        return "Avatar"
    if avatar_id == "default":
        return "Predeterminado"
    return avatar_id.replace("_", " ").title()


class ProcessingMessage(QMessageBox):
    """Mensaje de procesamiento que se cierra automáticamente"""

    def __init__(self, text="Procesando...", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Procesando")
        self.setText(text)
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
                background-color: #ffffff;
                border: 1px solid #e8eef7;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
                transition: all 0.3s ease;
            }
            QPushButton#selectBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                font-size: 13px;
            }
            QPushButton#selectBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #357abd, stop:1 #1f4d7b);
            }
            QPushButton#selectBtn:pressed {
                padding: 9px 14px 7px 16px;
            }
            QPushButton#uploadBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #7c3aed, stop:1 #6d28d9);
                color: white;
                font-size: 13px;
            }
            QPushButton#uploadBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #6d28d9, stop:1 #581c87);
            }
            QPushButton#cancelBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #ef4444, stop:1 #dc2626);
                color: white;
                font-size: 13px;
            }
            QPushButton#cancelBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #dc2626, stop:1 #991b1b);
            }
            QFrame.avatar-frame {
                border: 2px solid #e5e7eb;
                border-radius: 60px;
                padding: 5px;
                background-color: white;
            }
            QFrame.avatar-frame:hover {
                border: 2px solid #4a90e2;
                background-color: #f0f7ff;
            }
            QFrame.avatar-frame.selected {
                border: 3px solid #10b981;
                background-color: #f0fdf4;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title = QLabel("Selecciona un avatar")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Área de scroll para avatares
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        scroll_widget = QWidget()
        self.avatars_layout = QHBoxLayout(scroll_widget)
        self.avatars_layout.setSpacing(20)
        self.avatars_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        upload_btn = QPushButton("📤 Cargar Archivo")
        upload_btn.setObjectName("uploadBtn")
        upload_btn.setFixedSize(140, 40)
        upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_btn.setStyleSheet(
            """
            QPushButton#uploadBtn {
                background-color: #9b59b6;
                color: white;
            }
            QPushButton#uploadBtn:hover {
                background-color: #8e44ad;
            }
        """
        )
        upload_btn.clicked.connect(self.cargar_archivo_avatar)

        select_btn = QPushButton("Seleccionar")
        select_btn.setObjectName("selectBtn")
        select_btn.setFixedSize(120, 40)
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        select_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setFixedSize(120, 40)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(upload_btn)
        buttons_layout.addWidget(select_btn)
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

    def cargar_avatars(self):
        """Cargar avatares desde la carpeta local assets/avatars"""
        try:
            self.avatars = []
            avatars_dir = resource_path(os.path.join("assets", "avatars"))

            if os.path.exists(avatars_dir):
                # Listar archivos png en la carpeta
                files = [f for f in os.listdir(avatars_dir) if f.endswith(".png")]
                files.sort()  # Asegurar orden

                for filename in files:
                    avatar_id = filename.split(".")[0]
                    # Formatear nombre para mostrar (ej: avatar_01 -> Avatar 1)
                    display_name = avatar_id.replace("_", " ").title()
                    if avatar_id == "default":
                        display_name = "Predeterminado"

                    avatar_info = {
                        "id": avatar_id,
                        "nombre": display_name,
                        "path": os.path.join(avatars_dir, filename),
                    }
                    self.avatars.append(avatar_info)
                    self.crear_frame_avatar(avatar_info)

            if not self.avatars:
                # Si no hay archivos, usar los default por código como respaldo
                self.crear_avatars_default()

        except Exception as e:
            logger.error(f"Error cargando avatares locales: {e}")
            self.crear_avatars_default()

    def crear_frame_avatar(self, avatar):
        """Crear frame para un avatar"""
        frame = QFrame()
        frame.setObjectName("avatar-frame")
        frame.setProperty("class", "avatar-frame")
        frame.setFixedSize(120, 140)
        frame.setCursor(Qt.CursorShape.PointingHandCursor)

        if self.current_avatar and avatar.get("id") == self.current_avatar.get("id"):
            frame.setProperty("class", "avatar-frame selected")

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        # Contenedor de la imagen
        img_container = QLabel()
        img_container.setFixedSize(100, 100)
        img_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_container.setStyleSheet("border: none;")

        # Cargar imagen del avatar
        if avatar.get("path") and os.path.exists(avatar["path"]):
            try:
                pixmap = QPixmap(avatar["path"])
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(
                        90,
                        90,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    img_container.setPixmap(pixmap)
                else:
                    self.mostrar_iniciales(img_container, avatar.get("nombre", "AV"))
            except Exception as e:
                logger.error(f"Error cargando pixmap: {e}")
                self.mostrar_iniciales(img_container, avatar.get("nombre", "AV"))
        elif avatar.get("url"):
            try:
                response = requests.get(avatar["url"], timeout=5)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    pixmap = pixmap.scaled(
                        90,
                        90,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
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
        nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        painter.setPen(QPen(Qt.GlobalColor.white))
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, inicial)
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
            frame.setCursor(Qt.CursorShape.PointingHandCursor)

            layout = QVBoxLayout(frame)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Círculo con color
            img_label = QLabel()
            img_label.setFixedSize(90, 90)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            pixmap = QPixmap(90, 90)
            pixmap.fill(QColor(avatar["color"]))

            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.GlobalColor.white))
            painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
            painter.drawText(
                pixmap.rect(), Qt.AlignmentFlag.AlignCenter, avatar["nombre"][0]
            )
            painter.end()

            img_label.setPixmap(pixmap)
            layout.addWidget(img_label)

            # Nombre
            nombre = QLabel(avatar["nombre"])
            nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

    def cargar_archivo_avatar(self):
        """Cargar un archivo de imagen como avatar personalizado"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen para avatar",
            os.path.expanduser("~"),
            "Imágenes (*.png *.jpg *.jpeg *.gif *.bmp);;Todos (*.*)",
        )

        if file_path:
            # Validar que sea una imagen
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudo cargar la imagen. Asegúrate de que sea válida.",
                )
                return

            # Crear un diálogo de procesamiento
            msg = QMessageBox(self)
            msg.setWindowTitle("Subiendo avatar...")
            msg.setText("Por favor espera mientras se sube tu avatar")
            msg.show()
            QApplication.processEvents()

            try:
                # Subir archivo a través del API
                result = self.api_client.upload_avatar(file_path)
                msg.close()
                QApplication.processEvents()

                if result.get("success"):
                    # Crear objeto avatar con el ID retornado
                    avatar_id = result.get("avatar_id")
                    self.selected_avatar = {
                        "id": avatar_id,
                        "nombre": "Avatar personalizado",
                        "url": result.get("url"),
                        "is_custom": True,
                    }

                    # Actualizar la vista
                    self.crear_frame_avatar_custom()
                    pass  # Removed blocking dialog for seamlessness
                else:
                    error = result.get("error", "Error desconocido")
                    QMessageBox.critical(
                        self, "Error", f"Error al subir avatar: {error}"
                    )
            except Exception as e:
                msg.close()
                QApplication.processEvents()
                logger.error(f"Error uploading avatar: {e}")
                QMessageBox.critical(self, "Error", f"Error al subir avatar: {str(e)}")

    def crear_frame_avatar_custom(self):
        """Crear frame para el avatar personalizado cargado"""
        if not self.selected_avatar or not self.selected_avatar.get("is_custom"):
            return

        # Limpiar layout anterior si existe
        if self.avatars_layout.count() > 0:
            # Buscar y remover el avatar custom anterior
            for i in range(self.avatars_layout.count() - 1, -1, -1):
                widget = self.avatars_layout.itemAt(i).widget()
                if widget and hasattr(widget, "is_custom_avatar"):
                    self.avatars_layout.removeWidget(widget)
                    widget.deleteLater()

        frame = QFrame()
        frame.setObjectName("avatar-frame")
        frame.setProperty("class", "avatar-frame selected")
        frame.setFixedSize(120, 140)
        frame.setCursor(Qt.CursorShape.PointingHandCursor)
        frame.is_custom_avatar = True

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        # Contenedor de la imagen
        img_container = QLabel()
        img_container.setFixedSize(100, 100)
        img_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_container.setStyleSheet("border: none;")

        # Cargar imagen del avatar
        if self.selected_avatar.get("url"):
            try:
                response = requests.get(self.selected_avatar["url"], timeout=5)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    pixmap.loadFromData(response.content)
                    pixmap = pixmap.scaled(
                        90,
                        90,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    img_container.setPixmap(pixmap)
                else:
                    self.mostrar_iniciales(img_container, "CUSTOM")
            except:
                self.mostrar_iniciales(img_container, "CUSTOM")
        else:
            self.mostrar_iniciales(img_container, "CUSTOM")

        layout.addWidget(img_container)

        # Nombre del avatar
        nombre = QLabel("🆕 Personalizado")
        nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nombre.setStyleSheet("font-size: 11px; color: #2ecc71; font-weight: bold;")
        layout.addWidget(nombre)

        frame.mousePressEvent = lambda e: self.seleccionar_avatar(
            self.selected_avatar, frame
        )

        self.avatars_layout.insertWidget(0, frame)


class UserDialog(QDialog):
    def __init__(self, api_client, user_data=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = user_data
        self.selected_avatar = None  # Puede ser Dict
        self.setWindowTitle("Editar Usuario" if user_data else "Nuevo Usuario")
        self.setFixedWidth(650)
        self.setMinimumHeight(750)
        self.setup_ui()

        # Timer para validación en tiempo real
        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.validate_all_fields)

        if user_data:
            self.load_user_data()  # load_user_data establece selected_avatar correctamente
        else:
            self.set_default_avatar()

    def setup_ui(self):
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: #4b5563;
                font-weight: 600;
            }
            QLineEdit, QComboBox {
                padding: 12px 16px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f9fafb;
                color: #111827;
                margin-top: 6px;
                min-height: 22px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3b82f6;
                background-color: white;
            }
            QLineEdit.valid {
                border: 1px solid #10b981;
            }
            QLineEdit.invalid {
                border: 1px solid #ef4444;
            }
            QLabel.error {
                color: #ef4444;
                font-size: 12px;
                font-weight: 500;
                margin-bottom: 8px;
            }
            QLabel.success {
                color: #10b981;
                font-size: 12px;
                font-weight: 500;
            }
            QFrame#avatarContainer {
                background-color: #f3f4f6;
                border-radius: 50px;
                border: 2px solid #e5e7eb;
            }
            QPushButton#changeAvatarBtn {
                background-color: transparent;
                color: #3b82f6;
                font-size: 13px;
                font-weight: 600;
                border: none;
                text-decoration: underline;
                padding: 5px;
            }
            QPushButton#changeAvatarBtn:hover {
                color: #2563eb;
            }
            QProgressBar {
                border: none;
                background-color: #e5e7eb;
                height: 6px;
                border-radius: 3px;
                margin: 0px;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 3px;
            }
            QPushButton#saveBtn {
                background-color: #2563eb;
                color: white;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                border: none;
            }
            QPushButton#saveBtn:hover {
                background-color: #1d4ed8;
            }
            QPushButton#saveBtn:disabled {
                background-color: #94a3b8;
            }
            QPushButton#cancelBtn {
                background-color: white;
                color: #4b5563;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                border: 1px solid #d1d5db;
            }
            QPushButton#cancelBtn:hover {
                background-color: #f3f4f6;
            }
        """
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 30)
        main_layout.setSpacing(12)

        # Título
        title = QLabel("Editar Usuario" if self.user_data else "Nuevo Usuario")
        title.setStyleSheet(
            "font-size: 20px; color: #111827; font-weight: 700; margin-bottom: 15px;"
        )
        main_layout.addWidget(title)

        # Sección de Avatar
        avatar_section = QHBoxLayout()
        self.avatar_frame = QFrame()
        self.avatar_frame.setObjectName("avatarContainer")
        self.avatar_frame.setFixedSize(100, 100)
        self.avatar_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.avatar_frame.mousePressEvent = self.seleccionar_avatar

        avatar_inner_layout = QVBoxLayout(self.avatar_frame)
        avatar_inner_layout.setContentsMargins(0, 0, 0, 0)
        avatar_inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(80, 80)
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setStyleSheet("border: none; background: transparent;")
        avatar_inner_layout.addWidget(self.avatar_label)

        avatar_section.addWidget(self.avatar_frame)

        avatar_info = QVBoxLayout()
        avatar_info.setSpacing(2)
        avatar_info.addStretch()
        avatar_desc = QLabel("Foto de perfil")
        avatar_desc.setStyleSheet("font-size: 12px; font-weight: 400; color: #6b7280;")
        avatar_info.addWidget(avatar_desc)

        self.change_avatar_btn = QPushButton("Cambiar imagen")
        self.change_avatar_btn.setObjectName("changeAvatarBtn")
        self.change_avatar_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.change_avatar_btn.clicked.connect(self.seleccionar_avatar)
        avatar_info.addWidget(self.change_avatar_btn)
        avatar_info.addStretch()

        avatar_section.addLayout(avatar_info)
        avatar_section.addStretch()

        main_layout.addLayout(avatar_section)
        main_layout.addSpacing(10)

        # Campos del formulario
        def create_field(label_text, placeholder, is_password=False):
            container = QVBoxLayout()
            container.setSpacing(4)
            label = QLabel(label_text)
            container.addWidget(label)

            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            if is_password:
                field.setEchoMode(QLineEdit.EchoMode.Password)
            field.textChanged.connect(self.on_text_changed)
            container.addWidget(field)

            error_label = QLabel("")
            error_label.setProperty("class", "error")
            error_label.setWordWrap(True)
            container.addWidget(error_label)

            return field, error_label, container

        # Nombre
        self.nombre_input, self.nombre_error, name_cont = create_field(
            "Nombre Completo", "Ej: Juan Pérez"
        )
        main_layout.addLayout(name_cont)

        # Email
        self.email_input, self.email_error, email_cont = create_field(
            "Correo Electrónico", "correo@ejemplo.com"
        )
        main_layout.addLayout(email_cont)

        # Password (solo para nuevos)
        if not self.user_data:
            self.password_input, self.password_error, pass_cont = create_field(
                "Contraseña", "Mínimo 8 caracteres..."
            )
            main_layout.addLayout(pass_cont)

            # Contenedor de seguridad (separado para evitar solapamientos)
            security_layout = QVBoxLayout()
            security_layout.setContentsMargins(0, 5, 0, 10)
            security_layout.setSpacing(5)

            self.strength_label = QLabel("Nivel de seguridad:")
            self.strength_label.setStyleSheet(
                "font-size: 11px; color: #6b7280; font-weight: 500; margin-top: 5px;"
            )
            security_layout.addWidget(self.strength_label)

            self.password_strength = QProgressBar()
            self.password_strength.setRange(0, 100)
            self.password_strength.setValue(0)
            self.password_strength.setTextVisible(False)
            security_layout.addWidget(self.password_strength)

            main_layout.addLayout(security_layout)

            self.password_confirm_input, self.password_confirm_error, conf_cont = (
                create_field("Confirmar Contraseña", "Repite la contraseña")
            )
            main_layout.addLayout(conf_cont)

        # Rol y Estado en una fila
        row_layout = QHBoxLayout()

        rol_cont = QVBoxLayout()
        rol_cont.setSpacing(0)
        rol_cont.addWidget(QLabel("Rol"))
        self.rol_combo = QComboBox()
        self.rol_combo.addItems(["aprendiz", "administrador"])
        rol_cont.addWidget(self.rol_combo)
        row_layout.addLayout(rol_cont)

        estado_cont = QVBoxLayout()
        estado_cont.setSpacing(0)
        estado_cont.addWidget(QLabel("Estado"))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["activo", "inactivo"])
        estado_cont.addWidget(self.estado_combo)
        row_layout.addLayout(estado_cont)

        main_layout.addLayout(row_layout)
        main_layout.addSpacing(20)

        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.save_btn = QPushButton("Guardar Usuario")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.validate_and_accept)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(self.save_btn)

        main_layout.addLayout(buttons_layout)

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
        painter.setPen(QPen(Qt.GlobalColor.white))
        painter.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, iniciales)
        painter.end()

        self.avatar_label.setPixmap(pixmap)

    def seleccionar_avatar(self, event=None):
        """Abrir selector de avatar"""
        dialog = AvatarSelector(
            self.api_client, current_avatar=self.selected_avatar, parent=self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.selected_avatar = dialog.get_selected_avatar()
            self.actualizar_avatar()

    def actualizar_avatar(self):
        """Actualizar la vista del avatar"""
        if self.selected_avatar:
            # Primero intentar cargar por ruta local (lo más rápido)
            if self.selected_avatar.get("path") and os.path.exists(
                self.selected_avatar["path"]
            ):
                try:
                    pixmap = QPixmap(self.selected_avatar["path"])
                    if not pixmap.isNull():
                        pixmap = pixmap.scaled(
                            80,
                            80,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                        self.avatar_label.setPixmap(pixmap)
                        return
                except Exception as e:
                    logger.error(f"Error cargando avatar local: {e}")

            # Intentar por URL si existe
            elif self.selected_avatar.get("url"):
                try:
                    response = requests.get(self.selected_avatar["url"], timeout=5)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(response.content)
                        pixmap = pixmap.scaled(
                            80,
                            80,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
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
        if not self.user_data:
            return

        self.nombre_input.setText(self.user_data.get("nombre", ""))
        self.email_input.setText(self.user_data.get("email", ""))

        role = self.user_data.get("rol", "aprendiz")
        index = self.rol_combo.findText(role.capitalize())
        if index >= 0:
            self.rol_combo.setCurrentIndex(index)

        status = self.user_data.get("estado", "activo")
        index = self.estado_combo.findText(status.capitalize())
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)

        # Cargar avatar si existe
        # El servidor puede devolver 'avatar_id' (int) o 'avatar' (nombre string)
        avatar_id_val = self.user_data.get("avatar_id")  # int FK: 1,2,3...
        avatar_nombre = self.user_data.get("avatar")  # string: 'avatar_01'

        # Preferir avatar_id numérico; si no, intentar leerlo del nombre
        if avatar_id_val:
            # Construir nombre del archivo: 1 -> avatar_01.png
            try:
                nombre_archivo = f"avatar_{int(avatar_id_val):02d}"
            except Exception:
                nombre_archivo = str(avatar_nombre) if avatar_nombre else None
        elif avatar_nombre:
            nombre_archivo = avatar_nombre  # ya es 'avatar_01'
            # Intentar extraer el ID numérico del nombre
            try:
                avatar_id_val = int(str(avatar_nombre).replace("avatar_", ""))
            except Exception:
                avatar_id_val = None
        else:
            nombre_archivo = None

        if nombre_archivo:
            avatars_dir = resource_path(os.path.join("assets", "avatars"))
            path = os.path.join(avatars_dir, f"{nombre_archivo}.png")
            if os.path.exists(path):
                self.selected_avatar = {
                    "id": avatar_id_val,
                    "nombre": nombre_archivo,
                    "path": path,
                }
            else:
                self.selected_avatar = {
                    "id": avatar_id_val,
                    "nombre": nombre_archivo,
                    "url": self.user_data.get("avatar_url"),
                }
            self.actualizar_avatar()
        else:
            self.set_default_avatar()

        # Validar después de cargar
        self.nombre_input.textChanged.emit(self.nombre_input.text())
        self.email_input.textChanged.emit(self.email_input.text())

    def get_data(self):
        """Obtener datos del formulario"""
        data = {
            "nombre": self.nombre_input.text().strip(),
            "email": self.email_input.text().strip().lower(),
            "rol": self.rol_combo.currentText().lower(),
            "estado": self.estado_combo.currentText().lower(),
        }

        # Incluir avatar_id (entero) si hay avatar seleccionado
        if self.selected_avatar:
            av_id = self.selected_avatar.get("id")
            if av_id is not None:
                # Si es string tipo 'avatar_01', extraer el número
                if isinstance(av_id, str) and av_id.startswith("avatar_"):
                    try:
                        av_id = int(av_id.replace("avatar_", ""))
                    except Exception:
                        pass
                data["avatar_id"] = av_id

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
                background-color: #fafbfc;
            }
            QTableWidget {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f3f4f6;
                alternate-background-color: #f9fafb;
            }
            QTableWidget::item {
                padding: 10px 8px;
                vertical-align: center;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1f2937;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #f9fafb, stop:1 #f3f4f6);
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #4a90e2;
                font-weight: bold;
                font-size: 13px;
                color: #374151;
            }
            QLineEdit, QComboBox {
                padding: 10px 12px;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #4a90e2;
                background-color: #f8faff;
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
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #1f2937;")

        self.new_btn = QPushButton("Nuevo Usuario")
        self.new_btn.setFixedHeight(45)
        self.new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 140px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #357abd, stop:1 #1f4d7b);
            }
            QPushButton:pressed {
                padding: 11px 19px 9px 21px;
            }
        """
        )
        self.new_btn.clicked.connect(self.nuevo_usuario)

        self.refresh_btn = QPushButton("⟳")
        self.refresh_btn.setFixedSize(45, 45)
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_btn.setToolTip("Actualizar lista")
        self.refresh_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #10b981, stop:1 #059669);
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #059669, stop:1 #047857);
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
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

        # Controles de paginación
        pagination_layout = QHBoxLayout()
        pagination_layout.setSpacing(10)

        # Botones de paginación
        self.first_btn = QPushButton("◀◀")
        self.first_btn.setFixedSize(40, 35)
        self.first_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet(
            "font-size: 13px; color: #2c3e50; font-weight: bold;"
        )

        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(40, 35)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
        self.last_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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

        # Inicializar ToastNotification
        self.toast = ToastNotification(self)

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
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
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
            rol_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            rol_item.setFont(QFont("Segoe UI", 11))
            if usuario.get("rol") == "administrador":
                rol_item.setForeground(QColor("#e74c3c"))
                rol_item.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            else:
                rol_item.setForeground(QColor("#3498db"))
            self.table.setItem(row, 3, rol_item)

            # Acciones
            acciones = QWidget()
            acciones.setFixedHeight(50)
            acciones_layout = QHBoxLayout(acciones)
            acciones_layout.setContentsMargins(5, 0, 5, 0)
            acciones_layout.setSpacing(8)
            acciones_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Botón editar
            edit_btn = QPushButton("Editar")
            edit_btn.setFixedSize(70, 32)
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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

            # Botón estado: verde=activo, rojo=inactivo
            estado_btn = QPushButton("●")
            estado_btn.setFixedSize(32, 32)
            estado_btn.setCursor(Qt.CursorShape.PointingHandCursor)

            if usuario.get("estado") == "activo":
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
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            if not data.get("password"):
                QMessageBox.warning(self, "Error", "La contraseña es requerida")
                return

            # Forzar actualización de eventos
            QApplication.processEvents()

            # Procesar directamente sin QTimer
            self._procesar_nuevo_usuario(data, None)

    def _procesar_nuevo_usuario(self, data, msg):
        """Procesar creación de usuario"""
        try:
            # Mostrar feedback de guardado
            self.toast.show_saving("Guardando cambios...")

            result = self.api_client.create_usuario(data)
            QApplication.processEvents()

            if result["success"]:
                email_verified = result.get("email_verified", False)

                # Refrescar tabla inmediatamente
                self.cargar_usuarios(force_refresh=True)

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
                    self.toast.show_success("Cambios realizados")
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

                self.toast.show_error(f"Error al crear usuario:\n{error_msg}")
        except Exception as e:
            QApplication.processEvents()
            self.toast.show_error(f"Error inesperado: {str(e)}")

    def editar_usuario(self, usuario):
        dialog = UserDialog(self.api_client, usuario)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            # Forzar actualización de eventos
            QApplication.processEvents()

            # Procesar directamente sin QTimer
            self._procesar_editar_usuario(usuario["id"], data, None)

    def _procesar_editar_usuario(self, usuario_id, data, msg):
        """Procesar edición de usuario"""
        try:
            # Mostrar feedback de guardado
            self.toast.show_saving("Guardando cambios...")

            result = self.api_client.update_usuario(usuario_id, data)
            QApplication.processEvents()

            if result["success"]:
                # Refrescar tabla inmediatamente
                self.cargar_usuarios(force_refresh=True)
                self.toast.show_success("Cambios realizados")
            else:
                error_msg = result.get("error", "Error desconocido")
                if result.get("validation_errors"):
                    error_msg = "\n".join(result["validation_errors"])
                self.toast.show_error(f"Error al actualizar:\n{error_msg}")
        except Exception as e:
            QApplication.processEvents()
            self.toast.show_error(f"Error inesperado: {str(e)}")

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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
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
            # Actualizar localmente al instante para feedback visual inmediato
            nuevo_estado = "inactivo" if usuario["estado"] == "activo" else "activo"
            for u in self.usuarios:
                if u.get("id") == usuario["id"]:
                    u["estado"] = nuevo_estado
                    break
            for u in self.usuarios_filtrados:
                if u.get("id") == usuario["id"]:
                    u["estado"] = nuevo_estado
                    break
            self.actualizar_tabla()
            QApplication.processEvents()

            result = self.api_client.toggle_usuario_status(usuario["id"])

            # Cerrar mensaje de procesamiento
            msg.close()
            QApplication.processEvents()

            if result["success"]:
                # Refrescar desde servidor para confirmar estado real
                self.cargar_usuarios(force_refresh=True)
            else:
                # Revertir cambio local si falló
                for u in self.usuarios:
                    if u.get("id") == usuario["id"]:
                        u["estado"] = usuario["estado"]  # revertir
                        break
                self.actualizar_tabla()
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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
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
                # Refrescar tabla inmediatamente
                self.cargar_usuarios(force_refresh=True)
            else:
                QMessageBox.critical(self, "Error", f"Error: {result.get('error')}")
        except Exception as e:
            msg.close()
            QApplication.processEvents()
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
