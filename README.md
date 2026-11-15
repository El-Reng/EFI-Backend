# API - EFI Backend

API REST desarrollada como parte del Proyecto de Evaluación Final Integradora (EFI) de Backend.

El proyecto permite gestionar usuarios, categorías y productos de una panadería mediante operaciones CRUD. Incluye persistencia de datos, relaciones entre entidades, validaciones y documentación automática de los endpoints.

## Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **FastAPI:** desarrollo de la API REST.
- **SQLModel:** definición de modelos y comunicación con la base de datos.
- **SQLite:** sistema de gestión de base de datos.
- **Alembic:** administración de migraciones.
- **bcrypt:** hash de contraseñas.
- **fastapi-pagination:** paginación de resultados.
- **Uvicorn:** servidor ASGI.

## Funcionalidades

La API permite:

- Crear, consultar, actualizar y eliminar usuarios, categorías y productos.
- Consultar listados con paginación.
- Registrar la fecha y el usuario responsable de la última modificación de cada producto.
- Consultar productos junto con su categoría y el usuario que realizó su última modificación.
- Validar los datos recibidos y almacenar contraseñas mediante hash con bcrypt.

## Estructura del proyecto

```text
EFI-Backend/
│
├── alembic/
│   └── versions/
│
├── src/
│   ├── models/
│   │   ├── user.py
│   │   ├── category.py
│   │   └── product.py
│   │
│   ├── routers/
│   │   ├── users.py
│   │   ├── categories.py
│   │   └── products.py
│   │
│   ├── database.py
│   └── main.py
│
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## Requisitos previos

- Python 3.11 o superior.
- [uv](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias.
- Git para clonar el repositorio.

## Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/El-Reng/EFI-Backend
cd EFI-Backend
```

**2. Crear el entorno virtual**

```bash
uv venv
```

**3. Activar el entorno virtual**

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Linux:

```bash
source .venv/bin/activate
```

**4. Instalar las dependencias**

```bash
uv pip install -r requirements.txt
```

## Base de datos y migraciones

El proyecto utiliza SQLite mediante el archivo local `db_local.db`, configurado en `src/database.py`.

Para crear o actualizar la estructura de la base de datos, ejecutar:

```bash
uv run alembic upgrade head
```

Las migraciones se administran mediante Alembic, que mantiene un historial de los cambios realizados en la base de datos.

## Ejecución

Iniciar el servidor con:

```bash
uv run uvicorn src.main:app --reload
```

La API estará disponible en:

`http://127.0.0.1:8000`

## Documentación de la API

FastAPI genera automáticamente documentación interactiva:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Desde Swagger UI se pueden consultar y probar los endpoints directamente.

## Endpoints principales


| Recurso            | Ruta               | Operaciones      |
| -------------------- | -------------------- | ------------------ |
| Usuarios           | `/users/`          | GET, POST        |
| Usuarios por ID    | `/users/{id}`      | GET, PUT, DELETE |
| Categorías        | `/categories/`     | GET, POST        |
| Categorías por ID | `/categories/{id}` | GET, PUT, DELETE |
| Productos          | `/products/`       | GET, POST        |
| Productos por ID   | `/products/{id}`   | GET, PUT, DELETE |

Los listados admiten paginación y las operaciones individuales contemplan respuestas de error cuando el recurso solicitado no existe.

## Relaciones y seguridad

- Cada categoría puede contener varios productos.
- Cada producto pertenece a una categoría y registra el usuario responsable de su última modificación.
- Las contraseñas se almacenan mediante hash con bcrypt, sin exponerlas ni devolver sus hashes en las respuestas públicas.
- Se aplican validaciones sobre los datos recibidos, incluyendo nombres no vacíos, precios positivos y límites de longitud para las contraseñas.

**Nota:** el proyecto no implementa actualmente un sistema de autenticación ni autorización.

## Autores

Desarrollado por:

- Gabriel Acuña
- Leonel Rojo
- Ivo Roldan

**Proyecto de Evaluación Final Integradora — Backend, 2026.**
