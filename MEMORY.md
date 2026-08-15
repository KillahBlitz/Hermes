# Hermes Project - Memory Bank (MEMORY.md)

Para detalles y directrices completas de desarrollo, consulta [AGENTS.md](file:///Users/jmonroy/Documents/MyProjects/Hermes/AGENTS.md) y las especificaciones en [SPEC_AUTH.md](file:///Users/jmonroy/Documents/MyProjects/Hermes/hermes-spec/01_auth/SPEC_AUTH.md).

## Resumen Rápido de Contexto
* **Frontend**: Nuxt 4 (`hermes-platform`), dark mode con acentos neón en Azul (`#00E5FF`) y Rosa (`#FF007F`), estructurado en componentes, páginas (`app/pages`) y templates (`app/templates`).
* **Backend**: FastAPI (`hermes-api`), separación estricta con Pydantic (`models/request` y `models/response`), endpoints en `app/endpoints/auth.py` y servicios en `services/firebase_service.py`.
* **Autenticación**: Firebase Auth con Google Sign-In pidiendo scopes de Drive (`.../auth/drive`), Calendar (`.../auth/calendar`) y Gmail (`.../auth/gmail.modify`).
* **Navegación (BarMenu)**: Menú lateral dual (Fijo a 260px vs Colapsado a 72px) con 6 módulos: Servicios, Finanzas, Tableros, Listas, Progreso profesional y Conocimiento.
* **Servicios (Feature 4 - IMPLEMENTADO)**: Selector conmutable "Correos" (Gmail: Destacados e Importantes, modal de detalle, confirmación de eliminación con auditoría) y "Multimedia" (Drive Bucket: carpeta `hermes` con subcarpetas `multimedia` y `archivos`, carga de archivos con Drag & Drop y vista previa interactiva de imágenes, videos y documentos).
* **CI/CD & Deploy (Feature 0 - IMPLEMENTADO)**: `.github/workflows/main.yml` activado solo en `main` sobre *Self-Hosted Runner*. Pipeline en 2 pasos: `preparar-deploy` y `deploy-prod`, inyectando `~/.env.hermesapi` y `~/.env.hermesplatform`. Contenedores Docker multi-stage orquestados con `docker compose` en puertos host **9003** (Backend) y **3003** (Frontend).
* **Base de Datos**: MongoDB (`hermes-db`), cifrado de tokens en `user_credentials` y bitácora en `service_audit_logs`.
