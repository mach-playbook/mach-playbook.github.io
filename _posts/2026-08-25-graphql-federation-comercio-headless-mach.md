---
layout: post
title: "GraphQL Federation en Comercio Headless: Unificando Microservicios MACH con un Supergraph"
date: 2026-08-25 09:00:00 -0600
lang: es
categories: [API Design, Microservices]
tags: [graphql, federation, headless-commerce, mach, api-design, supergraph, apollo]
image:
  path: /assets/img/posts/2026-08-25-graphql-federation-comercio-headless-mach.png
---

Las arquitecturas MACH para comercio electronico presentan un dilema clasico: los microservicios independientes maximizan la modularidad y la velocidad de despliegue individual, pero complican enormemente la experiencia del frontend. Un componente de pagina de producto necesita datos de catalogo (del PIM), precios (del motor de precios), inventario (del WMS), reviews (del servicio de reviews) y recomendaciones (del motor de ML). Sin una capa de agregacion, el frontend debe hacer 5 llamadas HTTP independientes con toda la complejidad de manejo de errores, timeouts y cacheo que eso implica.

**GraphQL Federation** (o Federated GraphQL) es la solucion arquitectonica que resuelve este problema en el contexto MACH. En lugar de un GraphQL monolitico o multiples APIs GraphQL desconectadas, la Federation permite a cada microservicio exponer su propio subgraph (una porcion del schema GraphQL) que luego se compone automaticamente en un **Supergraph** unificado que el frontend consume como si fuera una sola API.

## El Problema: N+1 de APIs en Comercio Headless

Antes de explorar la solucion, vale la pena cuantificar el problema que GraphQL Federation resuelve en el contexto del comercio headless MACH.

Considera la pagina de listado de productos (PLP) de una tienda con arquitectura MACH tipica. Para renderizar 24 productos con sus precios, disponibilidad, imagenes y badges de promocion, el frontend necesita en una arquitectura sin Federation: una llamada al PIM para obtener los datos basicos de los 24 productos, una llamada al motor de precios con los 24 SKUs para obtener precios y descuentos, una llamada al WMS para verificar disponibilidad de los 24 productos, una llamada al CDN o servicio de imagenes para las URLs optimizadas, y una llamada al servicio de promociones para los badges activos.

Esto es 5 llamadas en paralelo con 120 roundtrips de datos, complejidad de cacheo distribuida entre el frontend y el BFF, y lentitud perceptible para el usuario en redes moviles. Si el servicio de precios tarda 800ms, toda la pagina se bloquea.

Con GraphQL Federation, el frontend hace **una sola query** al Supergraph que internamente orquesta las llamadas a los subgraphs, aplica el cacheo correcto a nivel de campo, y retorna exactamente los datos que el frontend necesita, sin over-fetching ni under-fetching.

## Como Funciona la GraphQL Federation

La Federation (especificamente la Apollo Federation v2, que es el estandar de facto) funciona mediante tres conceptos clave:

**Subgraphs:** Cada microservicio expone su propio schema GraphQL parcial. El servicio de Catalogo define los tipos Product y Category. El servicio de Precios extiende el tipo Product con los campos price y discountedPrice. El servicio de Inventario extiende Product con el campo inStock. Cada subgraph solo conoce sus propios tipos y los campos que extiende de otros servicios.

**El Router (Gateway):** Un componente central que recibe las queries del frontend, las parsea, determina que subgraphs necesitan ser consultados, orquesta las llamadas en paralelo y combina las respuestas en una sola respuesta unificada. Apollo Router es la implementacion de referencia, aunque tambien existen alternativas como Cosmo Router de WunderGraph y Hive Gateway.

**El Supergraph Schema:** La composicion automatica de todos los subgraph schemas en un schema unificado. Este proceso detecta automaticamente las referencias entre tipos (como cuando Precios extiende Product de Catalogo) y construye el plan de ejecucion optimo para cada query.

## Implementacion en una Arquitectura MACH de E-commerce

Para implementar GraphQL Federation en una plataforma MACH de comercio, el proceso tipico sigue estos pasos:

El primer paso es identificar los dominios que exponen subgraphs. En e-commerce tipicamente son: Catalogo y PIM (productos, categorias, variantes), Precios y Promociones (precios por segmento, descuentos, cupones), Inventario y Logistica (disponibilidad, tiempos de entrega), Cuenta y Perfil (datos del usuario, listas de deseos, historial), Checkout y Ordenes (carrito, orden, estado de envio), y Contenido y CMS (paginas, banners, descripciones enriquecidas).

El segundo paso es definir las entidades compartidas y las referencias entre subgraphs. En Federation, las entidades son tipos que existen en multiples subgraphs. El tipo Product puede ser definido por el subgraph de Catalogo (con id, name, sku, description) y extendido por Precios (con price, compareAtPrice, promotions), por Inventario (con inStock, availableQuantity, estimatedDelivery), y por Reviews (con rating, reviewCount, featuredReview).

El tercer paso es implementar el Router central. El Apollo Router se configura mediante un archivo YAML que lista las URLs de todos los subgraphs y sus schemas. En produccion, el Router se despliega como un pod de Kubernetes con auto-scaling horizontal, ya que es el punto de entrada de todas las queries del frontend y debe ser altamente disponible.

