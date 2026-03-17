from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget,
    QApplication, QStatusBar, QLabel
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from views.components.sidebar import Sidebar
from views.dashboard_view import DashboardView
from views.users_view import UsersView
from views.modules_view import ModulesView
from views.lessons_view import LessonsView
from views.exercises_view import ExercisesView
from views.evaluations_view import EvaluationsView
from utils.paths import resource_path


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Varchate Admin - Panel de Control")
        self.setMinimumSize(1300, 800)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_changed.connect(self.change_page)
        self.sidebar.connect_logout(self.handle_logout)
        main_layout.addWidget(self.sidebar)

        # Contenido principal
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(
            """
            QStackedWidget {
                background-color: #f8f9fa;
            }
        """
        )
        main_layout.addWidget(self.content_stack, 1)

        # Cargar páginas
        self.load_pages()

        # Mostrar dashboard por defecto
        self.sidebar.set_selected("dashboard")

        # ─── Status bar de sincronización ───────────────────────────────
        self._setup_status_bar()

    def _setup_status_bar(self):
        """Barra de estado inferior con indicador de conexión/sincronización."""
        bar = QStatusBar(self)
        bar.setSizeGripEnabled(False)
        bar.setFixedHeight(26)
        bar.setStyleSheet("""
            QStatusBar {
                background-color: #f1f5f9;
                border-top: 1px solid #e2e8f0;
                padding: 0 12px;
            }
            QStatusBar QLabel {
                font-size: 12px;
                color: #475569;
                background: transparent;
                border: none;
                padding: 0;
            }
        """)
        self.setStatusBar(bar)

        # Indicador (esquina derecha)
        self._status_label = QLabel("🟢  Conectado")
        self._status_label.setFont(QFont("Segoe UI", 9))
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._status_label.setStyleSheet("padding-right: 10px;")
        bar.addPermanentWidget(self._status_label)

        # Timer para resetear el estado
        self._status_reset_timer = QTimer(self)
        self._status_reset_timer.setSingleShot(True)
        self._status_reset_timer.timeout.connect(self._on_status_idle)

        # Contador de peticiones activas (para no resetear antes de tiempo)
        self._active_requests = 0

        # Conectar señales del api_client
        self.api_client.request_started.connect(self._on_request_started)
        self.api_client.request_finished.connect(self._on_request_finished)
        self.api_client.error_occurred.connect(self._on_error)

    def _on_request_started(self):
        self._active_requests += 1
        self._status_reset_timer.stop()
        self._status_label.setText("🔄  Sincronizando...")
        self._status_label.setStyleSheet("color: #2563eb;")

    def _on_request_finished(self):
        self._active_requests = max(0, self._active_requests - 1)
        if self._active_requests == 0:
            # Esperar 600 ms antes de mostrar "Conectado" para que no parpadee
            self._status_reset_timer.start(600)

    def _on_error(self, msg: str):
        self._active_requests = 0
        self._status_label.setText("🔴  Sin conexión")
        self._status_label.setStyleSheet("color: #dc2626;")
        # Volver a "Conectado" después de 4 s
        self._status_reset_timer.start(4000)

    def _on_status_idle(self):
        self._status_label.setText("🟢  Conectado")
        self._status_label.setStyleSheet("color: #16a34a;")

    def load_pages(self):
        """Cargar todas las páginas del panel"""
        self.dashboard_page = DashboardView(self.api_client)
        self.users_page = UsersView(self.api_client)
        self.modules_page = ModulesView(self.api_client)
        self.lessons_page = LessonsView(self.api_client)
        self.exercises_page = ExercisesView(self.api_client)
        self.evaluations_page = EvaluationsView(self.api_client)

        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.users_page)
        self.content_stack.addWidget(self.modules_page)
        self.content_stack.addWidget(self.lessons_page)
        self.content_stack.addWidget(self.exercises_page)
        self.content_stack.addWidget(self.evaluations_page)

    def change_page(self, page_name):
        """Cambiar la página actual"""
        pages = {
            "dashboard": 0,
            "users": 1,
            "modules": 2,
            "lessons": 3,
            "exercises": 4,
            "evaluations": 5,
        }

        if page_name in pages:
            self.content_stack.setCurrentIndex(pages[page_name])
            self.setWindowTitle(f"Varchate Admin - {page_name.capitalize()}")

    def handle_logout(self):
        """Cerrar sesión y volver al login"""
        try:
            self.api_client.logout()
        except Exception:
            pass
        from views.login_window import LoginWindow
        self.login_window = LoginWindow(self.api_client)
        self.login_window.show()
        self.close()
