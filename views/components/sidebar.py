from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QFont, QPixmap, QMovie
from utils.paths import resource_path
import os


class Sidebar(QWidget):
    navigation_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(200)
        self.setMaximumWidth(260)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        # Variable para animación
        self.current_hover = None

        # Contenedor principal con color de fondo #AFCBFF
        main_container = QFrame(self)
        main_container.setObjectName("mainContainer")
        main_container.setStyleSheet(
            """
            QFrame#mainContainer {
                background-color: #AFCBFF;
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
        logo_container.setFixedHeight(80)
        logo_container.setStyleSheet(
            """
            QFrame {
                background-color: #AFCBFF;
            }
        """
        )

        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 15, 0, 15)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        logo_path = resource_path(os.path.join("assets", "logo.png"))
        logo_pixmap = QPixmap(logo_path)

        if not logo_pixmap.isNull():
            scaled_pixmap = logo_pixmap.scaled(
                160,
                60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo.setPixmap(scaled_pixmap)
        else:
            logo.setText("VARCHATE")
            logo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            logo.setStyleSheet(
                "color: #0099FF; letter-spacing: 1px; background-color: transparent;"
            )

        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo)
        container_layout.addWidget(logo_container)
        # Separador
        separator = QFrame()
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color: #e2e8f0; margin: 15px 20px;")
        container_layout.addWidget(separator)
        # Espaciador
        spacer = QFrame()
        spacer.setFixedHeight(15)
        spacer.setStyleSheet("background-color: transparent;")
        container_layout.addWidget(spacer)

        # Botones con textos completos
        self.buttons = {}
        self.avatar_label = None

        buttons_data = [
            ("dashboard", "Dashboard"),
            ("users", "Usuarios"),
            ("modules", "Módulos"),
            ("lessons", "Lecciones"),
            ("exercises", "Ejercicios"),
            ("evaluations", "Evaluaciones"),
        ]

        # Estilo MEJORADO para botones - texto centrado, más grande y negrita
        button_style = """
            QPushButton {
                text-align: center;
                padding: 16px 20px;
                border: none;
                color: #334155;
                font-size: 15px;
                font-weight: bold;
                min-width: 160px;
                margin: 4px 12px;
                border-radius: 10px;
                background-color: transparent;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #e6f0ff;
                color: #0099FF;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #0099FF;
                color: white;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #0077cc;
            }
        """

        for key, text in buttons_data:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda checked, k=key: self.navigate(k))
            self.buttons[key] = btn
            container_layout.addWidget(btn)

        container_layout.addStretch()

        # Información del usuario MEJORADA
        user_info = QFrame()
        user_info.setStyleSheet(
            """
            QFrame {
                background-color: #eef2f6;
                margin: 8px 15px;
                border-radius: 15px;
                padding: 12px;
            }
        """
        )
        user_layout = QVBoxLayout(user_info)
        user_layout.setContentsMargins(15, 15, 15, 15)
        user_layout.setSpacing(8)

        # Cerrar sesión MEJORADO
        self.logout_btn = QPushButton("🚪 Cerrar Sesión")
        self.logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_btn.setStyleSheet(
            """
            QPushButton {
                color: #ef4444;
                border-top: 2px solid #e2e8f0;
                margin-top: 10px;
                border-radius: 0;
                font-weight: bold;
                font-size: 14px;
                background-color: transparent;
                text-align: center;
                padding: 16px 20px;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #dc2626;
                color: white;
                font-weight: bold;
            }
        """
        )
        container_layout.addWidget(self.logout_btn)

        # Layout principal del widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_container)

        self.setLayout(main_layout)

    def navigate(self, page):
        """Navegar a una página"""
        for btn in self.buttons.values():
            btn.setChecked(False)
        if page in self.buttons:
            self.buttons[page].setChecked(True)
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
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        original_rect = button.geometry()
        anim.setKeyValueAt(0, original_rect)
        anim.setKeyValueAt(0.5, original_rect.adjusted(2, 2, -2, -2))
        anim.setKeyValueAt(1, original_rect)

        anim.start()

    def enterEvent(self, event):
        """Efecto al entrar a la sidebar"""
        self.animate_width(200, 220)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Efecto al salir de la sidebar"""
        self.animate_width(220, 200)
        super().leaveEvent(event)

    def animate_width(self, start, end):
        """Animación de cambio de ancho"""
        anim = QPropertyAnimation(self, b"minimumWidth")
        anim.setDuration(200)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

    def connect_logout(self, callback):
        """Conectar el botón de logout con una función"""
        self.logout_btn.clicked.connect(callback)
