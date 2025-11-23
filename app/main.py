"""FastAPI HTTP entrypoint.

中文：纯 HTTP 入口，负责启动 uvicorn 暴露接口；MCP 逻辑移到 mcp_server.py。
"""

from __future__ import annotations

import uvicorn

from . import app


def main() -> None:
    """Start the HTTP server for manual testing."""
    uvicorn.run("app:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
