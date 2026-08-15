# Hermes Project - Feature 08: Módulo de Progreso & Bóveda de Conocimiento (SPEC_PROFETIONAL.md)

Este documento especifica los requerimientos funcionales, técnicos, arquitectónicos y de experiencia de usuario para el módulo **"Progreso"** en Hermes, el cual unifica y sustituye las antiguas secciones de *Progreso profesional* y *Conocimiento*.

---

## 1. Visión General y Propósito

El módulo **Progreso** (`/progress`) es el centro neurálgico de crecimiento profesional, académico y de gestión del conocimiento de largo plazo dentro de Hermes. Proporciona 3 herramientas sinérgicas diseñadas para separar el estudio y los grandes proyectos de las responsabilidades laborales o tareas inmediatas del día a día:

1. **🗺️ Árbol de Mapas (Roadmap Canvas)**: Pizarrón interactivo donde se modelan rutas de aprendizaje, arquitecturas y etapas modulares mediante rectángulos interconectados con flechas. Al pulsar cualquier nodo/módulo, se abre un editor/visor Markdown (`.md`) para documentar avances, bitácoras y apuntes técnicos específicos de ese paso.
2. **🎯 Gestor de Hitos (Milestones Tracker)**: Monitor visual de metas y proyectos de gran escala (ej. titulación de ingeniería, certificaciones cloud como AWS Solutions Architect, periodos críticos de exámenes y temarios académicos). Incluye cuentas regresivas de días restantes (*deadlines*) y barras de progreso porcentual ponderadas por temarios/entregables.
3. **🧠 Red de Enlaces Zettelkasten (Knowledge Vault & Graph)**: Bóveda de notas Markdown interconectadas que escala los apuntes del árbol de mapas mediante la metodología formal Zettelkasten, soportando enlaces bidireccionales (`[[NombreDeNota]]`), etiquetas (`#tags`), backlinks automáticos y un grafo visual interactivo de nodos y conexiones.

---

## 2. Reorganización de Navegación (BarMenu)

* **Unificación**: Se elimina la categoría separada *"Conocimiento"* (`/knowledge`) y se unifica con *"Progreso profesional"* en una sola opción de navegación llamada **"Progreso"** (`/progress`).
* **Nuevo Menú Lateral (5 Módulos Principales)**:
  1. `Administrador de servicios` (`/services`)
  2. `Administración económica` (`/finance`)
  3. `Tableros` (`/boards`)
  4. `Listas` (`/lists`)
  5. `Progreso` (`/progress`)
* **Icono Oficial**: Cohete / Diagrama de red (`progress` / `rocket`).

---

## 3. Especificación Detallada de Herramientas

```
                     ┌─────────────────────────────────────────────────────────┐
                     │              MÓDULO DE PROGRESO (/progress)             │
                     └─────────────────────────────────────────────────────────┘
                                                  │
                 ┌────────────────────────────────┼──────────────────────────────┐
                 ▼                                ▼                              ▼
    ┌─────────────────────────┐      ┌─────────────────────────┐    ┌─────────────────────────┐
    │    ÁRBOL DE MAPAS       │      │     GESTOR DE HITOS     │    │    RED ZETTELKASTEN     │
    │  - Pizarrón de nodos    │      │  - Proyectos Macro      │    │  - Bóveda de notas .md  │
    │  - Conexiones & Flechas │      │  - Cuentas regresivas   │    │  - Wikilinks [[Nota]]   │
    │  - Click -> Apuntes .md │      │  - Progreso por temario │    │  - Grafo 2D interactivo │
    └─────────────────────────┘      └─────────────────────────┘    └─────────────────────────┘
```

---

### 3.1. Herramienta 1: Árbol de Mapas (Roadmap Canvas)

