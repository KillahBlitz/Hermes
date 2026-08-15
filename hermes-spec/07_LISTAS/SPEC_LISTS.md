# Feature 07: Listas & Gestión de Deseos (SPEC_LISTS.md)

Este documento define la especificación funcional, técnica, modelos de datos y diseño de interfaz para el módulo **Listas** (`/lists`) en Hermes.

---

## 1. Visión General del Módulo

El módulo de **Listas** provee un centro ágil de organización personal y material dividido en dos herramientas principales accesibles mediante un selector superior de pestañas:

1. **Lista de Deseos (Wishlist)**: Catálogo visual de artículos, compras futuras e inversiones personales. Permite registrar nombre, precio, descripción, fotos y enlace directo a la tienda o distribuidor. Las imágenes se almacenan de forma segura y persistente en el Google Drive del usuario dentro de la carpeta `hermes/whitelist`.
2. **Lista de Tareas (Estilo Microsoft To-Do)**: Gestor de tareas recurrentes y operativas con interfaz minimalista, ágil y de respuesta inmediata, organizadas en secciones/categorías temáticas con puntaje de dificultad/esfuerzo, fechas límite y frecuencias de repetición.

---

## 2. Requerimientos Funcionales

### 2.1. Navegación y Conmutador de Herramientas
En la cabecera de la página `app/pages/lists.vue` se dispondrá de un selector de pestañas conmutable:
* **"Lista de Deseos"** (Icono: 🎁 / 🛍️)
* **"Lista de Tareas"** (Icono: 📝 / ✅)

---

### 2.2. Herramienta 1: Lista de Deseos (Wishlist)

#### 2.2.1. Estructura de un Artículo de Deseo
Cada artículo registrado contará con:
* **Nombre del Artículo**: Título descriptivo (Requerido, ej. *"Monitor LG UltraWide 34'' Curvo"*).
* **Precio Estimado**: Monto numérico en moneda local (Requerido, ej. `$8,499.00`).
* **Categoría**: Categoría del artículo (ej. *Tecnología*, *Ropa/Estilo*, *Hogar*, *Gaming*, *Herramientas*, *Libros/Educación*).
* **Prioridad**: Nivel de deseo o urgencia (`ALTA` 🔥, `MEDIA` ⚡, `BAJA` 💤).
* **Descripción / Notas**: Notas adicionales, variantes, tallas o especificaciones (Opcional).
* **Enlace de Compra (URL)**: Enlace web directo a Amazon, MercadoLibre, AliExpress, sitio oficial, etc.
* **Fotos / Galería de Imágenes**: Lista de IDs y URLs de fotos alojadas en Google Drive en la carpeta `hermes/whitelist`.
* **Estado de Compra**:
  - `PENDING` (Deseo pendiente)
  - `PURCHASED` (Adquirido / Comprado)
  - `ARCHIVED` (Descartado / Pospuesto)
* **Fecha de Registro y Fecha de Adquisición**.

#### 2.2.2. Integración con Google Drive Bucket (`hermes/whitelist`)
* Al dar de alta un deseo y adjuntar fotos:
  1. El backend verifica la existencia de la carpeta raíz `hermes` en Google Drive (creada en Feature 4).
  2. El backend asegura la existencia de la subcarpeta `whitelist` dentro de `hermes` (`hermes/whitelist/`).
  3. Las imágenes se suben en formato multipart a la subcarpeta `whitelist`.
  4. Los IDs de archivo de Drive y URLs de vista previa se asocian al documento en MongoDB (`wishlist_items`).
  5. Al eliminar un artículo de deseo, se ofrece la opción de limpiar los archivos multimedia asociados de Drive.

#### 2.2.3. Funcionalidades Visuales y de Interacción (Wishlist)
* **Vista en Cuadrícula de Tarjetas**: Visualización estilo e-commerce premium con imagen principal, badge de precio neón, prioridad y botón de acceso directo `Ir a Comprar ↗`.
* **Filtros Rápidos**: Filtrar por Estado (`Pendientes`, `Comprados`, `Todos`), por Categoría y por Prioridad.
* **Marcado Rápido de Comprado**: Checkbox o botón `Marcar como Comprado` con animación de confetti / efecto neón verde.
* **KPIs Rápidos de Deseos**:
  - Total de artículos pendientes.
  - Valor monetario acumulado estimado en deseos pendientes.
  - Total de deseos cumplidos/comprados.

---

### 2.3. Herramienta 2: Lista de Tareas (Estilo Microsoft To-Do)

#### 2.3.1. Enfoque de Diseño y Simplicidad
* Inspirada en la fluidez de **Microsoft To-Do**:
  - Barra lateral o menú de secciones/categorías (ej. *Mi Día*, *Importantes*, *Hogar*, *Trabajo*, *Finanzas*, *Estudio* + Secciones personalizadas).
  - Input rápido en la parte superior para añadir una tarea presionando `Enter`.
  - Checkbox circular con micro-animación de marcado inmediato y tachado elegante.
  - Panel o modal lateral para añadir notas, fechas de vencimiento y configuración de repetición.

