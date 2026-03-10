import os
import math
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame,
)
from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
    pyqtSignal,
    QPoint,
    QSize,
)
from PyQt6.QtGui import (
    QFont,
    QPixmap,
    QMovie,
    QPainter,
    QColor,
    QPen,
    QBrush,
    QPainterPath,
)
from controllers.api_client import APIClient
from views.main_window import MainWindow

from utils.paths import resource_path
from views.components.toast import ToastNotification


class SpinnerWidget(QWidget):
    """Widget de spinner giratorio moderno"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(30)

    def rotate(self):
        self.angle = (self.angle + 5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = QPoint(self.width() // 2, self.height() // 2)

        pen = QPen(QColor("#4361ee"), 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        # Círculo base
        pen.setColor(QColor("#e0e0e0"))
        painter.setPen(pen)
        painter.drawArc(center.x() - 15, center.y() - 15, 30, 30, 0, 360 * 16)

        # Arco giratorio
        pen.setColor(QColor("#4361ee"))
        painter.setPen(pen)
        span = 270 * 16
        start = self.angle * 16
        painter.drawArc(center.x() - 15, center.y() - 15, 30, 30, start, span)


class LoadingOverlay(QFrame):
    """Overlay de carga con bordes animados"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("loadingOverlay")

        # MODIFICADO: El overlay ahora cubre todo el padre
        self.setStyleSheet(
            """
            QFrame#loadingOverlay {
                background-color: rgba(0, 0, 0, 0.5);  /* Fondo negro semitransparente */
                border-radius: 25px;  /* Mantiene el border radius del contenedor */
            }
        """
        )

        # MODIFICADO: Ocupar todo el espacio del padre (todo el login)
        if parent:
            self.setGeometry(0, 0, parent.width(), parent.height())

        # Layout para centrar el contenido del loading
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        # Crear un contenedor interno para el contenido del loading
        loading_container = QFrame()
        loading_container.setObjectName("loadingContainer")
        loading_container.setStyleSheet(
            """
            QFrame#loadingContainer {
                background-color: rgba(255, 255, 255, 0.98);
                border-radius: 25px;
                border: 2px solid #4361ee;
            }
        """
        )
        loading_container.setFixedSize(300, 400)

        container_layout = QVBoxLayout(loading_container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.setSpacing(15)

        # Gato animado
        self.cat_label = QLabel()
        self.cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cat_label.setFixedSize(150, 150)

        gif_path = resource_path(os.path.join("assets", "cat_running.gif"))
        self.movie = QMovie(gif_path)
        if self.movie.isValid():
            self.movie.setScaledSize(QSize(130, 130))
            self.cat_label.setMovie(self.movie)
        else:
            self.cat_label.setText("🐱")
            self.cat_label.setFont(QFont("Segoe UI", 14))
            self.cat_label.setStyleSheet("color: #4361ee;")

        container_layout.addWidget(self.cat_label)

        # Spinner
        self.spinner = SpinnerWidget()
        container_layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        # Texto de carga
        self.loading_text = QLabel("Cargando...")
        self.loading_text.setFont(QFont("Segoe UI", 12))
        self.loading_text.setStyleSheet("color: #2c3e50; padding: 3px;")
        self.loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_text.setWordWrap(True)
        self.loading_text.setMaximumWidth(250)
        container_layout.addWidget(self.loading_text)

        # Puntos animados
        self.dots_label = QLabel("...")
        self.dots_label.setFont(QFont("Segoe UI", 16))
        self.dots_label.setStyleSheet("color: #4361ee;")
        self.dots_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.dots_label)

        # Texto de ADSO
        adso_text = QLabel("ADSO")
        adso_text.setFont(QFont("Segoe UI", 8))
        adso_text.setStyleSheet("color: #95a5a6; margin-top: 5px;")
        adso_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(adso_text)

        # BURBUJITAS ANIMADAS
        self.bubbles_widget = BubblesAnimation(loading_container)
        self.bubbles_widget.setGeometry(0, 0, 300, 400)
        self.bubbles_widget.lower()

        layout.addWidget(loading_container, 0, Qt.AlignmentFlag.AlignCenter)

        # Timers (tus timers originales)
        self.dots_timer = QTimer()
        self.dots_timer.timeout.connect(self.animate_dots)
        self.dots_count = 2

        self.message_timer = QTimer()
        self.message_timer.timeout.connect(self.cycle_messages)
        self.messages = [
            "Conectando...",
            "Verificando...",
            "Cargando info...",
            "Preparando panel...",
            "Casi listo...",
        ]
        self.message_index = 0

    def showEvent(self, event):
        if self.movie.isValid():
            self.movie.start()
        self.dots_timer.start(500)
        self.message_timer.start(2000)
        super().showEvent(event)

    def hideEvent(self, event):
        self.dots_timer.stop()
        self.message_timer.stop()
        if self.movie.isValid():
            self.movie.stop()
        super().hideEvent(event)

    def animate_dots(self):
        self.dots_count = (self.dots_count + 1) % 4
        self.dots_label.setText("." * self.dots_count)

    def cycle_messages(self):
        self.message_index = (self.message_index + 1) % len(self.messages)
        self.loading_text.setText(self.messages[self.message_index])

    def set_message(self, message):
        self.loading_text.setText(message)


