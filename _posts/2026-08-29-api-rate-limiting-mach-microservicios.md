---
layout: post
title: "Rate Limiting y Throttling en APIs MACH: Proteccion Multicapa sin Impactar Performance"
date: 2026-08-29 09:00:00 -0600
lang: es
categories: [API Design, Seguridad]
tags: [rate-limiting, throttling, api-gateway, mach, microservices, redis, token-bucket]
image:
  path: /assets/img/posts/2026-08-29-api-rate-limiting-mach-microservicios.png
---

El rate limiting es uno de los mecanismos de proteccion mas fundamentales en cualquier plataforma MACH expuesta al mundo exterior. Sin rate limiting, un cliente malicioso o incluso un consumidor legitimo con un bug de retry infinito podria saturar los recursos de toda la plataforma, causando una denegacion de servicio para el resto de los usuarios. En una arquitectura MACH donde un API Gateway central orquesta el acceso a multiples microservicios, el rate limiting debe implementarse en multiples capas para ser efectivo.

## Las Cuatro Capas del Rate Limiting en MACH

En una arquitectura MACH de produccion, el rate limiting se implementa tipicamente en cuatro capas distintas, cada una con un proposito diferente.

### Capa 1: CDN y Edge (Primera Linea de Defensa)

El rate limiting a nivel de CDN (Cloudflare, Fastly, Akamai) es la primera linea de defensa contra ataques volumetricos. Opera a nivel de IP o de ASN (Autonomous System Number) y puede absorber ataques de cientos de miles de requests por segundo sin que ninguna peticion llegue a los servidores de la aplicacion.

Configurar rate limiting en Cloudflare es simple mediante reglas de WAF: bloquear o challenge cualquier IP que supere 1,000 requests por minuto a cualquier endpoint de la API. Este limite es lo suficientemente alto para no afectar clientes legitimos pero suficientemente bajo para detectar comportamientos anomalos de bots o scripts maliciosos.

### Capa 2: API Gateway (Rate Limiting por Credencial)

El API Gateway (Kong, AWS API Gateway, Apigee, o custom) es donde se implementa el rate limiting por credencial del cliente: por API key, por JWT, o por combinacion de usuario y endpoint.

Los algoritmos de rate limiting mas comunes en esta capa son:

**Token Bucket**: el cliente tiene un bucket con capacidad maxima de N tokens. Cada request consume un token. El bucket se rellena a una tasa fija de R tokens por segundo. Si el bucket esta vacio, la request es rechazada con HTTP 429. Este algoritmo permite bursts controlados: si un cliente ha estado inactivo y su bucket esta lleno, puede hacer una rafaga de N requests instantaneas.

**Fixed Window Counter**: se cuenta el numero de requests en ventanas de tiempo fijas (por ejemplo, cada minuto). Si el contador supera el limite en la ventana actual, las requests adicionales son rechazadas. Este algoritmo es el mas simple pero tiene un problema en las fronteras de ventana: un cliente puede hacer el doble de las requests permitidas en un corto periodo si distribuye las requests en el final de una ventana y el inicio de la siguiente.

**Sliding Window Log**: para cada cliente se mantiene un log de los timestamps de las ultimas N requests. Cada nueva request verifica cuantas requests hay en el log en los ultimos T segundos. Si supera el limite, la request es rechazada. Es el algoritmo mas preciso pero el mas costoso en memoria.

La implementacion en Redis es el patron mas comun para el rate limiting en el API Gateway, ya que Redis ofrece las operaciones atomicas necesarias (INCR, EXPIRE, TIME) para implementar cualquiera de estos algoritmos con latencias de menos de 1ms.

### Capa 3: Microservicio (Rate Limiting por Tenant y Recurso)

El rate limiting a nivel de microservicio es el mas granular y permite implementar limites por tenant y por recurso especifico. Por ejemplo, en un servicio de busqueda de productos, un tenant en plan Starter puede hacer hasta 100 busquedas por minuto, mientras que un tenant Enterprise tiene un limite de 10,000 busquedas por minuto.

