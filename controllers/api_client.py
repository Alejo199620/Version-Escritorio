import requests
import os
import time
import json
import hashlib
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread
import logging
from datetime import datetime, timedelta

# OPTIMIZACIÓN 1: Reducir logging al mínimo en producción
logging.basicConfig(level=logging.ERROR)  # Cambiado de WARNING a ERROR
logger = logging.getLogger(__name__)


def retry_on_failure(max_retries=1, delay=0.2):  # Reducido de 2 a 1 reintento
    """Decorador para reintentar peticiones fallidas"""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(self, *args, **kwargs)
                except (requests.ConnectionError, requests.Timeout) as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay)
                except Exception as e:
                    raise

        return wrapper

    return decorator


class CacheEntry:
    """Entrada de caché optimizada"""

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
    """Agrupa múltiples peticiones"""

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
            self.batch_timer.start(30)  # Reducido de 50ms a 30ms

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

    def __init__(self):
        super().__init__()
        self.base_url = os.getenv("API_URL", "http://localhost:8000/api")
        self.token = None
        self.refresh_token = None
        self.user = None

        # ============= CONFIGURACIÓN DE RED OPTIMIZADA =============
        self.session = requests.Session()
        self.timeout = (2.0, 10)  # Reducido: (connect, read)

        # Pool de conexiones más grande
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=30,  # Aumentado de 20 a 30
            pool_maxsize=30,  # Aumentado de 20 a 30
            max_retries=1,  # Reducido de 2 a 1
            pool_block=False,
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Headers optimizados
        self.session.headers.update(
            {
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Varchate-Admin/1.0",
                "Cache-Control": "no-cache",  # Evitar caché del navegador
            }
        )

        # ============= CACHÉ AVANZADO =============
        self.cache = {}
        self.default_cache_timeout = 300

        # Configuración de caché por tipo (timeouts más largos)
        self.cache_config = {
            "modulos": {
                "timeout": 180,
                "enabled": True,
                "preload": True,
            },  # Aumentado 120→180
            "usuarios": {
                "timeout": 90,
                "enabled": True,
                "preload": False,
            },  # Aumentado 60→90
            "lecciones": {
                "timeout": 180,
                "enabled": True,
                "preload": True,
            },  # Aumentado 120→180
            "dashboard": {
                "timeout": 60,
                "enabled": True,
                "preload": True,
            },  # Aumentado 30→60
            "evaluaciones": {
                "timeout": 180,
                "enabled": True,
                "preload": False,
            },  # Aumentado 120→180
        }

        # Caché en disco
        self.disk_cache_enabled = True
        self.cache_dir = "api_cache"
        if self.disk_cache_enabled and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

        self.batch_manager = BatchRequestManager(self)
        self.pending_workers = []

    # ============= MÉTODOS DE CACHÉ ACELERADOS =============
    def _get_cache_key(self, endpoint: str, params: Dict = None) -> str:
        """Generar clave única usando hash rápido"""
        # OPTIMIZACIÓN: Usar str() en lugar de json.dumps para params simples
        if params:
            # Si params es pequeño, usar representación directa
            params_str = (
                str(sorted(params.items()))
                if len(params) < 5
                else json.dumps(params, sort_keys=True)
            )
        else:
            params_str = ""
        key_str = f"{endpoint}:{params_str}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_from_cache(self, key: str, cache_type: str = None) -> Optional[Any]:
        """Obtener de caché (solo memoria para máxima velocidad)"""
        # OPTIMIZACIÓN: Solo usar memoria, disco es lento
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                return entry.data
            else:
                del self.cache[key]
        return None

    def _save_to_cache(self, key: str, data: Any, cache_type: str = None):
        """Guardar solo en memoria (más rápido)"""
        timeout = self.cache_config.get(cache_type, {}).get("timeout", 300)
        self.cache[key] = CacheEntry(data, timeout)

    def clear_cache(self, cache_type: str = None):
        """Limpiar caché (solo memoria)"""
        if cache_type:
            keys_to_delete = [k for k in self.cache.keys() if cache_type in k]
            for key in keys_to_delete:
                del self.cache[key]
        else:
            self.cache.clear()

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

    # ============= MÉTODO BASE OPTIMIZADO =============
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
            return self._handle_response_fast(response)  # Usar versión rápida

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
        """Manejador de respuesta ultra rápido"""
        # OPTIMIZACIÓN: Manejo simplificado para velocidad

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
            except:
                error_msg = f"Error {response.status_code}"
            self.error_occurred.emit(error_msg)
            return {"success": False, "error": error_msg}

        # Éxito rápido
        try:
            data = response.json()
        except:
            return {"success": True, "data": {}}

        # Formato estándar
        if "data" in data:
            return {"success": True, "data": data["data"], "meta": data.get("meta")}
        return {"success": True, "data": data}

    # ============= MÉTODO GET ACELERADO =============
    def get(
        self,
        endpoint: str,
        params: Dict = None,
        cache_type: str = None,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        """GET con caché en memoria (ultra rápido)"""

        # Sin caché
        if not cache_type or force_refresh:
            return self._request("GET", endpoint, params=params or {})

        # Verificar caché
        if (
            cache_type in self.cache_config
            and not self.cache_config[cache_type]["enabled"]
        ):
            return self._request("GET", endpoint, params=params or {})

        # Intentar caché (solo memoria)
        cache_key = self._get_cache_key(endpoint, params)
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if not entry.is_expired():
                return entry.data
            else:
                del self.cache[cache_key]

        # Petición real
        result = self._request("GET", endpoint, params=params or {})

        # Guardar en caché
        if result.get("success", False):
            timeout = self.cache_config.get(cache_type, {}).get("timeout", 300)
            self.cache[cache_key] = CacheEntry(result, timeout)

        return result

    # ============= MÉTODOS CON INVALIDACIÓN =============
    def post(
        self,
        endpoint: str,
        data: Dict = None,
        json: Dict = None,
        invalidate_cache: list = None,
    ) -> Dict[str, Any]:
        result = self._request("POST", endpoint, data=data, json=json)
        if result.get("success", False) and invalidate_cache:
            for ct in invalidate_cache:
                self.clear_cache(ct)
        return result

    def put(
        self,
        endpoint: str,
        data: Dict = None,
        json: Dict = None,
        invalidate_cache: list = None,
    ) -> Dict[str, Any]:
        result = self._request("PUT", endpoint, data=data, json=json)
        if result.get("success", False) and invalidate_cache:
            for ct in invalidate_cache:
                self.clear_cache(ct)
        return result

    def patch(
        self,
        endpoint: str,
        data: Dict = None,
        json: Dict = None,
        invalidate_cache: list = None,
    ) -> Dict[str, Any]:
        result = self._request("PATCH", endpoint, data=data, json=json)
        if result.get("success", False) and invalidate_cache:
            for ct in invalidate_cache:
                self.clear_cache(ct)
        return result

    def delete(self, endpoint: str, invalidate_cache: list = None) -> Dict[str, Any]:
        result = self._request("DELETE", endpoint)
        if result.get("success", False) and invalidate_cache:
            for ct in invalidate_cache:
                self.clear_cache(ct)
        return result

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
                timeout=3,
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

    # ============= PRE-CARGA =============
    def preload_cache(self):
        """Pre-cargar datos en segundo plano"""
        preload_endpoints = {
            "modulos": "/admin/modulos",
            "dashboard": "/admin/dashboard",
        }
        for ct, ep in preload_endpoints.items():
            if ct in self.cache_config and self.cache_config[ct].get("preload"):
                self.get_async(ep, lambda x: None, cache_type=ct)

    # ============= LOGIN/LOGOUT =============
    @retry_on_failure(max_retries=1)
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
                QTimer.singleShot(50, self.preload_cache)  # Más rápido
            else:
                return {"success": False, "error": "No token"}
        return result

    def logout(self) -> Dict[str, Any]:
        result = self.post("/logout")
        self.token = None
        self.refresh_token = None
        self.user = None
        self.clear_cache()
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
        self, params: Dict = None, force_refresh: bool = False
    ) -> Dict[str, Any]:
        return self.get(
            "/admin/usuarios",
            params=params or {},
            cache_type="usuarios",
            force_refresh=force_refresh,
        )

    def create_usuario(self, data: Dict) -> Dict[str, Any]:
        return self.post("/admin/usuarios", json=data, invalidate_cache=["usuarios"])

    def update_usuario(self, usuario_id: int, data: Dict) -> Dict[str, Any]:
        return self.put(
            f"/admin/usuarios/{usuario_id}", json=data, invalidate_cache=["usuarios"]
        )

    def delete_usuario(self, usuario_id: int) -> Dict[str, Any]:
        return self.delete(
            f"/admin/usuarios/{usuario_id}", invalidate_cache=["usuarios"]
        )

    def toggle_usuario_status(self, usuario_id: int) -> Dict[str, Any]:
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
        return self.post("/admin/modulos", json=data, invalidate_cache=["modulos"])

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

    def get_modulos_statistics(self, force_refresh: bool = False) -> Dict[str, Any]:
        return self.get(
            "/admin/modulos/statistics",
            cache_type="modulos",
            force_refresh=force_refresh,
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
        return self.post(
            f"/admin/modulos/{modulo_id}/lecciones",
            json=data,
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
            cache_type="lecciones",
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
            cache_type="lecciones",
            force_refresh=force_refresh,
        )

    def create_ejercicio(
        self, modulo_id: int, leccion_id: int, data: Dict
    ) -> Dict[str, Any]:
        return self.post(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios",
            json=data,
            invalidate_cache=["lecciones"],
        )

    def update_ejercicio(
        self, modulo_id: int, leccion_id: int, ejercicio_id: int, data: Dict
    ) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios/{ejercicio_id}",
            json=data,
            invalidate_cache=["lecciones"],
        )

    def delete_ejercicio(
        self, modulo_id: int, leccion_id: int, ejercicio_id: int
    ) -> Dict[str, Any]:
        return self.delete(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios/{ejercicio_id}",
            invalidate_cache=["lecciones"],
        )

    def update_ejercicio_opciones(
        self, modulo_id: int, leccion_id: int, ejercicio_id: int, opciones: list
    ) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios/{ejercicio_id}/opciones",
            json={"opciones": opciones},
            invalidate_cache=["lecciones"],
        )

    # ============= EVALUACIONES =============
    def get_evaluacion(
        self, modulo_id: int, force_refresh: bool = False
    ) -> Dict[str, Any]:
        return self.get(
            f"/admin/modulos/{modulo_id}/evaluacion",
            cache_type="evaluaciones",
            force_refresh=force_refresh,
        )

    def update_evaluacion_config(self, modulo_id: int, data: Dict) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}/evaluacion/config",
            json=data,
            invalidate_cache=["evaluaciones"],
        )

    def create_pregunta(
        self, modulo_id: int, evaluacion_id: int, data: Dict
    ) -> Dict[str, Any]:
        return self.post(
            f"/admin/modulos/{modulo_id}/evaluacion/{evaluacion_id}/preguntas",
            json=data,
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

    def get_evaluaciones_statistics(
        self, force_refresh: bool = False
    ) -> Dict[str, Any]:
        return self.get(
            "/admin/evaluaciones/statistics",
            cache_type="evaluaciones",
            force_refresh=force_refresh,
        )
