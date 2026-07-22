# LLMOps Industrial Unified Pipeline 🚀🏭

![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Gateway-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Langfuse](https://img.shields.io/badge/Langfuse-Observability-orange?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD_Pipeline-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

> **O Ápice da Engenharia de LLMs**: Arquitetura Unificada de Referência Industrial integrando API Gateway, Cache Semântico, Guardrails de Segurança (PII & Prompt Injection), Agentes Inteligentes, CI/CD com Quality Gates e Observabilidade Centralizada no Langfuse.

---

## 🧭 Visão Geral da Arquitetura

O **`llm-llmops`** unifica todas as fases anteriores do portfólio em um único ecossistema pronto para produção:

```mermaid
flowchart TD
    Client[Cliente / Frontend] --> Gateway[API Gateway Unificado FastAPI]
    
    subgraph Security & Efficiency [Camada de Segurança e Performance]
        Gateway --> Guardrails[Guardrails Proxy: Sanitização PII e Anti-Jailbreak]
        Guardrails -- Bloqueado --> Blocked[Retorna HTTP 400 Bad Request]
        Guardrails -- Aprovado --> CacheCheck{Cache Semântico Hit?}
        CacheCheck -- Sim (Similarity >= 0.88) --> FastReturn[Resposta Instantânea da Memória]
    end
    
    subgraph Intelligence Layer [Agentes & LLM Inferencia]
        CacheCheck -- Não --> SalesAgent[LLM Sales Agent & Engine]
        SalesAgent --> AgentResponse[Resposta Gerada]
    end
    
    subgraph Telemetry & Observability [Observabilidade & CI/CD]
        FastReturn -. Trace .-> Langfuse[Langfuse Centralized Observability]
        AgentResponse -. Trace .-> Langfuse
        Blocked -. Trace .-> Langfuse
        
        GHActions[GitHub Actions CI/CD] --> PytestRun[Avaliador de Testes e Cobertura]
        PytestRun --> DockerBuild[Build de Imagem Docker de Produção]
    end
```

---

## ⚡ Módulos Integrados

| Módulo | Função |
| :--- | :--- |
| **API Gateway Unificado** | Orquestra a pipeline de requisição ponta a ponta com rotas REST e documentação OpenAPI. |
| **Guardrails Proxy** | Inspeciona ataques de Prompt Injection e higieniza automaticamente dados sensíveis (CPFs/Emails). |
| **Semantic Cache** | Evita chamadas custosas à LLM retornando respostas pré-computadas para dúvidas frequentes. |
| **Langfuse Observability** | Grava o ciclo de vida completo da requisição, métricas de latência e sinalizações de segurança. |
| **GitHub Actions CI/CD** | Executa o Quality Gate automatizado a cada `push` / `pull_request`. |

---

## 🚀 Como Executar

### 1. Execução via Docker Compose
```bash
docker-compose up --build
```
Acesse o endpoint de saúde:
```bash
curl http://localhost:8000/health
```

### 2. Execução dos Testes Integrados
```bash
docker run --rm -e PYTHONPATH=/app -v $(pwd):/app -w /app python:3.12-slim bash -c "pip install pytest pytest-cov fastapi uvicorn pydantic pydantic-settings langfuse httpx && pytest --cov=app --cov-report=term-missing"
```

---

## 🛡️ Licença & Autor
Desenvolvido por **Cayo Neves** ([@cayoesn](https://github.com/cayoesn)) como o projeto final e consolidado do Portfólio de LLM & LLMOps de Alta Performance.