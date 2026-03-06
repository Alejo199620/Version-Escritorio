from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QToolBar,
    QColorDialog,
    QFontComboBox,
    QComboBox,
    QApplication,
    QDialog,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
    QMessageBox,
    QFileDialog,
    QFormLayout,
    QSpinBox,
)
from PyQt6.QtCore import Qt, QSize, QByteArray, QBuffer, QIODevice, QUrl, QEvent
from PyQt6.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QFont,
    QColor,
    QTextListFormat,
    QAction,
    QImage,
    QTextDocument,
)
import logging
import base64
import os
import mimetypes
from utils.paths import resource_path

logger = logging.getLogger(__name__)


class ImageResizeDialog(QDialog):
    def __init__(self, current_w, current_h, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Redimensionar Imagen")
        self.setFixedSize(300, 160)
        self.ratio = current_w / current_h if current_h > 0 else 1
        
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #1e293b;
                font-size: 13px;
                font-weight: 500;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                background-color: #f8fafc;
                color: #0f172a;
                font-size: 13px;
            }
            QPushButton {
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
                padding: 6px 12px;
                color: #0f172a;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            """
        )
        
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        self.w_input = QSpinBox()
        self.w_input.setRange(10, 2000)
        self.w_input.setValue(int(current_w))
        
        self.h_input = QSpinBox()
        self.h_input.setRange(10, 2000)
        self.h_input.setValue(int(current_h))
        
        form.addRow("Ancho (px):", self.w_input)
        form.addRow("Alto (px):", self.h_input)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.w_input.valueChanged.connect(self._update_h)
        self.h_input.valueChanged.connect(self._update_w)
        
        self.updating = False

    def _update_h(self, w):
        if not self.updating and self.ratio > 0:
            self.updating = True
            self.h_input.setValue(int(w / self.ratio))
            self.updating = False

    def _update_w(self, h):
        if not self.updating and self.ratio > 0:
            self.updating = True
            self.w_input.setValue(int(h * self.ratio))
            self.updating = False
            
    def get_data(self):
        return self.w_input.value(), self.h_input.value()


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
        self.size_combo.setCurrentText("14")
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
            lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignLeft)
        )
        toolbar_layout.addWidget(self.align_left_btn)

        self.align_center_btn = QPushButton("⬤")
        self.align_center_btn.setCheckable(True)
        self.align_center_btn.setFixedWidth(30)
        self.align_center_btn.setToolTip("Centrar")
        self.align_center_btn.clicked.connect(
            lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        )
        toolbar_layout.addWidget(self.align_center_btn)

        self.align_right_btn = QPushButton("▶")
        self.align_right_btn.setCheckable(True)
        self.align_right_btn.setFixedWidth(30)
        self.align_right_btn.setToolTip("Alinear derecha")
        self.align_right_btn.clicked.connect(
            lambda: self.editor.setAlignment(Qt.AlignmentFlag.AlignRight)
        )
        toolbar_layout.addWidget(self.align_right_btn)

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

        self.image_btn = QPushButton("🖼️")
        self.image_btn.setFixedWidth(40)
        self.image_btn.setToolTip("Insertar imagen")
        self.image_btn.clicked.connect(self.insert_image)
        toolbar_layout.addWidget(self.image_btn)

        self.file_btn = QPushButton("📎")
        self.file_btn.setFixedWidth(40)
        self.file_btn.setToolTip("Adjuntar archivo")
        self.file_btn.clicked.connect(self.insert_file)
        toolbar_layout.addWidget(self.file_btn)

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
        
        # Interceptar clicks para redimensionar imágenes
        self.editor.viewport().installEventFilter(self)

        # Forzar el tamaño de fuente inicial
        fmt = QTextCharFormat()
        fmt.setFontPointSize(14)
        self.editor.setCurrentCharFormat(fmt)

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
        weight = QFont.Weight.Bold if fmt.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal
        fmt.setFontWeight(weight)
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
        cursor.insertList(QTextListFormat.Style.ListDisc)

    def insert_number_list(self):
        cursor = self.editor.textCursor()
        cursor.insertList(QTextListFormat.Style.ListDecimal)


    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Imagen",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.gif *.bmp *.webp)",
        )
        if file_path:
            try:
                with open(file_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
                
                # Averiguar el tipo MIME simple
                ext = file_path.lower().split('.')[-1]
                mime_type = f"image/{ext}" if ext != 'jpg' else "image/jpeg"
                
                # Crear tag de imagen con base64 embebido
                img_tag = f'<img src="data:{mime_type};base64,{encoded_string}" alt="Imagen incrustada" style="max-width: 100%;">'
                
                # Insertar en el editor
                self.editor.insertHtml(img_tag)
                self.editor.insertPlainText("\n") # Nueva línea después de la imagen
            except Exception as e:
                logger.error(f"Error al cargar la imagen: {e}")
                QMessageBox.critical(self, "Error", "No se pudo cargar la imagen seleccionada.")

    def insert_file(self):
        """Adjuntar un archivo como enlace referenciado localmente"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Adjuntar Archivo",
            "",
            "Todos los archivos (*.*)",
        )
        if file_path:
            file_name = os.path.basename(file_path)
            # URL encode basico para espacios y caracteres localizados (idealmente urllib, pero simple)
            safe_path = file_path.replace(" ", "%20")
            html = f'<a href="file:///{safe_path}">📎 {file_name}</a>'
            self.editor.insertHtml(html)
            self.editor.insertPlainText(" ") # Espacio para continuar escribiendo

    def update_format_buttons(self):
        # Actualizar estado de los botones según el formato actual
        fmt = self.editor.currentCharFormat()

        self.bold_btn.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        self.italic_btn.setChecked(fmt.fontItalic())
        self.underline_btn.setChecked(fmt.fontUnderline())

        # Actualizar alineación
        alignment = self.editor.alignment()
        self.align_left_btn.setChecked(alignment == Qt.AlignmentFlag.AlignLeft)
        self.align_center_btn.setChecked(alignment == Qt.AlignmentFlag.AlignCenter)
        self.align_right_btn.setChecked(alignment == Qt.AlignmentFlag.AlignRight)


        # Actualizar fuente y tamaño
        if fmt.font().family():
            index = self.font_combo.findText(fmt.font().family())
            if index >= 0:
                self.font_combo.setCurrentIndex(index)

        if fmt.fontPointSize() > 0:
            self.size_combo.setCurrentText(str(int(fmt.fontPointSize())))

    def eventFilter(self, obj, event):
        """Filtro para interceptar doble clic en imágenes"""
        if obj == self.editor.viewport() and event.type() == QEvent.Type.MouseButtonDblClick:
            cursor = self.editor.cursorForPosition(event.pos())
            
            # Revisamos carácter siguiente al clic
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
            fmt_char = cursor.charFormat()
            
            if not fmt_char.isImageFormat():
                # Revisamos carácter previo al clic
                cursor = self.editor.cursorForPosition(event.pos())
                cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, 1)
                fmt_char = cursor.charFormat()
                
            if fmt_char.isImageFormat():
                img_fmt = fmt_char.toImageFormat()
                w = img_fmt.width()
                h = img_fmt.height()
                
                # Intentar obtener tamaño original si no está definido en el formato HTML
                if w <= 0 or h <= 0:
                    name = img_fmt.name()
                    res = self.editor.document().resource(QTextDocument.ResourceType.ImageResource, QUrl(name))
                    if isinstance(res, QImage):
                        w = res.width()
                        h = res.height()
                    else:
                        w, h = 300, 300 # Fallback
                
                dialog = ImageResizeDialog(w, h, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_w, new_h = dialog.get_data()
                    img_fmt.setWidth(new_w)
                    img_fmt.setHeight(new_h)
                    
                    # Aplicar formato (el cursor ya tiene la imagen seleccionada)
                    cursor.setCharFormat(img_fmt)
                    
                    # Actualizar cursor de la vista
                    cursor.clearSelection()
                    self.editor.setTextCursor(cursor)
                return True
                
        return super().eventFilter(obj, event)