#### 2.3.2. Estructura de la Tarea To-Do
* **Título**: Texto descriptivo de la tarea (Requerido, ej. *"Revisar estado de cuenta bancario"*).
* **Sección / Categoría**: ID de la sección asociada (ej. *Rutinas*, *Hogar*, *Personal*, *Estudio*).
* **Puntaje de Dificultad / Esfuerzo**:
  - `1 pt` (Muy fácil / Rápida < 5 min)
  - `2 pts` (Fácil / 15 min)
  - `3 pts` (Media / 30-45 min)
  - `5 pts` (Exigente / > 1 hora)
* **Frecuencia de Repetición**:
  - `NONE` (Sin repetición / Una sola vez)
  - `DAILY` (Diaria)
  - `WEEKDAYS` (Lunes a Viernes)
  - `WEEKLY` (Semanal)
  - `MONTHLY` (Mensual)
* **Fecha de Vencimiento**: Fecha límite opcional.
* **Notas / Pasos**: Texto complementario o checklist de sub-pasos.
* **Estado**: `COMPLETED` | `PENDING`.
* **Fecha de Realización**: Timestamp de cuándo se marcó como completada.

#### 2.3.3. CRUD de Secciones / Categorías de Tareas
* CRUD completo de secciones: Nombre, Icono (Emoji) y Color identificador.
* Secciones predeterminadas sembradas para el usuario:
  - ☀️ **Mi Día** (Tareas del día presente)
  - 🔁 **Rutinas Repetitivas**
  - 🏠 **Hogar & Personal**
  - 💼 **Trabajo & Proyectos**

---

## 3. Modelo de Base de Datos (MongoDB)

### 3.1. Colección: `wishlist_items`
```json
{
  "_id": ObjectId("..."),
  "user_id": "google_oauth_sub_or_uid",
  "name": "Monitor LG UltraWide 34''",
  "price": 8499.00,
  "currency": "MXN",
  "category": "Tecnología",
  "priority": "ALTA", // "ALTA" | "MEDIA" | "BAJA"
  "description": "Panel IPS QHD, 144Hz para productividad y gaming",
  "url": "https://www.amazon.com.mx/dp/example",
  "images": [
    {
      "drive_file_id": "1A2B3C4D5E...",
      "name": "monitor_front.jpg",
      "mime_type": "image/jpeg",
      "size": 1048576,
      "thumbnail_link": "https://...",
      "web_view_link": "https://drive.google.com/..."
    }
  ],
  "status": "PENDING", // "PENDING" | "PURCHASED" | "ARCHIVED"
  "purchased_at": null,
  "created_at": ISODate("2026-08-14T22:00:00Z"),
  "updated_at": ISODate("2026-08-14T22:00:00Z")
}
```

### 3.2. Colección: `todo_sections`
```json
{
  "_id": ObjectId("..."),
  "user_id": "google_oauth_sub_or_uid",
  "name": "Rutinas Diarias",
  "icon": "🔁",
  "color": "#00E5FF",
  "is_default": true,
  "order": 1,
  "created_at": ISODate("2026-08-14T22:00:00Z")
}
```

### 3.3. Colección: `todo_tasks`
```json
{
  "_id": ObjectId("..."),
  "user_id": "google_oauth_sub_or_uid",
  "section_id": "ObjectId_de_todo_sections",
  "title": "Limpiar bandeja de entrada de correos",
  "difficulty_points": 1, // 1 | 2 | 3 | 5
  "repeat": "DAILY", // "NONE" | "DAILY" | "WEEKDAYS" | "WEEKLY" | "MONTHLY"
  "due_date": ISODate("2026-08-15T00:00:00Z"),
  "notes": "Archivar o responder correos con etiqueta importante",
  "is_completed": false,
  "completed_at": null,
  "created_at": ISODate("2026-08-14T22:00:00Z"),
  "updated_at": ISODate("2026-08-14T22:00:00Z")
}
```

---

## 4. Endpoints REST (FastAPI - `hermes-api`)

Todos los endpoints se ubican bajo el prefijo `/api/v1/lists/` y requieren autenticación mediante JWT (`Bearer Token`).

### 4.1. Endpoints de Lista de Deseos (`/api/v1/lists/wishlist`)
* `GET /api/v1/lists/wishlist`: Listado de artículos de deseo con filtros por `status`, `category`, `priority` y búsqueda `search`. Incluye KPI resumen (total valor acumulado, pendientes, comprados).
* `POST /api/v1/lists/wishlist`: Creación de un artículo de deseo.
* `POST /api/v1/lists/wishlist/{item_id}/upload-photo`: Subida multipart de imágenes a Google Drive en la carpeta `hermes/whitelist`.
* `PUT /api/v1/lists/wishlist/{item_id}`: Edición de campos del artículo.
* `PATCH /api/v1/lists/wishlist/{item_id}/status`: Cambio rápido de estado (`PENDING` <-> `PURCHASED` <-> `ARCHIVED`).
* `DELETE /api/v1/lists/wishlist/{item_id}`: Eliminación de artículo y limpieza opcional de fotos en Drive.

