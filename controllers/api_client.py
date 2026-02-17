import requests
import os
import time
import json
import hashlib
import re  # AÑADIDO PARA VALIDACIONES
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

    # ============= SEÑALES NUEVAS PARA ACTUALIZACIÓN EN TIEMPO REAL =============
    data_changed = pyqtSignal(str)  # Señal genérica cuando cualquier dato cambia
    usuarios_changed = pyqtSignal()  # Señal específica para usuarios
    modulos_changed = pyqtSignal()  # Señal específica para módulos
    lecciones_changed = pyqtSignal()  # Señal específica para lecciones
    ejercicios_changed = pyqtSignal()  # Señal específica para ejercicios
    evaluaciones_changed = pyqtSignal()  # Señal específica para evaluaciones

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

        # ============= REGISTRO DE VISTAS/OBSERVADORES =============
        self.observers = {}  # Diccionario para almacenar callbacks por tipo

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
            logger.debug(
                f"Cache limpiado para tipo: {cache_type}, {len(keys_to_delete)} entradas"
            )
        else:
            self.cache.clear()
            logger.debug("Cache completamente limpiado")

    # ============= NUEVO: SISTEMA DE OBSERVADORES =============
    def subscribe(self, data_type: str, callback: Callable):
        """Suscribir una vista a cambios en un tipo de datos"""
        if data_type not in self.observers:
            self.observers[data_type] = []
        if callback not in self.observers[data_type]:
            self.observers[data_type].append(callback)
            logger.debug(f"Vista suscrita a cambios en: {data_type}")

    def unsubscribe(self, data_type: str, callback: Callable):
        """Desuscribir una vista"""
        if data_type in self.observers and callback in self.observers[data_type]:
            self.observers[data_type].remove(callback)
            logger.debug(f"Vista desuscrita de cambios en: {data_type}")

    def notify_changed(self, data_type: str):
        """Notificar a todas las vistas que un tipo de datos cambió"""
        logger.debug(f"Notificando cambio en: {data_type}")

        # Emitir señales
        self.data_changed.emit(data_type)

        # Emitir señal específica
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

        # Llamar callbacks registrados
        if data_type in self.observers:
            for callback in self.observers[data_type]:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error en callback para {data_type}: {e}")

    # ============= NUEVO: INVALIDAR CACHÉ POR TIPO =============
    def invalidate_cache_type(self, cache_type: str):
        """Invalidar TODO el caché de un tipo específico - SOLUCIÓN DEFINITIVA"""
        logger.debug(f"🔄 INVALIDANDO CACHÉ COMPLETO para: {cache_type}")

        # 1. Limpiar caché en memoria
        keys_to_delete = []
        for key in list(self.cache.keys()):
            # Buscar cualquier clave que contenga el tipo
            if cache_type.lower() in key.lower() or key == cache_type:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.cache[key]

        logger.debug(f"   📦 Memoria: eliminadas {len(keys_to_delete)} entradas")

        # 2. Limpiar caché en disco si está habilitado
        if self.disk_cache_enabled and os.path.exists(self.cache_dir):
            try:
                disk_count = 0
                for filename in os.listdir(self.cache_dir):
                    if cache_type.lower() in filename.lower():
                        file_path = os.path.join(self.cache_dir, filename)
                        os.remove(file_path)
                        disk_count += 1
                if disk_count > 0:
                    logger.debug(f"   💾 Disco: eliminados {disk_count} archivos")
            except Exception as e:
                logger.error(f"Error limpiando caché en disco: {e}")

        # 3. Notificar a las vistas
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

                # Capturar errores de validación de Laravel
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

        # Formato estándar
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
        """GET con caché en memoria (ultra rápido)"""

        # Si es force_refresh, ignorar completamente la caché
        if force_refresh:
            logger.debug(f"Force refresh para {endpoint}")
            return self._request("GET", endpoint, params=params or {})

        # Sin caché configurada
        if not cache_type:
            return self._request("GET", endpoint, params=params or {})

        # Verificar si el tipo de caché está habilitado
        if (
            cache_type in self.cache_config
            and not self.cache_config[cache_type]["enabled"]
        ):
            return self._request("GET", endpoint, params=params or {})

        # Intentar obtener de caché
        cache_key = self._get_cache_key(endpoint, params)
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            if not entry.is_expired():
                logger.debug(f"Cache HIT para {endpoint}")
                return entry.data
            else:
                logger.debug(f"Cache EXPIRED para {endpoint}")
                del self.cache[cache_key]

        # Petición real
        logger.debug(f"Cache MISS para {endpoint}")
        result = self._request("GET", endpoint, params=params or {})

        # Guardar en caché si fue exitoso
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

        # Invalidar caché y notificar cambios
        if result.get("success", False):
            if invalidate_cache:
                for cache_type in invalidate_cache:
                    self.invalidate_cache_type(cache_type)
            else:
                # Si no se especifica, intentar inferir del endpoint
                self._auto_invalidate_from_endpoint(endpoint, "POST")

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
                self._auto_invalidate_from_endpoint(endpoint, "PUT")

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
                self._auto_invalidate_from_endpoint(endpoint, "PATCH")

        return result

    def delete(self, endpoint: str, invalidate_cache: list = None) -> Dict[str, Any]:
        result = self._request("DELETE", endpoint)

        if result.get("success", False):
            if invalidate_cache:
                for cache_type in invalidate_cache:
                    self.invalidate_cache_type(cache_type)
            else:
                self._auto_invalidate_from_endpoint(endpoint, "DELETE")

        return result

    def _auto_invalidate_from_endpoint(self, endpoint: str, method: str):
        """Inferir qué tipo de caché invalidar basado en el endpoint"""
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
        else:
            logger.debug(f"No se pudo inferir tipo de caché para: {endpoint}")

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

    # ============= USUARIOS - VERSIÓN MEJORADA =============
    def get_usuarios(
        self, page: int = 1, per_page: int = 100, force_refresh: bool = False
    ) -> Dict[str, Any]:
        """
        Obtener usuarios con paginación
        page: número de página
        per_page: cantidad por página (100 para traer casi todos)
        """
        params = {"page": page, "per_page": per_page}

        result = self.get(
            "/admin/usuarios",
            params=params,
            cache_type="usuarios",
            force_refresh=force_refresh,
        )

        # Log para depuración
        if result.get("success", False):
            data = result.get("data", [])
            logger.debug(
                f"get_usuarios página {page}: {len(data) if isinstance(data, list) else 'no es lista'} usuarios"
            )

            # Verificar si la respuesta incluye meta datos de paginación
            meta = result.get("meta", {})
            if meta:
                logger.debug(
                    f"Meta datos: total={meta.get('total')}, página={meta.get('current_page')}, últimas={meta.get('last_page')}"
                )

        return result

    def create_usuario(self, data: Dict) -> Dict[str, Any]:
        """
        Crear nuevo usuario con validaciones según API Laravel

        La API espera:
        - nombre: string, requerido
        - email: string, email válido, único en la BD
        - password: string, mínimo 8 caracteres, con mayúsculas, minúsculas y números
        - rol: 'aprendiz' o 'administrador'
        - estado: 'activo' o 'inactivo'
        - avatar_id: (opcional) ID del avatar seleccionado

        La API automáticamente:
        - Envía email de verificación
        - Asigna avatar por defecto si no se especifica
        - Hashea la contraseña
        """
        logger.debug(f"🔄 Creando usuario: {data.get('email')}")

        # Validaciones locales antes de enviar a la API
        errores = []

        # Validar nombre
        nombre = data.get("nombre", "").strip()
        if not nombre:
            errores.append("El nombre es requerido")
        elif len(nombre) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres")
        else:
            data["nombre"] = nombre

        # Validar email
        email = data.get("email", "").strip().lower()
        if not email:
            errores.append("El email es requerido")
        elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            errores.append("Formato de email inválido")
        else:
            # Actualizar email a minúsculas
            data["email"] = email

        # Validar contraseña
        password = data.get("password", "")
        if not password:
            errores.append("La contraseña es requerida")
        else:
            # Reglas de contraseña de Laravel
            if len(password) < 8:
                errores.append("La contraseña debe tener mínimo 8 caracteres")
            if not re.search(r"[A-Z]", password):
                errores.append("La contraseña debe tener al menos una mayúscula")
            if not re.search(r"[a-z]", password):
                errores.append("La contraseña debe tener al menos una minúscula")
            if not re.search(r"[0-9]", password):
                errores.append("La contraseña debe tener al menos un número")

        # Validar rol
        rol = data.get("rol", "aprendiz")
        if rol not in ["aprendiz", "administrador"]:
            errores.append("Rol inválido. Debe ser 'aprendiz' o 'administrador'")

        # Validar estado
        estado = data.get("estado", "activo")
        if estado not in ["activo", "inactivo"]:
            errores.append("Estado inválido. Debe ser 'activo' o 'inactivo'")

        # Si hay errores, retornar sin enviar a la API
        if errores:
            logger.error(f"❌ Errores de validación: {errores}")
            return {
                "success": False,
                "error": "Errores de validación",
                "errors": errores,
                "status_code": 422,
            }

        # Preparar datos para la API
        api_data = {
            "nombre": nombre,
            "email": email,
            "password": password,
            "rol": rol,
            "estado": estado,
        }

        # Incluir avatar si está seleccionado
        if data.get("avatar_id"):
            api_data["avatar_id"] = data["avatar_id"]

        logger.debug(f"📤 Enviando a API: {api_data}")

        try:
            # Enviar a la API
            result = self.post(
                "/admin/usuarios",
                json=api_data,
                invalidate_cache=["usuarios"],
            )

            # Procesar respuesta de la API
            if result.get("success"):
                logger.info(f"✅ Usuario creado exitosamente: {email}")

                # La API Laravel envía email de verificación automáticamente
                # Verificar si la respuesta incluye información adicional
                if result.get("data"):
                    user_data = result["data"]

                    # Agregar información sobre verificación de email
                    if user_data.get("email_verified_at"):
                        result["email_verified"] = True
                        result["message"] = "Usuario creado con email verificado"
                    else:
                        result["email_verified"] = False
                        result["message"] = (
                            "Usuario creado. Se envió email de verificación"
                        )

                        # Registrar que se envió el email
                        logger.info(f"📧 Email de verificación enviado a: {email}")

                return result

            else:
                # Manejar errores de la API Laravel
                error_msg = result.get("error", "Error desconocido")
                status_code = result.get("status_code", 500)

                # Laravel típicamente retorna errores de validación con código 422
                if status_code == 422:
                    # Intentar parsear errores de validación de Laravel
                    if "errors" in result:
                        errores_laravel = []
                        for field, messages in result["errors"].items():
                            for msg in messages:
                                errores_laravel.append(f"{field}: {msg}")

                        logger.error(
                            f"❌ Errores de validación Laravel: {errores_laravel}"
                        )
                        result["validation_errors"] = errores_laravel

                        # Mensajes específicos
                        if "email" in str(errores_laravel).lower():
                            if "unique" in str(errores_laravel).lower():
                                result["error"] = (
                                    "El email ya está registrado en el sistema"
                                )

                    elif "email" in str(error_msg).lower():
                        if (
                            "unique" in str(error_msg).lower()
                            or "taken" in str(error_msg).lower()
                        ):
                            result["error"] = "❌ El email ya está registrado"
                        elif "format" in str(error_msg).lower():
                            result["error"] = "❌ Formato de email inválido"

                    elif "password" in str(error_msg).lower():
                        result["error"] = (
                            "❌ La contraseña no cumple con los requisitos de seguridad"
                        )

                elif status_code == 401:
                    result["error"] = (
                        "❌ Sesión expirada. Por favor, inicia sesión nuevamente"
                    )

                elif status_code == 403:
                    result["error"] = "❌ No tienes permisos para crear usuarios"

                logger.error(f"❌ Error API ({status_code}): {result.get('error')}")
                return result

        except requests.ConnectionError:
            logger.error("❌ Error de conexión con la API")
            return {
                "success": False,
                "error": "Error de conexión con el servidor",
                "status_code": 503,
            }
        except requests.Timeout:
            logger.error("❌ Timeout de conexión")
            return {
                "success": False,
                "error": "Tiempo de espera agotado",
                "status_code": 504,
            }
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}")
            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}",
                "status_code": 500,
            }

    def update_usuario(self, usuario_id: int, data: Dict) -> Dict[str, Any]:
        """Actualizar usuario existente"""
        logger.debug(f"Actualizando usuario ID: {usuario_id}")

        # Validaciones básicas para actualización
        errores = []

        # Validar nombre si está presente
        if "nombre" in data:
            nombre = data["nombre"].strip()
            if not nombre:
                errores.append("El nombre no puede estar vacío")
            elif len(nombre) < 3:
                errores.append("El nombre debe tener al menos 3 caracteres")
            else:
                data["nombre"] = nombre

        # Validar email si está presente
        if "email" in data:
            email = data["email"].strip().lower()
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                errores.append("Formato de email inválido")
            else:
                data["email"] = email

        # Validar contraseña si está presente
        if "password" in data and data["password"]:
            password = data["password"]
            if len(password) < 8:
                errores.append("La contraseña debe tener mínimo 8 caracteres")
            if not re.search(r"[A-Z]", password):
                errores.append("La contraseña debe tener al menos una mayúscula")
            if not re.search(r"[a-z]", password):
                errores.append("La contraseña debe tener al menos una minúscula")
            if not re.search(r"[0-9]", password):
                errores.append("La contraseña debe tener al menos un número")

        # Validar rol si está presente
        if "rol" in data and data["rol"] not in ["aprendiz", "administrador"]:
            errores.append("Rol inválido. Debe ser 'aprendiz' o 'administrador'")

        # Validar estado si está presente
        if "estado" in data and data["estado"] not in ["activo", "inactivo"]:
            errores.append("Estado inválido. Debe ser 'activo' o 'inactivo'")

        # Si hay errores, retornar sin enviar a la API
        if errores:
            logger.error(f"❌ Errores de validación: {errores}")
            return {
                "success": False,
                "error": "Errores de validación",
                "errors": errores,
                "status_code": 422,
            }

        result = self.put(
            f"/admin/usuarios/{usuario_id}",
            json=data,
            invalidate_cache=["usuarios"],
        )
        return result

    def delete_usuario(self, usuario_id: int) -> Dict[str, Any]:
        """Eliminar usuario"""
        logger.debug(f"Eliminando usuario ID: {usuario_id}")
        result = self.delete(
            f"/admin/usuarios/{usuario_id}",
            invalidate_cache=["usuarios"],
        )
        return result

    def toggle_usuario_status(self, usuario_id: int) -> Dict[str, Any]:
        """Cambiar estado de usuario"""
        logger.debug(f"Cambiando estado usuario ID: {usuario_id}")
        result = self.patch(
            f"/admin/usuarios/{usuario_id}/toggle-status",
            invalidate_cache=["usuarios"],
        )
        return result

    # ============= MÓDULOS - VERSIÓN CORREGIDA =============
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
        # Validaciones básicas para módulo
        if not data.get("titulo"):
            return {"success": False, "error": "El título es requerido"}
        if not data.get("descripcion"):
            return {"success": False, "error": "La descripción es requerida"}

        return self.post("/admin/modulos", json=data, invalidate_cache=["modulos"])

    def update_modulo(self, modulo_id: int, data: Dict) -> Dict[str, Any]:
        return self.put(
            f"/admin/modulos/{modulo_id}",
            json=data,
            invalidate_cache=["modulos"],
        )

    def delete_modulo(self, modulo_id: int) -> Dict[str, Any]:
        return self.delete(
            f"/admin/modulos/{modulo_id}",
            invalidate_cache=["modulos"],
        )

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

    # ============= LECCIONES - VERSIÓN CORREGIDA =============
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
        # Validaciones básicas para lección
        if not data.get("titulo"):
            return {"success": False, "error": "El título es requerido"}
        if not data.get("contenido"):
            return {"success": False, "error": "El contenido es requerido"}

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

    # ============= EJERCICIOS - VERSIÓN CORREGIDA =============
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
        # Validaciones básicas para ejercicio
        if not data.get("pregunta"):
            return {"success": False, "error": "La pregunta es requerida"}
        if not data.get("tipo"):
            return {"success": False, "error": "El tipo de ejercicio es requerido"}

        return self.post(
            f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios",
            json=data,
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

    # ============= EVALUACIONES - VERSIÓN CORREGIDA =============
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
        # Validaciones básicas para pregunta
        if not data.get("pregunta"):
            return {"success": False, "error": "La pregunta es requerida"}

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
