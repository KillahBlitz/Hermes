# Feature 06: Tableros Inteligentes (SPEC_TABLERO.md)

Este documento define la especificación funcional, técnica, modelos de datos y diseño de interfaz para el módulo **Tableros** (`/boards`) en Hermes.

---

## 1. Visión General del Módulo

El módulo de **Tableros** provee un centro unificado de productividad, desarrollo personal y creatividad estructurado en tres herramientas especializadas accesibles mediante un menú superior de selección conmutable:

1. **Tablero de Actividades**: Sistema de gestión de tareas estilo Jira con tablero Kanban de 4 columnas (`ToDo`, `In Progress`, `To Be Tested`, `Done`), Backlog de priorización, archivo de tareas finalizadas (+7 días), categorización por Tipos (`Mejora`, `Urgente`, `Pendiente`, `Análisis`), niveles de complejidad y CRUD de Épicas (`Escuela`, `Trabajo`, `Cursos`, etc.).
2. **Tablero de Hábitos**: Sistema de seguimiento y consolidación de hábitos basado en el método científico de los **21 días consecutivos** con matriz visual de racha, porcentaje de cumplimiento y recompensas visuales.
3. **Pizarrón de Ideas**: Canvas interactivo de post-its / notas adhesivas con posicionamiento libre en cualquier área (coordenadas X/Y), paleta de colores neón, edición de contenido y persistencia en tiempo real.

---

## 2. Requerimientos Funcionales

### 2.1. Navegación Superior y Conmutador de Vistas
El módulo debe incluir una barra de pestañas superior en `app/pages/boards.vue` con 3 secciones:
* **"Tablero de Actividades"** (Icono: 📋)
* **"Tablero de Hábitos (21 Días)"** (Icono: ⚡)
* **"Pizarrón de Ideas"** (Icono: 💡)

---

### 2.2. Sección 1: Tablero de Actividades

#### 2.2.1. Sub-Vistas del Tablero de Actividades
La sección de actividades cuenta con tres modos de visualización rápidos:
1. **Tablero Kanban (Activo)**: Visualización en 4 columnas con tarjetas interactivas y drag & drop / selección rápida de estado.
2. **Backlog**: Lista estructurada para planificar, estimar y priorizar tareas antes de pasarlas al tablero activo.
3. **Finalizados (Histórico)**: Repositorio de tareas completadas hace más de 7 días para auditoría y consulta histórica sin saturar el flujo visual del tablero.

#### 2.2.2. Columnas del Tablero Kanban
* `ToDo` (Por Hacer) - Tareas listas para ser abordadas.
* `In Progress` (En Progreso) - Tareas en desarrollo activo.
* `To Be Tested` (Por Probar / En Revisión) - Tareas pendientes de validación o pruebas.
* `Done` (Finalizado) - Tareas completadas recientemente (< 7 días).

#### 2.2.3. Tipos de Tarea (Etiquetado Estricto)
Cada tarea debe pertenecer obligatoriamente a uno de los 4 tipos predefinidos con código de color e icono:
* 🟢 **Mejora** (`IMPROVEMENT`): Optimización, refactorización o nueva funcionalidad (Color: `#00FFC6` Verde Neón).
* 🔴 **Urgente** (`URGENT`): Incidencia crítica o tarea bloqueante con alta prioridad (Color: `#FF007F` Rosa Neón).
* 🟡 **Pendiente** (`PENDING`): Tarea operativa o pendiente estándar (Color: `#FFD166` Amarillo).
* 🔵 **Análisis** (`ANALYSIS`): Investigación, diseño de arquitectura o análisis de requerimientos (Color: `#00E5FF` Azul Neón).

#### 2.2.4. Estructura de la Tarea
* **Título**: Nombre descriptivo de la tarea (Requerido, máx. 140 caracteres).
* **Descripción**: Detalle en formato Markdown o texto (Opcional).
* **Tipo**: `IMPROVEMENT` | `URGENT` | `PENDING` | `ANALYSIS`.
* **Nivel de Complejidad**:
  - `XS` (1 punto / Muy baja)
  - `S` (2 puntos / Baja)
  - `M` (3 puntos / Media)
  - `L` (5 puntos / Alta)
  - `XL` (8 puntos / Muy alta)
