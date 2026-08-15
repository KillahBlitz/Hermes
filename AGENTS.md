# Hermes Project - Agent Guidelines & Context Memory (AGENTS.md)

Este documento actúa como la memoria central y contexto arquitectónico de **Hermes** para todos los agentes de desarrollo.

---

## 1. Visión General del Proyecto

Hermes es una plataforma modular y moderna dividida en:
* **`hermes-platform`**: Frontend desarrollado en **Nuxt 4** (Vue 3, Bootstrap 5, Vanilla CSS).
* **`hermes-api`**: Backend desarrollado en **FastAPI** (Python 3.11+).
* **`hermes-db`**: Base de datos **MongoDB**.
* **`hermes-spec`**: Especificaciones funcionales y técnicas de cada feature (e.g., `01_auth/SPEC_AUTH.md`, `02_barmenu/`, etc.).

---

## 2. Sistema de Diseño y Frontend (hermes-platform)

### 2.1. Paleta de Colores Oficial
Se deben emplear estrictamente las variables CSS definidas en el sistema:

```css
:root {
  /* Fondos */
  --hermes-bg-base: #0c0c0e;
  --hermes-bg-surface: #17171c;
  
  /* Acentos Neón */
  --hermes-accent-teal: #00FFC6;
  --hermes-accent-blue: #00E5FF; /* Principal para animaciones */
  --hermes-accent-pink: #FF007F; /* Principal para animaciones */
  
  /* Texto */
  --hermes-text-primary: #F4F4F5;
  --hermes-text-muted: #94949E;
}
```

### 2.2. Arquitectura de Componentes
* Ubicada dentro del directorio `app/`:
  - `app/components/`: Componentes reutilizables (átomos, moléculas).
  - `app/templates/`: Contenedores y templates estructurales (e.g., `AuthTemplate.vue`).
  - `app/pages/`: Vistas y rutas de la aplicación (e.g., `login.vue`, `index.vue`).
  - `app/layouts/`: Layouts globales de Nuxt (`default.vue`).
  - `app/assets/css/main.css`: Variables de tema y utilidades globales.
* **Estilo Visual**: Dark mode premium, bordes brillantes con neón, glassmorphism (`backdrop-filter: blur(12px)`) y animaciones con gradientes dinámicos basados en azul (`#00E5FF`) y rosa (`#FF007F`).

---

## 3. Arquitectura del Backend (hermes-api)

### 3.1. Estructura de Directorios
```
hermes-api/
├── assets/
│   └── requirements.txt        # Dependencias de Python (FastAPI, Pydantic, Firebase, etc.)
└── src/
    ├── app/
    │   ├── endpoints/          # Controladores HTTP por módulo (e.g., auth.py)
    │   └── main.py             # Instanciación de FastAPI y registro de routers
    ├── models/
    │   ├── request/            # Pydantic schemas para peticiones entrantes
    │   └── response/           # Pydantic schemas para respuestas salientes
    ├── services/               # Lógica de negocio y clientes externos (e.g., firebase_service.py)
    └── utils/                  # Utilidades comunes (criptografía, helpers)
```

### 3.2. Reglas de Desarrollo Backend
1. **Modelado con Pydantic**: 
   - Cualquier petición recibida debe estar tipada en `models/request/<modulo>.py`.
   - Cualquier respuesta debe estar tipada en `models/response/<modulo>.py`.
2. **Capa de Servicios**:
   - Todo acceso o interacción con Firebase Admin SDK debe estar encapsulado en `src/services/firebase_service.py`. Ningún endpoint debe llamar a Firebase directamente.
3. **Cifrado de Credenciales**:
   - Los tokens de Google OAuth (`access_token`, `refresh_token`) deben ser cifrados antes de persistirse en MongoDB.

---

## 4. Feature 1: Autenticación con Google (Firebase) & Integraciones

