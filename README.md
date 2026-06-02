# Monetto

Monetto es una aplicacion full-stack para gestion de finanzas personales. Permite registrar usuarios, iniciar sesion con JWT, administrar categorias, registrar ingresos y gastos, definir presupuestos mensuales, consultar un dashboard financiero y generar reportes mensuales en JSON o PDF.

El proyecto incluye:

- Backend async con FastAPI, SQLAlchemy, Alembic y MySQL.
- Frontend con Vue 3, TypeScript y Vite.
- Autenticacion Bearer JWT.
- Coleccion Postman, mapa de rutas y guia de contrato para frontend.
- Tests por controladores, servicios, repositorios, DTOs y mappers.

## Stack

| Capa | Tecnologias |
| --- | --- |
| Backend | Python 3.11+, FastAPI, SQLAlchemy asyncio, aiomysql, Pydantic v2 |
| Base de datos | MySQL 8, Alembic |
| Seguridad | JWT con `python-jose`, hashing con `passlib`/`bcrypt` |
| Reportes | ReportLab para PDF |
| Frontend | Vue 3, TypeScript, Vite |
| Calidad | Pytest, pytest-asyncio, Ruff, Mypy, Coverage, Pre-commit |

## Estructura

```text
monetto-api/
  app/
    api/              Controllers, router y dependencias de FastAPI
    config/           Settings, variables de entorno y seguridad
    db/               Motor async, sesiones y Base SQLAlchemy
    dto/              Contratos Pydantic de entrada/salida
    exceptions/       Errores de dominio y handlers HTTP
    mappers/          Conversion de modelos SQLAlchemy a DTOs
    models/           Modelos de base de datos
    repositories/     Consultas y acceso a datos
    services/         Reglas de negocio
    utils/            Fechas, dinero y categorias default
    main.py           Punto de entrada de FastAPI
  alembic/            Migraciones de base de datos
  docs/               Postman, mapa de rutas y notas de autenticacion
  monettoF/           Frontend Vue/Vite
  scripts/            Scripts de arranque para Windows
  tests/              Suite de pruebas
  start-dev.cmd       Levanta backend y frontend en dos ventanas
  guiaF.md            Contrato detallado para el frontend
  pyproject.toml      Dependencias y configuracion de herramientas Python
```

## Requisitos

- Python 3.11 o superior.
- MySQL 8.
- Node.js y npm para el frontend.
- Git Bash, PowerShell o una terminal compatible.

## Arranque Rapido En Windows

Desde la raiz `monetto-api/`, usa:

```powershell
.\start-dev.cmd
```

Ese comando abre dos ventanas: una para el backend y otra para el frontend. Tambien prepara lo necesario para evitar los errores comunes:

- Agrega `C:\Program Files\nodejs` al `PATH` si `npm` no aparece.
- Usa `.venv` para Python y crea el entorno si falta.
- Instala dependencias faltantes de backend/frontend.
- Ejecuta `alembic upgrade head` antes de levantar la API.

URLs locales:

- Frontend: `http://127.0.0.1:5173`
- Swagger: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

Para levantar servicios por separado:

```powershell
.\start-backend.cmd
.\start-frontend.cmd
```

Si solo quieres reparar `npm` en el `PATH`, ejecuta:

```powershell
.\repair-node-path.cmd
```

Despues de reparar el `PATH`, abre una terminal nueva para que Windows cargue el cambio.

## Configuracion

La API lee variables desde `.env` en la raiz del proyecto. Si no existe, usa valores locales por defecto.

Ejemplo recomendado:

```env
APP_NAME=Monetto API
ENVIRONMENT=local
DEBUG=false
API_PREFIX=/api
DB_URL=mysql+aiomysql://root:1234@localhost:3306/monetto
SECRET_KEY=change-me-for-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_ALGORITHM=HS256
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Para el frontend puedes crear `monettoF/.env` si quieres apuntar a otra URL:

```env
VITE_MONETTO_API_URL=http://127.0.0.1:8000/api
```

## Base De Datos

Crea la base local antes de levantar la API:

```sql
CREATE DATABASE monetto CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

Aplica las migraciones:

```powershell
alembic upgrade head
```

Las migraciones actuales crean usuarios, categorias, transacciones y presupuestos. Tambien se manejan categorias default para ingresos y gastos.

## Backend

Instala dependencias y levanta la API:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
```

La API queda disponible en:

- API base: `http://127.0.0.1:8000/api`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

Si necesitas otro puerto:

```powershell
uvicorn app.main:app --reload --port 8001
```

## Frontend

El frontend vive en `monettoF/`.

```powershell
cd monettoF
npm install
npm run dev
```

Por defecto Vite levanta la app en `http://localhost:5173` y consume `http://127.0.0.1:8000/api`.

Scripts disponibles:

```powershell
npm run dev
npm run build
npm run preview
```

## API

Todas las rutas cuelgan de `/api`. Las rutas protegidas requieren:

```http
Authorization: Bearer <access_token>
```

Resumen de endpoints principales:

