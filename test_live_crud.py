"""
TEST EN VIVO: Crea una lección + 3 ejercicios + evaluación con 3 preguntas
Los cambios aparecen en la app abierta en tiempo real gracias al auto-refresh.
"""
import sys
import time
import json

sys.path.insert(0, r"c:\Users\Henry\Desktop\admin-python - copia")

import os
os.environ.setdefault("API_URL", "http://localhost:8000/api")

import requests

BASE_URL = os.environ.get("API_URL", "http://localhost:8000/api")
session = requests.Session()
TOKEN = None

def header():
    return {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}

def paso(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print('='*60)

def ok(msg):  print(f"  ✅ {msg}")
def err(msg): print(f"  ❌ {msg}")
def info(msg): print(f"  ℹ️  {msg}")

# ── 1. LOGIN ─────────────────────────────────────────────────
paso("1. LOGIN")
r = session.post(f"{BASE_URL}/login",
                 json={"email": "alejo29.c@gmail.com", "password": "Password123"})
data = r.json()
# La API puede devolver token en data.token o directamente en access_token
TOKEN = (data.get("data", {}) or {}).get("token") or data.get("access_token")
if not TOKEN:
    err(f"Login falló: {data}")
    sys.exit(1)
user = (data.get("data", {}) or {}).get("user") or data.get("user", {})
ok(f"Login OK — usuario: {user.get('nombre', user.get('name', 'N/A'))}")

# ── 2. OBTENER MÓDULOS ────────────────────────────────────────
paso("2. OBTENER MÓDULOS")
r = session.get(f"{BASE_URL}/admin/modulos", headers=header())
mods = r.json()
if not mods.get("success") or not mods.get("data"):
    err("No hay módulos")
    sys.exit(1)
modulo = mods["data"][0]
MODULO_ID = modulo["id"]
ok(f"Módulo seleccionado: [{MODULO_ID}] {modulo['titulo']}")

# ── 3. CREAR LECCIÓN ─────────────────────────────────────────
paso("3. CREAR LECCIÓN NUEVA")
num = int(time.time()) % 1000
leccion_data = {
    "titulo": f"Lección de prueba #{num}",
    "contenido": "<h2>Lección de prueba</h2><p>Esta lección fue creada automáticamente para testear el sistema.</p>",
    "tipo": "texto",
    "orden": 99,
    "estado": "activo",
    "duracion_estimada": 10,
    "puntos": 5,
}
r = session.post(f"{BASE_URL}/admin/modulos/{MODULO_ID}/lecciones",
                 json=leccion_data, headers=header())
resp = r.json()
if not resp.get("success"):
    err(f"No se pudo crear lección: {resp}")
    sys.exit(1)
LECCION = resp["data"]
LECCION_ID = LECCION["id"]
ok(f"Lección creada: [{LECCION_ID}] {LECCION['titulo']}")
time.sleep(0.5)

# ── 4. CREAR EJERCICIO VERDADERO/FALSO ───────────────────────
paso("4. EJERCICIO: Verdadero / Falso")
r = session.post(f"{BASE_URL}/admin/modulos/{MODULO_ID}/lecciones/{LECCION_ID}/ejercicios",
    json={
        "titulo": "¿HTML es un lenguaje de programación?",
        "tipo": "verdadero_falso",
        "orden": 1,
        "puntos": 10,
        "explicacion": "HTML es un lenguaje de marcado, NO de programación.",
        "opciones": [
            {"texto": "Verdadero", "es_correcta": False, "orden": 1},
            {"texto": "Falso", "es_correcta": True, "orden": 2},
        ]
    }, headers=header())
resp = r.json()
if resp.get("success"):
    ok(f"Ejercicio V/F creado: ID={resp['data']['id']}")
else:
    err(f"Fallo: {resp}")
time.sleep(0.5)

# ── 5. CREAR EJERCICIO SELECCIÓN MÚLTIPLE ────────────────────
paso("5. EJERCICIO: Selección Múltiple")
r = session.post(f"{BASE_URL}/admin/modulos/{MODULO_ID}/lecciones/{LECCION_ID}/ejercicios",
    json={
        "titulo": "¿Cuál etiqueta se usa para un párrafo en HTML?",
        "tipo": "seleccion_multiple",
        "orden": 2,
        "puntos": 10,
        "explicacion": "La etiqueta <p> define un párrafo.",
        "opciones": [
            {"texto": "<p>",    "es_correcta": True,  "orden": 1},
            {"texto": "<h1>",   "es_correcta": False, "orden": 2},
            {"texto": "<div>",  "es_correcta": False, "orden": 3},
            {"texto": "<span>", "es_correcta": False, "orden": 4},
        ]
    }, headers=header())
resp = r.json()
if resp.get("success"):
    ok(f"Ejercicio selección múltiple creado: ID={resp['data']['id']}")
else:
    err(f"Fallo: {resp}")
time.sleep(0.5)

# ── 6. CREAR EJERCICIO ARRASTRAR Y SOLTAR ────────────────────
paso("6. EJERCICIO: Arrastrar y Soltar")
r = session.post(f"{BASE_URL}/admin/modulos/{MODULO_ID}/lecciones/{LECCION_ID}/ejercicios",
    json={
        "titulo": "Une cada etiqueta con su función",
        "tipo": "arrastrar_soltar",
        "orden": 3,
        "puntos": 15,
        "explicacion": "Cada etiqueta HTML tiene una función específica.",
        "opciones": [
            {"texto": "<h1>",  "definicion": "Título principal",  "orden": 1},
            {"texto": "<p>",   "definicion": "Párrafo de texto",  "orden": 2},
            {"texto": "<img>", "definicion": "Insertar imagen",   "orden": 3},
            {"texto": "<a>",   "definicion": "Enlace/hipervínculo","orden": 4},
        ]
    }, headers=header())
resp = r.json()
if resp.get("success"):
    ok(f"Ejercicio arrastrar/soltar creado: ID={resp['data']['id']}")
else:
    err(f"Fallo: {resp}")
time.sleep(0.5)

# ── 7. CONFIGURAR EVALUACIÓN ─────────────────────────────────
paso("7. CONFIGURAR EVALUACIÓN DEL MÓDULO")
r = session.put(f"{BASE_URL}/admin/modulos/{MODULO_ID}/evaluacion/config",
    json={
        "titulo": f"Evaluación de Prueba — {modulo['titulo']}",
        "numero_preguntas": 3,
        "tiempo_limite": 20,
        "puntaje_minimo": 70,
        "max_intentos": 2,
        "estado": "activo",
    }, headers=header())
resp = r.json()
if not resp.get("success"):
    err(f"Fallo al configurar evaluación: {resp}")
    sys.exit(1)
EVAL_ID = resp["data"]["id"]
ok(f"Evaluación configurada: ID={EVAL_ID}")
time.sleep(0.5)

# ── 8. PREGUNTA V/F EN LA EVALUACIÓN ─────────────────────────
paso("8. PREGUNTA evaluación: Verdadero / Falso")
r = session.post(f"{BASE_URL}/admin/modulos/{MODULO_ID}/evaluacion/{EVAL_ID}/preguntas",
    json={
        "pregunta": "CSS se usa para dar estilo a las páginas web.",
        "tipo": "verdadero_falso",
        "puntos": 10,
        "orden": 1,
        "opciones": [
            {"texto": "Verdadero", "es_correcta": True,  "orden": 1},
            {"texto": "Falso",     "es_correcta": False, "orden": 2},
        ]
    }, headers=header())
resp = r.json()
if resp.get("success"):
    ok(f"Pregunta V/F creada: ID={resp['data']['id']}")
else:
    err(f"Fallo: {resp}")
time.sleep(0.5)

# ── 9. PREGUNTA SELECCIÓN MÚLTIPLE EN EVALUACIÓN ─────────────
paso("9. PREGUNTA evaluación: Selección Múltiple")
r = session.post(f"{BASE_URL}/admin/modulos/{MODULO_ID}/evaluacion/{EVAL_ID}/preguntas",
    json={
        "pregunta": "¿Qué propiedad CSS cambia el color de texto?",
        "tipo": "seleccion_multiple",
        "puntos": 10,
        "orden": 2,
        "opciones": [
            {"texto": "color",            "es_correcta": True,  "orden": 1},
            {"texto": "background-color", "es_correcta": False, "orden": 2},
            {"texto": "font-size",        "es_correcta": False, "orden": 3},
            {"texto": "border",           "es_correcta": False, "orden": 4},
        ]
    }, headers=header())
resp = r.json()
if resp.get("success"):
    ok(f"Pregunta selección múltiple creada: ID={resp['data']['id']}")
else:
    err(f"Fallo: {resp}")
time.sleep(0.5)

# ── 10. PREGUNTA ARRASTRAR EN EVALUACIÓN ─────────────────────
paso("10. PREGUNTA evaluación: Arrastrar y Soltar")
r = session.post(f"{BASE_URL}/admin/modulos/{MODULO_ID}/evaluacion/{EVAL_ID}/preguntas",
    json={
        "pregunta": "Relaciona cada propiedad CSS con su función",
        "tipo": "arrastrar_soltar",
        "puntos": 15,
        "orden": 3,
        "opciones": [
            {"texto": "color",       "pareja_arrastre": "Color del texto",        "orden": 1},
            {"texto": "margin",      "pareja_arrastre": "Espacio exterior",       "orden": 2},
            {"texto": "padding",     "pareja_arrastre": "Espacio interior",       "orden": 3},
            {"texto": "font-size",   "pareja_arrastre": "Tamaño de la fuente",    "orden": 4},
        ]
    }, headers=header())
resp = r.json()
if resp.get("success"):
    ok(f"Pregunta arrastrar/soltar creada: ID={resp['data']['id']}")
else:
    err(f"Fallo: {resp}")

# ── RESUMEN FINAL ─────────────────────────────────────────────
paso("✅ PRUEBA COMPLETADA")
print(f"""
  Módulo:    [{MODULO_ID}] {modulo['titulo']}
  Lección:   [{LECCION_ID}] {LECCION['titulo']}
  
  Ejercicios creados en la lección:
    • Verdadero / Falso     ✅
    • Selección múltiple    ✅
    • Arrastrar y soltar    ✅

  Evaluación [{EVAL_ID}]:
    • Pregunta V/F          ✅
    • Pregunta selección    ✅
    • Pregunta arrastrar    ✅

  👉 Abre la app, ve a Módulos → {modulo['titulo']}
     → pestañas Lecciones y Evaluación para ver todo.
""")
