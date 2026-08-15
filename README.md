<p align="center">
  <img src="./hermes-platform/public/logo.png" alt="Hermes Platform Logo" width="130" height="130" style="border-radius: 28px; box-shadow: 0 0 40px rgba(0, 229, 255, 0.45);" />
</p>

<h1 align="center">Hermes — Full-Stack Productivity & Knowledge Ecosystem</h1>

<p align="center">
  <b>Plataforma integral y modular de productividad, administración económica, servicios en la nube (Google Workspace) y gestión del conocimiento personal.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11" />
  <img src="https://img.shields.io/badge/Nuxt-4.5.2-00DC82?style=for-the-badge&logo=nuxtdotjs&logoColor=white" alt="Nuxt 4" />
  <img src="https://img.shields.io/badge/Vue-3.5-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue 3" />
  <img src="https://img.shields.io/badge/MongoDB-Async%20Motor-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/Firebase-Admin%20SDK-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" alt="Firebase" />
  <img src="https://img.shields.io/badge/Docker-Production%20Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="CI/CD" />
</p>

---

## 🏛️ 1. ¿Qué es Hermes?

**Hermes** es un ecosistema digital de alta gama diseñado como centro de comando unificado para desarrolladores, ingenieros y profesionales técnicos. Centraliza en una sola experiencia fluida:

1. **Productividad Diaria & Ágil**: Tableros Kanban interactivos, matriz de consolidación de hábitos (método 21 días) y notas adhesivas.
2. **Control Financiero**: Monitoreo de balance neto, comparativas mensuales (*Month-over-Month*), desglose por categorías y metas de ahorro.
3. **Servicios Cloud (Google Workspace)**: Integración bidireccional en tiempo real con **Google Calendar API v3**, **Gmail API** y **Google Drive API**.
4. **Listas & Tareas**: Lista de deseos (*Wishlist*) con fotos en la nube y lista de tareas rutinarias estilo Microsoft To-Do con puntuaciones de esfuerzo.
5. **Progreso Profesional & Bóveda de Conocimiento**: Árboles de aprendizaje interactivos con editor Markdown, gestor de hitos macro con cuentas regresivas en vivo y bóveda Zettelkasten interconectada con grafo 2D de fuerzas.

Todo el ecosistema está construido bajo una estética **Dark-Neon Glassmorphism** (obsidiana oscura, orbes ambientales, partículas interactivas de constelación neón y micro-animaciones).

---

## 🏗️ 2. Arquitectura del Sistema

El proyecto está estructurado como un monorepo modular de 3 capas principales:

```
                                    ┌─────────────────────────────────────────┐
                                    │        USUARIO / NAVEGADOR WEB          │
                                    └────────────────────┬────────────────────┘
                                                         │
                                    ┌────────────────────▼────────────────────┐
                                    │    FRONTEND: hermes-platform (Nuxt 4)   │
                                    │  - Vue 3 + TypeScript + SSR/Nitro       │
                                    │  - HTML5 Canvas Particles + Glassmorphism│
                                    │  - Puerto Host: 3003                    │
                                    └────────────────────┬────────────────────┘
                                                         │ REST API (JSON / JWT)
                                    ┌────────────────────▼────────────────────┐
                                    │      BACKEND: hermes-api (FastAPI)      │
                                    │  - Python 3.11+ / Async / Uvicorn       │
                                    │  - Modelos Pydantic v2 (Request/Response)│
                                    │  - Cifrado Fernet de Tokens OAuth       │
                                    │  - Puerto Host: 9003                    │
                                    └────────┬───────────┬───────────┬────────┘
                                             │           │           │
                    ┌────────────────────────┘           │           └────────────────────────┐
                    ▼                                    ▼                                    ▼
       ┌─────────────────────────┐         ┌───────────────────────────┐        ┌─────────────────────────┐
       │   BASE DE DATOS (NoSQL) │         │     FIREBASE AUTH (SDK)   │        │     GOOGLE APIS (v3)    │
       │   MongoDB (Motor Async) │         │  - Validación de ID Token │        │  - Google Calendar      │
       │  - 14 Colecciones       │         │  - Gestión de Identidad   │        │  - Google Drive Bucket  │
       │  - Bitácoras Inmutables │         └───────────────────────────┘        │  - Gmail                │
       └─────────────────────────┘                                              └─────────────────────────┘
```

---

## 📂 3. Estructura del Repositorio

