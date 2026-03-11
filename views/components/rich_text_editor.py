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
    QGridLayout,
    QMenu,
    QCompleter,
)
from PyQt6.QtCore import Qt, QSize, QUrl, QEvent, QPoint, QTimer, QRect, QRectF, pyqtSignal
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
    QIcon,
    QTextImageFormat,
    QTextBlockFormat,
    QPen,
    QTextFormat,
)
import logging
import base64
import os
from utils.paths import resource_path

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
#  DIÁLOGO DE REDIMENSIONAR IMAGEN
# ═══════════════════════════════════════════════════════════════════════════════

class ImageResizeDialog(QDialog):
    def __init__(self, current_w, current_h, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Redimensionar Imagen")
        self.setFixedSize(320, 180)
        self.ratio = current_w / current_h if current_h > 0 else 1
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; }
            QLabel { color: #1e293b; font-size: 13px; font-weight: 500; font-family: 'Segoe UI'; }
            QSpinBox {
                padding: 8px 10px; border: 1.5px solid #e2e8f0; border-radius: 8px;
                background-color: #f8fafc; color: #0f172a; font-size: 13px; font-family: 'Segoe UI';
            }
            QSpinBox:focus { border-color: #4361ee; background-color: #ffffff; }
        """)
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


# ═══════════════════════════════════════════════════════════════════════════════
#  PALETA DE COLORES POPUP
# ═══════════════════════════════════════════════════════════════════════════════

_PALETTE_COLORS = [
    "#000000","#434343","#666666","#999999","#b7b7b7","#cccccc","#d9d9d9","#efefef","#f3f3f3","#ffffff",
    "#980000","#ff0000","#ff9900","#ffff00","#00ff00","#00ffff","#4a86e8","#0000ff","#9900ff","#ff00ff",
    "#e6b8af","#f4cccc","#fce5cd","#fff2cc","#d9ead3","#d0e0e3","#c9daf8","#cfe2f3","#d9d2e9","#ead1dc",
    "#dd7e6b","#ea9999","#f9cb9c","#ffe599","#b6d7a8","#a2c4c9","#a4c2f4","#9fc5e8","#b4a7d6","#d5a6bd",
    "#cc4125","#e06666","#f6b26b","#ffd966","#93c47d","#76a5af","#6d9eeb","#6fa8dc","#8e7cc3","#c27ba0",
    "#a61c00","#cc0000","#e69138","#f1c232","#6aa84f","#45818e","#3c78d8","#3d85c6","#674ea7","#a64d79",
    "#85200c","#990000","#b45f06","#bf9000","#38761d","#134f5c","#1155cc","#0b5394","#351c75","#741b47",
]

class ColorPalettePopup(QDialog):
    def __init__(self, current_color: QColor, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.selected_color = None
        self.setFixedSize(292, 260)
        self.setStyleSheet("QDialog{background:#fff;border:1px solid #e2e8f0;border-radius:10px;}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 8)
        layout.setSpacing(8)

        title = QLabel("Color de texto")
        title.setStyleSheet("color:#64748b;font-size:11px;font-family:'Segoe UI';font-weight:600;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(2)
        for i, hc in enumerate(_PALETTE_COLORS):
            btn = QPushButton()
            btn.setFixedSize(24, 24)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            is_light = hc.upper() in ("#FFFFFF", "#EFEFEF", "#F3F3F3")
            bd = "1px solid #d1d5db" if is_light else "none"
            btn.setStyleSheet(
                f"QPushButton{{background:{hc};border:{bd};border-radius:4px;}}"
                f"QPushButton:hover{{border:2px solid #1e293b;}}"
            )
            btn.setToolTip(hc)
            btn.clicked.connect(lambda _, c=hc: self._pick(c))
            grid.addWidget(btn, i // 10, i % 10)
        layout.addLayout(grid)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:#e2e8f0;")
        layout.addWidget(sep)

        custom_btn = QPushButton("  Personalizado...")
        custom_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        custom_btn.setStyleSheet(
            "QPushButton{background:transparent;color:#4361ee;border:none;border-radius:6px;"
            "font-size:12px;font-family:'Segoe UI';font-weight:600;text-align:left;padding:4px 6px;}"
            "QPushButton:hover{background:#eef2ff;}"
        )
        custom_btn.clicked.connect(lambda: self._custom(current_color))
        layout.addWidget(custom_btn)

    def _pick(self, hc):
        self.selected_color = QColor(hc)
        self.close()

    def _custom(self, cur):
        c = QColorDialog.getColor(cur, self, "Seleccionar color")
        if c.isValid():
            self.selected_color = c
        self.close()


# ═══════════════════════════════════════════════════════════════════════════════
#  OVERLAY DE SELECCIÓN + HANDLES SOBRE IMÁGENES
# ═══════════════════════════════════════════════════════════════════════════════

_HS = 10   # Tamaño de cada handle (px)
_HH = 5    # Mitad del handle

# Cursores según handle index (0-7 en sentido horario desde top-left)
_CURSORS = [
    Qt.CursorShape.SizeFDiagCursor,   # 0 top-left
    Qt.CursorShape.SizeVerCursor,     # 1 top-center
    Qt.CursorShape.SizeBDiagCursor,   # 2 top-right
    Qt.CursorShape.SizeHorCursor,     # 3 mid-right
    Qt.CursorShape.SizeFDiagCursor,   # 4 bottom-right
    Qt.CursorShape.SizeVerCursor,     # 5 bottom-center
    Qt.CursorShape.SizeBDiagCursor,   # 6 bottom-left
    Qt.CursorShape.SizeHorCursor,     # 7 mid-left
]


class ImageSelectionOverlay(QWidget):
    """
    Overlay transparente que se superpone al viewport del QTextEdit.
    Cuando se selecciona una imagen, dibuja:
      - Un borde azul punteado
      - 8 handles (esquinas + medios) arrastrables para redimensionar
      - Mini-barra de info con dimensiones
      - Mini-botones de alineación y eliminación
    """

    image_deselected = pyqtSignal()

    def __init__(self, editor_widget: 'RichTextEditor', text_edit: QTextEdit, parent=None):
        super().__init__(parent or text_edit.viewport())
        self._editor = editor_widget
        self._text_edit = text_edit
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        # Estado
        self._active = False
        self._cursor: QTextCursor = None      # cursor con la imagen seleccionada
        self._fmt: QTextImageFormat = None     # formato de la imagen
        self._rect = QRect()                   # rectángulo de la imagen (viewport coords)
        self._img_w = 0.0                      # ancho real de la imagen
        self._img_h = 0.0                      # alto real de la imagen
        self._ratio = 1.0                      # aspect ratio (h/w)

        # Arrastre
        self._dragging = False
        self._drag_idx = -1
        self._drag_origin = QPoint()
        self._drag_rect0 = QRect()

        # Conectar scroll para re-posicionar
        sb = text_edit.verticalScrollBar()
        if sb:
            sb.valueChanged.connect(self._on_scroll)

        self.hide()

    # ── Activar / Desactivar ────────────────────────────────────────────────

    def activate(self, cursor: QTextCursor, fmt: QTextImageFormat, rect: QRect):
        self._cursor = QTextCursor(cursor)
        self._fmt = QTextImageFormat(fmt)
        self._rect = QRect(rect)
        self._img_w = rect.width()
        self._img_h = rect.height()
        self._ratio = self._img_h / self._img_w if self._img_w > 0 else 1
        self._active = True
        self._dragging = False

        # Cubrir todo el viewport
        vp = self._text_edit.viewport()
        self.setGeometry(0, 0, vp.width(), vp.height())
        self.show()
        self.raise_()
        self.update()

    def deactivate(self):
        if not self._active:
            return
        self._active = False
        self._dragging = False
        self.hide()
        self.image_deselected.emit()

    def _on_scroll(self):
        """Deselecciona al hacer scroll para evitar desfase."""
        if self._active:
            self.deactivate()

    # ── Handles ─────────────────────────────────────────────────────────────

    def _handles(self):
        r = self._rect
        cx, cy = r.center().x(), r.center().y()
        return [
            QRect(r.left() - _HH,  r.top() - _HH,    _HS, _HS),   # 0 TL
            QRect(cx - _HH,        r.top() - _HH,    _HS, _HS),   # 1 TC
            QRect(r.right() - _HH, r.top() - _HH,    _HS, _HS),   # 2 TR
            QRect(r.right() - _HH, cy - _HH,         _HS, _HS),   # 3 MR
            QRect(r.right() - _HH, r.bottom() - _HH, _HS, _HS),   # 4 BR
            QRect(cx - _HH,        r.bottom() - _HH, _HS, _HS),   # 5 BC
            QRect(r.left() - _HH,  r.bottom() - _HH, _HS, _HS),   # 6 BL
            QRect(r.left() - _HH,  cy - _HH,         _HS, _HS),   # 7 ML
        ]

    def _hit(self, pos) -> int:
        for i, hr in enumerate(self._handles()):
            if hr.adjusted(-4, -4, 4, 4).contains(pos):
                return i
        return -1

    # ── Painting ────────────────────────────────────────────────────────────

    def paintEvent(self, ev):
        if not self._active:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Sombra semi-transparente fuera de la imagen
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(0, 0, 0, 20))
        # Dibujamos 4 rectángulos alrededor (sin afectar la imagen)
        vr = self.rect()
        ir = self._rect
        p.drawRect(QRect(0, 0, vr.width(), ir.top()))                                   # arriba
        p.drawRect(QRect(0, ir.bottom(), vr.width(), vr.height() - ir.bottom()))        # abajo
        p.drawRect(QRect(0, ir.top(), ir.left(), ir.height()))                           # izquierda
        p.drawRect(QRect(ir.right(), ir.top(), vr.width() - ir.right(), ir.height()))   # derecha

        # Borde azul continuo
        pen = QPen(QColor("#4361ee"), 2)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(self._rect)

        # Handles
        for hr in self._handles():
            # Sombra
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(0, 0, 0, 50))
            p.drawRoundedRect(hr.adjusted(1, 1, 1, 1), 2, 2)
            # Cuadro blanco con borde azul
            p.setPen(QPen(QColor("#4361ee"), 1.5))
            p.setBrush(QColor("#ffffff"))
            p.drawRoundedRect(hr, 2, 2)

        # Info badge (dimensiones)
        info = f"{int(self._img_w)} × {int(self._img_h)}"
        font = QFont("Segoe UI", 9, QFont.Weight.Bold)
        p.setFont(font)
        fm = p.fontMetrics()
        tw = fm.horizontalAdvance(info) + 16
        th = fm.height() + 8
        tx = ir.center().x() - tw // 2
        ty = ir.top() - th - 8
        if ty < 2:
            ty = ir.bottom() + 8
        badge = QRect(tx, ty, tw, th)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#1e293b"))
        p.drawRoundedRect(badge, 5, 5)
        p.setPen(QColor("#ffffff"))
        p.drawText(badge, Qt.AlignmentFlag.AlignCenter, info)

        # Mini toolbar (alinear + eliminar) — debajo de la imagen
        self._paint_mini_toolbar(p)

        p.end()

    def _paint_mini_toolbar(self, p: QPainter):
        """Pinta una mini-barra debajo de la imagen con botones de alineación."""
        ir = self._rect
        bar_w = 180
        bar_h = 30
        bx = ir.center().x() - bar_w // 2
        by = ir.bottom() + 12
        if by + bar_h > self.height() - 4:
            by = ir.top() - bar_h - 12

        bar = QRect(bx, by, bar_w, bar_h)
        self._mini_bar_rect = bar  # Guardar para hit-testing

        # Fondo
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#1e293b"))
        p.drawRoundedRect(bar, 7, 7)

        # Botones
        btns = [("◧", "left"), ("◫", "center"), ("◨", "right"), ("|", "sep"), ("🗑", "delete")]
        bw = bar_w // len(btns)
        font = QFont("Segoe UI", 11)
        p.setFont(font)

        self._mini_btns = []
        for i, (lbl, action) in enumerate(btns):
            btn_r = QRect(bx + i * bw, by, bw, bar_h)
            self._mini_btns.append((btn_r, action))

            if action == "sep":
                # Separador vertical
                sx = btn_r.center().x()
                p.setPen(QPen(QColor("#475569"), 1))
                p.drawLine(sx, by + 6, sx, by + bar_h - 6)
            else:
                p.setPen(QColor("#e2e8f0"))
                p.drawText(btn_r, Qt.AlignmentFlag.AlignCenter, lbl)

    # ── Mouse Events ────────────────────────────────────────────────────────

    def mousePressEvent(self, ev):
        if not self._active:
            ev.ignore()
            return

        pos = ev.pos()

        # ¿Clic en un handle?
        idx = self._hit(pos)
        if idx >= 0:
            self._dragging = True
            self._drag_idx = idx
            self._drag_origin = pos
            self._drag_rect0 = QRect(self._rect)
            ev.accept()
            return

        # ¿Clic en mini toolbar?
        if hasattr(self, '_mini_btns'):
            for btn_r, action in self._mini_btns:
                if action != "sep" and btn_r.contains(pos):
                    self._handle_mini_action(action)
                    ev.accept()
                    return

        # ¿Clic dentro de la imagen? — mantener selección
        if self._rect.contains(pos):
            ev.accept()
            return

        # Clic fuera → deseleccionar y pasar evento al editor
        self.deactivate()
        # Re-enviar el clic al viewport del editor
        self._text_edit.viewport().update()
        ev.ignore()

    def mouseMoveEvent(self, ev):
        if not self._active:
            ev.ignore()
            return

        pos = ev.pos()

        if self._dragging:
            self._do_drag(pos)
            ev.accept()
            return

        # Cambiar cursor
        idx = self._hit(pos)
        if idx >= 0:
            self.setCursor(_CURSORS[idx])
        elif self._rect.contains(pos):
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif hasattr(self, '_mini_bar_rect') and self._mini_bar_rect.contains(pos):
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        ev.accept()

    def mouseReleaseEvent(self, ev):
        if self._dragging:
            self._dragging = False
            self._apply_size()
            ev.accept()
        else:
            ev.ignore()

    def mouseDoubleClickEvent(self, ev):
        if self._active and self._rect.contains(ev.pos()):
            dlg = ImageResizeDialog(self._img_w, self._img_h, self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                nw, nh = dlg.get_data()
                self._img_w = nw
                self._img_h = nh
                self._ratio = nh / nw if nw > 0 else 1
                self._apply_size()
            ev.accept()
        else:
            ev.ignore()

    # ── Arrastre ────────────────────────────────────────────────────────────

    def _do_drag(self, pos: QPoint):
        dx = pos.x() - self._drag_origin.x()
        dy = pos.y() - self._drag_origin.y()
        r0 = self._drag_rect0
        h = self._drag_idx
        MIN_SZ = 30

        # Todos los handles mantienen proporción usando _ratio
        if h in (4, 2):       # bottom-right, top-right → ancho crece con dx
            nw = max(MIN_SZ, r0.width() + dx)
        elif h in (0, 6):     # top-left, bottom-left → ancho decrece con dx
            nw = max(MIN_SZ, r0.width() - dx)
        elif h in (3, 7):     # mid-right, mid-left → horizontal puro
            nw = max(MIN_SZ, r0.width() + dx) if h == 3 else max(MIN_SZ, r0.width() - dx)
        elif h in (1, 5):     # top-center, bottom-center → vertical → calc w inversamente
            nh_raw = max(MIN_SZ, r0.height() + dy) if h == 5 else max(MIN_SZ, r0.height() - dy)
            nw = int(nh_raw / self._ratio) if self._ratio > 0 else nh_raw
        else:
            nw = r0.width()

        nh = int(nw * self._ratio)

        # Anclar posición según handle
        if h in (0, 7):       # izquierda: anclar derecha
            nx = r0.right() - nw
            ny = r0.top() if h == 7 else (r0.bottom() - nh if h == 0 else r0.top())
        elif h == 1:          # top-center: anclar abajo
            nx = r0.left()
            ny = r0.bottom() - nh
        elif h == 6:          # bottom-left
            nx = r0.right() - nw
            ny = r0.top()
        elif h == 2:          # top-right
            nx = r0.left()
            ny = r0.bottom() - nh
        else:                 # 3, 4, 5: anclar top-left
            nx = r0.left()
            ny = r0.top()

        self._rect = QRect(int(nx), int(ny), int(nw), int(nh))
        self._img_w = nw
        self._img_h = nh
        self.update()

    def _apply_size(self):
        """Aplica el tamaño final al QTextImageFormat del documento."""
        if not self._cursor or not self._fmt:
            return
        new_fmt = QTextImageFormat(self._fmt)
        new_fmt.setWidth(int(self._img_w))
        new_fmt.setHeight(int(self._img_h))
        self._cursor.setCharFormat(new_fmt)
        self._fmt = new_fmt
        # Recalcular rect tras el cambio
        QTimer.singleShot(80, self._refresh_after_apply)

    def _refresh_after_apply(self):
        if not self._active or not self._cursor:
            return
        # Recalcular posición
        new_rect = self._editor._calc_image_rect(self._cursor, self._fmt)
        if new_rect.isValid() and new_rect.width() > 10:
            self._rect = new_rect
        self.update()

    # ── Mini toolbar actions ────────────────────────────────────────────────

    def _handle_mini_action(self, action: str):
        if not self._cursor:
            return
        if action == "left":
            self._align_image(Qt.AlignmentFlag.AlignLeft)
        elif action == "center":
            self._align_image(Qt.AlignmentFlag.AlignCenter)
        elif action == "right":
            self._align_image(Qt.AlignmentFlag.AlignRight)
        elif action == "delete":
            self._cursor.deleteChar()
            self.deactivate()

    def _align_image(self, alignment):
        block_fmt = QTextBlockFormat()
        block_fmt.setAlignment(alignment)
        self._cursor.mergeBlockFormat(block_fmt)
        self._text_edit.setTextCursor(self._cursor)
        # Deseleccionar y re-renderizar
        self.deactivate()


# ═══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES DE ESTILO
# ═══════════════════════════════════════════════════════════════════════════════

class ToolbarSeparator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFixedSize(1, 24)
        self.setStyleSheet("background-color:#e2e8f0;")


_TOOLBAR_BTN = """
    QPushButton {{
        background-color:transparent; color:{fg}; border:none; border-radius:6px;
        padding:0; font-size:{fs}px; font-family:'Segoe UI'; font-weight:{fw};
        min-width:{w}px; min-height:30px; max-height:30px;
    }}
    QPushButton:hover {{ background-color:#f1f5f9; }}
    QPushButton:checked {{ background-color:#eef2ff; color:#4361ee; }}
    QPushButton:pressed {{ background-color:#e0e7ff; }}
"""

def _btn_style(fg="#374151", fs=13, fw="600", w=32):
    return _TOOLBAR_BTN.format(fg=fg, fs=fs, fw=fw, w=w)

_COMBO_STYLE = """
    QComboBox {
        border:1.5px solid #e2e8f0; border-radius:7px; padding:3px 8px;
        background:#f8fafc; color:#1e293b; font-size:12px; font-family:'Segoe UI';
    }
    QComboBox:hover { border-color:#94a3b8; background:#fff; }
    QComboBox:focus { border-color:#4361ee; background:#fff; }
    QComboBox::drop-down { border:none; padding-right:6px; }
    QComboBox::down-arrow {
        image:none; border-left:4px solid transparent; border-right:4px solid transparent;
        border-top:5px solid #64748b; width:0; height:0; margin-right:4px;
    }
    QComboBox QAbstractItemView {
        border:1px solid #e2e8f0; border-radius:8px; background:white; color:#1e293b;
        selection-background-color:#eef2ff; selection-color:#4361ee;
        font-size:12px; font-family:'Segoe UI'; padding:4px;
    }
"""

_FONTCOMBO_STYLE = """
    QFontComboBox {
        border:1.5px solid #e2e8f0; border-radius:7px; padding:3px 8px;
        background:#f8fafc; color:#1e293b; font-size:12px; font-family:'Segoe UI';
    }
    QFontComboBox:hover { border-color:#94a3b8; background:#fff; }
    QFontComboBox:focus { border-color:#4361ee; background:#fff; }
    QFontComboBox::drop-down { border:none; padding-right:6px; }
    QFontComboBox::down-arrow {
        image:none; border-left:4px solid transparent; border-right:4px solid transparent;
        border-top:5px solid #64748b; width:0; height:0; margin-right:4px;
    }
    QFontComboBox QAbstractItemView {
        border:1px solid #e2e8f0; border-radius:8px; background:white; color:#1e293b;
        selection-background-color:#eef2ff; selection-color:#4361ee;
        font-size:12px; font-family:'Segoe UI'; padding:4px;
    }
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  EDITOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

class RichTextEditor(QWidget):
    """
    Editor de texto enriquecido moderno con toolbar premium.
    API pública: setHtml(), toHtml(), toPlainText(), clear()
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_color = QColor("#1e293b")
        self._updating_toolbar = False
        self._overlay: ImageSelectionOverlay = None
        self.setup_ui()

    # ── Setup ───────────────────────────────────────────────────────────────

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._build_toolbar())
        layout.addWidget(self._build_editor())

    def _build_toolbar(self) -> QWidget:
        tb = QWidget()
        tb.setObjectName("rtToolbar")
        tb.setFixedHeight(50)
        tb.setStyleSheet("""
            #rtToolbar {
                background:#fff; border:1.5px solid #e2e8f0; border-bottom:none;
                border-top-left-radius:10px; border-top-right-radius:10px;
            }
        """)
        row = QHBoxLayout(tb)
        row.setContentsMargins(10, 0, 10, 0)
        row.setSpacing(4)

        # Font
        self.font_combo = QFontComboBox()
        self.font_combo.setFixedWidth(150); self.font_combo.setFixedHeight(32)
        self.font_combo.setStyleSheet(_FONTCOMBO_STYLE)

        # Búsqueda: habilitar edición y autocompletado inteligente
        self.font_combo.setEditable(True)
        completer = self.font_combo.completer()
        if completer:
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)

        self.font_combo.setCurrentFont(QFont("Segoe UI"))
        self.font_combo.currentFontChanged.connect(self._on_font_changed)
        self.font_combo.activated.connect(lambda _: self.editor.setFocus())
        row.addWidget(self.font_combo); row.addSpacing(4)

        # Size
        self.size_combo = QComboBox()
        self.size_combo.addItems(["8","9","10","11","12","14","16","18","20","22","24","26","28","36","48","72"])
        self.size_combo.setEditable(True); self.size_combo.setCurrentText("14")
        self.size_combo.setFixedWidth(62); self.size_combo.setFixedHeight(32)
        self.size_combo.setStyleSheet(_COMBO_STYLE)
        self.size_combo.currentTextChanged.connect(self._on_size_changed)
        self.size_combo.activated.connect(lambda _: self.editor.setFocus())
        row.addWidget(self.size_combo)

        row.addSpacing(6); row.addWidget(ToolbarSeparator()); row.addSpacing(6)

        # Format buttons
        self.bold_btn = self._make_btn("B", True, "Negrita", extra="font-weight:800;")
        self.bold_btn.clicked.connect(self.toggle_bold); row.addWidget(self.bold_btn)

        self.italic_btn = self._make_btn("I", True, "Cursiva", extra="font-style:italic;font-family:'Georgia';")
        self.italic_btn.clicked.connect(self.toggle_italic); row.addWidget(self.italic_btn)

        self.underline_btn = self._make_btn("U", True, "Subrayado", extra="text-decoration:underline;")
        self.underline_btn.clicked.connect(self.toggle_underline); row.addWidget(self.underline_btn)

        self.strike_btn = self._make_btn("S", True, "Tachado", extra="text-decoration:line-through;font-size:12px;")
        self.strike_btn.clicked.connect(self.toggle_strikethrough); row.addWidget(self.strike_btn)

        row.addSpacing(6); row.addWidget(ToolbarSeparator()); row.addSpacing(6)

        # Alignment
        self.align_left_btn = self._make_btn("≡", True, "Izquierda", extra="font-size:15px;letter-spacing:-1px;")
        self.align_left_btn.setChecked(True)
        self.align_left_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignmentFlag.AlignLeft))
        row.addWidget(self.align_left_btn)

        self.align_center_btn = self._make_btn("≡", True, "Centrar", extra="font-size:15px;")
        self.align_center_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignmentFlag.AlignCenter))
        row.addWidget(self.align_center_btn)

        self.align_right_btn = self._make_btn("≡", True, "Derecha", extra="font-size:15px;letter-spacing:1px;")
        self.align_right_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignmentFlag.AlignRight))
        row.addWidget(self.align_right_btn)

        self.align_justify_btn = self._make_btn("▤", True, "Justificar", extra="font-size:14px;")
        self.align_justify_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignmentFlag.AlignJustify))
        row.addWidget(self.align_justify_btn)

        row.addSpacing(6); row.addWidget(ToolbarSeparator()); row.addSpacing(6)

        # Color
        self.color_btn = QPushButton()
        self.color_btn.setFixedSize(36, 30)
        self.color_btn.setToolTip("Color de texto")
        self.color_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh_color_btn()
        self.color_btn.clicked.connect(self._show_color_palette)
        row.addWidget(self.color_btn)

        row.addSpacing(6); row.addWidget(ToolbarSeparator()); row.addSpacing(6)

        # Lists
        b = self._make_btn("•  —", False, "Viñetas", w=46, extra="font-size:11px;")
        b.clicked.connect(self.insert_bullet_list); row.addWidget(b)

        b = self._make_btn("1. —", False, "Numerada", w=46, extra="font-size:11px;")
        b.clicked.connect(self.insert_number_list); row.addWidget(b)

        row.addSpacing(6); row.addWidget(ToolbarSeparator()); row.addSpacing(6)

        # Insert
        b = self._make_btn("🖼", False, "Imagen", w=34, extra="font-size:14px;")
        b.clicked.connect(self.insert_image); row.addWidget(b)

        b = self._make_btn("📎", False, "Archivo", w=34, extra="font-size:14px;")
        b.clicked.connect(self.insert_file); row.addWidget(b)

        row.addStretch()
        return tb

    def _build_editor(self) -> QTextEdit:
        self.editor = QTextEdit()
        self.editor.setObjectName("rtEditor")
        self.editor.setStyleSheet("""
            #rtEditor {
                border:1.5px solid #e2e8f0; border-bottom-left-radius:10px; border-bottom-right-radius:10px;
                padding:14px 16px; background:#fff; color:#1e293b;
                font-size:14px; font-family:'Segoe UI'; line-height:1.6;
                selection-background-color:#c7d7fe; selection-color:#1e293b;
            }
        """)
        self.editor.document().setDefaultFont(QFont("Segoe UI", 14))

        fmt = QTextCharFormat()
        fmt.setFont(QFont("Segoe UI", 14))
        fmt.setForeground(self._current_color)
        self.editor.setCurrentCharFormat(fmt)

        self.editor.selectionChanged.connect(self.update_format_buttons)
        self.editor.cursorPositionChanged.connect(self.update_format_buttons)
        self.editor.viewport().installEventFilter(self)

        # Context menu
        self.editor.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self._show_context_menu)

        return self.editor

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _make_btn(self, text, checkable=False, tooltip="", w=32, extra=""):
        btn = QPushButton(text)
        btn.setCheckable(checkable)
        btn.setFixedSize(w, 30)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        s = _btn_style(w=w)
        if extra:
            s = s.replace("font-family:'Segoe UI';", f"font-family:'Segoe UI';{extra}")
        btn.setStyleSheet(s)
        return btn

    def _refresh_color_btn(self):
        self.color_btn.setStyleSheet(
            "QPushButton{background:transparent;border:none;border-radius:6px;"
            "min-width:36px;min-height:30px;max-height:30px;}"
            "QPushButton:hover{background:#f1f5f9;}"
        )
        pix = QPixmap(28, 28)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        p.setPen(QColor("#1e293b"))
        p.drawText(0, 0, 28, 20, Qt.AlignmentFlag.AlignCenter, "A")
        p.setBrush(self._current_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(4, 21, 20, 5, 2, 2)
        p.end()
        self.color_btn.setIcon(QIcon(pix))
        self.color_btn.setIconSize(QSize(28, 28))

    def _set_alignment(self, a):
        self.editor.setAlignment(a)
        self._updating_toolbar = True
        self.align_left_btn.setChecked(a == Qt.AlignmentFlag.AlignLeft)
        self.align_center_btn.setChecked(a == Qt.AlignmentFlag.AlignCenter)
        self.align_right_btn.setChecked(a == Qt.AlignmentFlag.AlignRight)
        self.align_justify_btn.setChecked(a == Qt.AlignmentFlag.AlignJustify)
        self._updating_toolbar = False

    def _get_overlay(self) -> ImageSelectionOverlay:
        if self._overlay is None:
            self._overlay = ImageSelectionOverlay(self, self.editor, self.editor.viewport())
        return self._overlay

    # ── Image detection ─────────────────────────────────────────────────────

    def _find_image_at_pos(self, pos):
        """Busca una imagen en la posición del clic escaneando los fragmentos del bloque."""
        doc = self.editor.document()
        cursor = self.editor.cursorForPosition(pos)

        # 1) Intento rápido: verificar carácter a derecha e izquierda
        for direction in (QTextCursor.MoveOperation.Right, QTextCursor.MoveOperation.Left):
            c = QTextCursor(cursor)
            c.movePosition(direction, QTextCursor.MoveMode.KeepAnchor, 1)
            fmt = c.charFormat()
            if fmt.isImageFormat():
                return c, fmt.toImageFormat()

        # 2) Escanear fragmentos del bloque actual y adyacentes
        block = cursor.block()
        blocks_to_check = [block]
        if block.previous().isValid():
            blocks_to_check.append(block.previous())
        if block.next().isValid():
            blocks_to_check.append(block.next())

        for blk in blocks_to_check:
            it = blk.begin()
            while it != blk.end():
                frag = it.fragment()
                if frag.isValid():
                    frag_fmt = frag.charFormat()
                    if frag_fmt.isImageFormat():
                        # Crear cursor que selecciona esta imagen
                        c = QTextCursor(doc)
                        c.setPosition(frag.position())
                        c.setPosition(frag.position() + frag.length(),
                                      QTextCursor.MoveMode.KeepAnchor)
                        img_fmt = frag_fmt.toImageFormat()
                        # Verificar si el clic cae dentro del rect de esta imagen
                        rect = self._calc_image_rect_for(c, img_fmt)
                        if rect.isValid() and rect.contains(pos):
                            return c, img_fmt
                it += 1

        return None, None

    def _calc_image_rect_for(self, cursor: QTextCursor, img_fmt: QTextImageFormat) -> QRect:
        """Calcula el rectángulo renderizado de la imagen en coordenadas del viewport."""
        doc = self.editor.document()

        # Obtener dimensiones reales
        w = img_fmt.width()
        h = img_fmt.height()
        if w <= 0 or h <= 0:
            name = img_fmt.name()
            res = doc.resource(QTextDocument.ResourceType.ImageResource, QUrl(name))
            if isinstance(res, QImage):
                w, h = res.width(), res.height()
            elif isinstance(res, QPixmap):
                w, h = res.width(), res.height()
            else:
                w, h = 300, 200

        # Limitar al ancho del viewport (simula max-width:100%)
        vp_w = self.editor.viewport().width() - 32  # padding
        if w > vp_w:
            ratio = vp_w / w
            w = vp_w
            h = int(h * ratio)

        # Obtener posición superior-izquierda via cursor rect
        temp = QTextCursor(cursor)
        temp.setPosition(cursor.selectionStart())
        r = self.editor.cursorRect(temp)

        return QRect(r.left(), r.top(), int(w), int(h))

    def _calc_image_rect(self, cursor: QTextCursor, img_fmt: QTextImageFormat) -> QRect:
        """Alias público para compatibilidad con el overlay."""
        return self._calc_image_rect_for(cursor, img_fmt)

    # ── API pública ─────────────────────────────────────────────────────────

    def setHtml(self, html):
        try:
            if html and isinstance(html, str):
                self.editor.setHtml(html)
            else:
                self.editor.clear()
        except Exception as e:
            logger.error(f"Error setHtml: {e}")
            self.editor.clear()

    def toHtml(self) -> str:
        try:
            html = self.editor.toHtml()
            if not html or html in ("<p></p>", "<p><br></p>"):
                return ""
            return html
        except Exception as e:
            logger.error(f"Error toHtml: {e}")
            return ""

    def toPlainText(self) -> str:
        try:
            return self.editor.toPlainText()
        except Exception as e:
            logger.error(f"Error toPlainText: {e}")
            return ""

    def clear(self):
        self.editor.clear()

    # ── Format actions ──────────────────────────────────────────────────────

    def _on_font_changed(self, font):
        if self._updating_toolbar:
            return
        f = QTextCharFormat()
        f.setFontFamilies([font.family()])
        self.editor.mergeCurrentCharFormat(f)

    def _on_size_changed(self, txt):
        if self._updating_toolbar:
            return
        import re
        m = re.search(r'\d+', str(txt))
        if not m: return
        
        try:
            sz = int(m.group())
            if sz <= 0: return

            cursor = self.editor.textCursor()
            cursor.beginEditBlock()
            
            # Formato de fuente con doble unidad para machacar cualquier CSS previo
            f = QTextCharFormat()
            f.setFontPointSize(sz)
            f.setProperty(QTextFormat.Property.FontPixelSize, sz)
            
            if cursor.hasSelection():
                # 1. Quitar 'Heading' (H1-H6) de todos los bloques en la selección
                # Esto es vital porque los headings ignoran el tamaño de fuente en el visor de Qt
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                block = self.editor.document().findBlock(start)
                while block.isValid() and block.position() <= end:
                    bf = block.blockFormat()
                    if bf.headingLevel() > 0:
                        bf.setHeadingLevel(0)
                        bc = self.editor.textCursor()
                        bc.setPosition(block.position())
                        bc.setBlockFormat(bf)
                    block = block.next()
                
                # 2. Aplicar el tamaño a toda la selección
                cursor.mergeCharFormat(f)
            else:
                # 3. Si no hay selección, aplicar al formato actual
                self.editor.mergeCurrentCharFormat(f)

            cursor.endEditBlock()
            self.editor.setFocus()
            self.editor.viewport().update()
        except Exception as e:
            logger.error(f"Error cambiando tamaño de fuente: {e}")

    def toggle_bold(self):
        f = QTextCharFormat()
        f.setFontWeight(QFont.Weight.Normal if self.editor.currentCharFormat().fontWeight() == QFont.Weight.Bold else QFont.Weight.Bold)
        self.editor.mergeCurrentCharFormat(f)

    def toggle_italic(self):
        f = QTextCharFormat()
        f.setFontItalic(not self.editor.currentCharFormat().fontItalic())
        self.editor.mergeCurrentCharFormat(f)

    def toggle_underline(self):
        f = QTextCharFormat()
        f.setFontUnderline(not self.editor.currentCharFormat().fontUnderline())
        self.editor.mergeCurrentCharFormat(f)

    def toggle_strikethrough(self):
        f = QTextCharFormat()
        f.setFontStrikeOut(not self.editor.currentCharFormat().fontStrikeOut())
        self.editor.mergeCurrentCharFormat(f)

    def _show_color_palette(self):
        popup = ColorPalettePopup(self._current_color, self)
        popup.move(self.color_btn.mapToGlobal(QPoint(0, self.color_btn.height())))
        popup.exec()
        if popup.selected_color:
            self._current_color = popup.selected_color
            self._refresh_color_btn()
            f = QTextCharFormat()
            f.setForeground(popup.selected_color)
            self.editor.mergeCurrentCharFormat(f)
            self.editor.setFocus()

    def insert_bullet_list(self):
        self.editor.textCursor().insertList(QTextListFormat.Style.ListDisc)

    def insert_number_list(self):
        self.editor.textCursor().insertList(QTextListFormat.Style.ListDecimal)

    def insert_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "",
            "Imágenes (*.png *.jpg *.jpeg *.gif *.bmp *.webp)")
        if path:
            try:
                with open(path, "rb") as f:
                    enc = base64.b64encode(f.read()).decode("utf-8")
                ext = path.lower().rsplit(".", 1)[-1]
                mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
                self.editor.insertHtml(
                    f'<img src="data:{mime};base64,{enc}" alt="Imagen" style="max-width:100%;">'
                )
                self.editor.insertPlainText("\n")
            except Exception as e:
                logger.error(f"Error imagen: {e}")
                QMessageBox.critical(self, "Error", "No se pudo cargar la imagen.")

    def insert_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Adjuntar Archivo", "", "Todos (*.*)")
        if path:
            name = os.path.basename(path)
            safe = path.replace(" ", "%20")
            self.editor.insertHtml(f'<a href="file:///{safe}">📎 {name}</a>')
            self.editor.insertPlainText(" ")

    # ── Context menu ────────────────────────────────────────────────────────

    def _show_context_menu(self, pos):
        c_img, i_fmt = self._find_image_at_pos(pos)
        menu = self.editor.createStandardContextMenu()
        menu.setStyleSheet(
            "QMenu{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:6px;"
            "font-family:'Segoe UI';font-size:12px;}"
            "QMenu::item{padding:6px 16px;border-radius:4px;}"
            "QMenu::item:selected{background:#eef2ff;color:#4361ee;}"
            "QMenu::separator{height:1px;background:#e2e8f0;margin:4px 8px;}"
        )
        if c_img and i_fmt:
            menu.addSeparator()
            im = menu.addMenu("🖼 Imagen")
            al = im.addAction("◧ Alinear izquierda")
            ac = im.addAction("◫ Centrar")
            ar = im.addAction("◨ Alinear derecha")
            im.addSeparator()
            ars = im.addAction("⇲ Redimensionar...")
            ad = im.addAction("🗑 Eliminar")

            action = menu.exec(self.editor.viewport().mapToGlobal(pos))
            if not action:
                return
            if action in (al, ac, ar):
                align = {al: Qt.AlignmentFlag.AlignLeft, ac: Qt.AlignmentFlag.AlignCenter,
                         ar: Qt.AlignmentFlag.AlignRight}[action]
                bf = QTextBlockFormat()
                bf.setAlignment(align)
                c_img.mergeBlockFormat(bf)
            elif action == ars:
                w, h = i_fmt.width(), i_fmt.height()
                if w <= 0 or h <= 0: w, h = 300, 200
                d = ImageResizeDialog(w, h, self)
                if d.exec() == QDialog.DialogCode.Accepted:
                    nw, nh = d.get_data()
                    nf = QTextImageFormat(i_fmt)
                    nf.setWidth(nw); nf.setHeight(nh)
                    c_img.setCharFormat(nf)
            elif action == ad:
                c_img.deleteChar()
        else:
            menu.exec(self.editor.viewport().mapToGlobal(pos))

    # ── Sync toolbar ────────────────────────────────────────────────────────

    def update_format_buttons(self):
        if self._updating_toolbar:
            return
        self._updating_toolbar = True
        fmt = self.editor.currentCharFormat()

        self.bold_btn.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        self.italic_btn.setChecked(fmt.fontItalic())
        self.underline_btn.setChecked(fmt.fontUnderline())
        self.strike_btn.setChecked(fmt.fontStrikeOut())

        a = self.editor.alignment()
        self.align_left_btn.setChecked(a == Qt.AlignmentFlag.AlignLeft or a == Qt.AlignmentFlag.AlignAbsolute)
        self.align_center_btn.setChecked(a == Qt.AlignmentFlag.AlignCenter)
        self.align_right_btn.setChecked(a == Qt.AlignmentFlag.AlignRight)
        self.align_justify_btn.setChecked(a == Qt.AlignmentFlag.AlignJustify)

        fam = fmt.fontFamilies()
        if fam:
            idx = self.font_combo.findText(fam[0])
            if idx >= 0:
                self.font_combo.setCurrentIndex(idx)

        sz = fmt.fontPointSize()
        if sz > 0:
            self.size_combo.setCurrentText(str(int(sz)))

        fg = fmt.foreground().color()
        if fg.isValid() and fg != self._current_color:
            self._current_color = fg
            self._refresh_color_btn()

        self._updating_toolbar = False

    # ── Event filter ────────────────────────────────────────────────────────

    def eventFilter(self, obj, event):
        if obj != self.editor.viewport():
            return super().eventFilter(obj, event)

        # Clic en imagen → activar overlay
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            c_img, i_fmt = self._find_image_at_pos(event.pos())
            if c_img and i_fmt:
                overlay = self._get_overlay()
                rect = self._calc_image_rect(c_img, i_fmt)
                overlay.activate(c_img, i_fmt, rect)
                return True  # Consumir: el overlay maneja desde aquí

        return super().eventFilter(obj, event)
