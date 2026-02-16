from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QPixmap, QMovie
from utils.paths import resource_path
import os  # <-- IMPORTANTE: Faltaba este import


class Sidebar(QWidget):
    navigation_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(180)
        self.setMaximumWidth(240)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Variable para animación
        self.current_hover = None

        # Contenedor principal con color de fondo #AFCBFF
        main_container = QFrame(self)
        main_container.setObjectName("mainContainer")
        main_container.setStyleSheet(
            """
            QFrame#mainContainer {
                background-color: #AFCBFF;  /* Fondo azul claro para todo el contenedor */
                border-radius: 0px;
            }
        """
        )

        # Layout para el contenedor principal
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(2)

        # Logo con imagen
        logo_container = QFrame()
        logo_container.setFixedHeight(70)
        logo_container.setStyleSheet(
            """
            QFrame {
                background-color: #AFCBFF;
            }
        """
        )

        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 10, 0, 10)
        logo_layout.setAlignment(Qt.AlignCenter)

        # ===== CORREGIDO: Cargar imagen correctamente =====
        logo = QLabel()

        # Intentar cargar como PNG primero
        logo_path = resource_path(os.path.join("assets", "logo.png"))
        logo_pixmap = QPixmap(logo_path)

        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(
                140, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo.setPixmap(scaled_pixmap)
        else:
            # Si no hay imagen, mostrar texto
            logo.setText("VARCHATE")
            logo.setFont(QFont("Segoe UI", 16, QFont.Bold))
            logo.setStyleSheet(
                "color: #0099FF; letter-spacing: 1px; background-color: transparent;"
            )

        logo.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo)
        container_layout.addWidget(logo_container)

        # Espaciador
        spacer = QFrame()
        spacer.setFixedHeight(10)
        spacer.setStyleSheet("background-color: transparent;")
        container_layout.addWidget(spacer)

        # Botones con textos completos
        self.buttons = {}
        self.avatar_label = None  # Guardar referencia al avatar

        buttons_data = [
            ("dashboard", "Dashboard"),
            ("users", "Usuarios"),
            ("modules", "Módulos"),
            ("lessons", "Lecciones"),
            ("exercises", "Ejercicios"),
            ("evaluations", "Evaluaciones"),
        ]

        # Estilo para botones
        button_style = """
            QPushButton {
                text-align: left;
                padding: 14px 20px;
                border: none;
                color: #334155;
                font-size: 13px;
                font-weight: 500;
                min-width: 140px;
                margin: 2px 8px;
                border-radius: 8px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #e6f0ff;
                color: #0099FF;
            }
            QPushButton:checked {
                background-color: #0099FF;
                color: white;
                font-weight: 600;
            }
            QPushButton:pressed {
                background-color: #0077cc;
            }
        """

        for key, text in buttons_data:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda checked, k=key: self.navigate(k))
            self.buttons[key] = btn
            container_layout.addWidget(btn)

        container_layout.addStretch()

        # Separador
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #e2e8f0; margin: 10px 15px;")
        container_layout.addWidget(separator)

        # Información del usuario
        user_info = QFrame()
        user_info.setStyleSheet(
            """
            QFrame {
                background-color: #eef2f6;
                margin: 5px 10px;
                border-radius: 10px;
                padding: 5px;
            }
        """
        )
        user_layout = QVBoxLayout(user_info)
        user_layout.setContentsMargins(10, 10, 10, 10)
        user_layout.setSpacing(5)

        # Avatar con fondo azul
        self.avatar_label = QLabel("👤")
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setFont(QFont("Segoe UI", 20))
        self.avatar_label.setStyleSheet(
            "color: #0099FF; background-color: transparent;"
        )
        user_layout.addWidget(self.avatar_label)

        # Nombre de usuario
        self.user_name = QLabel("Admin")
        self.user_name.setAlignment(Qt.AlignCenter)
        self.user_name.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.user_name.setStyleSheet("color: #1e293b; background-color: transparent;")
        user_layout.addWidget(self.user_name)

        # Email
        self.user_email = QLabel("admin@varchate.com")
        self.user_email.setAlignment(Qt.AlignCenter)
        self.user_email.setFont(QFont("Segoe UI", 8))
        self.user_email.setStyleSheet("color: #64748b; background-color: transparent;")
        user_layout.addWidget(self.user_email)

        container_layout.addWidget(user_info)

        # Cerrar sesión
        self.logout_btn = QPushButton("🚪 Cerrar Sesión")
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.setStyleSheet(
            """
            QPushButton {
                color: #ef4444;
                border-top: 1px solid #e2e8f0;
                margin-top: 5px;
                border-radius: 0;
                font-weight: 500;
                background-color: transparent;
                text-align: left;
                padding: 14px 20px;
            }
            QPushButton:hover {
                background-color: #dc2626;
                color: white;
            }
        """
        )
        container_layout.addWidget(self.logout_btn)

        # Layout principal del widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_container)

        self.setLayout(main_layout)

    def set_user_info(self, nombre, email):
        """Actualizar información del usuario"""
        self.user_name.setText(nombre)
        self.user_email.setText(email)

        # Actualizar avatar con inicial
        if nombre and len(nombre) > 0:
            # Usar la primera letra del nombre
            inicial = nombre[0].upper()
            self.avatar_label.setText(inicial)

            # Animación suave al actualizar
            self.animate_avatar_update()

    def animate_avatar_update(self):
        """Animación al actualizar avatar"""
        if hasattr(self, "avatar_label"):
            anim = QPropertyAnimation(self.avatar_label, b"geometry")
            anim.setDuration(300)
            anim.setEasingCurve(QEasingCurve.OutBounce)

            original_rect = self.avatar_label.geometry()
            anim.setKeyValueAt(0, original_rect)
            anim.setKeyValueAt(0.5, original_rect.adjusted(-5, -5, 5, 5))
            anim.setKeyValueAt(1, original_rect)

            anim.start()

    def navigate(self, page):
        """Navegar a una página"""
        for btn in self.buttons.values():
            btn.setChecked(False)
        if page in self.buttons:
            self.buttons[page].setChecked(True)
            # Pequeña animación de clic
            self.animate_button_click(self.buttons[page])
        self.navigation_changed.emit(page)

    def set_selected(self, page):
        """Establecer página seleccionada sin emitir señal"""
        if page in self.buttons:
            for btn in self.buttons.values():
                btn.setChecked(False)
            self.buttons[page].setChecked(True)

    def animate_button_click(self, button):
        """Animación sutil al hacer clic"""
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(100)
        anim.setEasingCurve(QEasingCurve.OutQuad)

        original_rect = button.geometry()
        anim.setKeyValueAt(0, original_rect)
        anim.setKeyValueAt(0.5, original_rect.adjusted(2, 2, -2, -2))
        anim.setKeyValueAt(1, original_rect)

        anim.start()

    def enterEvent(self, event):
        """Efecto al entrar a la sidebar"""
        # Animación suave al expandir
        self.animate_width(180, 200)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Efecto al salir de la sidebar"""
        self.animate_width(200, 180)
        super().leaveEvent(event)

    def animate_width(self, start, end):
        """Animación de cambio de ancho"""
        anim = QPropertyAnimation(self, b"minimumWidth")
        anim.setDuration(200)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

    # ===== MÉTODO PARA CERRAR SESIÓN =====
    def connect_logout(self, callback):
        """Conectar el botón de logout con una función"""
        self.logout_btn.clicked.connect(callback)
