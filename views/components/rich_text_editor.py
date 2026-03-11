from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
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
    QFrame,
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
    QPainter,
    QPixmap,
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
        self.setFixedSize(320, 180)
        self.ratio = current_w / current_h if current_h > 0 else 1

        self.setStyleSheet(
            """
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #1e293b;
                font-size: 13px;
                font-weight: 500;
                font-family: 'Segoe UI';
            }
            QSpinBox {
                padding: 8px 10px;
                border: 1.5px solid #e2e8f0;
                border-radius: 8px;
                background-color: #f8fafc;
                color: #0f172a;
                font-size: 13px;
                font-family: 'Segoe UI';
            }
            QSpinBox:focus {
                border-color: #4361ee;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-family: 'Segoe UI';
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3f37c9;
            }
            QPushButton[text="Cancel"], QPushButton[flat=true] {
                background-color: #f1f5f9;
                color: #475569;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        form = QFormLayout()
        form.setSpacing(12)
        self.w_input = QSpinBox()
        self.w_input.setRange(10, 2000)
        self.w_input.setValue(int(current_w))

        self.h_input = QSpinBox()
        self.h_input.setRange(10, 2000)
        self.h_input.setValue(int(current_h))

        form.addRow("Ancho (px):", self.w_input)
        form.addRow("Alto (px):", self.h_input)
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
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


def _make_color_icon(color: QColor, size: int = 16) -> QPixmap:
    """Genera un icono sólido del color especificado."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 3, 3)
    painter.end()
    return pixmap


class ToolbarSeparator(QFrame):
    """Separador vertical fino para la toolbar."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFixedSize(1, 24)
        self.setStyleSheet("background-color: #e2e8f0;")


# ─── ESTILOS COMPARTIDOS ────────────────────────────────────────────────────

_TOOLBAR_BTN = """
    QPushButton {{
        background-color: transparent;
        color: {fg};
        border: none;
        border-radius: 6px;
        padding: 0px;
        font-size: {fs}px;
        font-family: 'Segoe UI';
        font-weight: {fw};
        min-width: {w}px;
        min-height: 30px;
        max-height: 30px;
    }}
    QPushButton:hover {{
        background-color: #f1f5f9;
    }}
    QPushButton:checked {{
        background-color: #eef2ff;
        color: #4361ee;
    }}
    QPushButton:pressed {{
        background-color: #e0e7ff;
    }}
"""


def _btn_style(fg="#374151", fs=13, fw="600", w=32):
    return _TOOLBAR_BTN.format(fg=fg, fs=fs, fw=fw, w=w)


_COMBO_STYLE = """
    QComboBox {
        border: 1.5px solid #e2e8f0;
        border-radius: 7px;
        padding: 3px 8px;
        background-color: #f8fafc;
        color: #1e293b;
        font-size: 12px;
        font-family: 'Segoe UI';
        selection-background-color: #4361ee;
    }
    QComboBox:hover {
        border-color: #94a3b8;
        background-color: #ffffff;
    }
    QComboBox:focus {
        border-color: #4361ee;
        background-color: #ffffff;
    }
    QComboBox::drop-down {
        border: none;
        padding-right: 6px;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid #64748b;
        width: 0;
        height: 0;
        margin-right: 4px;
    }
    QComboBox QAbstractItemView {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background-color: white;
        color: #1e293b;
        selection-background-color: #eef2ff;
        selection-color: #4361ee;
        font-size: 12px;
        font-family: 'Segoe UI';
        padding: 4px;
    }
"""

_FONTCOMBO_STYLE = """
    QFontComboBox {
        border: 1.5px solid #e2e8f0;
        border-radius: 7px;
        padding: 3px 8px;
        background-color: #f8fafc;
        color: #1e293b;
        font-size: 12px;
        font-family: 'Segoe UI';
    }
    QFontComboBox:hover {
        border-color: #94a3b8;
        background-color: #ffffff;
    }
    QFontComboBox:focus {
        border-color: #4361ee;
        background-color: #ffffff;
    }
    QFontComboBox::drop-down {
        border: none;
        padding-right: 6px;
    }
    QFontComboBox::down-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid #64748b;
        width: 0;
        height: 0;
        margin-right: 4px;
    }
    QFontComboBox QAbstractItemView {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background-color: white;
        color: #1e293b;
        selection-background-color: #eef2ff;
        selection-color: #4361ee;
        font-size: 12px;
        font-family: 'Segoe UI';
        padding: 4px;
    }