class BubblesAnimation(QWidget):
    """Widget con burbujas animadas en los bordes"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.bubbles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bubbles)
        self.timer.start(50)  # 20 fps

        # Crear burbujas
        for i in range(8):  # 8 burbujas alrededor
            self.bubbles.append(
                {
                    "pos": i * 45,  # Posición angular
                    "size": 8 + i % 3 * 2,  # Tamaño variable
                    "speed": 2 + i % 4,  # Velocidad variable
                    "alpha": 100 + i * 20,  # Transparencia
                }
            )

    def update_bubbles(self):
        """Actualizar posición de burbujas"""
        for bubble in self.bubbles:
            bubble["pos"] = (bubble["pos"] + bubble["speed"]) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 20

        for bubble in self.bubbles:
            # Calcular posición alrededor del borde
            angle = bubble["pos"] * 3.14159 / 180
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)

            # Dibujar burbuja
            color = QColor(67, 97, 238, bubble["alpha"])  # #4361ee con transparencia
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(int(x), int(y)), bubble["size"], bubble["size"])


class LoginWindow(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Varchate Admin - Login")
        self.setFixedSize(800, 600)

        #  QUITAR BORDES DE WINDOWS
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Variables para arrastrar la ventana
        self.drag_position = None
        self.is_dragging = False

        self.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
            }
        """
        )

        self.setup_ui()
        # Conectar señal de error a nuestro método mejorado
        self.api_client.error_occurred.connect(self.show_elegant_error)

        # CONFIGURACIÓN DE AUTO-LOGIN PARA PRUEBAS
        # Se puede desactivar cambiando False o usando una variable de entorno
        self.auto_login_enabled = False

        if self.auto_login_enabled:
            self.email_input.setText("alejo29.c@gmail.com")
            self.password_input.setText("Password123")
            # Iniciar login automáticamente después de un breve delay para que se vea la UI
            QTimer.singleShot(1000, self.handle_login)

    def showEvent(self, event):
        super().showEvent(event)
        # Iniciar animación de opacidad al mostrar
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def setup_ui(self):

        # Layout principal con márgenes para la sombra
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Contenedor principal
        main_container = QFrame()
        main_container.setObjectName("mainContainer")
        main_container.setFixedSize(760, 520)
        main_container.setStyleSheet(
            """
            QFrame#mainContainer {
                background-color: white;
                border-radius: 25px;
                position: relative;
            }
        """
        )

        # Layout vertical para el contenedor (para la barra de título + contenido)
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        #  BARRA DE TÍTULO PERSONALIZADA - MODIFICADA
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet(
            """
            QWidget#titleBar {
                background-color: #2c3e50;  /* Azul oscuro pero no muy oscuro */
                border-top-left-radius: 25px;
                border-top-right-radius: 25px;
            }
            QWidget#titleBar:hover {
                background-color: #34495e;  /* Un tono más claro al hover */
            }
        """
        )

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 15, 0)
        title_layout.setSpacing(8)

        # Título de la ventana - AHORA BLANCO
        window_title = QLabel("Bienvenido a Varchate - Admin")
        window_title.setStyleSheet(
            """
            QLabel {
                color: white;  /* Texto blanco */
                font-weight: bold;
                font-size: 20px;
            }
        """
        )
        title_layout.addWidget(window_title)

        title_layout.addStretch()

        # Botón minimizar - MODIFICADO
        self.min_btn = QPushButton("─")
        self.min_btn.setFixedSize(30, 30)
        self.min_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;  /* Texto blanco */
                border: none;
                font-size: 16px;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #34495e;  /* Azul más claro al hover */
                color: white;
            }
        """
        )
        self.min_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.min_btn)

        # Botón cerrar - MODIFICADO
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;  /* Texto blanco */
                border: none;
                font-size: 14px;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #e74c3c;  /* Rojo al hover (se mantiene) */
                color: white;
            }
        """
        )
        self.close_btn.clicked.connect(self.close)
        title_layout.addWidget(self.close_btn)

        container_layout.addWidget(title_bar)

        # Contenido (tu HBox con left_panel y right_panel)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # PANEL IZQUIERDO - SOLO IMAGEN
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(340)
        left_panel.setStyleSheet(
            """
            QFrame#leftPanel {
                background-color: #4361ee;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 25px;
            }
            """
        )

        # Layout sin márgenes para que la imagen ocupe todo
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        left_layout.setSpacing(0)

        # GIF en el panel izquierdo - OCUPA TODO
        self.left_cat = QLabel()
        self.left_cat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_cat.setFixedSize(340, 470)  # Mismo tamaño que el panel

        cat_path = resource_path(os.path.join("assets", "login_cat.png"))
        left_movie = QMovie(cat_path)
        if left_movie.isValid():
            # Escalar para que ocupe todo el espacio disponible
            left_movie.setScaledSize(QSize(340, 560))
            self.left_cat.setMovie(left_movie)
            left_movie.start()

            # Opcional: Si quieres que la imagen cubra todo sin deformarse
            self.left_cat.setScaledContents(True)
        else:
            # Fallback si no hay imagen
            self.left_cat.setText("🐱")
            self.left_cat.setFont(QFont("Segoe UI", 60))
            self.left_cat.setStyleSheet("color: white;")

        left_layout.addWidget(self.left_cat)

        # PANEL DERECHO
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_panel.setStyleSheet(
            """
            QFrame#rightPanel {
                background-color: #f0f8ff;  /* Azul muy clarito - Alice Blue */
                border-top-right-radius: 0px;
                border-bottom-right-radius: 25px;
            }
        """
        )

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(50, 40, 50, 40)
        right_layout.setSpacing(15)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        title = QLabel("Iniciar Sesión")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtítulo
        subtitle = QLabel("Ingresa tus credenciales")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; font-size: 13px; margin-bottom: 20px;")

        # Campo email - FONDO BLANCO
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        self.email_input.setStyleSheet(
            """
            QLineEdit {
                padding: 14px 16px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #1f2937;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
                background-color: #f8faff;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """
        )

        # Campo password - MEJORADO
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(
            """
            QLineEdit {
                padding: 14px 16px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #1f2937;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
                background-color: #f8faff;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """
        )
        #  AÑADE LAS CONEXIONES AQUÍ, DESPUÉS DE CREAR LOS INPUTS
        self.email_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

        # Botón de login - MEJORADO
        self.login_btn = QPushButton("Acceder")
        self.login_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                padding: 14px 16px;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #357abd, stop:1 #1f4d7b);
            }
            QPushButton:pressed {
                padding: 15px 15px 13px 17px;
            }
            QPushButton:disabled {
                background-color: #d1d5db;
                color: #9ca3af;
            }
        """
        )
        self.login_btn.clicked.connect(self.handle_login)

        right_layout.addWidget(title)
        right_layout.addWidget(subtitle)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.email_input)
        right_layout.addSpacing(5)
        right_layout.addWidget(self.password_input)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.login_btn)

        # Unir paneles al content_layout
        content_layout.addWidget(left_panel)
        content_layout.addWidget(right_panel)

        container_layout.addLayout(content_layout)

        # Agregar contenedor principal al layout
        main_layout.addWidget(main_container, 0, Qt.AlignmentFlag.AlignCenter)

        # Crear toast notification como hijo del main_container
        self.toast = ToastNotification(main_container)

        # Overlay de carga
        self.loading_overlay = LoadingOverlay(main_container)
        self.loading_overlay.hide()

        self.email_input.setFocus()

    #  MÉTODOS PARA ARRASTRAR LA VENTANA
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Solo arrastrar si se hace clic en la barra de título
            if event.position().y() <= 40:  # Altura de la barra de título
                self.drag_position = (
                    event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                )
                self.is_dragging = True
                event.accept()

    def mouseMoveEvent(self, event):
        if (
            event.buttons() & Qt.MouseButton.LeftButton
            and self.is_dragging
            and self.drag_position
        ):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        self.drag_position = None

    #  MÉTODOS DE LOGIN (sin cambios)
    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            self.show_elegant_error("Por favor, completa todos los campos")
            return

        self.loading_overlay.show()
        self.loading_overlay.set_message("Iniciando sesión...")

        self.email_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Ingresando...")

        QTimer.singleShot(800, lambda: self.do_login(email, password))

    def do_login(self, email, password):
        result = self.api_client.login(email, password)

        if result["success"]:
            self.loading_overlay.set_message("¡Bienvenido! Cargando panel...")
            QTimer.singleShot(1500, self.open_main_window)
        else:
            self.loading_overlay.hide()
            self.email_input.setEnabled(True)
            self.password_input.setEnabled(True)
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Acceder")

            self.email_input.setFocus()
            if "error" in result:
                self.show_elegant_error(result["error"])

    def open_main_window(self):
        self.main_window = MainWindow(self.api_client)
        self.main_window.show()
        self.close()

    def show_elegant_error(self, message):
        """Mostrar error de manera elegante sin modificar el diseño"""
        self.loading_overlay.hide()
        self.email_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Acceder")

        self.email_input.setFocus()

        self.toast.show_error(message)
        self.shake_widget(self.email_input)
        self.shake_widget(self.password_input)

    def shake_widget(self, widget):
        """Animación de shake para campos con error"""
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(100)
        anim.setLoopCount(3)
        anim.setKeyValueAt(0, widget.pos())
        anim.setKeyValueAt(0.25, widget.pos() + QPoint(5, 0))
        anim.setKeyValueAt(0.5, widget.pos() - QPoint(5, 0))
        anim.setKeyValueAt(0.75, widget.pos() + QPoint(5, 0))
        anim.setKeyValueAt(1, widget.pos())
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

        original_style = widget.styleSheet()
        widget.setStyleSheet(original_style + "border-color: #e74c3c;")
        QTimer.singleShot(1000, lambda: widget.setStyleSheet(original_style))

    def show_error(self, message):
        """Mantener compatibilidad con la señal original"""
        self.show_elegant_error(message)
