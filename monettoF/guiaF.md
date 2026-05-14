# Guia frontend - Contrato Monetto API

Esta guia resume lo que el frontend en Vue necesita saber para consumir el backend sin adivinar nombres, formatos ni flujos.

## Base tecnica

- API local: `http://127.0.0.1:8000`
- Prefijo real de rutas: `/api`
- Documentacion interactiva: `http://127.0.0.1:8000/docs`
- Coleccion Postman: `docs/monetto-api.postman_collection.json`
- Mapa JSON de rutas: `docs/routes-map.json`
- Formato general: JSON, salvo descarga PDF.
- Autenticacion: `Authorization: Bearer <access_token>`
- No usar slash final en las rutas. Ejemplo correcto: `/api/transactions`; evitar `/api/transactions/` porque FastAPI responde `307`.

## Mapa del proyecto backend

Este mapa ayuda a ubicar de donde sale cada contrato si el frontend necesita revisar algo.

| Carpeta/archivo | Rol |
| --- | --- |
| `app/main.py` | Crea FastAPI, CORS, lifespan y monta todas las rutas bajo `/api`. |
| `app/api/router.py` | Agrega todos los controllers. |
| `app/api/controllers/` | Metodos HTTP: auth, categorias, transacciones, presupuestos, dashboard, reportes, health. |
| `app/api/dependencies.py` | Lee el Bearer token y obtiene el usuario actual. |
| `app/dto/` | Contratos Pydantic de entrada/salida que consume el frontend. |
| `app/models/` | Tablas SQLAlchemy: users, categories, transactions, budgets. |
| `app/repositories/` | Queries a MySQL, filtros, ordenamientos y paginacion. |
| `app/services/` | Logica de negocio y reglas: auth, validacion de categoria, presupuestos unicos, dashboard, PDF. |
| `app/mappers/` | Conversion de modelos DB a DTOs de respuesta. |
| `app/config/` | Settings `.env` y seguridad JWT/bcrypt. |
| `app/db/` | Motor async SQLAlchemy, sesiones y Base. |
| `app/exceptions/` | Errores de dominio y formato `{"detail": "..."}`. |
| `app/utils/` | Fechas, dinero y categorias default. |
| `alembic/versions/` | Migraciones MySQL. |
| `docs/` | Postman, mapa JSON de rutas y guia de auth. |
| `tests/` | Tests por capas y endpoints. |

## Convenciones importantes

- Los `id` son llaves internas de base de datos. No representan orden visual.
- Para categorias, mostrar el orden del array devuelto o usar `display_order`.
- Las paginas empiezan en `page=1`, no en `page=0`.
- Los montos deben enviarse como string decimal para evitar errores de flotantes: `"125.00"`.
- Fechas de transacciones: `YYYY-MM-DD`.
- Meses para dashboard/reportes: `YYYY-MM`.
- Meses para presupuestos: enviar `YYYY-MM-01`.
- Tipos validos: `INCOME` y `EXPENSE`.
- Una transaccion `INCOME` solo puede usar categoria `INCOME`.
- Una transaccion `EXPENSE` solo puede usar categoria `EXPENSE`.
- Las fechas de transacciones no pueden ser futuras.
- Register no devuelve token. Despues de registrar, el front debe llamar login.
- Login devuelve token. Para mostrar nombre del usuario, el front debe llamar `GET /api/auth/me` con ese token.
- Si no hay presupuesto fijo para el mes, pero si hay ingresos, `budget_info` se calcula de forma dinamica con los ingresos del mes como limite disponible.

## Estados HTTP y errores

El backend responde errores de dominio con:

```json
{
  "detail": "Mensaje del error"
}
```

Errores comunes:

| Codigo | Cuando pasa | Ejemplo `detail` |
| --- | --- | --- |
| `401` | Falta token o token invalido | `Authentication token is required` |
| `401` | Login incorrecto | `Invalid email or password` |
| `403` | Intentar tocar recurso de otro usuario | `You can only access your own transactions` |
| `404` | Recurso no existe o categoria no valida | `Transaction not found` |
| `409` | Duplicados o conflicto de negocio | `Email already registered` |
| `422` | Validacion de body/query | `Date cannot be in the future` |

