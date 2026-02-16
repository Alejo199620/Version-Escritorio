from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from views.components.sidebar import Sidebar
from views.dashboard_view import DashboardView
from views.users_view import UsersView
from views.modules_view import ModulesView  # 👈 Usar el nuevo diseño
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

    def load_pages(self):
        """Cargar todas las páginas del panel"""
        self.dashboard_page = DashboardView(self.api_client)
        self.users_page = UsersView(self.api_client)
        self.modules_page = ModulesView(self.api_client)  # 👈 Nuevo diseño
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