* **Especificación Completa**: Consulta `hermes-spec/01_auth/SPEC_AUTH.md`.
* **Scopes de Google Requeridos**:
  1. `https://www.googleapis.com/auth/drive` (Google Drive)
  2. `https://www.googleapis.com/auth/calendar` (Google Calendar)
  3. `https://www.googleapis.com/auth/gmail.modify` (Gmail)
* **Flujo de Tokens**:
  1. Frontend ejecuta `signInWithPopup(auth, provider)` solicitando los 3 scopes.
  2. Frontend extrae `Firebase ID Token` y `Google Access/Refresh Token`.
  3. Frontend envía credenciales a `POST /api/v1/auth/login`.
  4. Backend valida el `ID Token` con `FirebaseService`, crea/actualiza el usuario en MongoDB y cifra los tokens de Google.

---

## 5. Variables de Entorno Requeridas

### Frontend (`hermes-platform/.env`)
* `NUXT_PUBLIC_API_BASE_URL`: URL base de la API FastAPI.
* `NUXT_PUBLIC_FIREBASE_API_KEY`: API Key del proyecto Firebase.
* `NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN`: Dominio de autenticación de Firebase.
* `NUXT_PUBLIC_FIREBASE_PROJECT_ID`: ID del proyecto Firebase.
* `NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET`: Storage bucket de Firebase.
* `NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`: Sender ID de Firebase.
* `NUXT_PUBLIC_FIREBASE_APP_ID`: App ID de Firebase.

