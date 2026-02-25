"""
Debug script: Ver exactamente qué devuelve el API para el dashboard y módulos
"""
import os, json, requests

BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")
EMAIL = "alejo29.c@gmail.com"
PASSWORD = "Password123"

s = requests.Session()
s.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

# ── LOGIN ──
r = s.post(f"{BASE_URL}/login", json={"email": EMAIL, "password": PASSWORD}, timeout=10)
res = r.json()
token = res.get("access_token") or res.get("token") or (res.get("data") or {}).get("access_token")
print(f"✅ Token: {token[:20]}...")
s.headers["Authorization"] = f"Bearer {token}"

# ── DASHBOARD STATS ──
print("\n═══ /admin/dashboard ═══")
r = s.get(f"{BASE_URL}/admin/dashboard", timeout=10)
data = r.json()
print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])

# ── MÓDULOS ──
print("\n═══ /admin/modulos ═══")
r = s.get(f"{BASE_URL}/admin/modulos", timeout=10)
modulos_resp = r.json()
print(json.dumps(modulos_resp, indent=2, ensure_ascii=False)[:2000])

# ── KEYS DE PRIMER MÓDULO ──
raw_data = modulos_resp.get("data", modulos_resp)
modulos = raw_data if isinstance(raw_data, list) else raw_data.get("data", [])
if modulos:
    print(f"\n═══ Primer módulo — keys: {list(modulos[0].keys())} ═══")
    print(json.dumps(modulos[0], indent=2, ensure_ascii=False)[:500])

    # ── LECCIONES del primer módulo ──
    m_id = modulos[0]["id"]
    print(f"\n═══ /admin/modulos/{m_id}/lecciones?per_page=1 ═══")
    r = s.get(f"{BASE_URL}/admin/modulos/{m_id}/lecciones", params={"per_page": 1}, timeout=10)
    lec_resp = r.json()
    print(json.dumps(lec_resp, indent=2, ensure_ascii=False)[:1500])

    # Mostrar claves de meta
    meta = lec_resp.get("meta")
    print(f"\n  ➡ meta keys: {list(meta.keys()) if meta else 'NO META'}")
    if meta:
        print(f"  ➡ meta.total  = {meta.get('total')}")
        print(f"  ➡ meta.count  = {meta.get('count')}")

    # ── LECCIONES con per_page=100 ──
    print(f"\n═══ /admin/modulos/{m_id}/lecciones?per_page=100 ═══")
    r = s.get(f"{BASE_URL}/admin/modulos/{m_id}/lecciones", params={"per_page": 100}, timeout=10)
    lec_full = r.json()
    data_full = lec_full.get("data", [])
    if isinstance(data_full, list):
        print(f"  ➡ len(data) = {len(data_full)} lecciones")
    else:
        print(f"  ➡ data type: {type(data_full)}")
        print(json.dumps(lec_full, indent=2, ensure_ascii=False)[:800])
