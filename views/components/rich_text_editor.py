from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QToolBar,
    QAction,
    QColorDialog,
    QFontComboBox,
    QComboBox,
    QApplication,
    QDialog,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QFont, QColor, QTextListFormat
import logging
from utils.paths import resource_path

logger = logging.getLogger(__name__)


class LinkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insertar Enlace")
        self.setFixedSize(400, 150)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://ejemplo.com")
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Texto
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("Texto:"))
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Texto del enlace")
        text_layout.addWidget(self.text_input)
        layout.addLayout(text_layout)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {"url": self.url_input.text(), "text": self.text_input.text()}


class RichTextEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QWidget()
        toolbar.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-bottom: none;
            }
            QPushButton, QComboBox, QFontComboBox {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                margin: 2px;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
            QPushButton:checked {
                background-color: #007bff;
                color: white;
            }
        """
        )

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        toolbar_layout.setSpacing(2)

        # Fuente
        self.font_combo = QFontComboBox()
        self.font_combo.setFixedWidth(140)
        self.font_combo.currentFontChanged.connect(self.change_font)
        toolbar_layout.addWidget(self.font_combo)

        # Tamaño
        self.size_combo = QComboBox()
        self.size_combo.addItems(
            [
                "8",
                "9",
                "10",
                "11",
                "12",
                "14",
                "16",
                "18",
                "20",
                "22",
                "24",
                "26",
                "28",
                "36",
                "48",
                "72",
            ]
        )
        self.size_combo.setEditable(True)
        self.size_combo.setCurrentText("12")
        self.size_combo.setFixedWidth(60)
        self.size_combo.currentTextChanged.connect(self.change_font_size)
        toolbar_layout.addWidget(self.size_combo)

        toolbar_layout.addSpacing(10)

        # Estilos
        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.setFixedWidth(30)
        self.bold_btn.setStyleSheet("font-weight: bold;")
        self.bold_btn.clicked.connect(self.toggle_bold)
        toolbar_layout.addWidget(self.bold_btn)

        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.setFixedWidth(30)
        self.italic_btn.setStyleSheet("font-style: italic;")
        self.italic_btn.clicked.connect(self.toggle_italic)
        toolbar_layout.addWidget(self.italic_btn)

        self.underline_btn = QPushButton("U")
        self.underline_btn.setCheckable(True)
        self.underline_btn.setFixedWidth(30)
        self.underline_btn.setStyleSheet("text-decoration: underline;")
        self.underline_btn.clicked.connect(self.toggle_underline)
        toolbar_layout.addWidget(self.underline_btn)

        toolbar_layout.addSpacing(10)

        # Color
        self.color_btn = QPushButton("🎨")
        self.color_btn.setFixedWidth(40)
        self.color_btn.setToolTip("Color de texto")
        self.color_btn.clicked.connect(self.change_color)
        toolbar_layout.addWidget(self.color_btn)

        # Alineación
        self.align_left_btn = QPushButton("◀")
        self.align_left_btn.setCheckable(True)
        self.align_left_btn.setFixedWidth(30)
        self.align_left_btn.setToolTip("Alinear izquierda")
        self.align_left_btn.clicked.connect(
            lambda: self.editor.setAlignment(Qt.AlignLeft)
        )
        toolbar_layout.addWidget(self.align_left_btn)

        self.align_center_btn = QPushButton("⬤")
        self.align_center_btn.setCheckable(True)
        self.align_center_btn.setFixedWidth(30)
        self.align_center_btn.setToolTip("Centrar")
        self.align_center_btn.clicked.connect(
            lambda: self.editor.setAlignment(Qt.AlignCenter)
        )
        toolbar_layout.addWidget(self.align_center_btn)

        self.align_right_btn = QPushButton("▶")
        self.align_right_btn.setCheckable(True)
        self.align_right_btn.setFixedWidth(30)
        self.align_right_btn.setToolTip("Alinear derecha")
        self.align_right_btn.clicked.connect(
            lambda: self.editor.setAlignment(Qt.AlignRight)
        )
        toolbar_layout.addWidget(self.align_right_btn)

        self.align_justify_btn = QPushButton("☰")
        self.align_justify_btn.setCheckable(True)
        self.align_justify_btn.setFixedWidth(30)
        self.align_justify_btn.setToolTip("Justificar")
        self.align_justify_btn.clicked.connect(
            lambda: self.editor.setAlignment(Qt.AlignJustify)
        )
        toolbar_layout.addWidget(self.align_justify_btn)

        toolbar_layout.addSpacing(10)

        # Listas
        self.bullet_list_btn = QPushButton("•")
        self.bullet_list_btn.setFixedWidth(30)
        self.bullet_list_btn.setToolTip("Lista con viñetas")
        self.bullet_list_btn.clicked.connect(self.insert_bullet_list)
        toolbar_layout.addWidget(self.bullet_list_btn)

        self.number_list_btn = QPushButton("1.")
        self.number_list_btn.setFixedWidth(30)
        self.number_list_btn.setToolTip("Lista numerada")
        self.number_list_btn.clicked.connect(self.insert_number_list)
        toolbar_layout.addWidget(self.number_list_btn)

        toolbar_layout.addSpacing(10)

        # Insertar
        self.link_btn = QPushButton("🔗")
        self.link_btn.setFixedWidth(40)
        self.link_btn.setToolTip("Insertar enlace")
        self.link_btn.clicked.connect(self.insert_link)
        toolbar_layout.addWidget(self.link_btn)

        self.image_btn = QPushButton("🖼️")
        self.image_btn.setFixedWidth(40)
        self.image_btn.setToolTip("Insertar imagen")
        self.image_btn.clicked.connect(self.insert_image)
        toolbar_layout.addWidget(self.image_btn)

        toolbar_layout.addStretch()

        layout.addWidget(toolbar)

        # Editor
        self.editor = QTextEdit()
        self.editor.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #dee2e6;
                border-top: none;
                padding: 10px;
                background-color: white;
                font-size: 14px;
            }
        """
        )

        # Conectar señales
        self.editor.selectionChanged.connect(self.update_format_buttons)
        self.editor.cursorPositionChanged.connect(self.update_format_buttons)

        layout.addWidget(self.editor)

    def setHtml(self, html):
        """Establecer contenido HTML"""
        try:
            if html and isinstance(html, str):
                self.editor.setHtml(html)
            else:
                self.editor.clear()
        except Exception as e:
            logger.error(f"Error al establecer HTML: {e}")
            self.editor.clear()

    def toHtml(self):
        """Obtener contenido HTML"""
        try:
            html = self.editor.toHtml()
            # Asegurar que no está vacío
            if not html or html == "<p></p>" or html == "<p><br></p>":
                return ""
            return html
        except Exception as e:
            logger.error(f"Error al obtener HTML: {e}")
            return ""

    def toPlainText(self):
        """Obtener texto plano"""
        try:
            return self.editor.toPlainText()
        except Exception as e:
            logger.error(f"Error al obtener texto plano: {e}")
            return ""

    def clear(self):
        """Limpiar editor"""
        self.editor.clear()

    def change_font(self, font):
        if self.editor.textCursor().hasSelection():
            fmt = QTextCharFormat()
            fmt.setFont(font)
            self.editor.mergeCurrentCharFormat(fmt)

    def change_font_size(self, size):
        try:
            size = int(size)
            if self.editor.textCursor().hasSelection():
                fmt = QTextCharFormat()
                fmt.setFontPointSize(size)
                self.editor.mergeCurrentCharFormat(fmt)
        except ValueError:
            pass

    def toggle_bold(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontWeight(
            QFont.Bold if not fmt.fontWeight() == QFont.Bold else QFont.Normal
        )
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.editor.mergeCurrentCharFormat(fmt)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.editor.mergeCurrentCharFormat(fmt)

    def insert_bullet_list(self):
        cursor = self.editor.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)

    def insert_number_list(self):
        cursor = self.editor.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)

    def insert_link(self):
        dialog = LinkDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data["url"] and data["text"]:
                html = f'<a href="{data["url"]}">{data["text"]}</a>'
                self.editor.insertHtml(html)

    def insert_image(self):
        # Por ahora solo insertamos placeholder
        self.editor.insertHtml(
            '<img src="placeholder.jpg" alt="Imagen" style="max-width: 100%;">'
        )
        QMessageBox.information(
            self,
            "Info",
            "En una versión completa podrías seleccionar imágenes de tu computadora",
        )

    def update_format_buttons(self):
        # Actualizar estado de los botones según el formato actual
        fmt = self.editor.currentCharFormat()

        self.bold_btn.setChecked(fmt.fontWeight() == QFont.Bold)
        self.italic_btn.setChecked(fmt.fontItalic())
        self.underline_btn.setChecked(fmt.fontUnderline())

        # Actualizar alineación
        alignment = self.editor.alignment()
        self.align_left_btn.setChecked(alignment == Qt.AlignLeft)
        self.align_center_btn.setChecked(alignment == Qt.AlignCenter)
        self.align_right_btn.setChecked(alignment == Qt.AlignRight)
        self.align_justify_btn.setChecked(alignment == Qt.AlignJustify)

        # Actualizar fuente y tamaño
        if fmt.font().family():
            index = self.font_combo.findText(fmt.font().family())
            if index >= 0:
                self.font_combo.setCurrentIndex(index)

        if fmt.fontPointSize() > 0:
            self.size_combo.setCurrentText(str(int(fmt.fontPointSize())))
