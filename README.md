# Palmeras en la Mancha — Backend

Backend de la aplicación **Palmeras en la Mancha**, desarrollado con FastAPI y SQLAlchemy.

La API permite gestionar el catálogo musical y las entidades principales del proyecto: álbumes, formatos físicos, filiales y discográficas.


---

## Índice

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Variables de entorno](#variables-de-entorno)
- [Base de datos](#base-de-datos)
- [Arquitectura de datos](#arquitectura-de-datos)
- [Diagrama DER](#diagrama-der)
- [Migraciones con Alembic](#migraciones-con-alembic)
- [Ejecución del proyecto](#ejecución-del-proyecto)
- [Documentación de la API](#documentación-de-la-api)
- [Endpoints](#endpoints)
  - [Albums](#albums)
  - [Formats](#formats)
  - [Branches](#branches)
  - [Labels](#labels)
- [Ejemplos de query parameters](#ejemplos-de-query-parameters)
- [Validaciones](#validaciones)
- [Manejo de errores](#manejo-de-errores)
- [Testing](#testing)
- [Cloudinary](#cloudinary)
- [Calidad y buenas prácticas](#calidad-y-buenas-prácticas)

---

## Descripción

Este repositorio contiene el backend REST de Palmeras en la Mancha.

La aplicación proporciona una API para:

- Gestionar álbumes.
- Gestionar formatos físicos.
- Gestionar filiales.
- Gestionar discográficas.
- Buscar álbumes por título o artista.
- Filtrar álbumes por género.
- Validar los datos recibidos mediante Pydantic.
- Gestionar errores HTTP desde los controllers.
- Ejecutar tests automáticos sobre los endpoints principales.

La API está preparada para ser consumida por el frontend del proyecto mediante HTTP y JSON.

---

## Tecnologías

### Backend

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **Uvicorn**
- **SQLite**
- **Alembic**
- **Pytest**
- **HTTPX**
- **python-dotenv**

### Dependencias principales

Las versiones actuales se encuentran fijadas en `requirements.txt`.

Entre ellas:

```text
fastapi==0.142.2
SQLAlchemy==2.1.2
pydantic==2.13.5
uvicorn==0.54.0
pytest==9.1.1
httpx==0.28.1
python-dotenv==1.0.1
python-multipart==0.0.32
```

---

## Estructura del proyecto

La estructura principal del backend es:

```text
backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── config/
│   └── config_variable.py
│
├── controller/
│   ├── albums_controller.py
│   ├── branches_controller.py
│   ├── formats_controller.py
│   └── label_controller.py
│
├── core/
│   ├── config.py
│   └── database.py
│
├── models/
│   ├── albums_models.py
│   ├── branches_models.py
│   ├── formats_models.py
│   └── labels_models.py
│
├── routers/
│   ├── albums.py
│   ├── branches.py
│   ├── formats.py
│   └── labels.py
│
├── schemas/
│   ├── albums.py
│   ├── branches.py
│   ├── formats.py
│   └── labels.py
│
├── tests/
│   ├── conftest.py
│   ├── test_albums.py
│   ├── test_branches.py
│   └── test_formats.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── main.py
├── README.md
└── requirements.txt
```

### Responsabilidad de cada capa

```text
models/
    ↓
Define las tablas de la base de datos.

schemas/
    ↓
Define y valida los datos de entrada y salida de la API.

controller/
    ↓
Contiene la lógica de acceso y modificación de datos.

routers/
    ↓
Define los endpoints HTTP de la API.

tests/
    ↓
Comprueba que la API funciona correctamente.

main.py
    ↓
Crea la aplicación FastAPI y registra los routers.
```

---

# Requisitos previos

Antes de instalar el proyecto necesitas:

- Python instalado.
- Git.
- Una terminal.
- Un navegador para acceder a Swagger.
- VS Code u otro editor de código recomendado.

El proyecto utiliza un entorno virtual de Python.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/Palmeras-en-la-Mancha-Records/backend.git
cd backend
```

## 2. Crear el entorno virtual

### Windows

```bash
python -m venv .venv
```

Activarlo:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Configuración

El proyecto utiliza variables de entorno almacenadas en `.env`.

El archivo `.env` **no debe subirse al repositorio**.

Para crear la configuración local:

```bash
copy .env.example .env
```

En Linux/macOS:

```bash
cp .env.example .env
```

Después edita `.env` con los valores correspondientes.

---

# Variables de entorno

El archivo `.env.example` debe servir como plantilla para la configuración local.

Ejemplo:

```env
PROJECT_NAME="Palmeras en la Mancha API"
DATABASE_URL="sqlite:///./palmeras.db"

# Cloudinary
CLOUDINARY_CLOUD_NAME="your_cloud_name"
CLOUDINARY_API_KEY="your_api_key"
CLOUDINARY_API_SECRET="your_api_secret"
```

## Descripción

### PROJECT_NAME

Nombre de la API mostrado por FastAPI.

```env
PROJECT_NAME="Palmeras en la Mancha API"
```

### DATABASE_URL

URL utilizada por SQLAlchemy para conectarse a la base de datos.

Para SQLite:

```env
DATABASE_URL="sqlite:///./palmeras.db"
```

### Cloudinary

Estas variables están previstas para la integración de subida de imágenes:

```env
CLOUDINARY_CLOUD_NAME="your_cloud_name"
CLOUDINARY_API_KEY="your_api_key"
CLOUDINARY_API_SECRET="your_api_secret"
```


Nunca publiques:

```text
CLOUDINARY_API_SECRET
```

ni cualquier otra credencial real.

---

# Base de datos

Actualmente se utiliza **SQLite**.

La conexión se obtiene mediante:

```python
DATABASE_URL
```

SQLAlchemy crea las sesiones mediante `SessionLocal`.

La aplicación utiliza una `Base` declarativa para registrar los modelos.

Las tablas principales actuales son:

```text
albums
formats
branches
labels
```

---

# Arquitectura de datos

## Albums

Un álbum contiene actualmente:

```text
id
title
artist
release_year
genre
record_label
price
stock
format_id
cover_image_url
```

## Formats

Un formato contiene:

```text
id
name
description
```

Ejemplos:

```text
Vinilo LP
CD Digipak
Cassette
Vinilo 7 Single
```

## Branches

Una filial contiene:

```text
id
name
address
phone
```

## Labels

Una discográfica contiene:

```text
id
name
country
website
```

---

# Diagrama DER


## Arquitectura

La arquitectura final contempla una relación N:M entre álbumes y formatos mediante una tabla intermedia:

```text
                 ┌───────────────────┐
                 │       ALBUM       │
                 │ PK id             │
                 └─────────┬─────────┘
                           │
                           │ N
                           │
                 ┌─────────▼─────────┐
                 │   ALBUM_FORMAT    │
                 ├───────────────────┤
                 │ PK id             │
                 │ FK album_id       │
                 │ FK format_id      │
                 │ price             │
                 │ stock             │
                 └─────────┬─────────┘
                           │
                           │ N
                           │
                 ┌─────────▼─────────┐
                 │      FORMAT       │
                 │ PK id             │
                 │ name              │
                 │ description       │
                 └───────────────────┘
```

Esto permitirá, por ejemplo:

```text
Un mismo álbum
    ├── Vinilo → 24.99 € → 10 unidades
    ├── CD     → 14.99 € → 20 unidades
    └── Cassette → 12.99 € → 5 unidades

---

# Migraciones con Alembic

Alembic permite versionar los cambios de estructura de la base de datos.

El proyecto contiene:

```text
alembic/
alembic.ini
```

## Crear una migración

Después de modificar los modelos:

```bash
alembic revision --autogenerate -m "describe your change"
```

## Aplicar las migraciones

```bash
alembic upgrade head
```

## Volver una migración atrás

```bash
alembic downgrade -1
```

Antes de ejecutar migraciones en un entorno compartido, revisa siempre el contenido de la migración generada.

---

# Ejecución del proyecto

Con el entorno virtual activado:

```bash
uvicorn main:app --reload
```

La API estará disponible normalmente en:

```text
http://127.0.0.1:8000
```

---

# Documentación de la API

FastAPI genera automáticamente documentación interactiva.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger permite probar los endpoints directamente desde el navegador.

---

# Endpoints

## Albums

### GET `/albums/`

Devuelve todos los álbumes.

También admite filtros mediante query parameters.

### Query parameters

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---:|---|
| `search` | string | No | Busca por título o artista |
| `genre` | string | No | Filtra por género |

Ejemplo:

```http
GET /albums/
```

Ejemplo con búsqueda:

```http
GET /albums/?search=El%20Madrileño
```

Ejemplo con género:

```http
GET /albums/?genre=Rock
```

Ejemplo combinando ambos:

```http
GET /albums/?search=Tangana&genre=Pop
```

La búsqueda y el filtro utilizan coincidencias parciales.

---

### GET `/albums/{album_id}`

Obtiene un álbum por ID.

Ejemplo:

```http
GET /albums/1
```

Respuesta:

```json
{
  "id": 1,
  "title": "El Madrileño",
  "artist": "C. Tangana",
  "release_year": 2021,
  "genre": "Pop / Fusión Urbana",
  "record_label": "Sony Music Spain",
  "price": 24.99,
  "stock": 10,
  "format_id": 1,
  "cover_image_url": "https://example.com/cover.jpg"
}
```

---

### POST `/albums/`

Crea un nuevo álbum.

Ejemplo:

```http
POST /albums/
```

Body:

```json
{
  "title": "El Madrileño",
  "artist": "C. Tangana",
  "release_year": 2021,
  "genre": "Pop / Fusión Urbana",
  "record_label": "Sony Music Spain",
  "price": 24.99,
  "stock": 10,
  "format_id": 1,
  "cover_image_url": "https://example.com/cover.jpg"
}
```

Respuesta:

```text
201 Created
```

---

### PUT `/albums/{album_id}`

Actualiza un álbum existente.

Ejemplo:

```http
PUT /albums/1
```

Body:

```json
{
  "title": "El Madrileño Deluxe",
  "price": 29.99,
  "stock": 15
}
```

Los campos no enviados conservan su valor actual.

---

### DELETE `/albums/{album_id}`

Elimina un álbum.

Ejemplo:

```http
DELETE /albums/1
```

Respuesta:

```json
{
  "message": "Album successfully deleted"
}
```

---

# Formats

## GET `/formats/`

Devuelve todos los formatos.

```http
GET /formats/
```

---

## GET `/formats/{format_id}`

Obtiene un formato por ID.

```http
GET /formats/1
```

---

## POST `/formats/`

Crea un formato.

```json
{
  "name": "Vinilo LP",
  "description": "Edición estándar en vinilo de 12 pulgadas"
}
```

---

## PUT `/formats/{format_id}`

Actualiza un formato.

```json
{
  "name": "Vinilo LP 180g",
  "description": "Edición de vinilo de alta calidad"
}
```

---

## DELETE `/formats/{format_id}`

Elimina un formato.

```http
DELETE /formats/1
```

Respuesta:

```json
{
  "message": "Format deleted successfully"
}
```

---

# Branches

## GET `/branches/`

Devuelve todas las filiales.

```http
GET /branches/
```

---

## GET `/branches/{branch_id}`

Obtiene una filial.

```http
GET /branches/1
```

---

## POST `/branches/`

Crea una filial.

```json
{
  "name": "Palmeras Records Centro",
  "address": "Calle Mayor 12",
  "phone": "+34 900 000 000"
}
```

---

## PUT `/branches/{branch_id}`

Actualiza una filial.

```json
{
  "name": "Palmeras Records Centro",
  "phone": "+34 900 111 111"
}
```

---

## DELETE `/branches/{branch_id}`

Elimina una filial.

```http
DELETE /branches/1
```

Respuesta:

```json
{
  "message": "Branch successfully deleted"
}
```

---

# Labels

El proyecto contiene router, controller, schema y modelo para Labels.

Los endpoints definidos son:

```text
GET    /labels/
GET    /labels/{label_id}
POST   /labels/
PUT    /labels/{label_id}
DELETE /labels/{label_id}
```

### GET `/labels/`

```http
GET /labels/
```

### GET `/labels/{label_id}`

```http
GET /labels/1
```

### POST `/labels/`

```json
{
  "name": "Sony Music Spain",
  "country": "Spain",
  "website": "https://www.sonymusic.es"
}
```

### PUT `/labels/{label_id}`

```json
{
  "name": "Sony Music Entertainment Spain"
}
```

### DELETE `/labels/{label_id}`

```http
DELETE /labels/1
```

---


Los endpoints son:

```text
GET    /discs/
GET    /discs/{album_id}
POST   /discs/
PUT    /discs/{album_id}
DELETE /discs/{album_id}
```

Estos endpoints reutilizan la lógica actual de Albums.


# Ejemplos de query parameters

## Buscar álbumes

```http
GET /albums/?search=Poeta
```

Busca coincidencias en:

```text
title
artist
```

---

## Filtrar por género

```http
GET /albums/?genre=Indie
```

---

## Combinar filtros

```http
GET /albums/?search=Halley&genre=Rock
```

Ambos parámetros se aplican simultáneamente.

---

# Validaciones

Los schemas utilizan Pydantic para validar los datos.

## Albums

Ejemplos de restricciones:

```text
title
- obligatorio
- 1 a 150 caracteres
- elimina espacios exteriores

artist
- obligatorio
- 1 a 150 caracteres
- elimina espacios exteriores

release_year
- entre 1900 y 2100

price
- mayor o igual que 0

stock
- mayor o igual que 0
```

Por ejemplo, este valor no es válido:

```json
{
  "title": "   ",
  "artist": "Test Artist"
}
```

La API responde con:

```text
422 Unprocessable Entity
```

---

## Formats

El nombre del formato:

```text
- mínimo 2 caracteres
- máximo 100 caracteres
- elimina espacios exteriores
```

La descripción admite hasta:

```text
255 caracteres
```

---

## Branches

Se validan:

```text
name
address
phone
```

evitando valores vacíos y espacios exteriores.

---

# Manejo de errores

El backend utiliza `HTTPException` para devolver errores HTTP apropiados.

Ejemplos:

### 404 Not Found

Cuando no existe un álbum:

```json
{
  "detail": "Album not found"
}
```

### 400 Bad Request

Cuando una operación incumple una restricción funcional, por ejemplo un formato duplicado:

```json
{
  "detail": "A format with this name already exists"
}
```

### 422 Unprocessable Entity

Cuando los datos enviados no cumplen los schemas de Pydantic.

### 500 Internal Server Error

Cuando ocurre un error inesperado de acceso a la base de datos.

---

# Testing

El proyecto utiliza **Pytest** y una base de datos SQLite en memoria durante los tests.

Los tests principales son:

```text
tests/
├── test_albums.py
├── test_formats.py
└── test_branches.py
```

## Ejecutar todos los tests

```bash
pytest
```

## Ejecutar solo Albums

```bash
pytest tests/test_albums.py
```

## Ejecutar solo Formats

```bash
pytest tests/test_formats.py
```

## Ejecutar solo Branches

```bash
pytest tests/test_branches.py
```

La suite comprueba:

- CRUD.
- Persistencia.
- Respuestas HTTP.
- Errores 404.
- Validaciones 422.
- Duplicados en Formats.
- Búsqueda de Albums.
- Filtros de Albums.
- Actualizaciones parciales.
- Limpieza de los registros creados durante las pruebas.

---

# Cloudinary

La arquitectura prevista será:

```text
Usuario
   │
   │ selecciona imagen
   ▼
Frontend
   │
   │ FormData
   ▼
FastAPI
   │
   │ UploadFile
   ▼
Cloudinary
   │
   │ URL pública
   ▼
Album.cover_image_url
```

Las credenciales no deben escribirse directamente en el código fuente.

Deben mantenerse en `.env`:

```env
CLOUDINARY_CLOUD_NAME="your_cloud_name"
CLOUDINARY_API_KEY="your_api_key"
CLOUDINARY_API_SECRET="your_api_secret"
```

---

# Calidad y buenas prácticas

El proyecto aplica varias medidas de calidad:

## Validación

Los datos de entrada se validan antes de llegar a la lógica de persistencia mediante Pydantic.

## Separación de responsabilidades

El código está separado en:

```text
routers
    ↓
controller
    ↓
models
    ↓
database
```

Los schemas se encargan de la validación y serialización de los datos.

## Manejo de errores

Los errores de base de datos se controlan en los controllers y los routers se encargan de exponer las respuestas HTTP.

## Tests

Las operaciones principales cuentan con tests automatizados.

## Variables de entorno

Las credenciales y la configuración se mantienen fuera del código fuente.

## Migraciones

Los cambios de estructura de la base de datos se gestionan mediante Alembic.

---

# Flujo de desarrollo recomendado

Antes de empezar a trabajar:

```bash
git pull
```

Crear una rama para una funcionalidad:

```bash
git switch -c nombre-de-la-rama
```

Trabajar y probar:

```bash
pytest
```

Guardar cambios:

```bash
git add .
git commit -m "describe the change"
```

Subir la rama:

```bash
git push -u origin nombre-de-la-rama
```

Después se puede crear una Pull Request hacia:

```text
dev
```

---

# Autoría

Proyecto académico desarrollado por el equipo de **Palmeras en la Mancha Records**.
