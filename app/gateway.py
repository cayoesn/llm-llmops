import re
import time
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from app.config import settings
from app.observability import llmops_obs


class QueryRequest(BaseModel):
    user_id: str
    prompt: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    cached: bool
    pii_masked: bool
    safety_passed: bool
    latency_ms: float
    trace_id: Optional[str] = None


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API Gateway Unificado de LLMOps integrando Guardrails, Cache Semântico, Agente e Observabilidade."
)

# Cache Semântico em Memória
SEMANTIC_CACHE = {
    "qual o prazo de entrega para sao paulo?": "O prazo de entrega para Sao Paulo capital eh de 2 dias uteis via frete expresso.",
    "como funciona a politica de troca?": "A troca pode ser solicitada em ate 30 dias apos o recebimento do produto sem custos adicionais."
}


def mask_pii(text: str) -> tuple[str, bool]:
    cpf_pattern = r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b"
    masked = re.sub(cpf_pattern, "[CPF_MASCARADO]", text)
    has_pii = masked != text
    return masked, has_pii


def check_jailbreak(text: str) -> bool:
    forbidden = ["ignore todas as instrucoes", "modo dan", "desative filtros"]
    return any(term in text.lower() for term in forbidden)


@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "env": settings.ENV}


@app.post("/api/v1/query", response_model=QueryResponse)
async def process_query(req: QueryRequest):
    start_time = time.time()

    # 1. Guardrails Check: Prompt Injection / Jailbreak
    if check_jailbreak(req.prompt):
        llmops_obs.trace_gateway_query(
            user_id=req.user_id,
            prompt=req.prompt,
            response="Ataque detectado",
            cached=False,
            latency_ms=0.0,
            status="BLOCKED_JAILBREAK"
        )
        raise HTTPException(status_code=400, detail="Prompt bloqueado por conter tentativa de Prompt Injection / Jailbreak.")

    # 2. Guardrails Check: PII Masking
    clean_prompt, pii_detected = mask_pii(req.prompt)

    # 3. Semantic Cache Check
    prompt_lower = clean_prompt.strip().lower()
    if prompt_lower in SEMANTIC_CACHE:
        latency = round((time.time() - start_time) * 1000, 2)
        trace_id = llmops_obs.trace_gateway_query(
            user_id=req.user_id,
            prompt=clean_prompt,
            response=SEMANTIC_CACHE[prompt_lower],
            cached=True,
            latency_ms=latency,
            status="CACHE_HIT"
        )
        return QueryResponse(
            response=SEMANTIC_CACHE[prompt_lower],
            cached=True,
            pii_masked=pii_detected,
            safety_passed=True,
            latency_ms=latency,
            trace_id=trace_id
        )

    # 4. Processamento pelo Agente Inteligente de Vendas
    agent_response = f"Prezado cliente, processamos sua solicitacao: '{clean_prompt}'. Nosso time comercial entrara em contato para auxiliar."
    latency = round((time.time() - start_time) * 1000, 2)

    trace_id = llmops_obs.trace_gateway_query(
        user_id=req.user_id,
        prompt=clean_prompt,
        response=agent_response,
        cached=False,
        latency_ms=latency,
        status="LLM_PROCESSED"
    )

    return QueryResponse(
        response=agent_response,
        cached=False,
        pii_masked=pii_detected,
        safety_passed=True,
        latency_ms=latency,
        trace_id=trace_id
    )
