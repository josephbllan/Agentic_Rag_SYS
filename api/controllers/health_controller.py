"""
Health Controller
System health, readiness, and liveness checks
"""
from typing import Dict, Any
from datetime import datetime, timezone
import psutil
import platform

from .base_controller import BaseController
from config.settings import APP_VERSION


class HealthController(BaseController):

    def __init__(self):
        """Initializes the health controller with no backing service,
        as health checks rely on system introspection rather than a domain service.
        """
        super().__init__(service=None)

    async def check_health(self) -> Dict[str, Any]:
        """Liveness probe -- always returns healthy if the process is up."""
        return {
            "status": "healthy",
            "service": "RAG Image Search System",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": APP_VERSION,
        }

    async def check_ready(self) -> Dict[str, Any]:
        """Readiness probe -- checks critical dependencies."""
        checks: Dict[str, str] = {}
        try:
            from config.database import test_connection
            checks["database"] = "ok" if test_connection() else "fail"
        except Exception:
            checks["database"] = "fail"

        all_ok = all(v == "ok" for v in checks.values())
        return {
            "status": "ready" if all_ok else "not_ready",
            "checks": checks,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": APP_VERSION,
        }

    async def check_detailed_health(self) -> Dict[str, Any]:
        """Detailed health with system metrics (admin)."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "status": "healthy",
                "service": "RAG Image Search System",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": APP_VERSION,
                "system": {
                    "platform": platform.system(),
                    "python_version": platform.python_version(),
                    "cpu_percent": cpu_percent,
                    "memory": {
                        "total": memory.total,
                        "available": memory.available,
                        "percent": memory.percent,
                    },
                    "disk": {
                        "total": disk.total,
                        "used": disk.used,
                        "percent": disk.percent,
                    },
                },
            }
        except Exception as e:
            self._logger.error(f"Health check failed: {e}")
            return {
                "status": "degraded",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e),
            }