En Vue conviene manejar:

- `401`: limpiar token y mandar a login.
- `403`: mostrar mensaje de permiso.
- `404`: mostrar "no encontrado" o volver al listado.
- `409`: mostrar conflicto especifico.
- `422`: pintar errores de formulario.

## Vistas requeridas para el MVP

El MVP frontend puede arrancar bien con 7 vistas base.

| Vista | Por que existe | Rutas principales |
| --- | --- | --- |
| Login / Registro | Entrada al sistema, obtencion del JWT y perfil actual. Puede ser una sola pantalla con tabs. | `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me` |
| Dashboard | Resumen financiero inicial con tarjetas y graficos. | `GET /api/dashboard/summary`, `GET /api/dashboard/expenses-by-category`, `GET /api/dashboard/monthly-trend` |
| Ingresos | Separada de gastos para no mezclar listas largas y porque usa categorias `INCOME`. | `GET /api/categories?type=INCOME`, `GET /api/transactions?type=INCOME`, `POST /api/transactions` |
| Gastos | Separada de ingresos para enfocar flujo de egresos y presupuesto. | `GET /api/categories?type=EXPENSE`, `GET /api/transactions?type=EXPENSE`, `POST /api/transactions` |
| Presupuesto mensual | Crear y editar el limite mensual que usa el dashboard. | `GET /api/budgets`, `POST /api/budgets`, `PUT /api/budgets/{id}`, `DELETE /api/budgets/{id}` |
| Categorias | Gestion de categorias personalizadas. Tambien puede ser modal dentro de Ingresos/Gastos. | `GET /api/categories`, `POST /api/categories`, `PUT /api/categories/{id}`, `DELETE /api/categories/{id}` |
| Reportes | Previsualizar JSON y descargar PDF mensual. | `GET /api/reports/monthly?format=json`, `GET /api/reports/monthly?format=pdf` |

Recomendacion de UX:

- En la pagina Ingresos, cargar solo `INCOME`.
- En la pagina Gastos, cargar solo `EXPENSE`.
- El formulario de nueva transaccion debe mostrar solo categorias compatibles con el tipo de la pagina.
- Las categorias default (`is_default=true`) no se editan ni eliminan. Solo las del usuario (`user_id` igual al usuario logueado) pueden editarse.

## Flujo recomendado de la app

1. Al abrir la app, revisar si hay token guardado.
2. Si no hay token, mostrar Login / Registro.
3. Si hay token, configurar header `Authorization`.
4. Cargar dashboard.
5. Para vistas de ingresos/gastos, cargar categorias filtradas por tipo antes del formulario.
6. Si cualquier request protegida responde `401`, limpiar sesion y volver a Login.

## Contrato de autenticacion

### Registrar usuario

`POST /api/auth/register`

Auth: no requiere token.

Body:

```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "password": "Strong123"
}
```

Validaciones:

- `name`: 2 a 120 caracteres.
- `email`: email valido.
- `password`: 8 a 128 caracteres, minimo 1 numero y 1 mayuscula.

Response `201`:

```json
{
  "id": 1,
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "created_at": "2026-05-11T23:43:31"
}
```

### Login

`POST /api/auth/login`

Auth: no requiere token.

Body:

```json
{
  "email": "ada@example.com",
  "password": "Strong123"
}
```

Response `200`:

```json
{
  "access_token": "jwt_aqui",
  "token_type": "bearer"
}
```

El frontend debe guardar `access_token` y enviarlo asi:

```text
Authorization: Bearer jwt_aqui
```

### Usuario actual

`GET /api/auth/me`

Auth: requiere token.

Uso frontend: llamar despues del login y al recargar la app con token guardado. Usar `name` para el perfil; el email puede quedar como dato secundario.

Response `200`:

```json
{
  "id": 1,
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "created_at": "2026-05-11T23:43:31"
}
```

