"""
Test completo del flujo: Login -> Módulo JS -> Lección -> Ejercicio -> Evaluación con 2 preguntas
Ejecutar con: venv\Scripts\python.exe test_workflow.py
"""
import os
import sys
import json
import requests

# Evitar que Qt se inicie al importar
os.environ.setdefault("API_URL", "http://localhost:8000/api")

BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")
EMAIL = "alejo29.c@gmail.com"
PASSWORD = "Password123"

session = requests.Session()
session.headers.update({
    "Accept": "application/json",
    "Content-Type": "application/json",
})

GREEN = "\033[92m"
RED   = "\033[91m"
CYAN  = "\033[96m"
YELLOW= "\033[93m"
RESET = "\033[0m"
BOLD  = "\033[1m"

def ok(label, data=None):
    print(f"  {GREEN}✔{RESET} {label}")
    if data:
        print(f"    {CYAN}{json.dumps(data, ensure_ascii=False, indent=2)[:300]}{RESET}")

def fail(label, error):
    print(f"  {RED}✘{RESET} {label}: {RED}{error}{RESET}")
    sys.exit(1)

def step(title):
    print(f"\n{BOLD}{YELLOW}{'='*55}{RESET}")
    print(f"{BOLD}{YELLOW}  {title}{RESET}")
    print(f"{BOLD}{YELLOW}{'='*55}{RESET}")