```
Hermes/
├── hermes-platform/                  # Frontend en Nuxt 4 (Vue 3, TypeScript, SSR)
│   ├── app/
│   │   ├── assets/css/main.css       # Variables globales, temas neón y animaciones
│   │   ├── components/               # Átomos, moléculas y organismos modulares
│   │   ├── composables/              # useAuth, useCalendarService, useFinance, useBoards...
│   │   ├── layouts/                  # default.vue (Sidebar, fondo de partículas)
│   │   ├── pages/                    # /, /services, /finance, /boards, /lists, /progress, /login
│   │   └── templates/                # AuthTemplate.vue
│   ├── public/                       # Logo oficial, favicon e iconos
│   ├── Dockerfile                    # Multi-stage build Node 22 Alpine (SSR)
│   └── nuxt.config.ts                # Configuración de módulos, SEO y fuentes
│
├── hermes-api/                       # Backend en FastAPI (Python 3.11+)
│   ├── assets/requirements.txt       # Dependencias de Python
│   ├── src/
│   │   ├── app/
│   │   │   ├── endpoints/            # auth.py, services.py, finance.py, boards.py, lists.py, progress.py
│   │   │   └── main.py               # Instancia FastAPI, CORS, middlewares y routers
│   │   ├── models/
│   │   │   ├── request/              # Schemas Pydantic de entrada
│   │   │   └── response/             # Schemas Pydantic de salida
│   │   ├── services/                 # firebase, calendar, gmail, drive, finance, boards, lists, progress, audit
│   │   └── utils/                    # Criptografía Fernet, helpers de fecha y MongoDB
│   └── Dockerfile                    # Base python:3.11-slim
│
├── hermes-spec/                      # Especificaciones técnicas y funcionales de cada módulo
│   ├── 00_deploy/SPEC_DEPLOY.md      # Pipeline CI/CD y despliegue
│   ├── 01_auth/SPEC_AUTH.md          # Autenticación y Scopes de Google
│   ├── 02_barmenu/SPEC_BARMENU.md    # Sidebar retráctil y fijo
│   ├── 04_services/SPEC_SERVICES.md  # Gmail, Drive y Google Calendar
│   ├── 05_economy/SPEC_ECONOMY.md    # Administración económica
│   ├── 06_tablero/SPEC_TABLERO.md    # Kanban, Hábitos y Post-its
│   ├── 07_LISTAS/SPEC_LISTS.md       # Wishlist y Microsoft To-Do
│   └── 08_profesional/SPEC_PROFETIONAL.md # Roadmap Canvas, Hitos y Zettelkasten
│
├── .github/workflows/main.yml        # CI/CD Pipeline automático para la rama main
├── docker-compose.yml                # Orquestación de servicios en hermes-network
└── AGENTS.md                         # Memoria contextual y directrices de desarrollo
```

---

## 🚀 4. Módulos del Sistema en Detalle

### 0. 🎛️ Centro de Control Bento Dashboard (`/`)
* **Hero Header**: Saludo dinámico, fecha actual, estado de conexión de Google y botón de sincronización concurrente.
* **Barra Quick Launcher**: Accesos rápidos de 1 clic para crear eventos, registrar gastos, añadir tareas o redactar apuntes.
* **Bento Grid**: 5 tarjetas modulares interactivas con métricas en tiempo real de finanzas, agenda de Google Calendar, foco diario, hitos críticos y tareas pendientes.
* **Partículas Reactivas (`HermesParticles`)**: Red de constelación en Canvas HTML5 con atracción y repulsión elástica ante el cursor.

---

### 1. 🔐 Autenticación & Seguridad (`/login`, `/api/v1/auth/*`)
* **Google OAuth 2.0 mediante Firebase**:
  - Scopes solicitados: `https://www.googleapis.com/auth/drive`, `https://www.googleapis.com/auth/calendar`, `https://www.googleapis.com/auth/gmail.modify`.
* **Cifrado de Tokens**: Los tokens de Google (`access_token`, `refresh_token`) se almacenan cifrados con **Fernet** en MongoDB.
* **Sesión JWT**: Emisión de JWT propio para autorización en cabeceras `Authorization: Bearer <token>`.
* **Endpoints**:
  - `POST /api/v1/auth/login`: Validación de Firebase ID Token, creación/actualización de usuario y cifrado de credenciales.
  - `GET /api/v1/auth/me`: Perfil del usuario autenticado.

---

