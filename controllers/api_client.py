import requests
import os
import time
import json
import hashlib
import re
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread
import logging
from datetime import datetime, timedelta

# OPTIMIZACIÓN EXTREMA: Reducir logging al mínimo
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def retry_on_failure(max_retries=0, delay=0.1):
    """Decorador para reintentar peticiones fallidas - OPTIMIZADO: sin reintentos"""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                raise

        return wrapper

    return decorator


class CacheEntry:
    """Entrada de caché ULTRA RÁPIDA"""

    __slots__ = ("data", "timestamp", "timeout")

    def __init__(self, data, timeout=300):
        self.data = data
        self.timestamp = time.time()
        self.timeout = timeout

    def is_expired(self):
        return time.time() - self.timestamp > self.timeout


class RequestWorker(QThread):
    """Worker para peticiones asíncronas"""

    finished = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit({"success": False, "error": str(e)})


class BatchRequestManager:
    """Agrupa múltiples peticiones - OPTIMIZADO"""

    def __init__(self, api_client):
        self.api_client = api_client
        self.pending_requests = {}
        self.batch_timer = QTimer()
        self.batch_timer.timeout.connect(self.execute_batch)
        self.batch_timer.setSingleShot(True)

    def add_request(self, request_id, endpoint, callback, params=None):
        self.pending_requests[request_id] = {
            "endpoint": endpoint,
            "callback": callback,
            "params": params,
        }
        if not self.batch_timer.isActive():
            self.batch_timer.start(20)  # REDUCIDO: 20ms para agrupar rápidamente

    def execute_batch(self):
        if not self.pending_requests:
            return

        for req_id, req in self.pending_requests.items():
            result = self.api_client.get(req["endpoint"], params=req["params"])
            if req["callback"]:
                req["callback"](result)

        self.pending_requests.clear()


