"""Health Service Barrel

Aggregates all usecases from the health usecases domain.
"""

from usecases.health import get_health_status

__all__ = ["get_health_status"]