## Health

### Verificar API y DB

`GET /api/health`

Auth: no requiere token.

Response `200`:

```json
{
  "status": "ok",
  "database": "ok"
}
```

Sirve para pantalla tecnica o para revisar si el backend esta levantado.

## Categorias

### Listar categorias

`GET /api/categories`

Auth: requiere token.

Query opcional:

| Param | Tipo | Uso |
| --- | --- | --- |
| `type` | `INCOME` o `EXPENSE` | Filtra categorias por pagina |

Ejemplos:

```text
GET /api/categories
GET /api/categories?type=INCOME
GET /api/categories?type=EXPENSE
```

Response `200`:

```json
[
  {
    "id": 1,
    "name": "Salario",
    "type": "INCOME",
    "user_id": null,
    "is_default": true,
    "sort_order": 10,
    "display_order": 1
  }
]
```

Notas para frontend:

- Usar `id` solo para enviar `category_id`.
- Para mostrar, usar `display_order` o el orden del array.
- En Ingresos usar `GET /api/categories?type=INCOME`.
- En Gastos usar `GET /api/categories?type=EXPENSE`.
- Las default globales llegan con `user_id: null`.
- Las personalizadas llegan con `user_id` numerico.

Categorias default actuales:

| Tipo | Categorias |
| --- | --- |
| `INCOME` | Salario, Freelance, Trabajos diarios, Ventas, Bonos, Inversiones, Regalos, Reembolsos, Otros ingresos |
| `EXPENSE` | Alimentacion, Transporte, Vivienda, Luz, Agua, Internet, Servicios, Salud, Educacion, Suscripciones, Entretenimiento, Juegos, Salidas, Compras, Emergencias, Otros gastos |

### Crear categoria

`POST /api/categories`

Auth: requiere token.

Body:

```json
{
  "name": "Comisiones",
  "type": "INCOME"
}
```

Response `201`: `CategoryOut`.

Reglas:

- `name`: 2 a 120 caracteres.
- `type`: obligatorio.
- El nombre no puede repetirse para el mismo usuario y tipo.

### Editar categoria

`PUT /api/categories/{category_id}`

Auth: requiere token.

Body parcial permitido:

```json
{
  "name": "Comisiones digitales"
}
```

Tambien acepta cambio de tipo:

```json
{
  "name": "Ventas online",
  "type": "INCOME"
}
```

Response `200`: `CategoryOut`.

Reglas:

- Solo se editan categorias propias.
- Categorias default no son editables porque no tienen `user_id` del usuario.

### Eliminar categoria

`DELETE /api/categories/{category_id}`

Auth: requiere token.

Response `200`:

```json
{
  "message": "Categoria eliminada correctamente"
}
```

Reglas:

- Solo se eliminan categorias propias.
- Si tiene transacciones asociadas responde `409`.

## Transacciones

### Crear transaccion

`POST /api/transactions`

Auth: requiere token.

Body para ingreso:

```json
{
  "type": "INCOME",
  "amount": "5.00",
  "description": "Pago diario",
  "date": "2026-05-11",
  "category_id": 3
}
```

Body para gasto:

```json
{
  "type": "EXPENSE",
  "amount": "125.00",
  "description": "Mercado",
  "date": "2026-05-11",
  "category_id": 10
}
```

Response `201`:

```json
{
  "id": 15,
  "type": "EXPENSE",
  "amount": "125.00",
  "description": "Mercado",
  "date": "2026-05-11",
  "category_id": 10,
  "user_id": 1,
  "created_at": "2026-05-11T23:44:00",
  "category": {
    "id": 10,
    "name": "Alimentacion",
    "type": "EXPENSE",
    "user_id": null,
    "is_default": true,
    "sort_order": 100,
    "display_order": 0
  }
}
```

Validaciones:

- `amount`: mayor a 0, maximo 12 digitos y 2 decimales.
- `description`: opcional, maximo 255 caracteres.
- `date`: no futura.
- `category_id`: debe existir, ser visible para el usuario y coincidir con `type`.

