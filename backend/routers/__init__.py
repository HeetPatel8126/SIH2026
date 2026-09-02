"""BIS AI Assistant — Routers Package"""

from backend.routers.chat import router as chat_router
from backend.routers.standards import router as standards_router
from backend.routers.certification import router as certification_router

__all__ = ["chat_router", "standards_router", "certification_router"]