### 2. 🌐 Administrador de Servicios (`/services`, `/api/v1/services/*`)
* **Google Calendar en Tiempo Real**:
  - Cuadrícula mensual fija (`92px` inmutables por día), vista de agenda cronológica y creación por lenguaje natural (*QuickAdd*).
  - Modal de programación completa con soporte para eventos de todo el día, ubicación y paleta de colores de Google Calendar.
  - Endpoints: `GET /calendar/events`, `POST /calendar/events`, `GET /calendar/events/{id}`, `PUT /calendar/events/{id}`, `DELETE /calendar/events/{id}`, `POST /calendar/quick-add`.
* **Gmail**:
  - Consulta de correos destacados (`is:starred`) e importantes (`is:important`).
  - Lector de mensajes y envío a la papelera.
  - Endpoints: `GET /gmail/emails`, `GET /gmail/emails/{id}`, `POST /gmail/emails/{id}/trash`.
* **Google Drive Bucket**:
  - Bucket raíz `hermes` con carpetas para `multimedia`, `archivos` y `whitelist`.
  - Subida multipart, navegación por carpetas y visor previo.
  - Endpoints: `GET /drive/files`, `POST /drive/upload`, `GET /drive/preview/{id}`, `DELETE /drive/files/{id}`.
* **Auditoría Inmutable**: Colección `service_audit_logs` que registra cada operación en servicios externos.

---

### 3. 💰 Administración Económica (`/finance`, `/api/v1/finance/*`)
* **Métricas Financieras**: Balance neto, ingresos totales, gastos totales y tasa de ahorro porcentual.
* **Comparativas MoM**: Diferencial nominal y porcentual contra el mes anterior.
* **Visualizaciones**: Desglose por categorías (SVG Donut Chart) y tendencias semestrales (Bar Chart).
* **Gestión de Transacciones & Categorías**: CRUD con paginación, filtros por tipo/categoría y búsqueda instantánea.
* **Endpoints**: `GET /summary`, `GET /transactions`, `POST /transactions`, `PUT /transactions/{id}`, `DELETE /transactions/{id}`, `GET /categories`, `POST /categories`, `PUT /categories/{id}`, `DELETE /categories/{id}`.

---

### 4. 📋 Tableros Inteligentes (`/boards`, `/api/v1/boards/*`)
* **Tablero Kanban de Actividades**:
  - 4 columnas (`ToDo`, `In Progress`, `Testing`, `Done`) con Drag & Drop nativo y persistencia inmediata.
  - Vistas: Tablero Activo, Backlog y Finalizados (+7 días).
  - Tipos (`Mejora`, `Urgente`, `Pendiente`, `Análisis`), Complejidad (`XS` a `XL`) y Épicas.
* **Tablero de Hábitos (21 Días)**:
  - Matriz interactiva de 21 casillas por hábito, cálculo de racha (`streak`) y porcentaje de consolidación.
* **Pizarrón de Ideas**:
  - Canvas infinito con Post-its flotantes reposicionables libremente (coordenadas X/Y) con colores neón.
* **Endpoints**: 18 endpoints REST bajo `/api/v1/boards/*` para tareas, épicas, hábitos y notas adhesivas.

---

### 5. 🎁 Listas & Deseos (`/lists`, `/api/v1/lists/*`)
* **Lista de Deseos (Wishlist)**:
  - Catálogo de compras futuras con nombre, precio, prioridad (`Alta`, `Media`, `Baja`) y enlace de compra.
  - Subida de fotografías persistidas directamente en Google Drive bajo la carpeta `hermes/whitelist`.
  - KPIs monetarios con total acumulado y conteo de artículos pendientes/comprados.
* **Lista de Tareas Diarias (Estilo Microsoft To-Do)**:
  - Organización por secciones temáticas, puntajes de dificultad (1, 2, 3, 5 pts) y frecuencias de repetición.
* **Endpoints**: 15 endpoints REST bajo `/api/v1/lists/*` para wishlist y tareas to-do.

---

### 6. 🧠 Progreso Profesional & Conocimiento (`/progress`, `/api/v1/progress/*`)
* **Árbol de Mapas (Roadmap Canvas)**:
  - Grafo infinito con nodos conectados por flechas vectoriales SVG y editor/visor Markdown integrado para apuntes técnicos de cada módulo.
* **Gestor de Hitos (Milestones Tracker)**:
  - Rastreador visual de proyectos macro (Titulación, Certificaciones Cloud AWS, Exámenes) con cuenta regresiva en vivo (*deadlines*) y barras ponderadas por temario.
* **Bóveda Zettelkasten (Knowledge Vault & Graph)**:
  - Bóveda de notas Markdown interconectadas con wikilinks `[[NombreDeNota]]` y tags `#etiqueta`.
  - Grafo interactivo 2D con física de fuerzas y enlaces bidireccionales automáticos (*backlinks*).
