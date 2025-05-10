# MUMO API Documentation

## Authentication

The API uses Django's built-in authentication system based on **username and password**. To access protected endpoints, you must log in and maintain an active session using cookies or basic authentication.

No token is required for authentication.

### Authentication Endpoints

#### Register a new user
```
POST /api/users/
```
Request body:
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string (optional)",
    "last_name": "string (optional)"
}

## API Endpoints

### Users
```
GET /api/users/ - List all users
POST /api/users/ - Create a new user
GET /api/users/{id}/ - Get user details
PUT /api/users/{id}/ - Update user
DELETE /api/users/{id}/ - Delete user
```

### Insumos (Ingredients)
```
GET /api/insumos/ - List all ingredients
POST /api/insumos/ - Create new ingredient
GET /api/insumos/{id}/ - Get ingredient details
PUT /api/insumos/{id}/ - Update ingredient
DELETE /api/insumos/{id}/ - Delete ingredient

# Special endpoints
GET /api/insumos/stock_bajo/ - Get ingredients with low stock (< 10 units)
GET /api/insumos/valor_total/ - Get total inventory value
```

Request body for creating/updating ingredients:
```json
{
    "nombre": "string",
    "cantidad": "decimal",
    "unidad": "string",
    "precio_unitario": "decimal"
}
```

### Recetas (Recipes)
```
GET /api/recetas/ - List all recipes
POST /api/recetas/ - Create new recipe
GET /api/recetas/{id}/ - Get recipe details
PUT /api/recetas/{id}/ - Update recipe
DELETE /api/recetas/{id}/ - Delete recipe

# Special endpoints
GET /api/recetas/por_categoria/?categoria={categoria} - Get recipes by category
POST /api/recetas/{id}/verificar_insumos/ - Check if there are enough ingredients
```

Request body for creating/updating recipes:
```json
{
    "nombre": "string",
    "descripcion": "string",
    "porciones": "decimal",
    "categoria": "string",
    "insumos": [
        {
            "insumo": "insumo_id",
            "cantidad": "decimal"
        }
    ]
}
```

### Ventas (Sales)
```
GET /api/ventas/ - List all sales
POST /api/ventas/ - Create new sale
GET /api/ventas/{id}/ - Get sale details
PUT /api/ventas/{id}/ - Update sale
DELETE /api/ventas/{id}/ - Delete sale

# Special endpoints
GET /api/ventas/ventas_por_periodo/?fecha_inicio={date}&fecha_fin={date} - Get sales by period
GET /api/ventas/resumen_ventas/ - Get sales summary
```

Request body for creating/updating sales:
```json
{
    "receta": ["receta_id"],
    "total": "decimal",
    "completada": "boolean"
}
```

### Mermas (Waste)
```
GET /api/mermas/ - List all waste records
POST /api/mermas/ - Create new waste record
GET /api/mermas/{id}/ - Get waste record details
PUT /api/mermas/{id}/ - Update waste record
DELETE /api/mermas/{id}/ - Delete waste record

# Special endpoints
GET /api/mermas/mermas_por_periodo/?fecha_inicio={date}&fecha_fin={date} - Get waste by period
GET /api/mermas/resumen_mermas/ - Get waste summary by ingredient
```

Request body for creating/updating waste records:
```json
{
    "insumo": "insumo_id",
    "cantidad": "decimal"
}
```

### RecetaInsumos (Recipe Ingredients)
```
GET /api/recetainsumos/ - List all recipe ingredients
POST /api/recetainsumos/ - Create new recipe ingredient
GET /api/recetainsumos/{id}/ - Get recipe ingredient details
PUT /api/recetainsumos/{id}/ - Update recipe ingredient
DELETE /api/recetainsumos/{id}/ - Delete recipe ingredient

# Filter by recipe
GET /api/recetainsumos/?receta={receta_id} - Get ingredients for a specific recipe
```

Request body for creating/updating recipe ingredients:
```json
{
    "receta": "receta_id",
    "insumo": "insumo_id",
    "cantidad": "decimal"
}
```

## Response Format

All responses are in JSON format and include:
- For list endpoints: paginated results with 10 items per page
- For detail endpoints: complete object details
- For error responses: error message and details

## Authentication Requirements

- Most endpoints require authentication
- Some endpoints allow read-only access without authentication
- User registration is open to all
- Session or basic authentication is required for write operations.
Token authentication is not used.

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Pagination

All list endpoints are paginated with 10 items per page. The response includes:
- count: total number of items
- next: URL for next page
- previous: URL for previous page
- results: array of items 