class APIClient(QObject):
    request_started = pyqtSignal()
    request_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    token_refreshed = pyqtSignal()
    session_expired = pyqtSignal()

    # ============= SEÑALES PARA ACTUALIZACIÓN EN TIEMPO REAL =============
    data_changed = pyqtSignal(str)
    usuarios_changed = pyqtSignal()
    modulos_changed = pyqtSignal()
    lecciones_changed = pyqtSignal()
    ejercicios_changed = pyqtSignal()
    evaluaciones_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.base_url = os.getenv("API_URL", "http://localhost:8000/api")
        self.token = None
        self.refresh_token = None
        self.user = None

        # ============= CONFIGURACIÓN DE RED ULTRA OPTIMIZADA =============
        self.session = requests.Session()
        self.timeout = (1.0, 5)  # REDUCIDO: (connect: 1s, read: 5s)

        # Pool de conexiones MÁXIMO
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=50,  # AUMENTADO: 50 conexiones
            pool_maxsize=50,  # AUMENTADO: 50 máximo
            max_retries=0,  # REDUCIDO: 0 reintentos
            pool_block=False,
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Headers ULTRA OPTIMIZADOS
        self.session.headers.update(
            {
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Varchate-Admin/1.0",
                "Cache-Control": "no-cache",
            }
        )

        # ============= CACHÉ EN MEMORIA ULTRA RÁPIDO =============
        self.cache = {}

        # Timeouts MÁS LARGOS para mejor caché
        self.cache_config = {
            "modulos": {"timeout": 300, "enabled": True, "preload": True},  # 5 minutos
            "usuarios": {
                "timeout": 180,
                "enabled": True,
                "preload": False,
            },  # 3 minutos
            "lecciones": {
                "timeout": 300,
                "enabled": True,
                "preload": True,
            },  # 5 minutos
            "dashboard": {
                "timeout": 120,
                "enabled": True,
                "preload": True,
            },  # 2 minutos
            "evaluaciones": {
                "timeout": 300,
                "enabled": True,
                "preload": False,
            },  # 5 minutos
        }

        # Caché en disco (solo para datos estáticos)
        self.disk_cache_enabled = False  # DESACTIVADO: más rápido sin disco

        self.batch_manager = BatchRequestManager(self)
        self.pending_workers = []

        # Cache de avatares en memoria
        self.avatars_cache = None
        self.avatars_cache_time = 0
        self.avatars_timeout = 3600  # 1 hora

        # ============= REGISTRO DE OBSERVADORES =============
        self.observers = {}

        # Pre-carga inmediata después de login
        self.preloaded = False

    # ============= MÉTODOS DE CACHÉ ULTRA RÁPIDOS =============
    def _get_cache_key(self, endpoint: str, params: Dict = None) -> str:
        """Generar clave ULTRA RÁPIDA"""
        if params:
            # Usar repr() que es más rápido que json.dumps
            params_str = repr(sorted(params.items())) if params else ""
        else:
            params_str = ""
        key_str = f"{endpoint}:{params_str}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_from_cache(self, key: str, cache_type: str = None) -> Optional[Any]:
        """Obtener de caché - ULTRA RÁPIDO"""
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                return entry.data
            else:
                del self.cache[key]
        return None

    def _save_to_cache(self, key: str, data: Any, cache_type: str = None):
        """Guardar en caché - ULTRA RÁPIDO"""
        timeout = self.cache_config.get(cache_type, {}).get("timeout", 300)
        self.cache[key] = CacheEntry(data, timeout)

    def clear_cache(self, cache_type: str = None):
        """Limpiar caché - ULTRA RÁPIDO"""
        if cache_type:
            # Limpiar solo las claves que coinciden
            keys_to_delete = [k for k in self.cache.keys() if cache_type in k]
            for key in keys_to_delete:
                del self.cache[key]
        else:
            self.cache.clear()

    # ============= SISTEMA DE OBSERVADORES =============
    def subscribe(self, data_type: str, callback: Callable):
        """Suscribir vista a cambios"""
        if data_type not in self.observers:
            self.observers[data_type] = []
        if callback not in self.observers[data_type]:
            self.observers[data_type].append(callback)

    def unsubscribe(self, data_type: str, callback: Callable):
        """Desuscribir vista"""
        if data_type in self.observers and callback in self.observers[data_type]:
            self.observers[data_type].remove(callback)

    def notify_changed(self, data_type: str):
        """Notificar cambios - ULTRA RÁPIDO"""
        # Emitir señales Qt
        self.data_changed.emit(data_type)

        # Señales específicas
        if data_type == "usuarios":
            self.usuarios_changed.emit()
        elif data_type == "modulos":
            self.modulos_changed.emit()
        elif data_type == "lecciones":
            self.lecciones_changed.emit()
        elif data_type == "ejercicios":
            self.ejercicios_changed.emit()
        elif data_type == "evaluaciones":
            self.evaluaciones_changed.emit()

        # Callbacks
        if data_type in self.observers:
            for callback in self.observers[data_type]:
                try:
                    callback()
                except:
                    pass

    # ============= INVALIDACIÓN DE CACHÉ ULTRA RÁPIDA =============
    def invalidate_cache_type(self, cache_type: str):
        """Invalidar caché - ULTRA RÁPIDO"""
        # Limpiar solo las claves relevantes
        keys_to_delete = []
        cache_type_lower = cache_type.lower()

        for key in list(self.cache.keys()):
            if cache_type_lower in key.lower():
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.cache[key]

        # Notificar cambios
        self.notify_changed(cache_type)

        return len(keys_to_delete)

    # ============= PETICIONES ASÍNCRONAS =============
    def get_async(
        self,
        endpoint: str,
        callback: Callable,
        cache_type: str = None,
        force_refresh: bool = False,
        **kwargs,
    ):
        """Petición GET asíncrona"""
        worker = RequestWorker(
            self.get,
            endpoint,
            cache_type=cache_type,
            force_refresh=force_refresh,
            **kwargs,
        )
        worker.finished.connect(callback)
        worker.finished.connect(worker.deleteLater)
        worker.finished.connect(
            lambda: (
                self.pending_workers.remove(worker)
                if worker in self.pending_workers
                else None
            )
        )
        self.pending_workers.append(worker)
        worker.start()
        return worker

    # ============= MÉTODO BASE ULTRA OPTIMIZADO =============
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Método base ULTRA RÁPIDO"""
        url = (
            f"{self.base_url}{endpoint if endpoint.startswith('/') else '/' + endpoint}"
        )

        # Headers con token
        if self.token:
            kwargs.setdefault("headers", {})
            kwargs["headers"]["Authorization"] = f"Bearer {self.token}"

        # Timeout agresivo
        kwargs.setdefault("timeout", self.timeout)

        no_cache = method.upper() != "GET"

        try:
            if not no_cache:
                self.request_started.emit()

            response = self.session.request(method, url, **kwargs)
            return self._handle_response_fast(response)

        except requests.ConnectionError:
            return {"success": False, "error": "Error de conexión"}
        except requests.Timeout:
            return {"success": False, "error": "Tiempo agotado"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if not no_cache:
                self.request_finished.emit()

    def _handle_response_fast(self, response: requests.Response) -> Dict[str, Any]:
        """Manejador de respuesta ULTRA RÁPIDO"""
        # Token expirado
        if response.status_code == 401 and self.refresh_token:
            if self._refresh_token():
                return {"success": None, "should_retry": True}
            else:
                self.session_expired.emit()
                return {"success": False, "error": "Sesión expirada"}

        # Error rápido
        if response.status_code >= 400:
            try:
                data = response.json()
                error_msg = data.get("message", data.get("error", "Error"))

                if response.status_code == 422 and "errors" in data:
                    return {
                        "success": False,
                        "error": error_msg,
                        "errors": data["errors"],
                        "status_code": response.status_code,
                    }
            except:
                error_msg = f"Error {response.status_code}"

            self.error_occurred.emit(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "status_code": response.status_code,
            }

        # Éxito rápido
        try:
            data = response.json()
        except:
            return {"success": True, "data": {}, "status_code": response.status_code}

        if "data" in data:
            return {
                "success": True,
                "data": data["data"],
                "meta": data.get("meta"),
                "status_code": response.status_code,
            }

        return {"success": True, "data": data, "status_code": response.status_code}

    # ============= MÉTODO GET ACELERADO =============
    def get(
        self,
        endpoint: str,
        params: Dict = None,
        cache_type: str = None,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        """GET con caché - ULTRA RÁPIDO"""
        if force_refresh or not cache_type:
            return self._request("GET", endpoint, params=params or {})

        # Verificar si el tipo de caché está habilitado
        config = self.cache_config.get(cache_type, {})
        if not config.get("enabled", True):
            return self._request("GET", endpoint, params=params or {})

        # Intentar caché
        cache_key = self._get_cache_key(endpoint, params)
        cached = self._get_from_cache(cache_key, cache_type)
        if cached is not None:
            return cached

        # Petición real
        result = self._request("GET", endpoint, params=params or {})

        # Guardar en caché
        if result.get("success", False):
            self._save_to_cache(cache_key, result, cache_type)

        return result

    # ============= MÉTODOS CON INVALIDACIÓN AUTOMÁTICA =============
    def post(
        self,
        endpoint: str,
        data: Dict = None,
        json: Dict = None,
        invalidate_cache: list = None,
    ) -> Dict[str, Any]:
        result = self._request("POST", endpoint, data=data, json=json)

        if result.get("success", False):
            if invalidate_cache:
                for cache_type in invalidate_cache:
                    self.invalidate_cache_type(cache_type)
            else:
                self._auto_invalidate_from_endpoint(endpoint)

        return result

    def put(
        self,
        endpoint: str,
        data: Dict = None,
        json: Dict = None,
        invalidate_cache: list = None,
    ) -> Dict[str, Any]:
        result = self._request("PUT", endpoint, data=data, json=json)

        if result.get("success", False):
            if invalidate_cache:
                for cache_type in invalidate_cache:
                    self.invalidate_cache_type(cache_type)
            else:
                self._auto_invalidate_from_endpoint(endpoint)

        return result

    def patch(
        self,
        endpoint: str,
        data: Dict = None,
        json: Dict = None,
        invalidate_cache: list = None,
    ) -> Dict[str, Any]:
        result = self._request("PATCH", endpoint, data=data, json=json)

        if result.get("success", False):
            if invalidate_cache:
                for cache_type in invalidate_cache:
                    self.invalidate_cache_type(cache_type)
            else:
                self._auto_invalidate_from_endpoint(endpoint)

        return result

    def delete(self, endpoint: str, invalidate_cache: list = None) -> Dict[str, Any]:
        result = self._request("DELETE", endpoint)

        if result.get("success", False):
            if invalidate_cache:
                for cache_type in invalidate_cache:
                    self.invalidate_cache_type(cache_type)
            else:
                self._auto_invalidate_from_endpoint(endpoint)

        return result

    def _auto_invalidate_from_endpoint(self, endpoint: str):
        """Inferir qué caché invalidar"""
        endpoint_lower = endpoint.lower()

        if "usuario" in endpoint_lower:
            self.invalidate_cache_type("usuarios")
        elif "modulo" in endpoint_lower:
            self.invalidate_cache_type("modulos")
        elif "leccion" in endpoint_lower:
            self.invalidate_cache_type("lecciones")
        elif "ejercicio" in endpoint_lower:
            self.invalidate_cache_type("ejercicios")
        elif "evaluacion" in endpoint_lower:
            self.invalidate_cache_type("evaluaciones")
        elif "dashboard" in endpoint_lower:
            self.invalidate_cache_type("dashboard")

    # ============= AUTENTICACIÓN =============
    def set_token(self, token: str, refresh_token: Optional[str] = None):
        self.token = token
        self.refresh_token = refresh_token

    def _refresh_token(self) -> bool:
        if not self.refresh_token:
            return False
        try:
            r = requests.post(
                f"{self.base_url}/refresh",
                json={"refresh_token": self.refresh_token},
                timeout=2,
            )
            if r.status_code == 200:
                data = r.json()
                self.token = data.get("access_token")
                if data.get("refresh_token"):
                    self.refresh_token = data.get("refresh_token")
                self.token_refreshed.emit()
                return True
            return False
        except:
            return False

    # ============= PRE-CARGA INMEDIATA =============
    def preload_cache(self):
        """Pre-cargar datos críticos"""
        if self.preloaded:
            return

        # Cargar solo los datos más importantes
        self.get_async("/admin/dashboard", lambda x: None, cache_type="dashboard")
        self.get_async("/admin/modulos", lambda x: None, cache_type="modulos")

        self.preloaded = True

    # ============= LOGIN/LOGOUT =============
    @retry_on_failure()
    def login(self, email: str, password: str) -> Dict[str, Any]:
        result = self.post("/login", json={"email": email, "password": password})

        if result["success"]:
            data = result["data"]
            token = data.get("access_token") or data.get("token")
            if token:
                self.set_token(token, data.get("refresh_token"))
                self.user = data.get("user", {})

                if self.user.get("rol") != "administrador":
                    return {"success": False, "error": "Acceso denegado"}

                # Pre-carga inmediata sin timer
                self.preload_cache()
            else:
                return {"success": False, "error": "No token"}

        return result

    def logout(self) -> Dict[str, Any]:
        result = self.post("/logout")
        self.token = None
        self.refresh_token = None
        self.user = None
        self.cache.clear()
        self.preloaded = False
        return result

    # ============= MÉTODOS DE PAGINACIÓN =============
    def get_paginated(
        self,
        endpoint: str,
        page: int = 1,
        per_page: int = 15,
        cache_type: str = None,
        **params,
    ) -> Dict[str, Any]:
        params.update({"page": page, "per_page": per_page})
        return self.get(endpoint, params=params, cache_type=cache_type)

    # ============= DASHBOARD =============
    def get_dashboard_stats(self, force_refresh: bool = False) -> Dict[str, Any]:
        return self.get(
            "/admin/dashboard", cache_type="dashboard", force_refresh=force_refresh
        )

    def get_dashboard_charts(self, force_refresh: bool = False) -> Dict[str, Any]:
        return self.get(
            "/admin/dashboard/charts",
            cache_type="dashboard",
            force_refresh=force_refresh,
        )

    def get_recent_activity(self, force_refresh: bool = False) -> Dict[str, Any]:
        return self.get(
            "/admin/dashboard/recent-activity",
            cache_type="dashboard",
            force_refresh=force_refresh,
        )

    # ============= USUARIOS =============
    def get_usuarios(
        self, page: int = 1, per_page: int = 100, force_refresh: bool = False
    ) -> Dict[str, Any]:
        params = {"page": page, "per_page": per_page}
        return self.get(
            "/admin/usuarios",
            params=params,
            cache_type="usuarios",
            force_refresh=force_refresh,
        )

    def get_avatars(self) -> Dict[str, Any]:
        """Obtener avatares con caché de 1 hora"""
        now = time.time()
        if (
            self.avatars_cache
            and (now - self.avatars_cache_time) < self.avatars_timeout
        ):
            return self.avatars_cache

        result = self.get("/admin/usuarios/avatars", cache_type="usuarios")

        if result.get("success"):
            self.avatars_cache = result
            self.avatars_cache_time = now

        return result

    def create_usuario(self, data: Dict) -> Dict[str, Any]:
        """Crear usuario - ULTRA RÁPIDO"""
        logger.debug(f"Creando usuario: {data.get('email')}")

        # Validaciones rápidas
        errores = []
        nombre = data.get("nombre", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not nombre or len(nombre) < 3:
            errores.append("Nombre inválido (mínimo 3 caracteres)")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            errores.append("Email inválido")
        if password and (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
        ):
            errores.append("Contraseña no cumple requisitos")

        if errores:
            return {
                "success": False,
                "error": "Validación fallida",
                "errors": errores,
                "status_code": 422,
            }

        api_data = {
            "nombre": nombre,
            "email": email,
            "password": password,
            "rol": data.get("rol", "aprendiz"),
            "estado": data.get("estado", "activo"),
        }

        if data.get("avatar_id"):
            api_data["avatar_id"] = data["avatar_id"]

        return self.post(
            "/admin/usuarios", json=api_data, invalidate_cache=["usuarios"]
        )

    def update_usuario(self, usuario_id: int, data: Dict) -> Dict[str, Any]:
        """Actualizar usuario"""
        return self.put(
            f"/admin/usuarios/{usuario_id}", json=data, invalidate_cache=["usuarios"]
        )

    def delete_usuario(self, usuario_id: int) -> Dict[str, Any]:
        """Eliminar usuario"""
        return self.delete(
            f"/admin/usuarios/{usuario_id}", invalidate_cache=["usuarios"]
        )

    def toggle_usuario_status(self, usuario_id: int) -> Dict[str, Any]:
        """Cambiar estado de usuario"""
        return self.patch(
            f"/admin/usuarios/{usuario_id}/toggle-status", invalidate_cache=["usuarios"]
        )

    # ============= MÓDULOS =============
    def get_modulos(
        self, params: Dict = None, force_refresh: bool = False
    ) -> Dict[str, Any]:
        return self.get(
            "/admin/modulos",
            params=params or {},
            cache_type="modulos",
            force_refresh=force_refresh,
        )

    def get_modulo(self, modulo_id: int, force_refresh: bool = False) -> Dict[str, Any]:
        return self.get(
            f"/admin/modulos/{modulo_id}",
            cache_type="modulos",
            force_refresh=force_refresh,
        )

    def create_modulo(self, data: Dict) -> Dict[str, Any]:
        """Crear módulo - Adaptado a la estructura de la BD"""

        # Validar campos requeridos según la tabla
        titulo = data.get("titulo", "").strip()
        descripcion_larga = (
            data.get("descripcion_larga")
            or data.get("descripcion")
            or data.get("contenido", "")
        )
        modulo_tipo = data.get(
            "modulo"
        )  # 'html', 'css', 'javascript', 'php', 'sql', 'introduccion'

        if not titulo:
            return {"success": False, "error": "El título es requerido"}

        if not modulo_tipo:
            return {
                "success": False,
                "error": "El tipo de módulo es requerido (html, css, javascript, php, sql, introduccion)",
            }

        if not descripcion_larga:
            return {"success": False, "error": "La descripción es requerida"}

        # Preparar datos para la API
        api_data = {
            "titulo": titulo,
            "descripcion_larga": descripcion_larga,  # Nombre correcto en la BD
            "modulo": modulo_tipo,
            "estado": data.get("estado", "borrador"),
            "orden_global": data.get("orden_global", 0),
            "created_by": (
                self.user.get("id") if self.user else None
            ),  # ID del usuario actual
        }

        # Generar slug automáticamente si no viene
        if "slug" in data and data["slug"]:
            api_data["slug"] = data["slug"]
        else:
            # Convertir título a slug (ej: "Mi Módulo" -> "mi-modulo")
            import re

            slug = titulo.lower()
            slug = re.sub(r"[^\w\s-]", "", slug)  # Eliminar caracteres especiales
            slug = re.sub(
                r"[-\s]+", "-", slug
            )  # Reemplazar espacios y guiones múltiples por un solo guión
            api_data["slug"] = slug.strip("-")

        # Hacer la petición POST
        result = self.post(
            "/admin/modulos", json=api_data, invalidate_cache=["modulos"]
        )

        return result

    def update_modulo(self, modulo_id: int, data: Dict) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}", json=data, invalidate_cache=["modulos"]
        )

    def delete_modulo(self, modulo_id: int) -> Dict[str, Any]:
        return self.delete(f"/admin/modulos/{modulo_id}", invalidate_cache=["modulos"])

    def reorder_modulos(self, modulos: list) -> Dict[str, Any]:
        return self.post(
            "/admin/modulos/reorder",
            json={"modulos": modulos},
            invalidate_cache=["modulos"],
        )

    # ============= LECCIONES =============
    def get_lecciones(
        self, modulo_id: int, params: Dict = None, force_refresh: bool = False
    ) -> Dict[str, Any]:
        return self.get(
            f"/admin/modulos/{modulo_id}/lecciones",
            params=params or {},
            cache_type="lecciones",
            force_refresh=force_refresh,
        )

    def get_leccion(
        self, modulo_id: int, leccion_id: int, force_refresh: bool = False
    ) -> Dict[str, Any]:
        return self.get(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}",
            cache_type="lecciones",
            force_refresh=force_refresh,
        )

    def create_leccion(self, modulo_id: int, data: Dict) -> Dict[str, Any]:
        if not data.get("titulo") or not data.get("contenido"):
            return {"success": False, "error": "Título y contenido requeridos"}

        # Asegurar que se incluya created_by
        api_data = dict(data)
        if "created_by" not in api_data and self.user:
            api_data["created_by"] = self.user.get("id")

        return self.post(
            f"/admin/modulos/{modulo_id}/lecciones",
            json=api_data,
            invalidate_cache=["lecciones"],
        )

    def update_leccion(
        self, modulo_id: int, leccion_id: int, data: Dict
    ) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}",
            json=data,
            invalidate_cache=["lecciones"],
        )

    def delete_leccion(self, modulo_id: int, leccion_id: int) -> Dict[str, Any]:
        return self.delete(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}",
            invalidate_cache=["lecciones"],
        )

    def reorder_lecciones(self, modulo_id: int, lecciones: list) -> Dict[str, Any]:
        return self.post(
            f"/admin/modulos/{modulo_id}/lecciones/reorder",
            json={"lecciones": lecciones},
            invalidate_cache=["lecciones"],
        )

    # ============= EJERCICIOS =============
    def get_ejercicios(
        self, modulo_id: int, leccion_id: int, force_refresh: bool = False
    ) -> Dict[str, Any]:
        return self.get(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios",
            cache_type="ejercicios",
            force_refresh=force_refresh,
        )

    def get_ejercicio(
        self,
        modulo_id: int,
        leccion_id: int,
        ejercicio_id: int,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        return self.get(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios/{ejercicio_id}",
            cache_type="ejercicios",
            force_refresh=force_refresh,
        )

    def create_ejercicio(
        self, modulo_id: int, leccion_id: int, data: Dict
    ) -> Dict[str, Any]:
        if not data.get("pregunta") or not data.get("tipo"):
            return {"success": False, "error": "Pregunta y tipo requeridos"}

        # Asegurar que se incluya created_by
        api_data = dict(data)
        if "created_by" not in api_data and self.user:
            api_data["created_by"] = self.user.get("id")

        return self.post(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios",
            json=api_data,
            invalidate_cache=["ejercicios"],
        )

    def update_ejercicio(
        self, modulo_id: int, leccion_id: int, ejercicio_id: int, data: Dict
    ) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios/{ejercicio_id}",
            json=data,
            invalidate_cache=["ejercicios"],
        )

    def delete_ejercicio(
        self, modulo_id: int, leccion_id: int, ejercicio_id: int
    ) -> Dict[str, Any]:
        return self.delete(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios/{ejercicio_id}",
            invalidate_cache=["ejercicios"],
        )

    def update_ejercicio_opciones(
        self, modulo_id: int, leccion_id: int, ejercicio_id: int, opciones: list
    ) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios/{ejercicio_id}/opciones",
            json={"opciones": opciones},
            invalidate_cache=["ejercicios"],
        )

    # ============= EVALUACIONES =============
    def get_evaluacion(
        self, modulo_id: int, force_refresh: bool = False
    ) -> Dict[str, Any]:
        """Obtener evaluación del módulo"""
        return self.get(
            f"/admin/modulos/{modulo_id}/evaluacion",
            cache_type="evaluaciones",
            force_refresh=force_refresh,
        )

    def update_evaluacion_config(self, modulo_id: int, data: Dict) -> Dict[str, Any]:
        """Actualizar configuración de evaluación"""

        # Asegurar que el título esté presente
        if "titulo" not in data or not data["titulo"]:
            # Si no hay título, crear uno por defecto
            data["titulo"] = f"Evaluación del Módulo {modulo_id}"

        # Asegurar created_by
        if "created_by" not in data and self.user:
            data["created_by"] = self.user.get("id")

        logger.debug(f"Enviando configuración de evaluación: {data}")

        return self.put(
            f"/admin/modulos/{modulo_id}/evaluacion/config",
            json=data,
            invalidate_cache=["evaluaciones"],
        )

    def invalidate_cache_type(self, cache_type: str):
        """Invalidar caché de evaluaciones"""
        keys_to_delete = []
        for key in list(self.cache.keys()):
            if "evaluaciones" in key.lower():
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.cache[key]

        # Notificar cambios
        self.evaluaciones_changed.emit()
        self.data_changed.emit("evaluaciones")

    def create_pregunta(
        self, modulo_id: int, evaluacion_id: int, data: Dict
    ) -> Dict[str, Any]:
        if not data.get("pregunta"):
            return {"success": False, "error": "Pregunta requerida"}

        # Asegurar que se incluya created_by
        api_data = dict(data)
        if "created_by" not in api_data and self.user:
            api_data["created_by"] = self.user.get("id")

        return self.post(
            f"/admin/modulos/{modulo_id}/evaluacion/{evaluacion_id}/preguntas",
            json=api_data,
            invalidate_cache=["evaluaciones"],
        )

    def update_pregunta(
        self, modulo_id: int, evaluacion_id: int, pregunta_id: int, data: Dict
    ) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/evaluacion/{evaluacion_id}/preguntas/{pregunta_id}",
            json=data,
            invalidate_cache=["evaluaciones"],
        )

    def delete_pregunta(
        self, modulo_id: int, evaluacion_id: int, pregunta_id: int
    ) -> Dict[str, Any]:
        return self.delete(
            f"/admin/modulos/{modulo_id}/evaluacion/{evaluacion_id}/preguntas/{pregunta_id}",
            invalidate_cache=["evaluaciones"],
        )

    def update_pregunta_opciones(
        self, modulo_id: int, evaluacion_id: int, pregunta_id: int, opciones: list
    ) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/evaluacion/{evaluacion_id}/preguntas/{pregunta_id}/opciones",
            json={"opciones": opciones},
            invalidate_cache=["evaluaciones"],
        )
