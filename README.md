<p align="center">
  <img src="./public/logo.png" alt="Hermes Platform Logo" width="120" height="120" style="border-radius: 24px; box-shadow: 0 0 35px rgba(0, 229, 255, 0.4);" />
</p>

<h1 align="center">Hermes Platform (Frontend)</h1>

<p align="center">
  <b>Plataforma integral de productividad, finanzas, servicios cloud y gestión del conocimiento.</b><br>
  Desarrollada con <b>Nuxt 4</b>, <b>Vue 3</b>, <b>TypeScript</b> y una estética <b>Dark-Neon Glassmorphism</b> ultra-premium.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Nuxt-4.5.2-00DC82?style=for-the-badge&logo=nuxtdotjs&logoColor=white" alt="Nuxt 4" />
  <img src="https://img.shields.io/badge/Vue-3.5-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue 3" />
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
</p>

---

## 🏛️ ¿Qué es Hermes?

**Hermes** es un ecosistema digital y centro de comando personal diseñado para ingenieros, desarrolladores y profesionales que buscan centralizar en un solo lugar sus responsabilidades técnicas, proyectos a gran escala, salud financiera, rutinas de hábitos y bóveda de apuntes.

Inspirado en el dinamismo, la velocidad y la comunicación del mensajero de los dioses, **Hermes** fusiona herramientas de productividad ágil con integraciones directas a servicios de **Google Cloud (Gmail, Drive y Google Calendar)**, respaldado por un diseño visual inmersivo con temática **Dark-Neon**, orbes ambientales dinámicos y un sistema de partículas reactivas.

---

## 🎨 Sistema de Diseño Visual

La interfaz está construida sobre una paleta cromática calibrada y componentes desacoplados:

* **Fondos Base**: Obsidiana oscura (`#0c0c0e`) y Superficie elevada (`#17171c`).
* **Acentos Neón**:
  - **Azul Cian (`#00E5FF`)**: Identidad principal, navegación y eventos.
  - **Rosa Magenta (`#FF007F`)**: Alertas, tareas urgentes y botones de acción.
  - **Verde Teal (`#00FFC6`)**: Finanzas, estados activos y confirmaciones.
* **Efectos Visuales**:
  - **Partículas Interactivas (`HermesParticles`)**: Red de constelación sobre Canvas HTML5 con atracción y repulsión elástica ante el cursor.
  - **Glassmorphism**: Paneles traslúcidos con `backdrop-filter: blur(12px)`.
  - **Transiciones de Página**: Movimiento fluido con curvas Bézier cúbicas (`cubic-bezier(0.16, 1, 0.3, 1)`).

---

## 🚀 Módulos y Funcionalidades Implementadas

```
Hermes Platform
├── 0. Centro de Control Bento Dashboard (/)
├── 1. Administrador de Servicios (/services)
│   ├── Gmail (Correos Destacados e Importantes)
│   ├── Multimedia & Drive Bucket (Archivos Cloud)
│   └── Google Calendar en Tiempo Real (Agenda y QuickAdd)
├── 2. Administración Económica (/finance)
│   ├── KPIs de Balance Neto, Ingresos y Gastos
│   ├── Comparativas Mensuales (MoM) y Tasa de Ahorro
│   └── Desglose por Categorías y Tendencias Semestrales
├── 3. Tableros Inteligentes (/boards)
│   ├── Tablero Kanban (ToDo, In Progress, Testing, Done)
│   ├── Tablero de Hábitos (Método de los 21 Días)
│   └── Pizarrón de Ideas (Post-its Neón Posicionables)
├── 4. Listas & Deseos (/lists)
│   ├── Lista de Deseos (Wishlist con fotos en Drive)
│   └── Lista de Tareas (Estilo Microsoft To-Do con dificultad)
└── 5. Progreso Profesional & Conocimiento (/progress)
    ├── Árbol de Mapas (Roadmap Canvas con Markdown)
    ├── Gestor de Hitos (Milestones con Deadlines y Progreso)
    └── Bóveda Zettelkasten (Wikilinks [[Nota]] y Grafo 2D)
```

---

### 0. 🎛️ Centro de Control Bento Dashboard (`/`)
* **Header Hero de Comando**: Saludo personalizado, fecha en tiempo real, estado de conectividad con Google y botón de sincronización concurrente.
* **Barra de Lanzador Rápido (*Quick Launcher*)**: Accesos directos de 1 clic para programar eventos, registrar gastos, crear tareas Kanban o redactar notas Zettelkasten.
* **Bento Grid en Tiempo Real**: Tarjetas modulares interactuando en vivo con los datos de finanzas, próximos eventos de calendario, tareas prioritarias, racha de hábitos, cuenta regresiva de hitos y lista de pendientes.

