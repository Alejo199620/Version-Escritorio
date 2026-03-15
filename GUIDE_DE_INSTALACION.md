# Guía de Instalación - Varchate Admin

Esta guía proporciona las instrucciones necesarias para instalar y ejecutar la aplicación **Varchate Admin** en cualquier equipo.

---

## Opción 1: Ejecución Portátil (Recomendado para usuarios)

Esta es la forma más rápida de ejecutar la aplicación sin necesidad de instalar Python o dependencias.

1.  Localiza la carpeta `dist/` en los archivos del proyecto.
2.  Dentro de `dist/`, encontrarás una carpeta llamada `varchate admin`.
3.  **Importante:** Asegúrate de que el archivo `varchate admin.exe` y la carpeta `_internal` permanezcan en la misma ubicación.
4.  Ejecuta `varchate admin.exe` para iniciar la aplicación.

---

## Opción 2: Instalación desde el Código Fuente (Para desarrolladores)

Si deseas ejecutar la aplicación desde el código fuente o realizar modificaciones, sigue estos pasos:

### 1. Requisitos Previos

- Tener instalado [Python 3.12](https://www.python.org/downloads/) o superior.
- Git (opcional, para clonar el repositorio).

### 2. Configuración del Entorno Virtual

Abre una terminal en la carpeta raíz del proyecto y ejecuta:

```powershell
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual (Windows)
.\venv\Scripts\activate
```

### 3. Instalación de Dependencias

Con el entorno virtual activado, instala las librerías necesarias:

```powershell
pip install -r requirements.txt
```

### 4. Ejecución de la Aplicación

Una vez instaladas las dependencias, puedes iniciar la aplicación con:

```powershell
python main.py
```

---

## Configuración Adicional

### Variables de Entorno (.env)

La aplicación requiere saber dónde se encuentra el servidor API. Asegúrate de tener un archivo `.env` en la raíz con el siguiente contenido:

```env
API_URL=http://localhost:8001/api
```

_Si el servidor está en otra dirección o puerto, actualiza esta URL._

### Base de Datos

Si necesitas configurar la base de datos localmente, se incluye el archivo `varchate_db.sql` con la estructura necesaria para importar en tu servidor MySQL/MariaDB.

---

## 📝 Notas

- La aplicación utiliza **PyQt6** para la interfaz gráfica.
- Si encuentras errores al iniciar, verifica que el archivo `.env` esté correctamente configurado.
- Para generar un nuevo ejecutable, puedes usar el archivo `Varchate.spec` con PyInstaller: `pyinstaller Varchate.spec`.
