# Especificaciones del Proyecto: Hermes

## Feature 1: Login con Google via Firebase (Crear Cuenta y Login)
**Estado:** PENDIENTE

**Descripción:**
Implementar un sistema de autenticación utilizando Google Sign-In mediante Firebase. Es crítico que este módulo quede perfectamente implementado, ya que la plataforma debe garantizar que cada usuario registrado tenga su propia información aislada.

**Requerimientos del Product Manager (Gemini 3.1 Pro):**
1. Definir los flujos de usuario (Éxito, Fallo, Usuario Nuevo).
2. Especificar qué datos exactos del perfil de Google se guardarán.

**Requerimientos del Arquitecto (Claude Opus 4.6):**
1. Diseñar el modelo de datos en MongoDB para enlazar el ID de Firebase de forma segura.
2. Definir la estrategia de validación del token entre el cliente y el servidor.
3. **ACCIÓN REQUERIDA:** Utilizar la skill para pausar el flujo y solicitar al usuario las variables de entorno: Firebase Admin SDK Key y MongoDB URI.

**Requerimientos de Desarrollo:**
1. Backend (Claude Sonnet 4.6 - Python): Implementar la validación del token de Firebase y crear el endpoint de autenticación.
2. Frontend (Claude Sonnet 4.6 - Vue/Nuxt): Crear el componente de UI para el botón de login y gestionar el estado de la sesión del usuario.

**Requerimientos de Testing (Gemini 3.7 Flash):**
1. Escribir pruebas unitarias para la validación del token en el backend.
2. Comprobar que los datos del usuario queden correctamente aislados.