### Listar transacciones

`GET /api/transactions`

Auth: requiere token.

Query params:

| Param | Tipo | Default | Nota |
| --- | --- | --- | --- |
| `type` | `INCOME` o `EXPENSE` | ninguno | Usarlo para separar paginas |
| `category_id` | number | ninguno | Filtra por categoria |
| `date_from` | `YYYY-MM-DD` | ninguno | Incluyente |
| `date_to` | `YYYY-MM-DD` | ninguno | Incluyente |
| `page` | number | `1` | Minimo 1 |
| `limit` | number | `20` | Entre 1 y 100 |

Ejemplos:

```text
GET /api/transactions?type=INCOME&page=1&limit=10
GET /api/transactions?type=EXPENSE&date_from=2026-05-01&date_to=2026-05-31&page=1&limit=10
GET /api/transactions?category_id=10&page=1&limit=20
```

Response `200`:

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "limit": 20,
  "total_pages": 1,
  "has_next": false,
  "has_previous": false
}
```

Orden:

- Primero fecha descendente.
- Si hay misma fecha, `id` descendente.

### Ver detalle

`GET /api/transactions/{transaction_id}`

Auth: requiere token.

Response `200`: `TransactionOut`.

### Editar transaccion

`PUT /api/transactions/{transaction_id}`

Auth: requiere token.

Body parcial permitido:

```json
{
  "amount": "150.00",
  "description": "Mercado actualizado"
}
```

Si se cambia `type` o `category_id`, ambos deben seguir siendo compatibles.

Response `200`: `TransactionOut`.

### Eliminar transaccion

`DELETE /api/transactions/{transaction_id}`

Auth: requiere token.

Response `200`:

```json
{
  "message": "Transaccion eliminada correctamente"
}
```

## Presupuestos

### Crear presupuesto

`POST /api/budgets`

Auth: requiere token.

Body:

```json
{
  "month": "2026-05-01",
  "amount": "1000.00"
}
```

Response `201`:

```json
{
  "id": 1,
  "user_id": 1,
  "month": "2026-05-01",
  "amount": "1000.00",
  "created_at": "2026-05-11T23:44:23",
  "updated_at": "2026-05-11T23:44:23"
}
```

Reglas:

- Un usuario solo puede tener un presupuesto por mes.
- `amount` debe ser mayor a 0.
- Enviar `month` como primer dia del mes.

### Listar presupuestos

`GET /api/budgets`

Auth: requiere token.

Response `200`:

```json
[
  {
    "id": 1,
    "user_id": 1,
    "month": "2026-05-01",
    "amount": "1000.00",
    "created_at": "2026-05-11T23:44:23",
    "updated_at": "2026-05-11T23:44:23"
  }
]
```

Orden:

- Mes descendente.

### Editar presupuesto

`PUT /api/budgets/{budget_id}`

Auth: requiere token.

Body parcial permitido:

```json
{
  "amount": "1500.00"
}
```

Tambien puede cambiar mes:

```json
{
  "month": "2026-06-01",
  "amount": "1200.00"
}
```

Response `200`: `BudgetOut`.

### Eliminar presupuesto

`DELETE /api/budgets/{budget_id}`

Auth: requiere token.

Response `200`:

```json
{
  "message": "Presupuesto eliminado correctamente"
}
```

## Dashboard

### Resumen mensual

`GET /api/dashboard/summary`

Auth: requiere token.

Query:

| Param | Tipo | Default |
| --- | --- | --- |
| `month` | `YYYY-MM` | mes actual |

Ejemplo:

```text
GET /api/dashboard/summary?month=2026-05
```

Response `200`:

```json
{
  "month": "2026-05",
  "total_income": "1500.00",
  "total_expenses": "400.00",
  "balance": "1100.00",
  "budget_info": {
    "amount": "1000.00",
    "spent": "400.00",
    "percentage": "40.00",
    "remaining": "600.00",
    "source": "FIXED",
    "is_dynamic": false
  }
}
```

Si no hay presupuesto fijo para el mes, pero si hay ingresos, el backend devuelve un limite dinamico basado en `total_income`:

```json
{
  "month": "2026-05",
  "total_income": "1500.00",
  "total_expenses": "400.00",
  "balance": "1100.00",
  "budget_info": {
    "amount": "1500.00",
    "spent": "400.00",
    "percentage": "26.67",
    "remaining": "1100.00",
    "source": "DYNAMIC_INCOME",
    "is_dynamic": true
  }
}
```

Si no hay presupuesto fijo ni ingresos en el mes:

```json
{
  "month": "2026-05",
  "total_income": "0.00",
  "total_expenses": "0.00",
  "balance": "0.00",
  "budget_info": null
}
```

### Gastos por categoria

`GET /api/dashboard/expenses-by-category`

Auth: requiere token.

Query:

| Param | Tipo | Default |
| --- | --- | --- |
| `month` | `YYYY-MM` | mes actual |

Response `200`:

```json
[
  {
    "category_id": 10,
    "category_name": "Alimentacion",
    "total": "250.00",
    "percentage": "62.50"
  }
]
```

Uso frontend:

- Grafico de dona/barras de gastos.
- Mostrar porcentaje como `percentage + "%"`.

### Tendencia mensual

`GET /api/dashboard/monthly-trend`

Auth: requiere token.

Query:

| Param | Tipo | Default | Rango |
| --- | --- | --- | --- |
| `months` | number | `6` | 1 a 24 |

Response `200`:

```json
[
  {
    "month": "2026-03",
    "income": "0.00",
    "expenses": "0.00",
    "balance": "0.00"
  },
  {
    "month": "2026-04",
    "income": "500.00",
    "expenses": "200.00",
    "balance": "300.00"
  }
]
```

Uso frontend:

- Grafico de lineas o barras.
- El backend completa meses sin movimientos con cero.

## Reportes

### Reporte mensual JSON

`GET /api/reports/monthly?month=2026-05&format=json`

Auth: requiere token.

Response `200`:

```json
{
  "user": {
    "id": 1,
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "created_at": "2026-05-11T23:43:31"
  },
  "month": "2026-05",
  "summary": {
    "month": "2026-05",
    "total_income": "1500.00",
    "total_expenses": "400.00",
    "balance": "1100.00",
    "budget_info": null
  },
  "transactions": [],
  "expenses_by_category": []
}
```

Uso frontend:

- Previsualizacion del reporte antes de descargar.
- Tabla mensual de transacciones.

### Reporte mensual PDF

`GET /api/reports/monthly?month=2026-05&format=pdf`

Auth: requiere token.

Response `200`:

- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="monetto-2026-05.pdf"`