---

### 1. 🌐 Administrador de Servicios (`/services`)
* **Google Calendar API v3**:
  - **Cuadrícula Mensual Fija**: Navegación por meses con vista de eventos sin deformación de celdas.
  - **Vista Agenda Cronológica**: Listado cronológico de eventos programados.
  - **Creación por Lenguaje Natural (*QuickAdd*)**: Creación ágil interpretando texto (ej. *"Reunión mañana a las 4pm"*).
  - **Modal de Edición Completa**: Configuración de fecha/hora, selector "Todo el día", ubicación, descripción y selector de paleta de colores nativa de Google Calendar.
* **Gmail API**:
  - Consulta de correos destacados (`is:starred`) e importantes (`is:important`).
  - Lector de correos en formato modal y envío a la papelera.
* **Google Drive Bucket**:
  - Bucket raíz `hermes` con carpetas dedicadas (`multimedia`, `archivos`, `whitelist`).
  - Subida multipart, visualización previa y explorador de archivos.
* **Auditoría Inmutable**: Registro de cada acción en la colección `service_audit_logs` de MongoDB.

---

### 2. 💰 Administración Económica (`/finance`)
* **Balance & Ahorro**: Métricas de ingresos totales, gastos totales, balance neto y porcentaje de tasa de ahorro mensual.
* **Análisis MoM (Month-over-Month)**: Comparativa porcentual y nominal contra el mes anterior.
* **Gráficos Dinámicos**:
  - Desglose porcentual por categorías (SVG Donut Chart interactivo).
  - Tendencias históricas semestrales (Bar Chart).
* **Gestión de Transacciones**: CRUD completo de ingresos/gastos con paginación, filtros por categoría y búsqueda en tiempo real.
* **Administrador de Categorías**: Creación de categorías con selector de iconos y colores neón.

---

### 3. 📋 Tableros Inteligentes (`/boards`)
* **Tablero Kanban de Actividades**:
  - 4 columnas de flujo de trabajo: `ToDo`, `In Progress`, `To Be Tested` y `Done`.
  - **Drag & Drop Nativo** con persistencia instantánea.
  - Sub-vistas: *Tablero Activo*, *Backlog* y *Finalizados* (+7 días).
  - Tipos de tarea: `Mejora` (Verde), `Urgente` (Rosa), `Pendiente` (Amarillo), `Análisis` (Azul).
  - Complejidades (`XS`, `S`, `M`, `L`, `XL`) y filtrado por Épicas (`Escuela`, `Trabajo`, `Cursos`).
* **Tablero de Hábitos (21 Días)**:
  - Matriz interactiva de 21 casillas por hábito.
  - Contador de racha activa (`streak`) y porcentaje de consolidación.
* **Pizarrón de Ideas**:
  - Canvas interactivo con Post-its flotantes arrastrables a cualquier coordenada X/Y.
  - Edición en tiempo real y selector de colores neón.

---

### 4. 🎁 Listas & Deseos (`/lists`)
* **Lista de Deseos (Wishlist)**:
  - Catálogo de compras futuras con nombre, precio, prioridad (`Alta`, `Media`, `Baja`) y enlace de compra externo.
  - Subida de fotografías persistidas directamente en Google Drive bajo la carpeta `hermes/whitelist`.
  - KPIs monetarios con total acumulado y conteo de artículos pendientes/adquiridos.
* **Lista de Tareas Diarias (Estilo Microsoft To-Do)**:
  - Organización por secciones temáticas personalizables.
  - Puntaje de dificultad/esfuerzo (1, 2, 3, 5 puntos) y frecuencias de repetición.
  - Checkbox de marcado rápido.

---

### 5. 🧠 Progreso Profesional & Conocimiento (`/progress`)
* **Árbol de Mapas (Roadmap Canvas)**:
  - Grafo infinito con nodos interconectados mediante flechas vectoriales SVG.
  - Al hacer clic en cualquier módulo, se abre un **Editor y Visor Markdown (`.md`)** integrado para documentar notas técnicas y bitácoras de aprendizaje.
