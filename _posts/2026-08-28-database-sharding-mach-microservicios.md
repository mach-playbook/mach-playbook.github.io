---
layout: post
title: "Database Sharding para Microservicios MACH: Estrategias de Particionado a Escala Global"
date: 2026-08-28 09:00:00 -0600
lang: es
categories: [Arquitectura Cloud, Data Engineering]
tags: [database-sharding, postgresql, mach, microservices, distributed-systems, scalability]
image:
  path: /assets/img/posts/2026-08-28-database-sharding-mach-microservicios.png
---

En arquitecturas MACH de escala global donde un microservicio individual maneja decenas de millones de registros y miles de transacciones por segundo, el escalado vertical de la base de datos (aumentar CPU y RAM del servidor) tiene un limite fisico y economico. El **Database Sharding** (particionado horizontal) es la tecnica que permite escalar una base de datos mas alla de las capacidades de un unico servidor distribuyendo los datos entre multiples instancias.

Este articulo analiza las estrategias de sharding especificamente en el contexto de microservicios MACH, donde cada servicio es dueno de su propia base de datos y el sharding es una decision que afecta exclusivamente al equipo responsable de ese servicio.

## Cuando Aplicar Sharding en un Microservicio MACH

El primer principio del sharding es no aplicarlo prematuramente. El sharding anade una complejidad operacional significativa y solo se justifica cuando otras tecnicas de escalado han sido agotadas. El orden recomendado de escalado para una base de datos en MACH es:

1. **Optimizacion de queries**: indices correctos, eliminacion de N+1 queries, reescritura de queries costosas. Esto puede mejorar el performance hasta 100 veces sin cambios estructurales.

2. **Caching**: Redis o Memcached delante de las queries mas frecuentes. Elimina entre el 70 y el 90 porciento de la carga de lectura en la mayoria de los workloads.

3. **Read replicas**: agregar replicas de lectura para distribuir la carga de queries de solo lectura. Escala la capacidad de lectura hasta 5 a 10 veces.

4. **Escalado vertical**: subir a una instancia con mas CPU y RAM. Soluccion rapida pero costosa y con limite fisico.

5. **Sharding**: cuando ninguna de las tecnicas anteriores es suficiente.

Los indicadores de que un microservicio necesita sharding incluyen: latencia de escritura consistentemente por encima de 50ms a pesar de indexes correctos, la base de datos principal no puede absorber mas replicas de lectura sin degradar la replicacion, el volumen de datos supera los 10TB y afecta los tiempos de backup y recovery, o el throughput de escrituras supera los 50,000 transacciones por segundo sostenidas.

## Estrategias de Sharding: Hash, Range y Directory

Existen tres estrategias principales de sharding, cada una con caracteristicas diferentes.

### Hash Sharding

En el Hash Sharding, el shard al que pertenece un registro se determina aplicando una funcion hash al valor de la shard key. Por ejemplo, si la shard key es el customer_id y hay 4 shards, el shard correspondiente seria: shard_number = hash(customer_id) % 4.

La ventaja del Hash Sharding es la distribucion uniforme de datos entre shards, evitando shards calientes donde un shard recibe mucho mas trafico que otros. La desventaja es que las queries de rango (todos los pedidos entre fecha A y fecha B) deben consultar todos los shards en paralelo, lo que es menos eficiente que en Range Sharding.

### Range Sharding

En el Range Sharding, los registros se distribuyen entre shards basandose en rangos del valor de la shard key. Por ejemplo, pedidos con order_id entre 1 y 10 millones van al shard 1, entre 10 y 20 millones al shard 2, etc.

La ventaja es que las queries de rango son eficientes porque solo necesitan consultar un shard especifico. La desventaja son los "hot shards": si los datos nuevos siempre caen en el rango mas alto (como es comun con IDs auto-incrementales o timestamps), el ultimo shard recibe toda la carga de escritura.

### Directory Sharding

