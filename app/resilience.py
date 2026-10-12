import time
from enum import StrEnum
from typing import Dict, Any, Optional, Callable


class CircuitState(StrEnum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class TokenBucketRateLimiter:
    """Enterprise Token Bucket Rate Limiter por Tenant / Usuário.
    
    Implementa reabastecimento fracionário contínuo em tempo real O(1) sem locks pesados.
    """

    def __init__(self, capacity: int = 10, refill_rate: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens por segundo
        self._buckets: Dict[str, Dict[str, float]] = {}

    def acquire(self, key: str, tokens: int = 1) -> bool:
        now = time.time()
        bucket = self._buckets.get(key)

        if bucket is None:
            bucket = {"tokens": float(self.capacity), "last_refill": now}
            self._buckets[key] = bucket

        # Reabastece proporcionalmente ao delta de tempo
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(float(self.capacity), bucket["tokens"] + (elapsed * self.refill_rate))
        bucket["last_refill"] = now

        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            return True
        return False

    def reset(self):
        self._buckets.clear()


class CircuitBreaker:
    """Enterprise 3-State Circuit Breaker (CLOSED, OPEN, HALF_OPEN).
    
    Protege o gateway contra tempestades de falhas e colapso de upstream LLM.
    """

    def __init__(self, failure_threshold: int = 3, recovery_timeout_seconds: float = 3.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    def can_execute(self) -> bool:
        now = time.time()
        if self.state == CircuitState.OPEN:
            if now - self.last_failure_time >= self.recovery_timeout_seconds:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def reset(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