#### Descripción Funcional
Un canvas interactivo infinito/expandible con soporte para arrastre (*pan*), zoom y creación de mapas de ruta (*roadmaps*).
* **Nodos Modulares (Rectángulos)**:
  - Representan pasos o temas de un aprendizaje o proyecto (ej. `01_Fundamentos_Go`, `02_Goroutines_Concurrency`, `03_Microservicios_gRPC`).
  - Personalización: Título, descripción corta, color neón de borde/fondo, icono y estado de avance (`PENDIENTE`, `EN_CURSO`, `DOMINADO`).
  - Posicionamiento libre en coordenadas $(X, Y)$ con arrastre fluido.
* **Conexiones (Aristas / Flechas)**:
  - Flechas direccionales que conectan el nodo de origen con el nodo de destino para indicar prerrequisitos y flujo de ruta.
  - Curvas Bezier dinámicas con color adaptable.
* **Integración con Apuntes Markdown (`.md`)**:
  - Al hacer clic sobre cualquier rectángulo, se abre el panel lateral / modal del documento `.md` asociado al nodo.
  - Permite redactar apuntes técnicos con sintaxis Markdown completa: bloques de código resaltados, listas, tablas y fórmulas.

---

### 3.2. Herramienta 2: Gestor de Hitos (Milestones Tracker)

#### Descripción Funcional
Un tablero visual diseñado específicamente para separar las responsabilidades diarias de los objetivos estratégicos y académicos de mediano/largo plazo.
* **Casos de Uso Principales**:
  1. *Proyecto de Titulación*: Avance por capítulos (Marco teórico, Desarrollo, Pruebas, Conclusiones) con fecha límite de entrega de tesis.
  2. *Certificaciones Técnicas (ej. AWS Certified Solutions Architect)*: Temarios de certificación por dominios (IAM, VPC, EKS, RDS, Cost Optimization) con fecha de examen.
  3. *Evaluaciones Críticas / Exámenes Finales*: Seguimiento de temas de estudio (ej. Probabilidad y Estadística: Distribuciones, Teorema de Bayes, Cadenas de Markov) con cuenta regresiva.
* **Elementos Visuales del Hito**:
  - **Título y Categoría**: `Académico`, `Certificación`, `Carrera Backend`, `Proyecto Personal`.
  - **Cuenta Regresiva (*Countdown*)**: Días, horas y minutos restantes hasta la fecha meta con indicador de alerta si la fecha está próxima (< 7 días en rosa neón `#FF007F`).
  - **Barra de Progreso Ponderada**: Porcentaje global calculado automáticamente a partir de los ítems o capítulos completados del temario.
  - **Checklist de Temario / Entregables**: Lista de tópicos o capítulos con checkbox de completado, dificultad y notas.

---

### 3.3. Herramienta 3: Red de Enlaces Zettelkasten (Knowledge Vault & Graph)

#### Descripción Funcional
Convierte a Hermes en una bóveda centralizada de conocimiento personal (PKM - *Personal Knowledge Management*) implementando los principios de Niklas Luhmann (Zettelkasten):
* **Sintaxis de Enlace Bidireccional (`[[Wikilinks]]`)**:
  - Escribir `[[Título de Otra Nota]]` dentro de cualquier documento `.md` vincula automáticamente ambas notas.
  - Si la nota referenciada no existe, se ofrece crearla con un solo clic.
* **Panel de Backlinks**:
  - Cada nota muestra en el pie de página todas las demás notas de la bóveda que la referencian ("Menciones y Notas Vinculadas").
* **Grafo de Conocimiento Interactivo 2D (*Knowledge Graph View*)**:
  - Visualización en red basada en física de fuerzas (Force-Directed Graph).
  - Nodos = Notas Markdown (tamaño según cantidad de conexiones).
  - Líneas = Enlaces directos entre notas.
  - Filtro por etiquetas (`#golang`, `#aws`, `#database`, `#algoritmos`).
  - Al hacer clic en un nodo del grafo, se abre inmediatamente el editor de esa nota.

---