En el Directory Sharding, existe una tabla de lookup centralizada que mapea cada valor de shard key a su shard correspondiente. Es el enfoque mas flexible ya que permite re-balancear shards sin cambiar la logica de la aplicacion, pero anade una llamada de red adicional para cada operacion de base de datos.

## Implementacion con Citus (PostgreSQL Distributed)

Para microservicios MACH que usan PostgreSQL, **Citus** es la extension de sharding mas madura y ampliamente adoptada. Citus transforma PostgreSQL en una base de datos distribuida que implementa sharding de forma transparente para la aplicacion.

Con Citus, el mismo ORM o cliente de PostgreSQL que usa el microservicio puede trabajar con una base de datos sharded sin cambios en el codigo de la aplicacion. El developer define cual columna es la distribution key (equivalente a la shard key) al crear la tabla, y Citus maneja automaticamente la distribucion de datos y el routing de queries al shard correcto.

La eleccion de la distribution key es la decision mas critica. Debe ser un campo que aparezca en todos los WHERE clause de las queries del microservicio, que tenga alta cardinalidad (muchos valores unicos diferentes), y que distribuya el trafico de forma equilibrada entre shards. En un microservicio de pedidos, tenant_id o customer_id suelen ser buenas distribution keys.

## Cross-Shard Queries: El Mayor Desafio del Sharding

Las queries que necesitan datos de multiples shards (cross-shard queries) son el mayor desafio operacional del sharding y la principal razon por la que se debe elegir la distribution key con mucho cuidado.

En Citus, las cross-shard queries se ejecutan en paralelo en todos los shards y los resultados se agregan en el coordinator node. Esto es automatico pero tiene un costo de latencia proporcional al numero de shards y la cantidad de datos que se transfieren entre nodos para la agregacion.

El patron para minimizar cross-shard queries en MACH es el **co-location**: cuando dos tablas que se consultan juntas frecuentemente tienen la misma distribution key, Citus garantiza que los registros relacionados esten siempre en el mismo shard. Por ejemplo, si orders y order_items usan customer_id como distribution key, todos los pedidos y sus items de un cliente siempre estaran en el mismo shard, permitiendo JOINs eficientes sin trafico de red entre shards.

## Sharding en el Ecosistema MACH: Coordinacion entre Equipos

En una arquitectura MACH pura, el sharding de la base de datos de un microservicio es una decision interna del equipo responsable de ese servicio. Ningun otro equipo debe depender de la implementacion de sharding de otro servicio.

Sin embargo, hay implicaciones que deben coordinarse: si el microservicio expone eventos a un bus de mensajes, la produccion de eventos debe ser correcta incluso durante la reparticion de datos entre shards (resharding); los SLAs del servicio deben mantenerse durante las operaciones de resharding, que tipicamente requieren un mantenimiento planificado o una migracion en linea.

## Alternativas al Sharding Tradicional: NewSQL

Antes de implementar sharding personalizado, vale la pena evaluar bases de datos que implementan sharding de forma nativa como parte de su diseno. Bases de datos como **YugabyteDB**, **CockroachDB** y **Spanner de Google** son SQL-compatibles con PostgreSQL y ofrecen escalado horizontal automatico con transacciones ACID distribuidas.

Estas bases de datos eliminan la complejidad de gestionar el sharding manualmente a costa de una mayor complejidad en la operacion de la base de datos en si misma y, en algunos casos, latencias ligeramente mas altas por transaccion individual por el overhead del consensus distribuido.

## Conclusion: Sharding como Ultima Herramienta de Escalado

El Database Sharding es una herramienta poderosa pero costosa en terminos de complejidad operacional. En el contexto de microservicios MACH, donde cada servicio es responsable de su propia base de datos, el sharding bien implementado puede escalar un servicio a decenas de miles de transacciones por segundo y petabytes de datos.

La clave del exito del sharding en produccion es: elegir la distribution key correcta antes de implementar (cambiarla despues requiere un resharding completo que es extremadamente costoso), co-locar tablas relacionadas con la misma distribution key, y minimizar las cross-shard queries en el diseno del schema desde el inicio.
