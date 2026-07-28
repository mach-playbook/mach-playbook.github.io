---
layout: post
title: "Arquitecturas Orientadas a Eventos en Entornos Multi-Nube: Orquestando GCP Pub/Sub y AWS SQS"
date: 2026-07-28 09:30:00 -0600
categories: [Arquitectura Cloud, Microservicios]
tags: [event-driven, gcp, aws, pub-sub, sqs, multi-cloud, asincrono]
lang: es
image:
  path: /assets/img/posts/2026-07-28-arquitecturas-orientadas-eventos-multi-nube.png
---

El paradigma de la computación síncrona (petición-respuesta) es insuficiente cuando se escalan plataformas de alto rendimiento. En las arquitecturas MACH (Microservices, API-first, Cloud-native, Headless), la resiliencia se logra mediante el desacoplamiento agresivo de los servicios. 

En este análisis, abordaremos cómo construir una Arquitectura Orientada a Eventos (EDA - Event-Driven Architecture) que cruza las fronteras de los proveedores de nube, integrando la alta capacidad de ingestión de Google Cloud Pub/Sub con los fiables mecanismos de encolado de Amazon SQS.

## El Límite de las APIs RESTful Síncronas

Cuando un microservicio de pedidos (Order Service) necesita notificar al servicio de inventario (Inventory Service) y al de facturación (Billing Service), realizar llamadas HTTP RESTful en cadena introduce puntos únicos de fallo. Si el servicio de facturación experimenta latencia, toda la transacción del pedido se retrasa. 

La solución es transicionar hacia la comunicación asíncrona mediante buses de eventos.

## Ingestión Global con GCP Pub/Sub

Google Cloud Pub/Sub es ideal como el enrutador de eventos global (Event Router) debido a su naturaleza verdaderamente *serverless* y su escalabilidad automática sin necesidad de particionado manual (a diferencia de Apache Kafka).

1.  **Publicación de Eventos:** El servicio de pedidos actúa como *Publisher*, enviando un evento inmutable (`OrderCreated`) a un tema (Topic) central en GCP.
2.  **Fan-out:** Pub/Sub replica este mensaje a múltiples suscripciones (Subscriptions), asegurando que cada microservicio interesado reciba su propia copia del evento de manera independiente.

## Consumo y Procesamiento Seguro con AWS SQS

Mientras Pub/Sub maneja la distribución masiva, AWS SQS (Simple Queue Service) brilla en la gestión del flujo de trabajo de los *Workers* locales alojados en AWS (por ejemplo, funciones Lambda o contenedores ECS).

Para conectar ambos mundos:
1.  **Suscripciones Push a Webhooks Seguros:** Se configura Pub/Sub para que realice envíos HTTP Push hacia un API Gateway en AWS. 
2.  **Encolado Local:** El API Gateway de AWS deposita el mensaje directamente en una cola SQS. 
3.  **Dead Letter Queues (DLQ):** SQS permite un control granular sobre los reintentos de procesamiento. Si un evento no puede procesarse después de 5 intentos debido a un fallo en la base de datos de destino, el mensaje se mueve automáticamente a una DLQ para su inspección manual, evitando el bloqueo de la cola principal.

## Conclusión

Diseñar topologías orientadas a eventos en entornos multi-nube permite a las organizaciones aprovechar lo mejor de ambos ecosistemas: la ingestión analítica global de GCP y el robusto ecosistema de procesamiento transaccional de AWS. Esta estrategia garantiza que los sistemas MACH permanezcan altamente disponibles, incluso frente a interrupciones parciales en servicios dependientes.