| Metodo | Ruta | Auth | Descripcion |
| --- | --- | --- | --- |
| `GET` | `/api/health` | No | Verifica API y conexion a MySQL |
| `POST` | `/api/auth/register` | No | Registra un usuario |
| `POST` | `/api/auth/login` | No | Devuelve `access_token` |
| `GET` | `/api/categories` | Si | Lista categorias, opcional `type=INCOME|EXPENSE` |
| `POST` | `/api/categories` | Si | Crea categoria personalizada |
| `PUT` | `/api/categories/{category_id}` | Si | Edita categoria propia |
| `DELETE` | `/api/categories/{category_id}` | Si | Elimina categoria propia |
| `POST` | `/api/transactions` | Si | Crea ingreso o gasto |
| `GET` | `/api/transactions` | Si | Lista transacciones con filtros y paginacion |
| `GET` | `/api/transactions/{transaction_id}` | Si | Obtiene detalle |
| `PUT` | `/api/transactions/{transaction_id}` | Si | Actualiza transaccion |
| `DELETE` | `/api/transactions/{transaction_id}` | Si | Elimina transaccion |
| `POST` | `/api/budgets` | Si | Crea presupuesto mensual |
| `GET` | `/api/budgets` | Si | Lista presupuestos |
| `PUT` | `/api/budgets/{budget_id}` | Si | Actualiza presupuesto |
| `DELETE` | `/api/budgets/{budget_id}` | Si | Elimina presupuesto |
| `GET` | `/api/dashboard/summary` | Si | Resumen mensual |
| `GET` | `/api/dashboard/expenses-by-category` | Si | Gastos agrupados por categoria |
| `GET` | `/api/dashboard/monthly-trend` | Si | Tendencia mensual |
| `GET` | `/api/reports/monthly` | Si | Reporte mensual en `pdf` o `json` |

Ejemplos utiles:

```http
GET /api/categories?type=EXPENSE
GET /api/transactions?type=INCOME&page=1&limit=20
GET /api/dashboard/summary?month=2026-05
GET /api/reports/monthly?month=2026-05&format=json
GET /api/reports/monthly?month=2026-05&format=pdf
```

Notas de contrato:

- `register` devuelve el usuario creado; despues se debe llamar `login` para obtener token.
- Los tipos validos de transaccion son `INCOME` y `EXPENSE`.
- Las fechas de transaccion usan `YYYY-MM-DD` y no pueden ser futuras.
- Los meses de dashboard/reportes usan `YYYY-MM`.
- Los presupuestos reciben `month` como fecha, normalmente el primer dia del mes: `YYYY-MM-01`.
- Los montos se manejan como decimales; en clientes JS conviene enviarlos como string, por ejemplo `"125.00"`.
- Las transacciones se paginan desde `page=1`.
- Evita slash final en rutas como `/api/transactions/`; usa `/api/transactions`.

## Documentacion Del Proyecto

Archivos utiles:

| Archivo | Uso |
| --- | --- |
| `guiaF.md` | Contrato detallado para conectar el frontend con la API |
| `docs/routes-map.json` | Mapa JSON de rutas, params y notas |
| `docs/monetto-api.postman_collection.json` | Coleccion Postman para probar la API |
| `docs/auth-testing.md` | Guia para probar endpoints autenticados en Postman y Swagger |
| `monettoF/README.md` | README base generado por Vite |

## Pruebas Y Calidad

Los tests usan MySQL. Crea una base separada para no tocar la base local:

```sql
CREATE DATABASE monetto_test CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

Por defecto Pytest usa:

```text
mysql+aiomysql://root:1234@localhost:3306/monetto_test
```

Tambien puedes cambiarlo con `TEST_DB_URL`. Por seguridad, la suite rechaza bases que no terminen en `_test`.

Comandos:

```powershell
pytest
ruff check .
ruff format --check .
mypy
coverage run -m pytest
coverage report
pre-commit run --all-files
```

Para regenerar el lock de dependencias Python:

```powershell
pip-compile pyproject.toml --extra dev --output-file requirements.lock
```

Para validar el frontend:

```powershell
cd monettoF
npm run build
```

## Flujo De Desarrollo

1. Levantar MySQL y crear `monetto`.
2. Activar `.venv` e instalar dependencias Python.
3. Ejecutar `alembic upgrade head`.
4. Levantar backend con `uvicorn app.main:app --reload`.
5. Levantar frontend con `npm run dev` dentro de `monettoF/`.
6. Crear usuario en `/api/auth/register`.
7. Hacer login en `/api/auth/login` y usar el token en rutas protegidas.

## Solucion De Problemas

| Problema | Revision rapida |
| --- | --- |
| `401 Authentication token is required` | Falta header `Authorization: Bearer <token>` |
| `401 Could not validate credentials` | Token invalido, expirado o firmado con otra `SECRET_KEY` |
| `307 Temporary Redirect` | Revisa que la ruta no tenga slash final |
| Error de conexion MySQL | Confirma que MySQL este activo y que `DB_URL` apunte a una base creada |
| Tests saltados por DB | Crea `monetto_test` o define `TEST_DB_URL` |
| CORS en frontend | Agrega el origen a `BACKEND_CORS_ORIGINS` |