* **Endpoints**: 15 endpoints REST bajo `/api/v1/progress/*` para roadmaps, hitos y notas Zettelkasten.

---

## 🗄️ 5. Esquema de Base de Datos (MongoDB)

| Colección | Descripción |
| :--- | :--- |
| `users` | Información del usuario, metadatos y tokens de Google cifrados con Fernet. |
| `finance_transactions` | Registro de ingresos y gastos con monto, fecha, categoría y notas. |
| `finance_categories` | Categorías de finanzas personalizadas (ingresos/gastos) con iconos y colores. |
| `board_epics` | Épicas de agrupación de tareas Kanban (`Escuela`, `Trabajo`, `Cursos`). |
| `board_tasks` | Tareas del Kanban con estado, columna, complejidad, tipo y ubicación. |
| `board_habits` | Hábitos con matriz de 21 casillas, racha actual y porcentaje de éxito. |
| `board_sticky_notes` | Post-its del canvas de ideas con posición `(x, y)`, color y contenido. |
| `wishlist_items` | Artículos deseados con precio, prioridad, link y referencias a fotos en Google Drive. |
| `todo_sections` | Secciones temáticas para la lista de tareas rutinarias. |
| `todo_tasks` | Tareas rutinarias con puntaje de dificultad y recurrencia. |
| `progress_roadmaps` | Mapas de ruta de aprendizaje con nodos, aristas y documentos Markdown asociados. |
| `progress_milestones` | Metas a gran escala con temarios ponderados, fechas límite y estado. |
| `progress_notes` | Notas de la bóveda Zettelkasten con contenido Markdown, wikilinks y tags. |
| `service_audit_logs` | Bitácora inmutable de operaciones ejecutadas contra Google Workspace APIs. |

---

## ⚙️ 6. Configuración de Variables de Entorno

### Frontend (`hermes-platform/.env`)
```env
# API Backend
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Firebase Authentication
NUXT_PUBLIC_FIREBASE_API_KEY=tu_api_key
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=tu_proyecto.firebaseapp.com
NUXT_PUBLIC_FIREBASE_PROJECT_ID=tu_proyecto_id
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET=tu_proyecto.appspot.com
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=tu_sender_id
NUXT_PUBLIC_FIREBASE_APP_ID=tu_app_id
```

### Backend (`hermes-api/.env`)
```env
# Servidor FastAPI
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:3003

# Base de Datos MongoDB
MONGO_HOST=mongodb://localhost:27017
MONGO_DATABASE=hermes_db

# Firebase Admin SDK
FIREBASE_CREDENTIALS_PATH=/ruta/a/serviceAccountKey.json

# Criptografía y JWT
ENCRYPTION_KEY=tu_clave_fernet_generada_en_base64
JWT_SECRET_KEY=tu_clave_secreta_jwt
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=43200
```

---

## 🛠️ 7. Instalación y Ejecución Local

### Prerrequisitos
* Node.js 20+ y npm
* Python 3.11+
* MongoDB en ejecución local o en contenedor

### 1. Iniciar el Backend (`hermes-api`)
```bash
cd hermes-api
python3 -m venv venv
source venv/bin/activate
pip install -r assets/requirements.txt
uvicorn src.app.main:app --reload --port 8000
```
*Documentación interactiva Swagger disponible en:* `http://localhost:8000/docs`

### 2. Iniciar el Frontend (`hermes-platform`)
```bash
cd hermes-platform
npm install
npm run dev
```
*Aplicación web disponible en:* `http://localhost:3000`

---

## 🐳 8. Despliegue con Docker & CI/CD Pipeline

El repositorio incluye automatización completa mediante **GitHub Actions** y **Docker Compose**:

* **Pipeline Automático** (`.github/workflows/main.yml`):
  1. Se ejecuta exclusivamente al hacer `push` a la rama `main`.
  2. Corre sobre un **Self-Hosted Runner** en el servidor de producción.
  3. Fase 1: Validación de entorno Docker y dependencias.
  4. Fase 2: Inyección segura de variables (`~/.env.hermesapi` y `~/.env.hermesplatform`), construcción de imágenes y levantamiento de contenedores (`docker compose up -d --build`).

* **Puertos Expuestos en Host**:
  - Frontend (`hermes-platform`): **Puerto 3003** (`3003:3000`)
  - Backend (`hermes-api`): **Puerto 9003** (`9003:8000`)

---

<p align="center">
  <b>Hermes Ecosystem</b> — Diseñado y construido con excelencia técnica para dominar la productividad y el conocimiento.
</p>