### 4.2. Endpoints de Tareas To-Do & Secciones (`/api/v1/lists/todo`)
* `GET /api/v1/lists/todo/sections`: Lista de secciones/categorías del usuario con contador de tareas activas.
* `POST /api/v1/lists/todo/sections`: Creación de una nueva sección.
* `PUT /api/v1/lists/todo/sections/{section_id}`: Actualización de sección.
* `DELETE /api/v1/lists/todo/sections/{section_id}`: Eliminación de sección y reasignación/limpieza de tareas asociadas.
* `GET /api/v1/lists/todo/tasks`: Listado de tareas con filtro por `section_id`, `completed` (true/false) y búsqueda.
* `POST /api/v1/lists/todo/tasks`: Creación rápida de una tarea To-Do.
* `PUT /api/v1/lists/todo/tasks/{task_id}`: Edición completa de una tarea To-Do.
* `PATCH /api/v1/lists/todo/tasks/{task_id}/toggle`: Conmutación inmediata de estado (`is_completed: true/false`).
* `DELETE /api/v1/lists/todo/tasks/{task_id}`: Eliminación permanente de la tarea.

---

## 5. Arquitectura del Frontend (`hermes-platform`)

### 5.1. Composable de Estado (`app/composables/useLists.ts`)
* Centraliza el estado de la Wishlist y de las Tareas To-Do:
  - `activeToolTab`: `'wishlist' | 'todo'`.
  - `wishlistItems`, `wishlistStats`, `activeWishlistFilter`.
  - `todoSections`, `todoTasks`, `selectedSectionId`.
  - Métodos CRUD completos y subida de archivos multipart para Drive.

### 5.2. Componentes Átomos y Moléculas
* `app/components/atoms/WishlistPriceTag.vue`: Badge con precio formateado con brillo neón.
* `app/components/atoms/WishlistPriorityBadge.vue`: Indicador de prioridad (`🔥 Alta`, `⚡ Media`, `💤 Baja`).
* `app/components/atoms/DifficultyPointsPill.vue`: Píldora de puntaje de esfuerzo (`1 pt`, `2 pts`, `3 pts`, `5 pts`).
* `app/components/molecules/WishlistCard.vue`: Tarjeta e-commerce con carrusel/preview de fotos, precio, prioridad, botón de compra externa y toggle de comprado.
* `app/components/molecules/TodoTaskRow.vue`: Fila minimalista estilo Microsoft To-Do con checkbox circular interactivo, tachado, fecha y dificultad.
* `app/components/molecules/TodoSectionItem.vue`: Ítem de la barra lateral de secciones con contador.

### 5.3. Componentes Organismos
* `app/components/organisms/WishlistSection.vue`: Cuadrícula de deseos, barra de filtros, KPIs monetarios y botón "+ Nuevo Deseo".
* `app/components/organisms/TodoSection.vue`: Layout con barra lateral de secciones, input rápido de creación y lista de tareas completadas/pendientes.
* `app/components/organisms/WishlistModal.vue`: Modal para crear/editar deseos y adjuntar fotos directamente hacia Google Drive.
* `app/components/organisms/TodoSectionModal.vue`: Modal para crear/editar secciones de tareas To-Do.
* `app/components/organisms/TodoDetailModal.vue`: Panel/modal de detalles de una tarea (notas, dificultad, frecuencia).

### 5.4. Vista Principal
* `app/pages/lists.vue`: Página protegida por Google Auth con conmutador superior de herramientas y renderizado reactivo de `WishlistSection` y `TodoSection`.

---

## 6. Criterios de Aceptación

1. **Persistencia en Drive**: Toda foto adjuntada a un artículo de la lista de deseos debe subirse directamente al Google Drive del usuario logeado en la ruta `hermes/whitelist/`.
2. **Navegación Externa Segura**: Los enlaces de compra registrados deben abrirse en una nueva pestaña con `rel="noopener noreferrer"`.
3. **Simplicidad To-Do**: La lista de tareas debe permitir agregar tareas con solo presionar `Enter` en el input y marcar/desmarcar con un solo clic instantáneo.
4. **Aislamiento Multiusuario**: Todos los deseos, secciones y tareas To-Do están estrictamente aislados por el identificador `user_id` del token JWT.
5. **Diseño Visual**: Aplicación coherente del sistema de diseño Hermes (Dark Mode, `#0c0c0e`, `#17171c`, acentos neón `#00FFC6`, `#00E5FF`, `#FF007F`, glassmorphism y transiciones suaves).
