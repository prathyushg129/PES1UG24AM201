# Lab 3 – Architecture Selection & Component Modelling

**Name:** Prathyush Gowda  
**SRN:** PES1UG24AM201  
**Project:** Webhook Ingestion & Retry Mechanism Hub

## Architecture Selection
We chose **Microservices Architecture** for the Webhook Ingestion & Retry Mechanism Hub.

### Two Reasons
1. **Independent scaling:** The project must support high-volume webhook ingestion, up to 2,500 requests per second. Separating ingestion, validation, delivery, retry, and storage responsibilities allows the high-traffic parts to scale independently.
2. **Fault isolation:** Failed deliveries must be retried using exponential backoff and repeatedly failed events must move to a dead-letter queue. Separating delivery and retry responsibilities limits the impact of target-service failures and supports recovery without losing accepted events.

### Security Advantage
The ingestion and validation components can validate incoming webhook requests before forwarding them to internal services. Invalid payloads are rejected and recorded instead of being passed downstream.

### Performance Benefit
The ingestion component can buffer incoming requests while delivery and retry processing happen independently. This supports high-throughput ingestion and prevents temporary target-service delays from directly blocking incoming webhook traffic.

## Components
- Webhook Ingestion
- Validation & Event Recorder
- Delivery / Target Router
- Retry Manager
- Dead-Letter Queue & Event Store
- Logging & Monitoring

The component diagram uses provided/required interfaces to represent webhook input, validation/event flow, delivery, retry state, dead-letter storage, and event logging.
