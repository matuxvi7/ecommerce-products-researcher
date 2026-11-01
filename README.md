# Sistema de Inteligencia y Selección de Productos para E-Commerce

## 1. Objetivo

Desarrollar una aplicación local que automatice el descubrimiento, investigación, evaluación y validación de productos potencialmente rentables para e-commerce.

El sistema debe reducir la investigación manual, centralizar evidencia y facilitar decisiones basadas en datos.

## 2. Alcance funcional

### Módulo 1 — Discovery Engine
- Identificar productos potenciales en distintas fuentes.
- Recopilar candidatos automáticamente.
- Normalizar nombres, categorías y características.
- Detectar y eliminar duplicados.

### Módulo 2 — Evidence Collector
- Recopilar anuncios de Meta Ads Library.
- Investigar precios internacionales y locales.
- Identificar competidores.
- Obtener información de proveedores.
- Registrar tendencias y señales de demanda.
- Almacenar fuente, fecha y evidencia de cada dato.

### Módulo 3 — Evaluation Engine
- Aplicar los 3 filtros eliminatorios.
- Evaluar los 7 criterios complementarios.
- Calcular puntuaciones automáticamente.
- Identificar motivos de rechazo.
- Permitir configurar los criterios y umbrales.

### Módulo 4 — Financial Engine
- Calcular Landed Cost.
- Calcular costos operativos.
- Estimar margen neto.
- Calcular CPA máximo admisible.
- Simular escenarios optimistas, base y pesimistas.

### Módulo 5 — AI Research Assistant
Utilizar un LLM local para:
- Analizar productos y sus características.
- Clasificar problemas que resuelven.
- Analizar reseñas de consumidores.
- Identificar oportunidades comerciales.
- Analizar competencia y propuestas de valor.
- Generar informes de investigación.

La IA no tomará decisiones financieras ni modificará puntuaciones deterministas.

### Módulo 6 — Market Validation
- Registrar experimentos comerciales.
- Asociar campañas y creatividades a productos.
- Registrar impresiones, clics, conversiones y gastos.
- Calcular CPA, ROAS y margen real.
- Comparar resultados con proyecciones.
- Clasificar productos como escalar, iterar o descartar.

### Módulo 7 — Dashboard
- Visualizar productos candidatos.
- Consultar evaluaciones y evidencias.
- Comparar oportunidades.
- Consultar rentabilidad proyectada y real.
- Supervisar experimentos.
- Consultar historial de decisiones.

## 3. Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Estilos | Bootstrap |
| Base de datos | SQLite |
| Acceso a datos | SQLAlchemy |
| Procesamiento | Pandas |
| Automatización web | Playwright |
| Recolección web | Requests, BeautifulSoup |
| Inteligencia artificial | LLM local |
| Inferencia local | llama.cpp |
| Pruebas | Pytest |
| Control de versiones | Git |

**Infraestructura:** ejecución completamente local, sin necesidad de hosting ni servidores externos.

El LLM se ejecutará mediante un servidor local compatible con una API HTTP. Se evaluará backend Vulkan o ROCm según compatibilidad efectiva con la GPU AMD RX 9060 XT de 16 GB.

## 4. Arquitectura

Aplicación modular organizada por responsabilidades:

- `routes/`: endpoints y navegación Flask.
- `services/`: lógica de negocio.
- `repositories/`: acceso a datos.
- `models/`: entidades y modelos de persistencia.
- `collectors/`: adaptadores de fuentes externas.
- `ai/`: integración con el LLM local.
- `evaluation/`: reglas y puntuaciones.
- `financial/`: cálculos financieros.
- `validation/`: experimentos y métricas.
- `templates/`: interfaz Jinja2.
- `static/`: CSS y JavaScript.
- `tests/`: pruebas automatizadas.

## 5. Flujo operativo

1. Descubrimiento automático de productos.
2. Recopilación de evidencia.
3. Almacenamiento de información.
4. Evaluación de criterios eliminatorios.
5. Puntuación de candidatos aprobados.
6. Análisis financiero.
7. Priorización de oportunidades.
8. Investigación asistida por IA.
9. Validación mediante experimentos comerciales.
10. Registro de resultados y decisiones.

## 6. Requisitos de calidad

- Cada evaluación debe ser reproducible.
- Toda información externa debe conservar su fuente y fecha.
- Los datos faltantes no deben interpretarse como datos positivos.
- Las decisiones financieras deben ser deterministas.
- Los módulos deben poder probarse independientemente.
- Los errores de recopilación deben quedar registrados.
- El sistema debe permitir actualizar criterios sin modificar la lógica central.
- Debe poder funcionar sin conexión para todas las funcionalidades que no requieran consultar fuentes externas.

## 7. Fuera de alcance inicial

- Gestión de inventario.
- Gestión de pedidos.
- Procesamiento de pagos.
- Administración de tiendas online.
- Gestión logística.
- Automatización completa de campañas publicitarias.
- Despliegue en servidores externos.

## 8. Objetivo del MVP

Construir una primera versión capaz de:

1. Incorporar productos candidatos.
2. Recopilar y almacenar evidencia.
3. Evaluar automáticamente los 10 criterios.
4. Calcular rentabilidad estimada.
5. Generar informes mediante un LLM local.
6. Mostrar y comparar oportunidades desde un dashboard.
7. Ejecutar pruebas automatizadas sobre las reglas y cálculos.

**Resultado esperado:** una herramienta local que permita pasar de una lista de productos potenciales a un conjunto priorizado de oportunidades respaldadas por evidencia y análisis financiero.
