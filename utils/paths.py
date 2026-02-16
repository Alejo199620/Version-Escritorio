# utils/paths.py
import sys
import os


def resource_path(relative_path):
    """Obtiene la ruta correcta para recursos en desarrollo y producción"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
