class StyleHelper:
    """
    Clase helper que centraliza la definición de estilos y colores
    para mantener consistencia visual en toda la aplicación.
    """

    # Paleta de colores principal
    PRIMARY_COLOR = "#4361ee"
    SECONDARY_COLOR = "#3f37c9"
    SUCCESS_COLOR = "#4cc9f0"
    DANGER_COLOR = "#f72585"
    WARNING_COLOR = "#f8961e"
    INFO_COLOR = "#4895ef"
    LIGHT_BG = "#f8f9fa"
    DARK_BG = "#212529"
    BORDER_COLOR = "#dee2e6"

    @staticmethod
    def card_style() -> str:
        """Estilo para tarjetas con efecto hover"""
        return """
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
            QFrame:hover {
                border: 2px solid #4361ee;
                background-color: #f8f9fa;
            }
        """

    @staticmethod
    def button_primary() -> str:
        """Estilo para botón principal"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {StyleHelper.SECONDARY_COLOR};
            }}
        """

    @staticmethod
    def button_secondary() -> str:
        """Estilo para botón secundario"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.SECONDARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #362d80;
            }}
        """

    @staticmethod
    def button_success() -> str:
        """Estilo para botón de éxito/confirmación"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.SUCCESS_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #3aa8d8;
            }}
        """

    @staticmethod
    def button_danger() -> str:
        """Estilo para botón de peligro/eliminación"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.DANGER_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #d91c72;
            }}
        """

    @staticmethod
    def button_warning() -> str:
        """Estilo para botón de advertencia"""
        return f"""
            QPushButton {{
                background-color: {StyleHelper.WARNING_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #e07c0e;
            }}
        """

    @staticmethod
    def badge_active() -> str:
        """Estilo para badge de estado activo"""
        return """
            QLabel {
                background-color: #d1fae5;
                color: #065f46;
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 11px;
                font-weight: bold;
            }
        """

    @staticmethod
    def badge_inactive() -> str:
        """Estilo para badge de estado inactivo"""
        return """
            QLabel {
                background-color: #fee2e2;
                color: #991b1b;
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 11px;
                font-weight: bold;
            }
        """

    @staticmethod
    def badge_draft() -> str:
        """Estilo para badge de estado borrador"""
        return """
            QLabel {
                background-color: #fff3cd;
                color: #856404;
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 11px;
                font-weight: bold;
            }
        """