Este rate limiting a nivel de servicio es especialmente importante para los endpoints computacionalmente costosos como las busquedas de texto completo o los reportes que requieren queries complejas. Sin este nivel de control, un tenant agresivo podria saturar los recursos de la base de datos e impactar a otros tenants.

La libreria **resilience4j** (Java), **tokio-rate-limiter** (Rust) o implementaciones basadas en Redis son comunes en esta capa.

### Capa 4: Circuito (Rate Limiting de Salida)

El rate limiting de salida (egress) es a menudo olvidado pero es critico en MACH donde los microservicios consumen APIs de terceros (Stripe, Contentful, Algolia, Salesforce) que tienen sus propios rate limits. Si el microservicio hace demasiadas llamadas a la API externa, la API externa rechaza las requests con 429 y el microservicio falla.

El patron para manejar esto es el **Adaptive Rate Limiter**: el microservicio mantiene un contador de las llamadas a cada API externa y un contador de los errores 429 recibidos. Cuando el rate de 429s supera un umbral, el microservicio reduce automaticamente la tasa de llamadas a esa API hasta que los 429s desaparecen.

## Headers de Rate Limiting: Comunicando los Limites al Consumidor

Cuando un cliente supera el rate limit y recibe un HTTP 429 Too Many Requests, la respuesta debe incluir headers que le indiquen cuando puede reintentar y cuantas requests le quedan disponibles. Los headers estandar son:

X-RateLimit-Limit indica el limite total de requests en la ventana temporal, X-RateLimit-Remaining indica cuantas requests quedan en la ventana actual, X-RateLimit-Reset contiene el timestamp Unix cuando la ventana se resetea y el cliente puede hacer nuevas requests, y Retry-After indica cuantos segundos el cliente debe esperar antes de reintentar (cuando el limite ya fue superado).

Proveer estos headers permite a los clientes implementar un backoff correcto en lugar de simplemente reintentar inmediatamente, lo que exacerbaria el problema.

## Estrategias de Backoff para Consumidores

Del lado del consumidor de la API, implementar una estrategia de retry con backoff exponencial es la contrapartida necesaria al rate limiting del servidor. El algoritmo es simple pero efectivo: en el primer intento fallido (429), esperar 1 segundo antes de reintentar; si vuelve a fallar, esperar 2 segundos; si vuelve a fallar, 4 segundos; hasta un maximo configurado (por ejemplo, 60 segundos).

Agregar un jitter aleatorio al backoff (esperar entre 1 y 1.5 segundos en lugar de exactamente 1 segundo) previene el problema de sincronizacion donde multiples clientes que fallaron al mismo tiempo reintentan al mismo tiempo, creando un nuevo spike de trafico.

## Monitoreo del Rate Limiting en Produccion

Las metricas mas importantes para monitorear el rate limiting en produccion son: el porcentaje de requests que son rate-limited (un valor alto indica que los limites son demasiado bajos o que hay un cliente mal configurado), la distribucion de requests por cliente (para identificar clientes que abusan de la API), y la tasa de errores 429 agrupada por endpoint (para identificar endpoints que necesitan limites mas restrictivos o necesitan ser optimizados para reducir el tiempo de procesamiento).

## Conclusion: Rate Limiting como Fundamento de Resiliencia

El rate limiting no es solo una medida de seguridad: es un mecanismo de resiliencia que garantiza la disponibilidad de la plataforma MACH para todos los clientes, incluso cuando algunos de ellos se comportan de forma anomala. Implementado en multiples capas, el rate limiting crea un sistema de defensa en profundidad que puede absorber picos de trafico inesperados, ataques de denegacion de servicio y errores de configuracion de los clientes sin impactar al resto de los usuarios de la plataforma.