### Backend (`hermes-api/.env`)
* `HOST` & `PORT`: Configuración de Uvicorn/FastAPI.
* `CORS_ORIGINS`: Orígenes permitidos (e.g., `http://localhost:3000`).
* `MONGO_HOST` & `MONGO_DATABASE`: Conexión a MongoDB.
* `FIREBASE_CREDENTIALS_PATH`: Ruta al archivo `serviceAccountKey.json`.
* `ENCRYPTION_KEY`: Llave Fernet para cifrar tokens en MongoDB.
* `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Configuración de sesiones JWT.

---

## 6. Feature 2: Menú Lateral Retráctil y Fijo (BarMenu)

* **Especificación Completa**: Consulta `hermes-spec/02_barmenu/SPEC_BARMENU.md`.
* **5 Módulos Obligatorios**:
  1. `Administrador de servicios` (`/services`)
  2. `Administración económica` (`/finance`)
  3. `Tableros` (`/boards`)
  4. `Listas` (`/lists`)
  5. `Progreso` (`/progress`) - *Unificación de Progreso profesional y Conocimiento*
* **Comportamiento y Persistencia**:
  - Dual: Fijo (`isPinned = true`, `260px`, empuja layout) vs. Colapsado (`isPinned = false`, `72px` compacto con hover flotante).
  - Persistencia del estado con composable `useSidebarState` y `localStorage`.
  - Micro-animaciones: Píldora neón indicadora de ruta activa (gradiente azul-rosa), rotación de pin y tooltips flotantes.

---

## 7. Feature 4: Administrador de Servicios (Gmail & Drive Bucket) - IMPLEMENTADO

* **Especificación Completa**: Consulta `hermes-spec/04_services/SPEC_SERVICES.md`.
* **Backend (`hermes-api`)**:
  - `src/services/gmail_service.py`: Consulta de correos destacados (`is:starred`) e importantes (`is:important`), lectura y papelera.
  - `src/services/drive_service.py`: Creación/verificación del bucket `hermes` con carpetas `multimedia` y `archivos`, navegación, subida multipart y vistas previas.
  - `src/services/audit_service.py`: Registro inmutable en `service_audit_logs` (MongoDB).
  - `src/app/endpoints/services.py`: 10 endpoints bajo `/api/v1/services/`.
* **Frontend (`hermes-platform`)**:
  - Selector dual de pestañas: **"Correos"** y **"Multimedia"** en `app/pages/services.vue`.
  - Composables: `useGmailService.ts` y `useDriveBucket.ts`.
  - Componentes: `EmailListSection`, `DriveBucketSection`, `EmailCard`, `DriveFileCard`, `DriveBreadcrumb`, `FileUploadZone`, `EmailDetailModal`, `DeleteConfirmModal`, `FilePreviewModal`.

---

## 8. Feature 0: CI/CD Pipeline & Despliegue (SPEC_DEPLOY.md) - IMPLEMENTADO

* **Especificación Completa**: Consulta `hermes-spec/00_deploy/SPEC_DEPLOY.md`.
* **Workflow**: `.github/workflows/main.yml`.
* **Disparador**: Exclusivo al hacer `push` a la rama `main`.
* **Runner**: GitHub Actions *Self-Hosted Runner* en el servidor de producción.
* **Pipeline en 2 Fases**:
  1. `preparar-deploy`: Validación de conectividad, runner y versiones de Docker / Docker Compose.
  2. `deploy-prod`: Checkout del código, inyección de variables desde el host (`~/.env.hermesapi` y `~/.env.hermesplatform`), ejecución de `docker compose -p hermes-prod up -d --build --remove-orphans` y limpieza de imágenes no utilizadas.
* **Dockerización & Puertos Host**:
  - `hermes-api/Dockerfile`: Base `python:3.11-slim` expuesta al host en **puerto 9003** (`9003:8000`).
  - `hermes-platform/Dockerfile`: Multi-stage `node:22-alpine` (SSR a `.output`) expuesta al host en **puerto 3003** (`3003:3000`).
  - `docker-compose.yml`: Orquestación de servicios en red `hermes-network` con límites de memoria de 512MB adaptados a servidores pequeños.

---

## 9. Feature 5: Administración Económica (SPEC_ECONOMY.md) - IMPLEMENTADO

* **Especificación Completa**: Consulta `hermes-spec/05_economy/SPEC_ECONOMY.md`.
* **Ruta Frontend**: `/finance`
* **Backend (`hermes-api`)**:
  - `src/services/finance_service.py`: CRUD de transacciones y categorías, agregaciones para KPIs de balance, comparativas MoM, desglose por categoría y tendencias semestrales.
  - `src/app/endpoints/finance.py`: 12 endpoints REST bajo `/api/v1/finance/`.
* **Frontend (`hermes-platform`)**:
  - `app/composables/useFinance.ts`: Manejo reactivo de estado financiero, meses, filtros y paginación.
  - Componentes: `MoneyBadge`, `PercentageIndicator`, `CategoryTag`, `FinanceKpiCard`, `MonthSelector`, `InsightBanner`, `TransactionRow`, `FinanceTrendsChart`, `CategoryDonutChart`, `TransactionListSection`, `TransactionModal`, `CategoryManagerModal`.
  - Página: `app/pages/finance.vue`.
* **Colecciones en MongoDB**: `finance_transactions` y `finance_categories`.

---

## 10. Feature 6: Tableros Inteligentes (SPEC_TABLERO.md) - IMPLEMENTADO

* **Especificación Completa**: Consulta `hermes-spec/06_tablero/SPEC_TABLERO.md`.
* **Ruta Frontend**: `/boards`
* **3 Herramientas Principales**:
  1. **Tablero de Actividades**:
     - Kanban de 4 columnas (`ToDo`, `In Progress`, `To Be Tested`, `Done`) con Drag & Drop nativo.
     - Sub-vistas: Tablero Activo, Backlog y Finalizados (+7 días tras completarse).
     - Tipos de tarea: `Mejora` (Verde), `Urgente` (Rosa), `Pendiente` (Amarillo), `Análisis` (Azul).
     - Niveles de complejidad (`XS`, `S`, `M`, `L`, `XL`) y CRUD de Épicas (`Escuela`, `Trabajo`, `Cursos`).
  2. **Tablero de Hábitos (21 Días)**: Matriz interactiva de 21 casillas por hábito, contador de racha (`streak`), porcentaje de cumplimiento y consolidación de hábitos.
  3. **Pizarrón de Ideas**: Canvas interactivo con Post-its posicionables libremente en cualquier coordenada X/Y, cambio dinámico de color neón y edición de contenido.
* **Colecciones en MongoDB**: `board_epics`, `board_tasks`, `board_habits`, `board_sticky_notes`.

---

## 11. Feature 7: Listas & Deseos (SPEC_LISTS.md) - IMPLEMENTADO

* **Especificación Completa**: Consulta `hermes-spec/07_LISTAS/SPEC_LISTS.md`.
* **Ruta Frontend**: `/lists`
* **2 Herramientas Principales**:
  1. **Lista de Deseos (Wishlist)**:
     - Catálogo de compras futuras con nombre, precio, descripción, fotos, enlace de compra (URL externa), prioridad y estado (`PENDING`, `PURCHASED`, `ARCHIVED`).
     - Almacenamiento de fotos en Google Drive bajo la carpeta `hermes/whitelist`.
  2. **Lista de Tareas (Estilo Microsoft To-Do)**:
     - Tareas repetitivas y rutinarias organizadas por secciones/categorías temáticas.
     - Puntaje de dificultad/esfuerzo (1, 2, 3, 5 puntos), frecuencia de repetición (`Diaria`, `Lunes a Viernes`, `Semanal`, `Mensual`, `Ninguna`), fechas límite y checkbox rápido de completado.
* **Colecciones en MongoDB**: `wishlist_items`, `todo_sections`, `todo_tasks`.
* **Backend (`hermes-api`)**:
  - `src/services/lists_service.py`: Lógica de Wishlist (CRUD, KPIs monetarios, subida multipart a Google Drive `hermes/whitelist`), Secciones To-Do (seeding atómico) y Tareas To-Do (creación ágil, conmutación de estado).
  - `src/app/endpoints/lists.py`: 15 endpoints REST bajo `/api/v1/lists/`.
* **Frontend (`hermes-platform`)**:
  - `app/composables/useLists.ts`: Estado reactivo y métodos CRUD para Wishlist y To-Do.
  - Componentes: `WishlistPriceTag`, `WishlistPriorityBadge`, `DifficultyPointsPill`, `WishlistCard`, `TodoTaskRow`, `TodoSectionSidebar`, `WishlistSection`, `TodoSection`, `WishlistModal`, `WishlistPhotoUploadModal`, `TodoSectionModal`, `TodoTaskModal`.
  - Página: `app/pages/lists.vue`.

---

## 12. Feature 8: Módulo de Progreso (SPEC_PROFETIONAL.md) - ESPECIFICADO

* **Especificación Completa**: Consulta `hermes-spec/08_profesional/SPEC_PROFETIONAL.md`.
* **Ruta Frontend**: `/progress` (Unifica Progreso profesional y Conocimiento).
* **3 Herramientas Principales**:
  1. **Árbol de Mapas (Roadmap Canvas)**:
     - Pizarrón interactivo infinito/expandible con nodos modulares conectados mediante flechas/aristas.
     - Al hacer clic en un rectángulo/nodo, se abre un editor/visor Markdown (`.md`) asociado para documentar bitácoras y apuntes técnicos de ese módulo.
  2. **Gestor de Hitos (Milestones Tracker)**:
     - Rastreador visual de proyectos de gran escala (Titulación, Certificaciones AWS, Exámenes críticos de materias como probabilidad).
     - Cuentas regresivas (*deadlines*) y barras de progreso porcentual ponderadas por temarios/entregables.
  3. **Red de Enlaces Zettelkasten (Knowledge Vault & Graph)**:
     - Bóveda de notas Markdown interconectadas con sintaxis de wikilinks `[[NombreDeNota]]` y `#tags`.
     - Grafo de conocimiento 2D interactivo con simulación de fuerzas y backlinks automáticos.
* **Colecciones en MongoDB**: `progress_roadmaps`, `progress_milestones`, `progress_notes`.


