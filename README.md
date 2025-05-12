# MUMO API Documentation

## Authentication

La API utiliza autenticación basada en tokens y protección CSRF. Para acceder a los endpoints protegidos, debes seguir estos pasos:

1. **Login inicial**:
   - Realiza una petición POST a `/api/login/` con las credenciales
   - El servidor devolverá un token de autenticación
   - Guarda este token para futuras peticiones

2. **Peticiones autenticadas**:
   - Incluye el token en el header `Authorization: Token <tu-token>`
   - El CSRF token se maneja automáticamente con las cookies

### Endpoints de Autenticación

#### Login

**POST** `/api/login/`

Request body:
```json
{
  "username": "string",
  "password": "string"
}
```

Response:
```json
{
  "token": "string",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

#### Registro de Usuario

**POST** `/api/users/`

Request body:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

## API Endpoints

### Users

* `GET /api/users/` – Listar todos los usuarios
* `POST /api/users/` – Crear nuevo usuario
* `GET /api/users/{id}/` – Obtener detalles de usuario
* `PUT /api/users/{id}/` – Actualizar usuario
* `DELETE /api/users/{id}/` – Eliminar usuario

### Insumos (Ingredients)

* `GET /api/insumos/` – Listar todos los ingredientes
* `POST /api/insumos/` – Crear nuevo ingrediente
* `GET /api/insumos/{id}/` – Obtener detalles de ingrediente
* `PUT /api/insumos/{id}/` – Actualizar ingrediente
* `DELETE /api/insumos/{id}/` – Eliminar ingrediente

**Endpoints especiales:**

* `GET /api/insumos/stock_bajo/` – Obtener ingredientes con stock bajo (< 10 unidades)
* `GET /api/insumos/valor_total/` – Obtener valor total del inventario

**Request body para crear/actualizar ingredientes:**

```json
{
  "nombre": "string",
  "cantidad": "decimal",
  "unidad": "string",
  "precio_unitario": "decimal"
}
```

### Recetas (Recipes)

* `GET /api/recetas/` – Listar todas las recetas
* `POST /api/recetas/` – Crear nueva receta
* `GET /api/recetas/{id}/` – Obtener detalles de receta
* `PUT /api/recetas/{id}/` – Actualizar receta
* `DELETE /api/recetas/{id}/` – Eliminar receta

**Endpoints especiales:**

* `GET /api/recetas/por_categoria/?categoria={categoria}` – Obtener recetas por categoría
* `POST /api/recetas/{id}/verificar_insumos/` – Verificar si hay suficientes ingredientes

**Request body para crear/actualizar recetas:**

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

* `GET /api/ventas/` – Listar todas las ventas
* `POST /api/ventas/` – Crear nueva venta
* `GET /api/ventas/{id}/` – Obtener detalles de venta
* `PUT /api/ventas/{id}/` – Actualizar venta
* `DELETE /api/ventas/{id}/` – Eliminar venta

**Endpoints especiales:**

* `GET /api/ventas/ventas_por_periodo/?fecha_inicio={date}&fecha_fin={date}` – Obtener ventas por período
* `GET /api/ventas/resumen_ventas/` – Obtener resumen de ventas

**Request body para crear/actualizar ventas:**

```json
{
  "receta": ["receta_id"],
  "total": "decimal",
  "completada": "boolean"
}
```

### Mermas (Waste)

* `GET /api/mermas/` – Listar todas las mermas
* `POST /api/mermas/` – Crear nueva merma
* `GET /api/mermas/{id}/` – Obtener detalles de merma
* `PUT /api/mermas/{id}/` – Actualizar merma
* `DELETE /api/mermas/{id}/` – Eliminar merma

**Endpoints especiales:**

* `GET /api/mermas/mermas_por_periodo/?fecha_inicio={date}&fecha_fin={date}` – Obtener mermas por período
* `GET /api/mermas/resumen_mermas/` – Obtener resumen de mermas por ingrediente

**Request body para crear/actualizar mermas:**

```json
{
  "insumo": "insumo_id",
  "cantidad": "decimal"
}
```

## Formato de Respuesta

Todas las respuestas están en formato JSON e incluyen:

* Para endpoints de lista: resultados paginados con 10 items por página
* Para endpoints de detalle: detalles completos del objeto
* Para respuestas de error: mensaje de error y detalles

## Requisitos de Autenticación

* La mayoría de los endpoints requieren autenticación
* Algunos endpoints permiten acceso de solo lectura sin autenticación
* El registro de usuarios está abierto para todos
* Se requiere token de autenticación para operaciones de escritura
* Se requiere CSRF token para todas las peticiones que modifican datos

## Manejo de Errores

La API utiliza códigos de estado HTTP estándar:

* 200: Éxito
* 201: Creado
* 400: Solicitud incorrecta
* 401: No autorizado (token inválido o expirado)
* 403: Prohibido (CSRF token inválido)
* 404: No encontrado
* 500: Error del servidor

## Paginación

Todos los endpoints de lista están paginados con 10 items por página. La respuesta incluye:

* `count`: número total de items
* `next`: URL para la siguiente página
* `previous`: URL para la página anterior
* `results`: array de items