* **Épica**: Asociación a una Épica de trabajo (con badge de color).
* **Estado**: `TODO` | `IN_PROGRESS` | `TESTING` | `DONE`.
* **Ubicación**: `BOARD` (En tablero activo) | `BACKLOG` (En cola).
* **Fechas**: Fecha de creación, fecha límite (opcional) y `completed_at` (marca temporal al pasar a `DONE`).

#### 2.2.5. Regla de los 7 Días para Tareas Finalizadas
* Cuando una tarea se mueve al estado `DONE`, el sistema registra `completed_at = datetime.utcnow()`.
* **Visualización en Tablero**: Las tareas con `completed_at` menor a 7 días se muestran en la columna `Done` del Kanban.
* **Transición a Finalizados**: Las tareas con `completed_at` mayor a 7 días se ocultan automáticamente del tablero activo y se listan de forma organizada en la pestaña/apartado **"Finalizados"**, manteniendo métricas de velocidad y tiempo de ciclo.

#### 2.2.6. Gestión de Épicas (CRUD)
* Catálogo de iniciativas / proyectos para agrupar tareas.
* **Épicas Base Predeterminadas**:
  - 🎓 `Escuela` (Color: `#118AB2`, Icono: `🎓`)
  - 💼 `Trabajo` (Color: `#00E5FF`, Icono: `💼`)
  - 📚 `Cursos` (Color: `#7209B7`, Icono: `📚`)
* Operaciones CRUD para crear nuevas épicas personalizadas con nombre, color neón y descripción.

---

### 2.3. Sección 2: Tablero de Hábitos (Método 21 Días)

#### 2.3.1. Filosofía y Funcionamiento
* El tablero permite registrar hábitos que el usuario desea incorporar a su rutina diaria.
* Cada hábito despliega una **cuadrícula de 21 casillas** numeradas del Día 1 al Día 21.

#### 2.3.2. Estados Diarios y Racha
* Cada casilla del día puede estar en:
  - `PENDING` (Pendiente / Día actual o futuro)
  - `COMPLETED` (Cumplido con éxito - Píldora verde neón brillante `✓`)
  - `FAILED` (No realizado - Píldora gris/roja)
* **Contador de Racha (`Streak`)**: Días consecutivos completados.
* **Barra de Progreso**: Porcentaje de avance hacia la meta de 21 días (e.g. `14/21 días - 66%`).
* **Estado del Hábito**:
  - `IN_PROGRESS`: En curso.
  - `CONSOLIDATED`: Hábito completado con éxito (21/21 días) con animación de logro.
  - `ARCHIVED`: Archivado.

#### 2.3.3. CRUD de Hábitos
* Campos: Nombre del hábito (ej. "Lectura técnica 30 min", "Ejercicio matutino"), categoría, icono representativo, fecha de inicio, notas motivacionales y frecuencia (Diario).

---

### 2.4. Sección 3: Pizarrón de Ideas (Sticky Notes Canvas)

#### 2.4.1. Lienzo Interactivo
* Área de canvas libre con patrón de rejilla oscura sutil y coordenadas libres.
* El usuario puede crear notas adhesivas (Post-its) y posicionarlas / arrastrarlas en cualquier punto del tablero (`x`, `y`).

#### 2.4.2. Personalización de Post-its
* **Paleta de Colores Neón Cyberpunk**:
  - 🟡 *Cyber Yellow*: `#FFD166`
  - 🟢 *Teal Mint*: `#00FFC6`
  - 🟣 *Neon Purple*: `#B5179E`
  - 🔵 *Electric Blue*: `#00E5FF`
  - 🔴 *Neon Pink*: `#FF007F`
* **Contenido**:
  - Título / Asunto rápido.
  - Cuerpo de la idea (con auto-resize y texto responsive).
  - Fecha de fijado.
  - Botón de cambio de color dinámico y botón de eliminar.
* **Comportamiento**:
  - Drag & drop libre con actualización de posición guardada en MongoDB (`x`, `y`, `z_index`).
  - Animación sutil de rotación ligera aleatoria (-1deg a +1.5deg) para sensación realista de post-it físico.

