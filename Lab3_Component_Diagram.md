# Lab 3 – UML Component Diagram

**Project:** Webhook Ingestion & Retry Mechanism Hub  
**SRN:** PES1UG24AM201  
**Name:** Prathyush Gowda

The component model below applies the Lab 3 component-modelling requirements to the existing webhook project. It identifies more than five components and shows the main interfaces/dependencies for ingestion, validation, delivery, retry, persistence, and logging.

```mermaid
flowchart LR
    S[Third-Party Source] -->|Webhook Input| I[<<component>> Webhook Ingestion]
    I -->|Validated Event| V[<<component>> Validation & Event Recorder]
    V -->|Delivery API| D[<<component>> Delivery / Target Router]
    D --> T[Target Internal Service]
    D -->|Failed delivery| R[<<component>> Retry Manager]
    R -->|Retry State| Q[<<component>> Dead-Letter Queue & Event Store]
    R -->|Exponential backoff retry| D
    I -->|Accepted payload| L[<<component>> Logging & Monitoring]
    V -->|Validation status| L
    D -->|Attempts / responses| L
    Q -->|DLQ / recovery status| L
```

**UML source:** `Lab3_Component_Diagram.puml`