## 4. Modelo de Datos (MongoDB)

### 4.1. Colección `progress_roadmaps` (Árboles de Mapas)
```json
{
  "_id": "ObjectId(...)",
  "user_id": "firebase_uid_123",
  "title": "Ruta de Especialización en Arquitectura Backend",
  "description": "Roadmap de tecnologías para nivel Senior en sistemas distribuidos",
  "category": "Backend",
  "color": "#00FFC6",
  "nodes": [
    {
      "id": "node_1",
      "title": "Concurrencia y Canales en Go",
      "icon": "⚡",
      "color": "#00E5FF",
      "status": "DOMINADO",
      "x": 120,
      "y": 240,
      "note_id": "ObjectId(note_abc123)"
    },
    {
      "id": "node_2",
      "title": "Patrones de Resiliencia (Circuit Breaker)",
      "icon": "🛡️",
      "color": "#FFD166",
      "status": "EN_CURSO",
      "x": 380,
      "y": 240,
      "note_id": "ObjectId(note_abc124)"
    }
  ],
  "edges": [
    {
      "id": "edge_1_2",
      "source_node_id": "node_1",
      "target_node_id": "node_2",
      "label": "Prerrequisito"
    }
  ],
  "created_at": "ISODate(...)",
  "updated_at": "ISODate(...)"
}
```

---

### 4.2. Colección `progress_milestones` (Gestor de Hitos)
```json
{
  "_id": "ObjectId(...)",
  "user_id": "firebase_uid_123",
  "title": "Certificación AWS Solutions Architect Associate (SAA-C03)",
  "category": "CERTIFICACION",
  "icon": "☁️",
  "color": "#FF9900",
  "target_date": "2026-10-15T09:00:00Z",
  "description": "Preparación teórica, laboratorios prácticos y simuladores de examen de AWS",
  "topics": [
    {
      "id": "top_1",
      "title": "Diseño de Arquitecturas Resilientes (VPC Multi-AZ, ASG, ALB)",
      "is_completed": true,
      "completed_at": "ISODate(...)"
    },
    {
      "id": "top_2",
      "title": "Diseño de Arquitecturas de Alto Rendimiento (EFS, EBS gp3, ElastiCache)",
      "is_completed": false,
      "completed_at": null
    },
    {
      "id": "top_3",
      "title": "Seguridad de Aplicaciones y Datos (KMS, IAM Roles, Secrets Manager)",
      "is_completed": false,
      "completed_at": null
    }
  ],
  "status": "IN_PROGRESS",
  "created_at": "ISODate(...)",
  "updated_at": "ISODate(...)"
}
```

---

### 4.3. Colección `progress_notes` (Bóveda Zettelkasten)
```json
{
  "_id": "ObjectId(...)",
  "user_id": "firebase_uid_123",
  "title": "Patrón Circuit Breaker en Go",
  "slug": "patron-circuit-breaker-en-go",
  "content_md": "# Circuit Breaker\n\nEl patrón Circuit Breaker previene fallas en cascada en microservicios...\n\nRelacionado con: [[Concurrencia y Canales en Go]] y [[Sistemas Distribuidos]].\n\n#golang #microservicios #resiliencia",
  "tags": ["golang", "microservicios", "resiliencia"],
  "outgoing_links": ["Concurrencia y Canales en Go", "Sistemas Distribuidos"],
  "roadmap_node_id": "node_2",
  "created_at": "ISODate(...)",
  "updated_at": "ISODate(...)"
}
```

---

## 5. Endpoints REST (`hermes-api`)

Todos los endpoints requieren autenticación con JWT Bearer Token (`Authorization: Bearer <session_token>`).

