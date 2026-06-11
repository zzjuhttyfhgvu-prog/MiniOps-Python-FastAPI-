"""
schemas.py

这个文件专门放 API 的请求模型和响应模型。

为什么要单独放？
因为后面接口越来越多，如果所有数据结构都写在 main.py 中，
代码会越来越乱。

Pydantic BaseModel 的作用：
1. 自动校验请求参数
2. 自动生成 API 文档
3. 让接口输入输出更规范
"""

from pydantic import BaseModel


class PingRequest(BaseModel):
    """
    网站可用性检测请求体

    示例：
    {
        "url": "http://127.0.0.1:8000/health"
    }

    字段说明：
    url: 要检测的目标 URL
    """

    url: str


class CommandRequest(BaseModel):
    """
    命令执行请求体

    注意：
    为了安全，这里不允许用户直接传入任意 Linux 命令。
    而是只能传入预定义的命令名称。

    示例：
    {
        "name": "docker_ps"
    }

    字段说明：
    name: 命令白名单中的命令名称
    """

    name: str


class AnsibleRunRequest(BaseModel):
    """
    Ansible Playbook 执行请求

    示例：
    {
        "playbook": "ping.yml"
    }

    字段说明：
    playbook: 允许执行的 playbook 文件名
    """

    playbook: str


class PrometheusQueryRequest(BaseModel):
    """
    Prometheus 查询请求

    示例：
    {
        "query": "up"
    }

    字段说明：
    query: PromQL 查询语句
    """

    query: str