---

## 3. Modelo de Datos y MongoDB

### 3.1. Colección `board_epics`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "name": "Escuela",
  "description": "Actividades académicas y proyectos escolares",
  "color": "#118AB2",
  "icon": "🎓",
  "is_default": true,
  "created_at": "2026-08-15T00:00:00Z",
  "updated_at": "2026-08-15T00:00:00Z"
}
```

### 3.2. Colección `board_tasks`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "title": "Implementar autenticación OAuth",
  "description": "Configurar Firebase popup y endpoints de backend",
  "type": "IMPROVEMENT", // "IMPROVEMENT" | "URGENT" | "PENDING" | "ANALYSIS"
  "complexity": "M", // "XS" | "S" | "M" | "L" | "XL"
  "epic_id": "ObjectId",
  "status": "IN_PROGRESS", // "TODO" | "IN_PROGRESS" | "TESTING" | "DONE"
  "location": "BOARD", // "BOARD" | "BACKLOG"
  "order": 1,
  "due_date": "2026-08-25T18:00:00Z",
  "completed_at": null,
  "created_at": "2026-08-15T00:00:00Z",
  "updated_at": "2026-08-15T00:00:00Z"
}
```

### 3.3. Colección `board_habits`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "title": "Meditación 15 minutos",
  "description": "Práctica de mindfulness al despertar",
  "icon": "🧘",
  "color": "#00FFC6",
  "start_date": "2026-08-01T00:00:00Z",
  "days": [
    { "day_number": 1, "status": "COMPLETED", "date": "2026-08-01" },
    { "day_number": 2, "status": "COMPLETED", "date": "2026-08-02" },
    { "day_number": 3, "status": "PENDING", "date": "2026-08-03" }
    // ... hasta 21 días
  ],
  "current_streak": 2,
  "total_completed": 2,
  "is_consolidated": false,
  "created_at": "2026-08-01T00:00:00Z",
  "updated_at": "2026-08-02T10:00:00Z"
}
```

### 3.4. Colección `board_sticky_notes`
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "title": "Idea: Arquitectura Serverless",
  "content": "Evaluar migración de workers a Cloud Functions para optimizar consumo en idle.",
  "color": "#FFD166",
  "x": 240,
  "y": 180,
  "z_index": 1,
  "rotation": -1.2,
  "created_at": "2026-08-15T00:00:00Z",
  "updated_at": "2026-08-15T00:00:00Z"
}
```

---

## 4. Arquitectura de Endpoints REST (`hermes-api`)

Todos los endpoints requieren autenticación con token de Google/Firebase mediante la dependencia de autenticación JWT y operan bajo el prefijo `/api/v1/boards`.

### 4.1. Actividades y Tareas
* `GET /api/v1/boards/tasks` - Lista tareas con filtros (`location=BOARD|BACKLOG`, `status`, `epic_id`, `type`, `search`).
* `POST /api/v1/boards/tasks` - Crea una nueva tarea (en Tablero o Backlog).
* `GET /api/v1/boards/tasks/{task_id}` - Obtiene detalle de tarea.
* `PUT /api/v1/boards/tasks/{task_id}` - Actualiza datos de la tarea.
* `PATCH /api/v1/boards/tasks/{task_id}/status` - Mueve la tarea de columna/estado (`TODO`, `IN_PROGRESS`, `TESTING`, `DONE`) y actualiza `completed_at`.
* `PATCH /api/v1/boards/tasks/{task_id}/location` - Mueve entre `BOARD` y `BACKLOG`.
* `DELETE /api/v1/boards/tasks/{task_id}` - Elimina una tarea.
* `GET /api/v1/boards/tasks/archived` - Obtiene listado histórico de tareas finalizadas (+7 días).

### 4.2. Épicas
* `GET /api/v1/boards/epics` - Lista las épicas del usuario (asegura las bases `Escuela`, `Trabajo`, `Cursos`).
* `POST /api/v1/boards/epics` - Crea una nueva épica personalizada.
* `PUT /api/v1/boards/epics/{epic_id}` - Actualiza una épica.
* `DELETE /api/v1/boards/epics/{epic_id}` - Elimina una épica (reasigna tareas a sin épica).