En Vue/Axios usar `responseType: "blob"` para descargar.

## Mapa completo de rutas

| Metodo | Ruta | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/api/health` | No | No | estado API/DB |
| `POST` | `/api/auth/register` | No | `UserCreate` | `UserOut` |
| `POST` | `/api/auth/login` | No | `UserLogin` | `Token` |
| `GET` | `/api/auth/me` | Si | No | `UserOut` |
| `GET` | `/api/categories` | Si | No | `CategoryOut[]` |
| `POST` | `/api/categories` | Si | `CategoryCreate` | `CategoryOut` |
| `PUT` | `/api/categories/{category_id}` | Si | `CategoryUpdate` | `CategoryOut` |
| `DELETE` | `/api/categories/{category_id}` | Si | No | `MessageOut` |
| `POST` | `/api/transactions` | Si | `TransactionCreate` | `TransactionOut` |
| `GET` | `/api/transactions` | Si | No | `PaginatedTransactionsOut` |
| `GET` | `/api/transactions/{transaction_id}` | Si | No | `TransactionOut` |
| `PUT` | `/api/transactions/{transaction_id}` | Si | `TransactionUpdate` | `TransactionOut` |
| `DELETE` | `/api/transactions/{transaction_id}` | Si | No | `MessageOut` |
| `POST` | `/api/budgets` | Si | `BudgetCreate` | `BudgetOut` |
| `GET` | `/api/budgets` | Si | No | `BudgetOut[]` |
| `PUT` | `/api/budgets/{budget_id}` | Si | `BudgetUpdate` | `BudgetOut` |
| `DELETE` | `/api/budgets/{budget_id}` | Si | No | `MessageOut` |
| `GET` | `/api/dashboard/summary` | Si | No | `DashboardSummaryOut` |
| `GET` | `/api/dashboard/expenses-by-category` | Si | No | `ExpensesByCategoryOut[]` |
| `GET` | `/api/dashboard/monthly-trend` | Si | No | `MonthlyTrendOut[]` |
| `GET` | `/api/reports/monthly` | Si | No | JSON o PDF |

## DTOs resumidos

### UserCreate

```ts
type UserCreate = {
  name: string
  email: string
  password: string
}
```

### UserLogin

```ts
type UserLogin = {
  email: string
  password: string
}
```

### UserOut

```ts
type UserOut = {
  id: number
  name: string
  email: string
  created_at: string
}
```

### Token

```ts
type Token = {
  access_token: string
  token_type: "bearer"
}
```

### CategoryOut

```ts
type CategoryOut = {
  id: number
  name: string
  type: "INCOME" | "EXPENSE"
  user_id: number | null
  is_default: boolean
  sort_order: number
  display_order: number
}
```

### TransactionCreate

```ts
type TransactionCreate = {
  type: "INCOME" | "EXPENSE"
  amount: string
  description?: string | null
  date: string
  category_id: number
}
```

### TransactionOut

```ts
type TransactionOut = {
  id: number
  type: "INCOME" | "EXPENSE"
  amount: string
  description: string | null
  date: string
  category_id: number
  user_id: number
  created_at: string
  category: CategoryOut | null
}
```

### PaginatedTransactionsOut

```ts
type PaginatedTransactionsOut = {
  items: TransactionOut[]
  total: number
  page: number
  limit: number
  total_pages: number
  has_next: boolean
  has_previous: boolean
}
```

### BudgetOut

```ts
type BudgetOut = {
  id: number
  user_id: number
  month: string
  amount: string
  created_at: string
  updated_at: string
}
```

### DashboardSummaryOut

```ts
type DashboardSummaryOut = {
  month: string
  total_income: string
  total_expenses: string
  balance: string
  budget_info: null | {
    amount: string
    spent: string
    percentage: string
    remaining: string
    source: 'FIXED' | 'DYNAMIC_INCOME'
    is_dynamic: boolean
  }
}
```

### ExpensesByCategoryOut

```ts
type ExpensesByCategoryOut = {
  category_id: number
  category_name: string
  total: string
  percentage: string
}
```

### MonthlyTrendOut

```ts
type MonthlyTrendOut = {
  month: string
  income: string
  expenses: string
  balance: string
}
```

## Servicios frontend sugeridos

Para Vue, separar el consumo asi ayuda bastante:

| Servicio/store | Responsabilidad |
| --- | --- |
| `authService` / `authStore` | login, register, guardar token, logout |
| `categoryService` | listar por tipo, crear, editar, eliminar |
| `transactionService` | CRUD, filtros, paginacion |
| `budgetService` | CRUD presupuesto mensual |
| `dashboardService` | summary, expenses-by-category, monthly-trend |
| `reportService` | preview JSON y descarga Blob PDF |

## Checklist para evitar problemas

- Enviar siempre token en rutas protegidas.
- Separar llamadas de categorias por pagina: `type=INCOME` para Ingresos, `type=EXPENSE` para Gastos.
- No ordenar categorias por `id`.
- No enviar fechas futuras en transacciones.
- No usar `page=0`.
- No usar slash final.
- Convertir montos a string con dos decimales antes de enviar.
- Para PDF, usar `blob`.
- Si el backend devuelve `409` al eliminar categoria, significa que tiene transacciones; pedir al usuario borrar/mover esas transacciones primero.