* **Gestor de Hitos (Milestones Tracker)**:
  - Rastreador visual de proyectos macro (Titulación, Certificaciones Cloud AWS, Exámenes de materias críticas).
  - Cuentas regresivas (*deadlines*) en vivo y barras de progreso ponderadas por porcentaje de temarios completados.
* **Bóveda Zettelkasten (Knowledge Vault & Graph)**:
  - Notas atómicas interconectadas con sintaxis de enlaces wiki `[[NombreDeNota]]` y etiquetas `#tema`.
  - **Grafo de Conocimiento 2D Interactivo** con simulación física de fuerzas y enlaces bidireccionales automáticos (*backlinks*).

---

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Framework Web** | [Nuxt 4](https://nuxt.com/) (Vue 3) | Arquitectura SSR/SPA moderna, enrutamiento y composición reactiva. |
| **Lenguaje** | TypeScript 5 | Tipado estricto en composables, modelos y componentes. |
| **Estilos** | Vanilla CSS + Bootstrap 5 (Grid/Utils) | Variables CSS en `:root`, micro-animaciones y glassmorphism personalizado. |
| **Gráficos & Canvas** | HTML5 Canvas + SVG | Partículas interactivas y visualización de grafos Zettelkasten. |
| **Markdown** | Visor / Editor Markdown reactivo | Bitácoras en Roadmap Canvas y notas Zettelkasten. |
| **Autenticación** | Firebase Auth + Google OAuth 2.0 | Inicio de sesión unificado con scopes de Google APIs. |

---

## 📦 Estructura del Proyecto Frontend

```
hermes-platform/
├── app/
│   ├── assets/
│   │   └── css/
│   │       └── main.css              # Variables globales, animaciones y temas neón
│   ├── components/
│   │   ├── atoms/                    # HermesLogo, HermesParticles, badges, botones neón
│   │   ├── molecules/                # Tarjetas de eventos, KPIs Bento, filas de tareas
│   │   └── organisms/                # Secciones Kanban, Calendario, Finanzas, Zettelkasten
│   ├── composables/                  # useAuth, useCalendarService, useFinance, useBoards...
│   ├── layouts/
│   │   └── default.vue               # Layout principal con Sidebar retráctil y partículas
│   ├── pages/
│   │   ├── index.vue                 # Centro de Control Bento Dashboard
│   │   ├── services.vue              # Gmail, Drive y Google Calendar
│   │   ├── finance.vue               # Administración Económica
│   │   ├── boards.vue                # Tableros Kanban, Hábitos y Post-its
│   │   ├── lists.vue                 # Wishlist y Microsoft To-Do
│   │   ├── progress.vue              # Roadmap Canvas, Hitos y Zettelkasten
│   │   └── login.vue                 # Pantalla de acceso con Google
│   └── templates/
│       └── AuthTemplate.vue          # Contenedor de autenticación con halo neón
├── public/                           # Logo oficial, favicon e iconos
├── nuxt.config.ts                    # Configuración de Nuxt 4, SSR, metadatos y fuentes
└── package.json                      # Dependencias del proyecto
```

---

## ⚙️ Configuración y Variables de Entorno

Crea un archivo `.env` en la raíz de `hermes-platform/`:

```env
# URL de la API Backend (FastAPI)
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Configuración de Firebase Authentication
NUXT_PUBLIC_FIREBASE_API_KEY=tu_firebase_api_key
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=tu_proyecto.firebaseapp.com
NUXT_PUBLIC_FIREBASE_PROJECT_ID=tu_proyecto_id
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET=tu_proyecto.appspot.com
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=tu_sender_id
NUXT_PUBLIC_FIREBASE_APP_ID=tu_app_id
```

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
npm install
```

### 2. Iniciar servidor de desarrollo
```bash
npm run dev
```
La aplicación estará disponible en `http://localhost:3000`.

### 3. Compilar para producción
```bash
npm run build
```

### 4. Previsualizar la compilación de producción
```bash
node .output/server/index.mjs
```

---

## 🛡️ Despliegue con Docker y CI/CD

Hermes cuenta con un pipeline de integración y despliegue continuo mediante **GitHub Actions** en servidor Self-Hosted:

* **Contenedor Frontend**: Expuesto en el puerto host `3003` (`3003:3000`).
* **Contenedor Backend**: Expuesto en el puerto host `9003` (`9003:8000`).
* **Orquestación**: Docker Compose dentro de la red privada `hermes-network`.

---

<p align="center">
  <b>Hermes Platform</b> — Construido con pasión para potenciar la productividad y el conocimiento técnico.
</p>