"""


# ─── EDITOR PRINCIPAL ────────────────────────────────────────────────────────

class RichTextEditor(QWidget):
    """
    Editor de texto enriquecido moderno con toolbar premium.
    API pública: setHtml(), toHtml(), toPlainText(), clear()
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_color = QColor("#1e293b")  # Color de texto activo
        self._updating_toolbar = False           # Evitar bucles de señales
        self.setup_ui()

    # ─── SETUP ──────────────────────────────────────────────────────────────

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_toolbar())
        layout.addWidget(self._build_editor())

    def _build_toolbar(self) -> QWidget:
        toolbar = QWidget()
        toolbar.setObjectName("rtToolbar")
        toolbar.setFixedHeight(50)
        toolbar.setStyleSheet(
            """
            #rtToolbar {
                background-color: #ffffff;
                border: 1.5px solid #e2e8f0;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            """
        )

        row = QHBoxLayout(toolbar)
        row.setContentsMargins(10, 0, 10, 0)
        row.setSpacing(4)

        # ── Fuente ──
        self.font_combo = QFontComboBox()
        self.font_combo.setFixedWidth(150)
        self.font_combo.setFixedHeight(32)
        self.font_combo.setStyleSheet(_FONTCOMBO_STYLE)
        self.font_combo.setCurrentFont(QFont("Segoe UI"))
        self.font_combo.currentFontChanged.connect(self._on_font_changed)
        row.addWidget(self.font_combo)

        row.addSpacing(4)

        # ── Tamaño ──
        self.size_combo = QComboBox()
        self.size_combo.addItems([
            "8", "9", "10", "11", "12", "14", "16", "18",
            "20", "22", "24", "26", "28", "36", "48", "72",
        ])
        self.size_combo.setEditable(True)
        self.size_combo.setCurrentText("14")
        self.size_combo.setFixedWidth(62)
        self.size_combo.setFixedHeight(32)
        self.size_combo.setStyleSheet(_COMBO_STYLE)
        self.size_combo.currentTextChanged.connect(self._on_size_changed)
        row.addWidget(self.size_combo)

        row.addSpacing(6)
        row.addWidget(ToolbarSeparator())
        row.addSpacing(6)

        # ── Formato ──
        self.bold_btn = self._make_btn("B", checkable=True, tooltip="Negrita (Ctrl+B)",
                                       extra_style="font-weight: 800; font-family: 'Segoe UI';")
        self.bold_btn.clicked.connect(self.toggle_bold)
        row.addWidget(self.bold_btn)

        self.italic_btn = self._make_btn("I", checkable=True, tooltip="Cursiva (Ctrl+I)",
                                         extra_style="font-style: italic; font-family: 'Georgia';")
        self.italic_btn.clicked.connect(self.toggle_italic)
        row.addWidget(self.italic_btn)

        self.underline_btn = self._make_btn("U", checkable=True, tooltip="Subrayado (Ctrl+U)",
                                            extra_style="text-decoration: underline;")
        self.underline_btn.clicked.connect(self.toggle_underline)
        row.addWidget(self.underline_btn)

        self.strike_btn = self._make_btn("S̶", checkable=True, tooltip="Tachado",
                                         extra_style="font-size: 12px;")
        self.strike_btn.clicked.connect(self.toggle_strikethrough)
        row.addWidget(self.strike_btn)

        row.addSpacing(6)
        row.addWidget(ToolbarSeparator())
        row.addSpacing(6)

        # ── Alineación ──
        self.align_left_btn = self._make_btn("≡", checkable=True, tooltip="Alinear izquierda",
                                             extra_style="font-size: 15px; letter-spacing: -1px;")
        self.align_left_btn.setChecked(True)
        self.align_left_btn.clicked.connect(
            lambda: self._set_alignment(Qt.AlignmentFlag.AlignLeft)
        )
        row.addWidget(self.align_left_btn)

        self.align_center_btn = self._make_btn("≡", checkable=True, tooltip="Centrar",
                                               extra_style="font-size: 15px;")
        self.align_center_btn.clicked.connect(
            lambda: self._set_alignment(Qt.AlignmentFlag.AlignCenter)
        )
        row.addWidget(self.align_center_btn)

        self.align_right_btn = self._make_btn("≡", checkable=True, tooltip="Alinear derecha",
                                              extra_style="font-size: 15px; letter-spacing: 1px;")
        self.align_right_btn.clicked.connect(
            lambda: self._set_alignment(Qt.AlignmentFlag.AlignRight)
        )
        row.addWidget(self.align_right_btn)

        self.align_justify_btn = self._make_btn("▤", checkable=True, tooltip="Justificar",
                                                extra_style="font-size: 14px;")
        self.align_justify_btn.clicked.connect(
            lambda: self._set_alignment(Qt.AlignmentFlag.AlignJustify)
        )
        row.addWidget(self.align_justify_btn)

        row.addSpacing(6)
        row.addWidget(ToolbarSeparator())
        row.addSpacing(6)

        # ── Color de texto ──
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(36, 30)
        self.color_btn.setToolTip("Color de texto")
        self.color_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh_color_btn()
        self.color_btn.clicked.connect(self.change_color)
        row.addWidget(self.color_btn)

        row.addSpacing(6)
        row.addWidget(ToolbarSeparator())
        row.addSpacing(6)

        # ── Listas ──
        self.bullet_btn = self._make_btn("•  —", checkable=False, tooltip="Lista con viñetas",
                                         w=46, extra_style="font-size: 11px; letter-spacing: 1px;")
        self.bullet_btn.clicked.connect(self.insert_bullet_list)
        row.addWidget(self.bullet_btn)

        self.number_btn = self._make_btn("1. —", checkable=False, tooltip="Lista numerada",
                                         w=46, extra_style="font-size: 11px;")
        self.number_btn.clicked.connect(self.insert_number_list)
        row.addWidget(self.number_btn)

        row.addSpacing(6)
        row.addWidget(ToolbarSeparator())
        row.addSpacing(6)

        # ── Insertar ──
        self.image_btn = self._make_btn("🖼", checkable=False, tooltip="Insertar imagen",
                                        w=34, extra_style="font-size: 14px;")
        self.image_btn.clicked.connect(self.insert_image)
        row.addWidget(self.image_btn)

        self.file_btn = self._make_btn("📎", checkable=False, tooltip="Adjuntar archivo",
                                       w=34, extra_style="font-size: 14px;")
        self.file_btn.clicked.connect(self.insert_file)
        row.addWidget(self.file_btn)

        row.addStretch()
        return toolbar

    def _build_editor(self) -> QTextEdit:
        self.editor = QTextEdit()
        self.editor.setObjectName("rtEditor")
        self.editor.setStyleSheet(
            """
            #rtEditor {
                border: 1.5px solid #e2e8f0;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                padding: 14px 16px;
                background-color: #ffffff;
                color: #1e293b;
                font-size: 14px;
                font-family: 'Segoe UI';
                line-height: 1.6;
                selection-background-color: #c7d7fe;
                selection-color: #1e293b;
            }
            """
        )
        self.editor.document().setDefaultFont(QFont("Segoe UI", 14))

        # Aplicar formato inicial al cursor para que el texto nuevo use la fuente/tamaño correctos
        fmt = QTextCharFormat()
        fmt.setFont(QFont("Segoe UI", 14))
        fmt.setForeground(self._current_color)
        self.editor.setCurrentCharFormat(fmt)

        # Señales
        self.editor.selectionChanged.connect(self.update_format_buttons)
        self.editor.cursorPositionChanged.connect(self.update_format_buttons)

        # Filtro para redimensionar imágenes con doble clic
        self.editor.viewport().installEventFilter(self)

        return self.editor

    # ─── HELPERS ────────────────────────────────────────────────────────────

    def _make_btn(self, text: str, checkable: bool = False, tooltip: str = "",
                  w: int = 32, extra_style: str = "") -> QPushButton:
        """Crea un botón de toolbar con estilos uniformes."""
        btn = QPushButton(text)
        btn.setCheckable(checkable)
        btn.setFixedSize(w, 30)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        style = _btn_style(w=w)
        if extra_style:
            # Inyectar estilos extra dentro del bloque QPushButton {}
            style = style.replace(
                "font-family: 'Segoe UI';",
                f"font-family: 'Segoe UI'; {extra_style}"
            )
        btn.setStyleSheet(style)
        return btn

    def _refresh_color_btn(self):
        """Actualiza el icono del botón de color con el color actual."""
        px = _make_color_icon(self._current_color, 14)
        # Construir un texto con un cuadrado unicode coloreado via hoja de estilo
        c = self._current_color.name()
        self.color_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 6px;
                min-width: 36px;
                min-height: 30px;
                max-height: 30px;
            }}
            QPushButton:hover {{
                background-color: #f1f5f9;
            }}
            QPushButton::after {{
                content: "";
            }}
            """
        )
        # Usar el pixmap como icono del botón
        from PyQt6.QtGui import QIcon
        # Hacer icono compuesto: "A" con raya de color debajo
        pix = QPixmap(28, 28)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Letra A
        p.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        p.setPen(QColor("#1e293b"))
        p.drawText(0, 0, 28, 20, Qt.AlignmentFlag.AlignCenter, "A")
        # Barra de color
        p.setBrush(self._current_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(4, 21, 20, 5, 2, 2)
        p.end()
        self.color_btn.setIcon(QIcon(pix))
        self.color_btn.setIconSize(QSize(28, 28))

    def _set_alignment(self, alignment):
        """Establece la alineación y actualiza los botones."""
        self.editor.setAlignment(alignment)
        self._updating_toolbar = True
        self.align_left_btn.setChecked(alignment == Qt.AlignmentFlag.AlignLeft)
        self.align_center_btn.setChecked(alignment == Qt.AlignmentFlag.AlignCenter)
        self.align_right_btn.setChecked(alignment == Qt.AlignmentFlag.AlignRight)
        self.align_justify_btn.setChecked(alignment == Qt.AlignmentFlag.AlignJustify)
        self._updating_toolbar = False

    # ─── API PÚBLICA ─────────────────────────────────────────────────────────

    def setHtml(self, html):
        """Establece contenido HTML en el editor."""
        try:
            if html and isinstance(html, str):
                self.editor.setHtml(html)
            else:
                self.editor.clear()
        except Exception as e:
            logger.error(f"Error al establecer HTML: {e}")
            self.editor.clear()

    def toHtml(self) -> str:
        """Retorna el contenido como HTML."""
        try:
            html = self.editor.toHtml()
            if not html or html in ("<p></p>", "<p><br></p>"):
                return ""
            return html
        except Exception as e:
            logger.error(f"Error al obtener HTML: {e}")
            return ""

    def toPlainText(self) -> str:
        """Retorna el contenido como texto plano."""
        try:
            return self.editor.toPlainText()
        except Exception as e:
            logger.error(f"Error al obtener texto plano: {e}")
            return ""

    def clear(self):
        """Limpia el editor."""
        self.editor.clear()

    # ─── ACCIONES DE FORMATO ─────────────────────────────────────────────────

    def _on_font_changed(self, font: QFont):
        """Cambia la fuente — aplica al cursor aunque no haya selección."""
        if self._updating_toolbar:
            return
        fmt = QTextCharFormat()
        fmt.setFontFamilies([font.family()])
        self.editor.mergeCurrentCharFormat(fmt)
        self.editor.setFocus()

    def _on_size_changed(self, size_text: str):
        """Cambia el tamaño — aplica al cursor aunque no haya selección."""
        if self._updating_toolbar:
            return
        try:
            size = int(size_text)
            if size <= 0:
                return
            fmt = QTextCharFormat()
            fmt.setFontPointSize(size)
            self.editor.mergeCurrentCharFormat(fmt)
            self.editor.setFocus()
        except ValueError:
            pass

    def toggle_bold(self):
        fmt = self.editor.currentCharFormat()
        is_bold = fmt.fontWeight() == QFont.Weight.Bold
        new_fmt = QTextCharFormat()
        new_fmt.setFontWeight(
            QFont.Weight.Normal if is_bold else QFont.Weight.Bold
        )
        self.editor.mergeCurrentCharFormat(new_fmt)

    def toggle_italic(self):
        fmt = self.editor.currentCharFormat()
        new_fmt = QTextCharFormat()
        new_fmt.setFontItalic(not fmt.fontItalic())
        self.editor.mergeCurrentCharFormat(new_fmt)

    def toggle_underline(self):
        fmt = self.editor.currentCharFormat()
        new_fmt = QTextCharFormat()
        new_fmt.setFontUnderline(not fmt.fontUnderline())
        self.editor.mergeCurrentCharFormat(new_fmt)

    def toggle_strikethrough(self):
        fmt = self.editor.currentCharFormat()
        new_fmt = QTextCharFormat()
        new_fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.editor.mergeCurrentCharFormat(new_fmt)

    def change_color(self):
        color = QColorDialog.getColor(self._current_color, self, "Seleccionar color de texto")
        if color.isValid():
            self._current_color = color
            self._refresh_color_btn()
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.editor.mergeCurrentCharFormat(fmt)
            self.editor.setFocus()

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

                ext = file_path.lower().split(".")[-1]
                mime_type = f"image/{ext}" if ext != "jpg" else "image/jpeg"
                img_tag = (
                    f'<img src="data:{mime_type};base64,{encoded_string}" '
                    f'alt="Imagen incrustada" style="max-width: 100%;">'
                )
                self.editor.insertHtml(img_tag)
                self.editor.insertPlainText("\n")
            except Exception as e:
                logger.error(f"Error al cargar la imagen: {e}")
                QMessageBox.critical(self, "Error", "No se pudo cargar la imagen seleccionada.")

    def insert_file(self):
        """Adjuntar un archivo como enlace referenciado localmente."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Adjuntar Archivo",
            "",
            "Todos los archivos (*.*)",
        )
        if file_path:
            file_name = os.path.basename(file_path)
            safe_path = file_path.replace(" ", "%20")
            html = f'<a href="file:///{safe_path}">📎 {file_name}</a>'
            self.editor.insertHtml(html)
            self.editor.insertPlainText(" ")

    # ─── SINCRONIZACIÓN TOOLBAR ───────────────────────────────────────────────

    def update_format_buttons(self):
        """Actualiza el estado de los botones según el formato en el cursor."""
        if self._updating_toolbar:
            return
        self._updating_toolbar = True

        fmt = self.editor.currentCharFormat()

        self.bold_btn.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        self.italic_btn.setChecked(fmt.fontItalic())
        self.underline_btn.setChecked(fmt.fontUnderline())
        self.strike_btn.setChecked(fmt.fontStrikeOut())

        # Alineación
        alignment = self.editor.alignment()
        self.align_left_btn.setChecked(
            alignment == Qt.AlignmentFlag.AlignLeft or alignment == Qt.AlignmentFlag.AlignAbsolute
        )
        self.align_center_btn.setChecked(alignment == Qt.AlignmentFlag.AlignCenter)
        self.align_right_btn.setChecked(alignment == Qt.AlignmentFlag.AlignRight)
        self.align_justify_btn.setChecked(alignment == Qt.AlignmentFlag.AlignJustify)

        # Fuente
        family = fmt.fontFamilies()
        if family:
            idx = self.font_combo.findText(family[0])
            if idx >= 0:
                self.font_combo.setCurrentIndex(idx)

        # Tamaño
        size = fmt.fontPointSize()
        if size > 0:
            self.size_combo.setCurrentText(str(int(size)))

        # Color actual
        fg = fmt.foreground().color()
        if fg.isValid() and fg != self._current_color:
            self._current_color = fg
            self._refresh_color_btn()

        self._updating_toolbar = False

    # ─── FILTRO DE EVENTOS (REDIMENSIÓN DE IMÁGENES) ──────────────────────────

    def eventFilter(self, obj, event):
        """Intercepta doble clic para redimensionar imágenes embebidas."""
        if obj == self.editor.viewport() and event.type() == QEvent.Type.MouseButtonDblClick:
            cursor = self.editor.cursorForPosition(event.pos())

            cursor.movePosition(
                QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1
            )
            fmt_char = cursor.charFormat()

            if not fmt_char.isImageFormat():
                cursor = self.editor.cursorForPosition(event.pos())
                cursor.movePosition(
                    QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, 1
                )
                fmt_char = cursor.charFormat()

            if fmt_char.isImageFormat():
                img_fmt = fmt_char.toImageFormat()
                w = img_fmt.width()
                h = img_fmt.height()

                if w <= 0 or h <= 0:
                    name = img_fmt.name()
                    res = self.editor.document().resource(
                        QTextDocument.ResourceType.ImageResource, QUrl(name)
                    )
                    if isinstance(res, QImage):
                        w = res.width()
                        h = res.height()
                    else:
                        w, h = 300, 300

                dialog = ImageResizeDialog(w, h, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_w, new_h = dialog.get_data()
                    img_fmt.setWidth(new_w)
                    img_fmt.setHeight(new_h)
                    cursor.setCharFormat(img_fmt)
                    cursor.clearSelection()
                    self.editor.setTextCursor(cursor)
                return True

        return super().eventFilter(obj, event)