### 4.3. Hábitos (21 Días)
* `GET /api/v1/boards/habits` - Lista los hábitos activos del usuario con su matriz de 21 días.
* `POST /api/v1/boards/habits` - Crea un nuevo hábito inicializando los 21 días.
* `PUT /api/v1/boards/habits/{habit_id}` - Actualiza título, icono o descripción.
* `PATCH /api/v1/boards/habits/{habit_id}/check-day` - Marca el estado de un día específico (`COMPLETED`, `FAILED`, `PENDING`) y recalcula rachas.
* `DELETE /api/v1/boards/habits/{habit_id}` - Elimina un hábito.

### 4.4. Pizarrón de Ideas (Post-its)
* `GET /api/v1/boards/notes` - Obtiene todas las notas adhesivas del usuario con sus posiciones X/Y.
* `POST /api/v1/boards/notes` - Crea un nuevo post-it en el lienzo.
* `PUT /api/v1/boards/notes/{note_id}` - Actualiza título, contenido o color.
* `PATCH /api/v1/boards/notes/{note_id}/position` - Actualiza coordenadas `x`, `y` y `z_index` tras arrastre.
* `DELETE /api/v1/boards/notes/{note_id}` - Elimina un post-it del lienzo.

---

## 5. Diseño y Componentes Frontend (`hermes-platform`)

### 5.1. Jerarquía de Componentes
```
app/
├── composables/
│   ├── useBoardTasks.ts       # Reactividad para tareas, columnas Kanban, Backlog y Finalizados
│   ├── useBoardHabits.ts      # Reactividad para hábitos, matriz 21 días y rachas
│   └── useStickyCanvas.ts     # Reactividad para Post-its, drag interactivo y posiciones
├── components/
│   ├── atoms/
│   │   ├── TaskTypeBadge.vue   # Píldora neón para Mejora, Urgente, Pendiente, Análisis
│   │   ├── ComplexityPill.vue  # Indicador de complejidad (XS, S, M, L, XL)
│   │   ├── HabitDayBox.vue     # Casilla interactiva individual del día (1 a 21)
│   │   └── StickyColorPicker.vue # Selector de color para notas adhesivas
│   ├── molecules/
│   │   ├── KanbanCard.vue      # Tarjeta de tarea con épica, tipo, complejidad y acciones
│   │   ├── HabitCard.vue       # Tarjeta de hábito con matriz de 21 días y barra de racha
│   │   ├── StickyNote.vue      # Post-it interactivo arrastrable con textarea y cambio de color
│   │   └── EpicBadge.vue       # Etiqueta con icono y color de la épica
│   └── organisms/
│       ├── KanbanBoardView.vue # Tablero con 4 columnas (ToDo, InProgress, Testing, Done)
│       ├── BacklogListView.vue # Vista de lista para priorización y paso a tablero
│       ├── ArchivedDoneView.vue # Vista de tareas completadas hace más de 7 días
│       ├── HabitsBoardView.vue # Cuadrícula de hábitos de 21 días con métricas
│       ├── StickyNotesCanvas.vue # Pizarrón interactivo con notas libres
│       ├── TaskModal.vue       # Modal para crear/editar tareas
│       ├── EpicManagerModal.vue # Modal para gestionar épicas
│       └── HabitModal.vue      # Modal para dar de alta nuevo hábito
└── pages/
    └── boards.vue              # Vista principal que ensambla las 3 herramientas
```

### 5.2. Estética Visual y Micro-interacciones
* **Dark Mode Cyberpunk**: Fondos `#0c0c0e` y `#17171c` con bordes sutiles y efectos glassmorphism.
* **Acentos Neón**:
  - Verde Neón `#00FFC6` para tareas de Mejora y días completados de hábitos.
  - Rosa Neón `#FF007F` para tareas Urgentes y alertas.
  - Azul Neón `#00E5FF` para Análisis y estado En Progreso.
  - Amarillo Neón `#FFD166` para post-its y tareas Pendientes.
* **Animaciones**: Transiciones fluidas al mover tarjetas entre columnas, brillo suave en casillas de hábitos completados y drag responsivo en el pizarrón de ideas.