## Cacheo y Performance en GraphQL Federation

El cacheo es uno de los aspectos mas criticos de una implementacion de Federation en produccion. GraphQL Federation ofrece capacidades de cacheo que van mas alla de lo que es posible con APIs REST:

El **cacheo por campo** permite definir directivas de cache a nivel de cada campo del schema. Los precios publicos pueden cachearse por 5 minutos, la disponibilidad por 30 segundos, los datos de producto base por 1 hora, y los datos personalizados del usuario por 0 segundos (sin cache). Esto maximiza el hit rate del cache sin servir datos desactualizados en campos criticos.

El **cacheo a nivel de entidad** permite que cuando multiple queries soliciten el mismo producto, el Router reutilice el resultado cacheado en lugar de hacer multiples llamadas al subgraph de Catalogo. Esto es especialmente valioso en PLPs donde el mismo producto puede aparecer en multiples posiciones.

La **persisted queries** en Apollo permite que el cliente envie un hash SHA-256 de la query en lugar del texto completo. Esto reduce el payload de las requests, mejora el tiempo de parsing en el Router, y permite activar el modo de seguridad donde solo se aceptan queries pre-registradas, bloqueando ataques de queries maliciosas.

## Observabilidad y Trazabilidad en el Supergraph

Una de las complejidades de GraphQL Federation es que una sola query del usuario puede traducirse en 5 o 10 llamadas a subgraphs diferentes. La observabilidad correcta es critica para diagnosticar problemas de latencia.

Apollo Router integra nativamente con OpenTelemetry, generando trazas distribuidas que muestran exactamente cuanto tiempo tomo cada subgraph en responder a cada query del usuario. Estas trazas se pueden enviar a Jaeger, Tempo de Grafana, o cualquier backend compatible con OTLP.

El Apollo Studio (la plataforma de gestion de graphs de Apollo) ofrece metricas de operacion por query, incluyendo percentiles de latencia, tasa de error por campo, y el analisis de cuales queries son las mas costosas en terminos de llamadas a subgraphs. Esta visibilidad permite al equipo de Platform Engineering identificar oportunidades de optimizacion y detectar regresiones de performance cuando se despliegan cambios en los subgraphs.

## Manejo de Versiones y Compatibilidad entre Subgraphs

En una arquitectura MACH, los subgraphs son desplegados por equipos independientes con sus propios ciclos de release. GraphQL Federation maneja esto mediante el concepto de **Schema Registry**: antes de que cualquier equipo despliegue cambios a su subgraph, estos se validan contra el Supergraph compuesto para detectar breaking changes.

Apollo Schema Registry y alternativas open-source como Hive de The Guild o Cosmo de WunderGraph ofrecen esta funcionalidad. El proceso tipico es: el equipo de Precios hace un pull request que incluye cambios al schema de su subgraph; el CI/CD ejecuta una validacion contra el schema registry que compone el nuevo subgraph con todos los otros y verifica que no hay breaking changes; si la composicion es exitosa, el pull request puede ser aprobado; si hay un breaking change, el CI/CD falla con un mensaje claro indicando que campos o tipos estan siendo eliminados o incompatiblemente modificados.

Este proceso permite iteracion rapida de cada equipo mientras se mantiene la estabilidad del Supergraph que todos los frontends consumen.

## Patron BFF sobre Federation vs. Federation Directa al Frontend

Un debate comun en arquitecturas MACH es si el frontend debe consumir el Supergraph directamente o si debe existir un Backend For Frontend (BFF) entre el cliente y el Router de Federation.

La recomendacion general es: **Federation directa al frontend para clientes web (Next.js, React), BFF para clientes moviles**. Los clientes web modernos se benefician del code generation de GraphQL que genera tipos TypeScript automaticamente del schema, garantizando type-safety de extremo a extremo. Los clientes moviles (iOS, Android) tienen restricciones diferentes: tamano del payload, caching off-line, y necesidades de datos muy especificas por pantalla que hacen mas practico un BFF ligero que adapte las queries del Supergraph.

## Conclusion: GraphQL Federation como API Gateway para MACH

GraphQL Federation no es solo una tecnologia de APIs: es una estrategia organizacional que alinea los dominios de negocio de tu arquitectura MACH con la forma en que el frontend consume datos. Al permitir que cada equipo sea dueno de su subgraph (su porcion del grafo de datos), Federation extiende el principio de ownership de datos de los microservicios al nivel de la API.

La adopcion de GraphQL Federation en comercio headless MACH tiene un ROI claro: reduccion del 60 al 80 porciento en el numero de llamadas de red del frontend, type-safety de extremo a extremo que elimina bugs en produccion por cambios de API, experiencias de usuario mas rapidas por cacheo inteligente por campo, y mayor velocidad de desarrollo por la autonomia de los equipos al evolucionar sus subgraphs sin coordinar cambios de API con todos los consumidores.

El camino hacia un Supergraph maduro es iterativo: empieza con los 3 o 4 dominios mas criticos, establece el proceso de Schema Registry desde el primer dia, y expande gradualmente a medida que cada equipo adopta el patron. En 6 a 12 meses, la Federation puede convertirse en el backbone de datos de toda tu arquitectura MACH.
