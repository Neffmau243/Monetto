# Probar endpoints autenticados

Los endpoints protegidos necesitan este header:

```http
Authorization: Bearer <access_token>
```

## En Postman

1. Ejecuta `02 Register main user`.
2. Ejecuta `04 Login main user`.
3. El test de ese request guarda automaticamente `access_token` en la variable de coleccion `token`.
4. Ejecuta requests protegidos como `08 List categories`, `08.1 List income categories` o `08.2 List expense categories`.

No uses `07 Categories without token should fail` para probar categorias normalmente. Ese request esta hecho a proposito sin token y debe devolver:

```json
{
  "detail": "Authentication token is required"
}
```

Si haces un request manual, configura:

```text
Auth > Type: Bearer Token
Token: {{token}}
```

O agrega el header manual:

```http
Authorization: Bearer {{token}}
```

## En Swagger

Hacer login en `POST /api/auth/login` no autentica automaticamente Swagger UI.

1. Copia el `access_token` de la respuesta del login.
2. Haz click en `Authorize`, arriba a la derecha.
3. Pega el token.
4. Confirma con `Authorize`.
5. Ejecuta `GET /api/categories`.
