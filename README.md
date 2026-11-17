# API - EFI Backend

API REST desarrollada como parte del Proyecto de Evaluación Final Integradora (EFI) de Backend.

El proyecto permite gestionar usuarios, categorías y productos de una panadería mediante operaciones CRUD. Incluye persistencia de datos, relaciones entre entidades, validaciones, autenticación mediante JWT y control de permisos según el rol del usuario.

## Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **FastAPI:** desarrollo de la API REST.
- **SQLModel:** definición de modelos y comunicación con la base de datos.
- **SQLite:** sistema de gestión de base de datos.
- **Alembic:** administración de migraciones.
- **bcrypt:** hash y verificación de contraseñas.
- **PyJWT:** generación y validación de tokens JWT.
- **python-dotenv:** lectura de variables de entorno.
- **fastapi-pagination:** paginación de resultados.
- **Uvicorn:** servidor ASGI.

## Funcionalidades

La API permite:

- Crear, consultar, actualizar y eliminar usuarios, categorías y productos.
- Consultar listados con paginación.
- Registrar la fecha y el usuario responsable de la última modificación de cada producto.
- Consultar productos junto con su categoría y el usuario que realizó su última modificación, según los permisos del usuario.
- Validar los datos recibidos antes de almacenarlos.
- Almacenar contraseñas mediante hash con bcrypt.
- Autenticar usuarios mediante tokens JWT.
- Diferenciar permisos entre empleados y propietarios.
- Permitir que los usuarios actualicen sus propias credenciales.

## Estructura del proyecto

```text
EFI-Backend/
│
├── alembic/
│   └── versions/
│
├── src/
│   ├── core/
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── category.py
│   │   └── product.py
│   │
│   ├── routers/
│   │   ├── users.py
│   │   ├── categories.py
│   │   ├── products.py
│   │   └── auth.py
│   │
│   ├── database.py
│   └── main.py
│
├── .env
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

## Configuración de variables de entorno

La API necesita una clave secreta para firmar y validar los tokens JWT.

Crear un archivo `.env` en la raíz del proyecto con la siguiente variable:

```env
SECRET_KEY=clave_secreta_generada
```

Para generar una clave segura se puede ejecutar:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

El archivo `.env` está incluido en `.gitignore` y no debe subirse al repositorio.

En entornos de producción, la variable `SECRET_KEY` debe configurarse mediante el sistema de variables de entorno o secretos de la plataforma de despliegue.

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

| Recurso | Ruta | Operaciones |
|---|---|---|
| Autenticación | `/auth/login` | POST |
| Usuarios | `/users/` | GET, POST |
| Usuarios por ID | `/users/{id}` | GET, PUT, DELETE |
| Datos propios del usuario | `/users/me` | PUT |
| Categorías | `/categories/` | GET, POST |
| Categorías por ID | `/categories/{id}` | GET, PUT, DELETE |
| Productos | `/products/` | GET, POST |
| Productos por ID | `/products/{id}` | GET, PUT, DELETE |

Los listados admiten paginación y las operaciones individuales contemplan respuestas de error cuando el recurso solicitado no existe.

## Autenticación y permisos

La API utiliza autenticación mediante tokens JWT. Para obtener un token, el usuario debe iniciar sesión mediante `/auth/login`, enviando sus credenciales.

Los tokens tienen una duración de 30 minutos y deben enviarse en las solicitudes protegidas mediante el encabezado:

```text
Authorization: Bearer <token>
```

El sistema contempla dos roles:

- **Empleado:** puede gestionar productos y categorías.
- **Propietario:** puede gestionar productos, categorías y usuarios, además de administrar los roles de las cuentas.

Las consultas públicas de productos y categorías no requieren autenticación. Sin embargo, los metadatos administrativos de los productos, como la fecha y el usuario responsable de su última modificación, solamente se muestran a usuarios autenticados.

Los usuarios pueden modificar sus propias credenciales mediante `/users/me`, verificando previamente su contraseña actual. La administración de otras cuentas está reservada a los propietarios.

### Inicialización del primer propietario

Cuando la base de datos todavía no contiene usuarios, el primer registro realizado mediante `POST /users/` se crea automáticamente con el rol de propietario.

Una vez creado ese usuario, los registros posteriores requieren autenticación y permisos de propietario.

El sistema también impide degradar o eliminar al último propietario para garantizar que siempre exista una cuenta con permisos administrativos.

## Relaciones entre entidades

- Cada categoría puede contener varios productos.
- Cada producto pertenece a una categoría.
- Cada producto registra el usuario responsable de su última modificación.
- Los usuarios pueden estar relacionados con varios productos que hayan modificado.

## Validaciones y seguridad

- Los nombres de usuarios, categorías y productos no pueden estar vacíos.
- Los precios de los productos deben ser positivos.
- Las contraseñas se almacenan mediante hash con bcrypt y se limita su longitud a 72 bytes.
- Los hashes de las contraseñas no se exponen en las respuestas de la API.
- Los tokens JWT se verifican antes de permitir el acceso a las operaciones protegidas.
- Se controla el acceso a las operaciones administrativas según el rol del usuario.

## Autores

Desarrollado por:

- Gabriel Acuña
- Leonel Rojo
- Ivo Roldan

**Proyecto de Evaluación Final Integradora — Backend, 2026.**