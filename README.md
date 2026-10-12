# LLMOps Industrial Unified Pipeline 🚀🏭

![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Gateway-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Langfuse](https://img.shields.io/badge/Langfuse-Observability-orange?style=for-the-badge)

> **Arquitetura Unificada de Referência Industrial**: API Gateway resiliente integrando **Token Bucket Rate Limiting**, **Circuit Breaker Tri-State**, Cache Semântico, Guardrails de Segurança (PII & Prompt Injection), Agentes Inteligentes e Observabilidade Langfuse.

---

## 🧭 Visão Geral da Arquitetura

```mermaid
flowchart TD
    Client[Cliente / Frontend] --> RateLimit{Token Bucket Rate Limiter}
    RateLimit -- Saturação (HTTP 429) --> Rejected[Rate Limit Exceeded]
    RateLimit -- Aprovado --> Guardrails[Guardrails Proxy: Sanitização PII e Anti-Jailbreak]
    
    subgraph Security & Efficiency [Camada de Segurança e Performance]
        Guardrails -- Ataque Detectado --> Blocked[Retorna HTTP 400 Bad Request]
        Guardrails -- Aprovado --> CacheCheck{Cache Semântico Hit?}
        CacheCheck -- Sim (Similarity >= 0.88) --> FastReturn[Resposta Instantânea da Memória]
    end
    
    subgraph Resilience & Agent [Camada de Resiliência e Agentes]
        CacheCheck -- Não --> CircuitCheck{Circuit Breaker Status?}
        CircuitCheck -- OPEN --> FallbackResp[Resposta de Contingência Degradada]
        CircuitCheck -- CLOSED / HALF-OPEN --> SalesAgent[LLM Sales Agent & Engine]
        SalesAgent --> AgentResponse[Resposta Gerada com Sucesso]
    end
    
    subgraph Telemetry [Observabilidade & Telemetria]
        FastReturn -. Trace .-> Langfuse[Langfuse Centralized Observability]
        AgentResponse -. Trace .-> Langfuse
        FallbackResp -. Trace .-> Langfuse
        Blocked -. Trace .-> Langfuse
    end
```

---

## ⚡ Módulos & Padrões Staff

| Módulo | Padrão / Algoritmo | Complexidade | Garantia Operacional |
| :--- | :--- | :--- | :--- |
| **Rate Limiter** | Token Bucket contínuo fracionário | $\mathcal{O}(1)$ | Prevenção de DoS e saturação por tenant |
| **Circuit Breaker** | Tri-State (`CLOSED`, `OPEN`, `HALF_OPEN`) | $\mathcal{O}(1)$ | Fallback gracioso contra colapso de upstream LLM |
| **Guardrails Proxy** | Regex Unificada + Detecção de Jailbreak | $\mathcal{O}(\|T\|)$ | Sanitização atômica de PII e bloqueio de injeção |
| **Semantic Cache** | Cache vetorial em memória | $\mathcal{O}(1)$ / sub-5ms | Economia de custo e baixa latência |
| **Langfuse Obs** | Rastreamento distribuído de traces/spans | Assíncrono | Visibilidade total de ciclo de vida e erros |

---

## 🚀 Como Executar no Docker

```bash
docker-compose up -d --build
```

Endpoints de acesso:
- **API Gateway**: `http://localhost:8000` (OpenAPI interativa em `/docs`)
- **Healthcheck & Circuit Status**: `http://localhost:8000/health`
- **Painel de Observabilidade (Langfuse)**: `http://localhost:3008`

---

## 🧪 Testes Automatizados (100% Hermético)

```bash
docker run --rm -v $(pwd):/workspace -w /workspace -e PYTHONPATH=/workspace portfolio-spec-engine:test pytest tests -v
```
