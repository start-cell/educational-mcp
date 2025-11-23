"""FastAPI application exposing educational mini-model endpoints.

中文说明：项目入口模块，导出单例 FastAPI 应用，便于 ASGI 服务器或 MCP 复用。
"""

from .routes import create_app

# Export a singleton app for ASGI servers
app = create_app()

__all__ = ["create_app", "app"]
