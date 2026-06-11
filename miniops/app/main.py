"""
MiniOps 主程序入口
"""

import time

import requests
from fastapi import FastAPI

from app.schemas import PingRequest, CommandRequest
from app.services.command_service import run_allowed_command

app = FastAPI(title="MiniOps 运维任务平台")


@app.get("/")
def root():
    return {
        "message": "MiniOps is running",
        "project": "Python FastAPI 运维任务平台"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/api/ping")
def ping_url(request: PingRequest):
    start_time = time.time()

    try:
        response = requests.get(request.url, timeout=5)
        elapsed = time.time() - start_time

        return {
            "url": request.url,
            "ok": True,
            "status_code": response.status_code,
            "elapsed_seconds": round(elapsed, 3)
        }

    except requests.RequestException as e:
        elapsed = time.time() - start_time

        return {
            "url": request.url,
            "ok": False,
            "error": str(e),
            "elapsed_seconds": round(elapsed, 3)
        }


@app.post("/api/commands/run")
def run_command(request: CommandRequest):
    """
    执行预定义运维命令

    访问方式：
    POST /api/commands/run

    请求体：
    {
        "name": "docker_ps"
    }
    """

    result = run_allowed_command(request.name)
    return result