### 5.1. Árbol de Mapas (`/api/v1/progress/roadmaps`)
* `GET /api/v1/progress/roadmaps`: Lista todos los árboles de mapas del usuario.
* `POST /api/v1/progress/roadmaps`: Crea un nuevo mapa.
* `GET /api/v1/progress/roadmaps/{id}`: Obtiene el detalle completo del mapa con nodos y aristas.
* `PUT /api/v1/progress/roadmaps/{id}`: Actualiza la estructura del mapa (título, nodos, posiciones, aristas).
* `DELETE /api/v1/progress/roadmaps/{id}`: Elimina un mapa de ruta.

### 5.2. Gestor de Hitos (`/api/v1/progress/milestones`)
* `GET /api/v1/progress/milestones`: Lista todos los hitos con cálculo de porcentaje de avance y días restantes.
* `POST /api/v1/progress/milestones`: Registra un nuevo hito con fecha meta y temario.
* `PUT /api/v1/progress/milestones/{id}`: Modifica datos o temario del hito.
* `PATCH /api/v1/progress/milestones/{id}/topics/{topic_id}/toggle`: Conmuta el estado de completado de un tema del checklist.
* `DELETE /api/v1/progress/milestones/{id}`: Elimina un hito.

### 5.3. Bóveda Zettelkasten & Notas (`/api/v1/progress/notes`)
* `GET /api/v1/progress/notes`: Lista todas las notas con búsqueda por título, contenido o etiqueta `#tag`.
* `POST /api/v1/progress/notes`: Crea una nota Markdown (extrayendo automáticamente wikilinks `[[...]]` y `#tags`).
* `GET /api/v1/progress/notes/{id}`: Obtiene el contenido de la nota junto con la lista de **backlinks** entrantes.
* `PUT /api/v1/progress/notes/{id}`: Actualiza contenido Markdown y reindexa conexiones.
* `DELETE /api/v1/progress/notes/{id}`: Elimina una nota.
* `GET /api/v1/progress/graph`: Genera la estructura de nodos y aristas de toda la bóveda Zettelkasten para renderizar el grafo de conocimiento interactivo.

---

## 6. Diseño UI / UX en Frontend (`hermes-platform`)

### 6.1. Estética Visual
* **Paleta Oficial**:
  - Azul Neón (`#00E5FF`) para conexiones de mapa y títulos Zettelkasten.
  - Verde Neón (`#00FFC6`) para temas dominados y estados completados.
  - Rosa Neón (`#FF007F`) para alertas de hitos cercanos a vencer (< 7 días).
  - Fondo `var(--hermes-bg-surface)` (`#17171c`) con efecto glassmorphism.
* **Componentes Clave**:
  - `RoadmapCanvas.vue`: Pizarrón con nodos arrastrables y renderizado SVG de flechas dinámicas.
  - `MarkdownNoteModal.vue`: Editor con vista dual (Editor / Preview enriquecido con resaltado de sintaxis `Prism/Highlight.js` y enlaces bidireccionales clickeables).
  - `MilestoneCard.vue`: Tarjeta con countdown en vivo, medidor de porcentaje circular y checklist desplegable.
  - `ZettelkastenGraphView.vue`: Canvas interactivo con simulación de fuerzas para explorar la red de notas interconectadas.

---

## 7. Criterios de Aceptación

1. **Unificación de Navegación**: El menú lateral tiene 5 módulos principales (`Servicios`, `Finanzas`, `Tableros`, `Listas`, `Progreso`) y la ruta `/progress` carga correctamente.
2. **Pizarrón de Mapas**: Se pueden crear nodos, arrastrarlos libremente por el canvas, trazar conexiones entre ellos y al hacer clic en un nodo abrir su nota Markdown correspondiente.
3. **Gestor de Hitos**: Permite fijar fechas límite con cálculo automático de cuenta regresiva (días restantes) y actualización en tiempo real de la barra de porcentaje al marcar temas completados.
4. **Zettelkasten**: Las notas soportan enlaces del tipo `[[Nombre de otra nota]]`, generan backlinks automáticamente y se visualizan en el grafo 2D de conocimiento interactivo.
