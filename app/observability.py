import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LLMOpsObservability:
    """Central de Observabilidade Unificada (Langfuse)."""

    def __init__(self) -> None:
        self.client = None
        self._init_client()

    def _init_client(self) -> None:
        try:
            from langfuse import Langfuse
            from app.config import settings
            self.client = Langfuse(
                public_key=settings.LANGFUSE_PUBLIC_KEY,
                secret_key=settings.LANGFUSE_SECRET_KEY,
                host=settings.LANGFUSE_HOST
            )
            logger.info("Langfuse Client inicializado no Gateway LLMOps.")
        except Exception as e:
            logger.warning(f"Langfuse SDK indisponível: {e}")
            self.client = None

    def trace_gateway_query(
        self,
        user_id: str,
        prompt: str,
        response: str,
        cached: bool,
        latency_ms: float,
        status: str
    ) -> Optional[str]:
        if not self.client:
            return "demo-llmops-trace"
        try:
            if hasattr(self.client, "trace"):
                trace = self.client.trace(
                    name="gateway_query_pipeline",
                    user_id=user_id,
                    metadata={
                        "cached": cached,
                        "latency_ms": latency_ms,
                        "status": status
                    },
                    tags=["llmops", "industrial_gateway"]
                )
                if hasattr(trace, "generation"):
                    trace.generation(
                        name="llm_inference",
                        prompt=prompt,
                        completion=response
                    )
                return getattr(trace, "id", "demo-llmops-trace")
            return "demo-llmops-trace"
        except Exception as e:
            logger.error(f"Erro ao registrar trace no Langfuse: {e}")
            return "demo-llmops-trace"


llmops_obs = LLMOpsObservability()