def post(endpoint, data, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = session.post(f"{BASE_URL}{endpoint}", json=data, headers=headers, timeout=10)
    try:
        return r.json()
    except Exception:
        return {"success": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}

def get(endpoint, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = session.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
    try:
        return r.json()
    except Exception:
        return {"success": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}

def put(endpoint, data, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = session.put(f"{BASE_URL}{endpoint}", json=data, headers=headers, timeout=10)
    try:
        return r.json()
    except Exception:
        return {"success": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}


# ─────────────────────────────────────────────
# PASO 1: LOGIN
# ─────────────────────────────────────────────
step("PASO 1: LOGIN")
res = post("/login", {"email": EMAIL, "password": PASSWORD})

if not res.get("access_token") and not (res.get("data") or {}).get("access_token"):
    # Intentar formato directo
    token = res.get("access_token") or res.get("token")
    if not token and isinstance(res.get("data"), dict):
        token = res["data"].get("access_token") or res["data"].get("token")
    if not token:
        fail("Login", f"No token en respuesta: {json.dumps(res, indent=2)[:400]}")
else:
    token = res.get("access_token") or res.get("token")
    if not token and isinstance(res.get("data"), dict):
        token = res["data"].get("access_token") or res["data"].get("token")

ok(f"Login exitoso como {EMAIL}")
ok("Token obtenido", {"token_preview": f"{token[:30]}..."})

user_data = res.get("user") or (res.get("data") or {}).get("user") or {}
user_id = user_data.get("id", 1)
ok(f"Usuario ID: {user_id}", user_data)


# ─────────────────────────────────────────────
# PASO 2: CREAR MÓDULO
# ─────────────────────────────────────────────
step("PASO 2: CREAR MÓDULO — JavaScript Fundamentals")

import re
titulo_modulo = "JavaScript Fundamentals - Test"
slug = re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", titulo_modulo.lower())).strip("-")

modulo_data = {
    "titulo": titulo_modulo,
    "descripcion_larga": "Módulo completo sobre los fundamentos de JavaScript: variables, funciones, arrays, objetos y más. Ideal para principiantes.",
    "modulo": "javascript",
    "estado": "activo",
    "orden_global": 99,
    "slug": slug,
    "created_by": user_id,
}

res = post("/admin/modulos", modulo_data, token)
if not res.get("success") and not res.get("id") and not (isinstance(res.get("data"), dict) and res["data"].get("id")):
    # Inspeccionar respuesta real
    print(f"  {YELLOW}Respuesta API:{RESET} {json.dumps(res, ensure_ascii=False, indent=2)[:600]}")
    # Si es éxito pero formato distinto, continuar
    modulo_id = res.get("id") or (res.get("data") or {}).get("id")
    if not modulo_id:
        fail("Crear módulo", res.get("error") or res.get("message") or str(res)[:300])
else:
    modulo_id = res.get("id") or (res.get("data") or {}).get("id")

ok(f"Módulo creado — ID: {modulo_id}")
ok("Datos del módulo", {"id": modulo_id, "titulo": titulo_modulo, "tipo": "javascript"})


# ─────────────────────────────────────────────
# PASO 3: CREAR LECCIÓN
# ─────────────────────────────────────────────
step("PASO 3: CREAR LECCIÓN — Variables y Tipos de Datos")

leccion_data = {
    "titulo": "Variables y Tipos de Datos en JavaScript",
    "contenido": "<h2>Variables en JavaScript</h2><p>JavaScript usa <code>var</code>, <code>let</code> y <code>const</code> para declarar variables. <code>let</code> y <code>const</code> son las formas modernas recomendadas.</p><pre><code>let nombre = 'Juan';\nconst PI = 3.14;\nvar edad = 25;</code></pre>",
    "orden": 1,
    "estado": "activo",
    "duracion_minutos": 20,
    "created_by": user_id,
}

res = post(f"/admin/modulos/{modulo_id}/lecciones", leccion_data, token)
leccion_id = res.get("id") or (res.get("data") or {}).get("id")
if not leccion_id:
    print(f"  {YELLOW}Respuesta:{RESET} {json.dumps(res, ensure_ascii=False)[:400]}")
    fail("Crear lección", res.get("error") or res.get("message") or str(res))

ok(f"Lección creada — ID: {leccion_id}")
ok("Datos de la lección", {"id": leccion_id, "titulo": leccion_data["titulo"]})


# ─────────────────────────────────────────────
# PASO 4: CREAR EJERCICIO
# ─────────────────────────────────────────────
step("PASO 4: CREAR EJERCICIO — Opción múltiple sobre JS")

ejercicio_data = {
    "pregunta": "¿Cuál es la forma moderna y recomendada para declarar una variable en JavaScript que NO cambiará su valor?",
    "tipo": "seleccion_multiple",
    "nivel_dificultad": "facil",
    "puntaje": 10,
    "explicacion": "La palabra clave 'const' declara una constante. Su valor no puede ser reasignado una vez definido, lo que la hace ideal para valores que no cambian.",
    "opciones": [
        {"texto": "var", "es_correcta": False},
        {"texto": "let", "es_correcta": False},
        {"texto": "const", "es_correcta": True},
        {"texto": "function", "es_correcta": False},
    ],
    "created_by": user_id,
}

res = post(f"/admin/modulos/{modulo_id}/lecciones/{leccion_id}/ejercicios", ejercicio_data, token)
ejercicio_id = res.get("id") or (res.get("data") or {}).get("id")
if not ejercicio_id:
    print(f"  {YELLOW}Respuesta:{RESET} {json.dumps(res, ensure_ascii=False)[:400]}")
    fail("Crear ejercicio", res.get("error") or res.get("message") or str(res))

ok(f"Ejercicio creado — ID: {ejercicio_id}")
ok("Ejercicio JS", {"id": ejercicio_id, "tipo": "opcion_multiple", "respuesta_correcta": "const"})


# ─────────────────────────────────────────────
# PASO 5: CONFIGURAR EVALUACIÓN
# ─────────────────────────────────────────────
step("PASO 5: CONFIGURAR EVALUACIÓN del Módulo")

eval_config = {
    "titulo": "Evaluación Final — JavaScript Fundamentals",
    "descripcion": "Prueba tu conocimiento sobre los fundamentos de JavaScript.",
    "tiempo_limite": 30,
    "numero_preguntas": 2,
    "puntaje_minimo": 70,
    "max_intentos": 3,
    "intentos_permitidos": 3,
    "puntaje_aprobacion": 70,
    "orden_preguntas_aleatorio": True,
    "mostrar_respuestas": True,
    "estado": "activo",
    "created_by": user_id,
}

res = put(f"/admin/modulos/{modulo_id}/evaluacion/config", eval_config, token)
evaluacion_id = res.get("id") or (res.get("data") or {}).get("id") or (res.get("evaluacion") or {}).get("id")
if not evaluacion_id:
    print(f"  {YELLOW}Respuesta config:{RESET} {json.dumps(res, ensure_ascii=False)[:400]}")
    # Intentar obtener evaluación existente
    r2 = get(f"/admin/modulos/{modulo_id}/evaluacion", token)
    evaluacion_id = r2.get("id") or (r2.get("data") or {}).get("id") or (r2.get("evaluacion") or {}).get("id")
    if not evaluacion_id:
        fail("Configurar evaluación", f"No se pudo obtener ID de la evaluación. Config resp: {str(res)[:250]} | Get resp: {str(r2)[:250]}")

ok(f"Evaluación configurada — ID: {evaluacion_id}")
ok("Config", {"titulo": eval_config["titulo"], "tiempo": "30min", "aprobacion": "70%"})


# ─────────────────────────────────────────────
# PASO 6: CREAR PREGUNTA 1
# ─────────────────────────────────────────────
step("PASO 6: CREAR PREGUNTA 1 de la Evaluación")

pregunta1_data = {
    "pregunta": "¿Qué operador se usa para comparar valor Y tipo en JavaScript?",
    "tipo": "seleccion_multiple",
    "puntos": 10,
    "explicacion": "El operador === compara tanto el valor como el tipo de dato, a diferencia de == que solo compara valor.",
    "opciones": [
        {"texto": "==",  "es_correcta": False},
        {"texto": "===", "es_correcta": True},
        {"texto": "!=",  "es_correcta": False},
        {"texto": "=",   "es_correcta": False},
    ],
    "created_by": user_id,
}

res = post(f"/admin/modulos/{modulo_id}/evaluacion/{evaluacion_id}/preguntas", pregunta1_data, token)
pregunta1_id = res.get("id") or (res.get("data") or {}).get("id")
if not pregunta1_id:
    print(f"  {YELLOW}Respuesta:{RESET} {json.dumps(res, ensure_ascii=False)[:400]}")
    fail("Crear pregunta 1", res.get("error") or res.get("message") or str(res))

ok(f"Pregunta 1 creada — ID: {pregunta1_id}")
ok("Pregunta 1", {"texto": pregunta1_data["pregunta"][:60] + "...", "correcta": "==="})


# ─────────────────────────────────────────────
# PASO 7: CREAR PREGUNTA 2
# ─────────────────────────────────────────────
step("PASO 7: CREAR PREGUNTA 2 de la Evaluación")

pregunta2_data = {
    "pregunta": "¿Cuál de los siguientes métodos sirve para agregar un elemento al FINAL de un array en JavaScript?",
    "tipo": "seleccion_multiple",
    "puntos": 10,
    "explicacion": "El método push() agrega uno o más elementos al final de un array y retorna la nueva longitud.",
    "opciones": [
        {"texto": "array.pop()",    "es_correcta": False},
        {"texto": "array.shift()",  "es_correcta": False},
        {"texto": "array.push()",   "es_correcta": True},
        {"texto": "array.splice()", "es_correcta": False},
    ],
    "created_by": user_id,
}

res = post(f"/admin/modulos/{modulo_id}/evaluacion/{evaluacion_id}/preguntas", pregunta2_data, token)
pregunta2_id = res.get("id") or (res.get("data") or {}).get("id")
if not pregunta2_id:
    print(f"  {YELLOW}Respuesta:{RESET} {json.dumps(res, ensure_ascii=False)[:400]}")
    fail("Crear pregunta 2", res.get("error") or res.get("message") or str(res))

ok(f"Pregunta 2 creada — ID: {pregunta2_id}")
ok("Pregunta 2", {"texto": pregunta2_data["pregunta"][:60] + "...", "correcta": "push()"})


# ─────────────────────────────────────────────
# RESUMEN FINAL
# ─────────────────────────────────────────────
print(f"\n{BOLD}{GREEN}{'='*55}{RESET}")
print(f"{BOLD}{GREEN}  ✅  FLUJO COMPLETO EXITOSO{RESET}")
print(f"{BOLD}{GREEN}{'='*55}{RESET}")
print(f"""
  {CYAN}Módulo    ID:{RESET} {modulo_id}  →  JavaScript Fundamentals - Test
  {CYAN}Lección   ID:{RESET} {leccion_id}  →  Variables y Tipos de Datos
  {CYAN}Ejercicio ID:{RESET} {ejercicio_id}  →  Opción múltiple (const vs var/let)
  {CYAN}Evaluación ID:{RESET} {evaluacion_id}  →  Evaluación Final JS
  {CYAN}Pregunta 1 ID:{RESET} {pregunta1_id}  →  Operador ===
  {CYAN}Pregunta 2 ID:{RESET} {pregunta2_id}  →  Método push()
""")
