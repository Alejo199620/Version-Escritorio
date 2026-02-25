from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont

class ToastNotification(QFrame):
    """Notificación tipo toast elegante y reutilizable"""

    SUCCESS = "success"
    ERROR = "error"
    INFO = "info"
    SAVING = "saving"

    # Posiciones
    TOP_RIGHT = "top_right"
    CENTER = "center"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("toastNotification")
        
        # Inicialmente invisible y sin geometría
        self.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(12)

        # Icono
        self.icon_label = QLabel()
        self.icon_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.icon_label.setStyleSheet("color: white; background-color: rgba(0,0,0,0.1); border-radius: 12px; min-width: 24px; min-height: 24px;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)

        # Mensaje
        self.message_label = QLabel()
        self.message_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.message_label.setStyleSheet("color: white;")
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label, 1)

        # Botón cerrar
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 20px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 6px;
            }
        """
        )
        self.close_btn.clicked.connect(self.hide_with_animation)
        layout.addWidget(self.close_btn)

        # Animaciones
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)

        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_with_animation)

    def _apply_style(self, type):
        if type == self.SUCCESS:
            self.icon_label.setText("✓")
            self.message_label.setStyleSheet("color: white;")
            self.icon_label.setStyleSheet("color: white; background-color: rgba(0,0,0,0.1); border-radius: 12px; min-width: 24px; min-height: 24px;")
            self.close_btn.setStyleSheet("QPushButton { background-color: transparent; color: white; border: none; font-size: 20px; font-weight: bold; }")
            self.setStyleSheet("""
                QFrame#toastNotification {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                               stop:0 #10b981, stop:1 #059669);
                    border-radius: 12px;
                    border: 1px solid #047857;
                }
            """)
        elif type == self.ERROR:
            self.icon_label.setText("!")
            self.message_label.setStyleSheet("color: white;")
            self.icon_label.setStyleSheet("color: white; background-color: rgba(0,0,0,0.1); border-radius: 12px; min-width: 24px; min-height: 24px;")
            self.close_btn.setStyleSheet("QPushButton { background-color: transparent; color: white; border: none; font-size: 20px; font-weight: bold; }")
            self.setStyleSheet("""
                QFrame#toastNotification {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                               stop:0 #ef4444, stop:1 #dc2626);
                    border-radius: 12px;
                    border: 1px solid #b91c1c;
                }
            """)
        elif type == self.SAVING:
            self.icon_label.setText("⏳")
            self.message_label.setStyleSheet("color: #1f2937;")
            self.icon_label.setStyleSheet("color: #4a90e2; background-color: rgba(0,0,0,0.05); border-radius: 12px; min-width: 24px; min-height: 24px;")
            self.close_btn.setStyleSheet("QPushButton { background-color: transparent; color: #9ca3af; border: none; font-size: 20px; font-weight: bold; }")
            self.setStyleSheet("""
                QFrame#toastNotification {
                    background-color: white;
                    border-radius: 12px;
                    border: 2px solid #e5e7eb;
                }
            """)
        else: # INFO
            self.icon_label.setText("ℹ")
            self.message_label.setStyleSheet("color: white;")
            self.icon_label.setStyleSheet("color: white; background-color: rgba(0,0,0,0.1); border-radius: 12px; min-width: 24px; min-height: 24px;")
            self.close_btn.setStyleSheet("QPushButton { background-color: transparent; color: white; border: none; font-size: 20px; font-weight: bold; }")
            self.setStyleSheet("""
                QFrame#toastNotification {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                               stop:0 #3b82f6, stop:1 #2563eb);
                    border-radius: 12px;
                    border: 1px solid #1d4ed8;
                }
            """)

    def show_message(self, message, type=INFO, duration=5000, position=CENTER):
        """Mostrar notificación con animación"""
        self._apply_style(type)
        self.message_label.setText(message)

        # Ajustar tamaño
        self.adjustSize()

        if self.parent():
            parent_rect = self.parent().rect()
            
            if position == self.CENTER:
                x = (parent_rect.width() - self.width()) // 2
                y = (parent_rect.height() - self.height()) // 2
                target_pos = QPoint(x, y)
                start_pos = QPoint(x, y - 40) # Aparece desde arriba un poco
            else: # TOP_RIGHT
                margin = 20
                x = parent_rect.width() - self.width() - margin
                y = margin
                target_pos = QPoint(x, y)
                start_pos = QPoint(x, -self.height())

            self.setGeometry(target_pos.x(), target_pos.y(), self.width(), self.height())
            self.show()

            # Animar entrada
            self.slide_animation.setStartValue(start_pos)
            self.slide_animation.setEndValue(target_pos)
            self.slide_animation.start()

            self.fade_animation.setStartValue(0)
            self.fade_animation.setEndValue(1)
            self.fade_animation.start()

        # Auto-ocultar (no para SAVING, se oculta manualmente o con nueva llamada)
        if type != self.SAVING:
            self.timer.start(duration)
        else:
            self.timer.stop()

    def show_success(self, message, duration=5000, position=CENTER):
        self.show_message(message, self.SUCCESS, duration, position)

    def show_error(self, message, duration=5000, position=CENTER):
        self.show_message(message, self.ERROR, duration, position)
    
    def show_saving(self, message="Guardando cambios...", position=CENTER):
        self.show_message(message, self.SAVING, duration=0, position=position)

    def hide_with_animation(self):
        """Ocultar con animación"""
        self.timer.stop()

        if self.isVisible() and self.parent():
            current_pos = self.pos()
            # Si está centrado, se desvanece en el sitio, si es top_right sube
            if current_pos.y() > 100: # Heurística para saber si está abajo
                 end_pos = QPoint(current_pos.x(), current_pos.y() + 20)
            else:
                 end_pos = QPoint(current_pos.x(), -self.height() - 10)

            self.slide_animation.setStartValue(current_pos)
            self.slide_animation.setEndValue(end_pos)
            self.slide_animation.finished.connect(self.hide)
            self.slide_animation.start()

            self.fade_animation.setStartValue(self.windowOpacity())
            self.fade_animation.setEndValue(0)
            self.fade_animation.start()
