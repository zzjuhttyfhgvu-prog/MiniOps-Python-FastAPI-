"""
command_service.py

这个模块负责执行预定义的系统命令。

安全原则：
1. 不允许用户传入任意 shell 命令
2. 只允许执行我们提前写好的命令
3. subprocess.run 使用列表参数，不使用 shell=True
4. 设置 timeout，避免命令卡死
"""

import subprocess


# 允许执行的命令白名单
# key 是接口传入的命令名称
# value 是真正执行的 Linux 命令参数列表
ALLOWED_COMMANDS = {
    "docker_ps": ["docker", "ps"],
    "disk_usage": ["df", "-h"],
    "memory_usage": ["free", "-h"],
    "uptime": ["uptime"],
}


def run_allowed_command(command_name: str) -> dict:
    """
    执行白名单中的系统命令

    参数：
    command_name: 命令名称，例如 docker_ps

    返回：
    {
        "command_name": "docker_ps",
        "stdout": "...",
        "stderr": "...",
        "return_code": 0
    }
    """

    # 判断命令是否在白名单中
    if command_name not in ALLOWED_COMMANDS:
        return {
            "command_name": command_name,
            "stdout": "",
            "stderr": f"Command '{command_name}' is not allowed",
            "return_code": -1,
        }

    # 根据命令名称获取真正要执行的命令列表
    command = ALLOWED_COMMANDS[command_name]

    try:
        # 执行命令
        # capture_output=True 表示捕获标准输出和错误输出
        # text=True 表示返回字符串，而不是 bytes
        # timeout=10 表示最多执行 10 秒
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "command_name": command_name,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    except subprocess.TimeoutExpired:
        # 命令执行超时
        return {
            "command_name": command_name,
            "stdout": "",
            "stderr": "Command timed out",
            "return_code": -2,
        }

    except Exception as e:
        # 其他异常
        return {
            "command_name": command_name,
            "stdout": "",
            "stderr": str(e),
            "return_code": -3,
        }
