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
* **6 Módulos Obligatorios**:
  1. `Administrador de servicios` (`/services`)
  2. `Administración económica` (`/finance`)
  3. `Tableros` (`/boards`)
  4. `Listas` (`/lists`)
  5. `Progreso profesional` (`/career`)
  6. `Conocimiento` (`/knowledge`)
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
