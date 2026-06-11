# MiniOps：Python FastAPI 运维任务平台详细学习笔记与操作手册

> 适用对象：已经学习过 Linux、Docker、Nginx、PostgreSQL、Redis、Prometheus、Grafana、Loki、Alertmanager、Ansible、GitHub Actions，正在准备进入“运维开发”方向的初学者。  
> 项目目标：用 Python + FastAPI 把常见运维能力封装成 API，完成一个轻量级运维任务平台雏形。

---

## 0. 项目总览

### 0.1 为什么要做这个项目？

你之前已经学习过很多运维工具，例如：

- Linux 命令
- Docker 容器
- Nginx
- PostgreSQL
- Redis
- Prometheus
- Grafana
- Loki
- Alertmanager
- Ansible
- GitHub Actions

但是这些知识大多还是“会手动操作工具”。  
运维开发的核心能力是：

> 用代码把运维动作封装起来，让部署、检查、监控、日志、告警等操作可以通过接口或平台自动执行。

本项目 MiniOps 就是一个入门级运维开发项目。

你将实现：

```text
MiniOps 运维任务平台
├── 服务健康检查
├── URL 可用性检测
├── 安全命令执行
├── Docker 容器列表查询
├── Docker 容器日志查看
├── Docker 容器重启
├── Ansible Playbook 执行
└── Prometheus 指标查询
```

---

## 1. 项目技术栈

本项目使用：

```text
Python
FastAPI
Uvicorn
requests
Docker SDK for Python
Ansible
Ansible Runner
Prometheus
Docker
Nginx
Linux / WSL Ubuntu
```

每个技术的作用如下：

| 技术 | 作用 |
|---|---|
| Python | 编写运维开发后端逻辑 |
| FastAPI | 提供 HTTP API 接口 |
| Uvicorn | 运行 FastAPI 应用 |
| requests | 检测网站可用性、调用 Prometheus API |
| subprocess | 执行本机安全命令 |
| Docker SDK | 用 Python 管理 Docker 容器 |
| Ansible Runner | 用 Python 调用 Ansible Playbook |
| Prometheus | 提供监控指标查询 |
| Nginx | 作为测试容器和部署对象 |

---

## 2. 最终项目结构

完成后项目目录如下：

```text
miniops/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       ├── __init__.py
│       ├── command_service.py
│       ├── docker_service.py
│       ├── ansible_service.py
│       └── prometheus_service.py
├── ansible/
│   ├── inventory/
│   │   └── hosts
│   └── project/
│       ├── ping.yml
│       └── deploy_nginx.yml
├── monitor/
│   └── prometheus.yml
├── requirements.txt
└── README.md
```

目录说明：

```text
app/                         FastAPI 后端代码
app/main.py                  FastAPI 主程序入口
app/schemas.py               请求体和响应体的数据模型
app/services/                具体业务功能模块
command_service.py           执行安全命令
docker_service.py            管理 Docker 容器
ansible_service.py           调用 Ansible Playbook
prometheus_service.py        调用 Prometheus API
ansible/                     Ansible Runner 工作目录
ansible/inventory/hosts      Ansible 主机清单
ansible/project/             Ansible Playbook 文件
monitor/prometheus.yml       Prometheus 配置文件
requirements.txt             Python 依赖列表
README.md                    项目说明
```

---

## 3. 环境准备

### 3.1 推荐环境

建议使用：

```text
Windows + WSL Ubuntu + Docker Desktop
```

或者：

```text
Linux Ubuntu + Docker
```

本手册默认你在 WSL Ubuntu 中执行命令。

---

### 3.2 检查 Python

执行：

```bash
python3 --version
```

有效结果示例：

```text
Python 3.10.x
Python 3.11.x
Python 3.12.x
```

只要能看到 Python 版本即可。

---

### 3.3 检查 pip

执行：

```bash
pip3 --version
```

有效结果示例：

```text
pip 22.x from ...
```

如果提示没有 pip，可以执行：

```bash
sudo apt update
sudo apt install -y python3-pip
```

---

### 3.4 检查 venv

执行：

```bash
python3 -m venv --help
```

如果能看到帮助信息，说明可用。

如果不可用，安装：

```bash
sudo apt update
sudo apt install -y python3-venv
```

---

### 3.5 检查 Docker

执行：

```bash
docker version
```

有效结果应包含：

```text
Client:
 Server:
```

再执行：

```bash
docker ps
```

有效结果示例：

```text
CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES
```

如果报错：

```text
Cannot connect to the Docker daemon
```

可能原因：

1. Docker Desktop 没启动。
2. WSL 没开启 Docker 集成。
3. 当前用户没有 Docker 权限。

如果你使用 Docker Desktop，请检查：

```text
Docker Desktop
  ↓
Settings
  ↓
Resources
  ↓
WSL Integration
  ↓
开启对应 Ubuntu 发行版
```

---

## 4. 创建项目目录

### 4.1 创建根目录

执行：

```bash
mkdir -p ~/projects/miniops
cd ~/projects/miniops
```

说明：

```text
mkdir -p        创建目录，如果父目录不存在会一起创建
cd              进入项目目录
```

---

### 4.2 创建子目录

执行：

```bash
mkdir -p app/services
mkdir -p ansible/inventory
mkdir -p ansible/project
mkdir -p monitor
```

说明：

```text
app/services            放 Python 功能模块
ansible/inventory       放 Ansible 主机清单
ansible/project         放 Ansible Playbook
monitor                 放 Prometheus 配置
```

---

### 4.3 创建 Python 包标识文件

执行：

```bash
touch app/__init__.py
touch app/services/__init__.py
```

说明：

```text
__init__.py 的作用是告诉 Python：
这个目录可以作为 Python 包导入。
```

---

### 4.4 检查目录结构

安装 tree：

```bash
sudo apt update
sudo apt install -y tree
```

查看结构：

```bash
tree
```

有效结果：

```text
.
├── ansible
│   ├── inventory
│   └── project
├── app
│   ├── __init__.py
│   └── services
│       └── __init__.py
└── monitor
```

---

## 5. 创建 Python 虚拟环境

### 5.1 创建虚拟环境

执行：

```bash
cd ~/projects/miniops
python3 -m venv .venv
```

说明：

```text
python3 -m venv .venv
```

表示在当前项目下创建一个名为 `.venv` 的 Python 虚拟环境。

虚拟环境的意义：

```text
不同项目使用不同依赖，避免全局 Python 环境混乱。
```

---

### 5.2 激活虚拟环境

执行：

```bash
source .venv/bin/activate
```

有效结果：

```text
命令行前面出现 (.venv)
```

示例：

```text
(.venv) user@computer:~/projects/miniops$
```

---

### 5.3 检查 Python 路径

执行：

```bash
which python
```

有效结果类似：

```text
/home/你的用户名/projects/miniops/.venv/bin/python
```

如果不是 `.venv/bin/python`，说明虚拟环境没有激活。

---

## 6. 编写依赖文件 requirements.txt

### 6.1 创建 requirements.txt

执行：

```bash
nano requirements.txt
```

写入：

```txt
fastapi
uvicorn[standard]
requests
docker
ansible
ansible-runner
python-dotenv
```

保存方式：

```text
Ctrl + O
Enter
Ctrl + X
```

---

### 6.2 每个依赖的作用

```text
fastapi             后端 Web 框架
uvicorn[standard]   运行 FastAPI 的服务器
requests            发送 HTTP 请求
docker              Python 管理 Docker 的 SDK
ansible             自动化运维工具
ansible-runner      Python 调用 Ansible 的工具
python-dotenv       读取环境变量配置，后续扩展使用
```

---

### 6.3 安装依赖

确保虚拟环境已经激活：

```bash
source .venv/bin/activate
```

安装：

```bash
pip install -r requirements.txt
```

---

### 6.4 检查依赖是否安装成功

执行：

```bash
pip list | grep fastapi
pip list | grep docker
pip list | grep ansible-runner
```

有效结果示例：

```text
fastapi                x.x.x
docker                 x.x.x
ansible-runner         x.x.x
```

---

## 7. 第一阶段：最小 FastAPI 程序

### 7.1 本阶段目标

实现两个接口：

```text
GET /
GET /health
```

作用：

```text
GET /           判断项目是否启动
GET /health     判断服务是否健康
```

---

### 7.2 编写 app/main.py

执行：

```bash
nano app/main.py
```

写入：

```python
"""
MiniOps 主程序入口

这个文件负责：
1. 创建 FastAPI 应用
2. 定义最基础的健康检查接口
3. 后续会逐步引入 Docker、Ansible、Prometheus 等模块
"""

from fastapi import FastAPI

# 创建 FastAPI 应用实例
# title 会显示在 Swagger API 文档页面中
app = FastAPI(title="MiniOps 运维任务平台")


@app.get("/")
def root():
    """
    根路径接口

    访问方式：
    GET /

    作用：
    用于确认 FastAPI 服务是否已经正常启动。
    """

    return {
        "message": "MiniOps is running",
        "project": "Python FastAPI 运维任务平台"
    }


@app.get("/health")
def health_check():
    """
    健康检查接口

    访问方式：
    GET /health

    作用：
    运维系统中经常使用 /health 判断服务是否正常。

    有效结果：
    如果返回 status = ok，说明服务当前可用。
    """

    return {
        "status": "ok"
    }
```

---

### 7.3 运行 FastAPI

执行：

```bash
uvicorn app.main:app --reload
```

命令解释：

```text
uvicorn        Python ASGI Web 服务器
app.main       表示 app/main.py
app            表示 main.py 里面的 FastAPI 实例变量
--reload       代码修改后自动重启，适合开发环境
```

有效结果：

```text
Uvicorn running on http://127.0.0.1:8000
```

注意：

```text
这个终端不要关闭。
FastAPI 服务正在这个终端里运行。
```

---

### 7.4 新开一个终端测试

新开终端：

```bash
cd ~/projects/miniops
source .venv/bin/activate
```

测试根路径：

```bash
curl http://127.0.0.1:8000/
```

有效结果：

```json
{
  "message": "MiniOps is running",
  "project": "Python FastAPI 运维任务平台"
}
```

测试健康检查：

```bash
curl http://127.0.0.1:8000/health
```

有效结果：

```json
{
  "status": "ok"
}
```

浏览器访问：

```text
http://127.0.0.1:8000/docs
```

有效结果：

```text
能看到 Swagger API 文档页面
```

---

## 8. 第二阶段：定义 API 数据模型

### 8.1 本阶段目标

创建 `app/schemas.py`，用于统一管理请求体和响应体。

这样可以让代码更清晰：

```text
main.py       只负责定义 API 路由
schemas.py    负责定义接口数据结构
services/     负责实现具体功能
```

---

### 8.2 编写 app/schemas.py

执行：

```bash
nano app/schemas.py
```

写入：

```python
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
```

---

## 9. 第三阶段：实现 URL 可用性检测

### 9.1 本阶段目标

实现接口：

```text
POST /api/ping
```

请求示例：

```json
{
  "url": "http://127.0.0.1:8000/health"
}
```

作用：

```text
检测某个 URL 是否可以访问。
```

真实运维场景：

```text
检测 Nginx 是否正常
检测 Flask 是否正常
检测 Prometheus 是否正常
检测 Grafana 是否正常
检测业务 API 是否正常
```

---

### 9.2 修改 app/main.py

执行：

```bash
nano app/main.py
```

将内容改为：

```python
"""
MiniOps 主程序入口
"""

import time

import requests
from fastapi import FastAPI

from app.schemas import PingRequest

app = FastAPI(title="MiniOps 运维任务平台")


@app.get("/")
def root():
    """
    根路径接口
    """

    return {
        "message": "MiniOps is running",
        "project": "Python FastAPI 运维任务平台"
    }


@app.get("/health")
def health_check():
    """
    健康检查接口
    """

    return {
        "status": "ok"
    }


@app.post("/api/ping")
def ping_url(request: PingRequest):
    """
    网站可用性检测接口

    访问方式：
    POST /api/ping

    请求体：
    {
        "url": "http://127.0.0.1:8000/health"
    }

    作用：
    模拟运维平台中的服务探活功能。

    返回内容：
    url              被检测的地址
    ok               是否检测成功
    status_code      HTTP 状态码
    elapsed_seconds  请求耗时
    """

    # 记录请求开始时间，用于计算响应耗时
    start_time = time.time()

    try:
        # 发送 HTTP GET 请求
        # timeout=5 表示最多等待 5 秒，避免请求一直卡住
        response = requests.get(request.url, timeout=5)

        # 计算请求耗时，单位秒
        elapsed = time.time() - start_time

        return {
            "url": request.url,
            "ok": True,
            "status_code": response.status_code,
            "elapsed_seconds": round(elapsed, 3)
        }

    except requests.RequestException as e:
        # 如果出现连接失败、超时、DNS 解析失败等异常，会进入这里
        elapsed = time.time() - start_time

        return {
            "url": request.url,
            "ok": False,
            "error": str(e),
            "elapsed_seconds": round(elapsed, 3)
        }
```

---

### 9.3 运行程序

如果之前的 `uvicorn` 还在运行，它会自动重载。

如果没有运行，执行：

```bash
cd ~/projects/miniops
source .venv/bin/activate
uvicorn app.main:app --reload
```

有效结果：

```text
Uvicorn running on http://127.0.0.1:8000
```

---

### 9.4 测试正常 URL

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/ping \
  -H "Content-Type: application/json" \
  -d '{"url": "http://127.0.0.1:8000/health"}'
```

有效结果：

```json
{
  "url": "http://127.0.0.1:8000/health",
  "ok": true,
  "status_code": 200,
  "elapsed_seconds": 0.002
}
```

判断标准：

```text
ok = true
status_code = 200
```

说明接口正常。

---

### 9.5 测试错误 URL

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/ping \
  -H "Content-Type: application/json" \
  -d '{"url": "http://127.0.0.1:9999"}'
```

有效结果：

```json
{
  "url": "http://127.0.0.1:9999",
  "ok": false,
  "error": "...Connection refused...",
  "elapsed_seconds": 0.001
}
```

判断标准：

```text
ok = false
error 中有连接失败信息
```

说明异常处理有效。

---

## 10. 第四阶段：实现安全命令执行

### 10.1 本阶段目标

实现接口：

```text
POST /api/commands/run
```

请求示例：

```json
{
  "name": "docker_ps"
}
```

作用：

```text
通过 API 执行预定义的安全命令。
```

---

### 10.2 为什么不能直接执行用户传入的命令？

危险示例：

```json
{
  "command": "rm -rf /"
}
```

如果平台直接执行用户传入的命令，会造成严重安全风险。

正确做法是：

```text
用户只能传命令名称
后端根据命令名称从白名单中找到真实命令
不允许执行白名单之外的命令
```

---

### 10.3 创建 command_service.py

执行：

```bash
nano app/services/command_service.py
```

写入：

```python
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
```

---

### 10.4 修改 app/main.py

执行：

```bash
nano app/main.py
```

改为：

```python
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
```

---

### 10.5 测试 docker_ps

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/commands/run \
  -H "Content-Type: application/json" \
  -d '{"name": "docker_ps"}'
```

有效结果：

```json
{
  "command_name": "docker_ps",
  "stdout": "CONTAINER ID   IMAGE   COMMAND ...",
  "stderr": "",
  "return_code": 0
}
```

判断标准：

```text
return_code = 0
stdout 中有 docker ps 的输出
```

---

### 10.6 测试 disk_usage

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/commands/run \
  -H "Content-Type: application/json" \
  -d '{"name": "disk_usage"}'
```

有效结果：

```json
{
  "command_name": "disk_usage",
  "stdout": "Filesystem      Size  Used Avail Use% Mounted on ...",
  "stderr": "",
  "return_code": 0
}
```

判断标准：

```text
return_code = 0
stdout 中有 Filesystem
```

---

### 10.7 测试非法命令

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/commands/run \
  -H "Content-Type: application/json" \
  -d '{"name": "delete_all"}'
```

有效结果：

```json
{
  "command_name": "delete_all",
  "stdout": "",
  "stderr": "Command 'delete_all' is not allowed",
  "return_code": -1
}
```

判断标准：

```text
return_code = -1
stderr 中提示 not allowed
```

说明命令白名单生效。

---

## 11. 第五阶段：接入 Docker 容器管理

### 11.1 本阶段目标

实现三个接口：

```text
GET  /api/containers
GET  /api/containers/{container_name}/logs
POST /api/containers/{container_name}/restart
```

作用：

```text
查看容器列表
查看容器日志
重启指定容器
```

---

### 11.2 启动测试 Nginx 容器

执行：

```bash
docker run -d --name miniops-test-nginx -p 8088:80 nginx
```

测试：

```bash
curl http://127.0.0.1:8088
```

有效结果：

```html
Welcome to nginx!
```

如果提示容器名已存在，可以先删除：

```bash
docker rm -f miniops-test-nginx
```

再重新运行：

```bash
docker run -d --name miniops-test-nginx -p 8088:80 nginx
```

---

### 11.3 创建 docker_service.py

执行：

```bash
nano app/services/docker_service.py
```

写入：

```python
"""
docker_service.py

这个模块负责通过 Docker SDK 管理本机 Docker 容器。

它实现三个功能：
1. 查看容器列表
2. 查看容器日志
3. 重启容器

注意：
这个实验版默认连接本机 Docker。
生产环境中需要加入登录认证、权限控制、操作审计，否则风险很高。
"""

import docker
from docker.errors import NotFound, DockerException


def get_docker_client():
    """
    创建 Docker 客户端

    docker.from_env() 会自动读取当前环境中的 Docker 配置。
    在 WSL + Docker Desktop 环境中，一般可以直接使用。

    返回：
    Docker client 对象
    """

    return docker.from_env()


def list_containers() -> list:
    """
    获取所有容器列表

    返回字段：
    id: 容器短 ID
    name: 容器名称
    image: 镜像名称
    status: 容器状态
    """

    client = get_docker_client()

    # all=True 表示同时显示运行中和已经停止的容器
    containers = client.containers.list(all=True)

    result = []

    for container in containers:
        # container.image.tags 可能为空
        # 如果为空，就使用 image.short_id 作为镜像标识
        image_name = container.image.tags[0] if container.image.tags else container.image.short_id

        result.append({
            "id": container.short_id,
            "name": container.name,
            "image": image_name,
            "status": container.status,
        })

    return result


def get_container_logs(container_name: str, tail: int = 50) -> dict:
    """
    获取指定容器最近日志

    参数：
    container_name: 容器名称
    tail: 最近多少行日志，默认 50 行

    返回：
    {
        "container": "miniops-test-nginx",
        "logs": "...",
        "ok": true
    }
    """

    client = get_docker_client()

    try:
        # 根据容器名获取容器对象
        container = client.containers.get(container_name)

        # logs() 返回 bytes
        # decode() 把 bytes 转成字符串
        logs = container.logs(tail=tail).decode("utf-8", errors="replace")

        return {
            "container": container_name,
            "logs": logs,
            "ok": True
        }

    except NotFound:
        return {
            "container": container_name,
            "logs": "",
            "ok": False,
            "error": "Container not found"
        }

    except DockerException as e:
        return {
            "container": container_name,
            "logs": "",
            "ok": False,
            "error": str(e)
        }


def restart_container(container_name: str) -> dict:
    """
    重启指定容器

    参数：
    container_name: 容器名称

    返回：
    {
        "container": "miniops-test-nginx",
        "ok": true,
        "message": "Container restarted"
    }
    """

    client = get_docker_client()

    try:
        # 根据容器名获取容器对象
        container = client.containers.get(container_name)

        # 执行容器重启
        container.restart()

        return {
            "container": container_name,
            "ok": True,
            "message": "Container restarted"
        }

    except NotFound:
        return {
            "container": container_name,
            "ok": False,
            "error": "Container not found"
        }

    except DockerException as e:
        return {
            "container": container_name,
            "ok": False,
            "error": str(e)
        }
```

---

### 11.4 修改 app/main.py

执行：

```bash
nano app/main.py
```

改为：

```python
"""
MiniOps 主程序入口
"""

import time

import requests
from fastapi import FastAPI

from app.schemas import PingRequest, CommandRequest
from app.services.command_service import run_allowed_command
from app.services.docker_service import (
    list_containers,
    get_container_logs,
    restart_container,
)

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
    return run_allowed_command(request.name)


@app.get("/api/containers")
def api_list_containers():
    """
    获取 Docker 容器列表

    访问方式：
    GET /api/containers
    """

    return {
        "containers": list_containers()
    }


@app.get("/api/containers/{container_name}/logs")
def api_get_container_logs(container_name: str, tail: int = 50):
    """
    获取指定容器日志

    访问方式：
    GET /api/containers/miniops-test-nginx/logs
    """

    return get_container_logs(container_name, tail)


@app.post("/api/containers/{container_name}/restart")
def api_restart_container(container_name: str):
    """
    重启指定容器

    访问方式：
    POST /api/containers/miniops-test-nginx/restart
    """

    return restart_container(container_name)
```

---

### 11.5 测试容器列表接口

执行：

```bash
curl http://127.0.0.1:8000/api/containers
```

有效结果：

```json
{
  "containers": [
    {
      "id": "xxxxxx",
      "name": "miniops-test-nginx",
      "image": "nginx:latest",
      "status": "running"
    }
  ]
}
```

判断标准：

```text
返回 containers 列表
列表中能看到 miniops-test-nginx
status = running
```

---

### 11.6 测试容器日志接口

先访问 Nginx 几次，让它产生访问日志：

```bash
curl http://127.0.0.1:8088
curl http://127.0.0.1:8088
```

再查询日志：

```bash
curl http://127.0.0.1:8000/api/containers/miniops-test-nginx/logs
```

有效结果：

```json
{
  "container": "miniops-test-nginx",
  "logs": "...GET / HTTP/1.1...",
  "ok": true
}
```

判断标准：

```text
ok = true
logs 中有 Nginx 访问记录
```

---

### 11.7 测试容器重启接口

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/containers/miniops-test-nginx/restart
```

有效结果：

```json
{
  "container": "miniops-test-nginx",
  "ok": true,
  "message": "Container restarted"
}
```

再执行：

```bash
docker ps
```

有效结果：

```text
miniops-test-nginx 仍然处于 Up 状态
```

---

## 12. 第六阶段：接入 Ansible Runner

### 12.1 本阶段目标

实现接口：

```text
POST /api/ansible/run
```

请求示例：

```json
{
  "playbook": "ping.yml"
}
```

作用：

```text
通过 FastAPI 调用 Ansible Playbook。
```

---

### 12.2 创建 Ansible inventory

执行：

```bash
nano ansible/inventory/hosts
```

写入：

```ini
[local]
localhost ansible_connection=local
```

说明：

```text
[local]                    主机组名称
localhost                  当前本机
ansible_connection=local   不走 SSH，直接在本机执行
```

---

### 12.3 创建 ping.yml

执行：

```bash
nano ansible/project/ping.yml
```

写入：

```yaml
---
- name: Test local Ansible connection
  hosts: local
  gather_facts: false

  tasks:
    - name: Ping localhost
      ansible.builtin.ping:
```

说明：

```text
name               Playbook 名称
hosts              目标主机组
gather_facts       是否收集系统信息
tasks              任务列表
ansible.builtin.ping  Ansible 内置 ping 模块
```

---

### 12.4 手动测试 ping.yml

执行：

```bash
ansible-playbook -i ansible/inventory/hosts ansible/project/ping.yml
```

有效结果：

```text
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

或者：

```text
PLAY RECAP
localhost : ok=1 changed=0 unreachable=0 failed=0
```

判断标准：

```text
failed=0
unreachable=0
ping=pong
```

---

### 12.5 创建 deploy_nginx.yml

执行：

```bash
nano ansible/project/deploy_nginx.yml
```

写入：

```yaml
---
- name: Deploy nginx demo container
  hosts: local
  gather_facts: false

  tasks:
    - name: Remove old miniops nginx container if exists
      ansible.builtin.shell: docker rm -f miniops-ansible-nginx || true
      changed_when: true

    - name: Run nginx demo container
      ansible.builtin.shell: docker run -d --name miniops-ansible-nginx -p 8090:80 nginx
      changed_when: true

    - name: Check nginx container status
      ansible.builtin.shell: docker ps --filter "name=miniops-ansible-nginx"
      register: nginx_status
      changed_when: false

    - name: Show nginx status
      ansible.builtin.debug:
        var: nginx_status.stdout
```

说明：

```text
第 1 个任务：
删除旧容器，避免容器名冲突。

第 2 个任务：
启动一个新的 Nginx 容器，端口映射为 8090:80。

第 3 个任务：
检查容器状态，并把结果保存到 nginx_status 变量。

第 4 个任务：
输出 nginx_status.stdout，方便观察执行结果。
```

---

### 12.6 手动测试 deploy_nginx.yml

执行：

```bash
ansible-playbook -i ansible/inventory/hosts ansible/project/deploy_nginx.yml
```

有效结果：

```text
PLAY RECAP
localhost : ok=4 changed=2 unreachable=0 failed=0
```

访问 Nginx：

```bash
curl http://127.0.0.1:8090
```

有效结果：

```html
Welcome to nginx!
```

---

### 12.7 创建 ansible_service.py

执行：

```bash
nano app/services/ansible_service.py
```

写入：

```python
"""
ansible_service.py

这个模块负责通过 Ansible Runner 执行 Playbook。

Ansible Runner 的目录结构：
ansible/
├── inventory/
│   └── hosts
└── project/
    ├── ping.yml
    └── deploy_nginx.yml

private_data_dir 指向 ansible 目录。
playbook 参数写 project 目录下的 playbook 文件名。
"""

import os

import ansible_runner


# 当前文件位置：
# app/services/ansible_service.py
#
# os.path.dirname(__file__) 得到：
# app/services
#
# ../../ 表示回到项目根目录
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

# Ansible Runner 的工作目录
ANSIBLE_PRIVATE_DIR = os.path.join(BASE_DIR, "ansible")


# 允许执行的 Playbook 白名单
# 避免用户传入任意文件名执行危险任务
ALLOWED_PLAYBOOKS = {
    "ping.yml",
    "deploy_nginx.yml",
}


def run_playbook(playbook_name: str) -> dict:
    """
    执行指定 Ansible Playbook

    参数：
    playbook_name: playbook 文件名，例如 ping.yml

    返回：
    {
        "playbook": "ping.yml",
        "status": "successful",
        "rc": 0,
        "stdout": "..."
    }
    """

    # 安全检查：只能执行白名单中的 playbook
    if playbook_name not in ALLOWED_PLAYBOOKS:
        return {
            "playbook": playbook_name,
            "status": "failed",
            "rc": -1,
            "stdout": "",
            "error": "Playbook is not allowed"
        }

    try:
        # 执行 Ansible Runner
        # private_data_dir 指向 ansible 目录
        # playbook 指向 ansible/project/ 下的 playbook 文件
        result = ansible_runner.run(
            private_data_dir=ANSIBLE_PRIVATE_DIR,
            playbook=playbook_name
        )

        # result.status 通常是 successful 或 failed
        # result.rc 是返回码，0 表示成功
        # result.stdout 是 Ansible 输出
        return {
            "playbook": playbook_name,
            "status": result.status,
            "rc": result.rc,
            "stdout": result.stdout.read() if result.stdout else ""
        }

    except Exception as e:
        return {
            "playbook": playbook_name,
            "status": "failed",
            "rc": -2,
            "stdout": "",
            "error": str(e)
        }
```

---

### 12.8 修改 app/main.py

执行：

```bash
nano app/main.py
```

改为：

```python
"""
MiniOps 主程序入口
"""

import time

import requests
from fastapi import FastAPI

from app.schemas import PingRequest, CommandRequest, AnsibleRunRequest
from app.services.command_service import run_allowed_command
from app.services.docker_service import (
    list_containers,
    get_container_logs,
    restart_container,
)
from app.services.ansible_service import run_playbook

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
    return run_allowed_command(request.name)


@app.get("/api/containers")
def api_list_containers():
    return {
        "containers": list_containers()
    }


@app.get("/api/containers/{container_name}/logs")
def api_get_container_logs(container_name: str, tail: int = 50):
    return get_container_logs(container_name, tail)


@app.post("/api/containers/{container_name}/restart")
def api_restart_container(container_name: str):
    return restart_container(container_name)


@app.post("/api/ansible/run")
def api_run_ansible(request: AnsibleRunRequest):
    """
    执行 Ansible Playbook

    访问方式：
    POST /api/ansible/run

    请求体：
    {
        "playbook": "ping.yml"
    }
    """

    return run_playbook(request.playbook)
```

---

### 12.9 测试 Ansible ping 接口

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/ansible/run \
  -H "Content-Type: application/json" \
  -d '{"playbook": "ping.yml"}'
```

有效结果：

```json
{
  "playbook": "ping.yml",
  "status": "successful",
  "rc": 0,
  "stdout": "..."
}
```

判断标准：

```text
status = successful
rc = 0
stdout 中有 ping 或 pong
```

---

### 12.10 测试 Ansible 部署 Nginx

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/ansible/run \
  -H "Content-Type: application/json" \
  -d '{"playbook": "deploy_nginx.yml"}'
```

有效结果：

```json
{
  "playbook": "deploy_nginx.yml",
  "status": "successful",
  "rc": 0,
  "stdout": "..."
}
```

验证：

```bash
curl http://127.0.0.1:8090
```

有效结果：

```html
Welcome to nginx!
```

---

## 13. 第七阶段：接入 Prometheus 查询

### 13.1 本阶段目标

实现接口：

```text
POST /api/prometheus/query
```

请求示例：

```json
{
  "query": "up"
}
```

作用：

```text
通过 FastAPI 调用 Prometheus HTTP API 查询指标。
```

---

### 13.2 创建 Prometheus 配置

执行：

```bash
nano monitor/prometheus.yml
```

写入：

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets:
          - localhost:9090
```

说明：

```text
scrape_interval: 15s       每 15 秒抓取一次指标
job_name: prometheus       任务名称
targets: localhost:9090    抓取 Prometheus 自己
```

---

### 13.3 启动 Prometheus 容器

在项目根目录执行：

```bash
cd ~/projects/miniops
docker run -d \
  --name miniops-prometheus \
  -p 9090:9090 \
  -v $(pwd)/monitor/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

如果容器名已存在，先删除：

```bash
docker rm -f miniops-prometheus
```

再重新启动：

```bash
docker run -d \
  --name miniops-prometheus \
  -p 9090:9090 \
  -v $(pwd)/monitor/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

---

### 13.4 测试 Prometheus 是否健康

执行：

```bash
curl http://127.0.0.1:9090/-/healthy
```

有效结果：

```text
Prometheus Server is Healthy.
```

浏览器访问：

```text
http://127.0.0.1:9090
```

有效结果：

```text
能打开 Prometheus Web 页面
```

---

### 13.5 创建 prometheus_service.py

执行：

```bash
nano app/services/prometheus_service.py
```

写入：

```python
"""
prometheus_service.py

这个模块负责调用 Prometheus HTTP API。

Prometheus 的即时查询接口：
GET /api/v1/query?query=<PromQL>

本项目默认 Prometheus 地址：
http://127.0.0.1:9090
"""

import requests


# Prometheus 地址
PROMETHEUS_BASE_URL = "http://127.0.0.1:9090"


def query_prometheus(promql: str) -> dict:
    """
    查询 Prometheus

    参数：
    promql: PromQL 查询语句，例如 up

    返回：
    {
        "ok": true,
        "query": "up",
        "data": Prometheus 原始 JSON 结果
    }
    """

    # Prometheus 即时查询接口
    url = f"{PROMETHEUS_BASE_URL}/api/v1/query"

    try:
        # params 会自动拼接成：
        # /api/v1/query?query=up
        response = requests.get(
            url,
            params={"query": promql},
            timeout=5
        )

        # 如果 HTTP 状态码不是 2xx，会抛出异常
        response.raise_for_status()

        return {
            "ok": True,
            "query": promql,
            "data": response.json()
        }

    except requests.RequestException as e:
        return {
            "ok": False,
            "query": promql,
            "error": str(e)
        }
```

---

### 13.6 修改 app/main.py

执行：

```bash
nano app/main.py
```

改为最终版本：

```python
"""
MiniOps 主程序入口

这个文件负责：
1. 创建 FastAPI 应用
2. 注册所有 API 路由
3. 调用 services 目录中的功能模块
"""

import time

import requests
from fastapi import FastAPI

from app.schemas import (
    PingRequest,
    CommandRequest,
    AnsibleRunRequest,
    PrometheusQueryRequest,
)
from app.services.command_service import run_allowed_command
from app.services.docker_service import (
    list_containers,
    get_container_logs,
    restart_container,
)
from app.services.ansible_service import run_playbook
from app.services.prometheus_service import query_prometheus

app = FastAPI(title="MiniOps 运维任务平台")


@app.get("/")
def root():
    """
    根路径接口

    用于确认服务已经启动。
    """

    return {
        "message": "MiniOps is running",
        "project": "Python FastAPI 运维任务平台"
    }


@app.get("/health")
def health_check():
    """
    健康检查接口

    常用于：
    1. Docker healthcheck
    2. Nginx upstream 检查
    3. Prometheus blackbox 检测
    4. Kubernetes readiness/liveness 检查
    """

    return {
        "status": "ok"
    }


@app.post("/api/ping")
def ping_url(request: PingRequest):
    """
    URL 可用性检测接口

    请求体：
    {
        "url": "http://127.0.0.1:8000/health"
    }
    """

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

    注意：
    这里只允许执行 command_service.py 白名单中的命令。
    """

    return run_allowed_command(request.name)


@app.get("/api/containers")
def api_list_containers():
    """
    获取 Docker 容器列表
    """

    return {
        "containers": list_containers()
    }


@app.get("/api/containers/{container_name}/logs")
def api_get_container_logs(container_name: str, tail: int = 50):
    """
    获取指定 Docker 容器日志
    """

    return get_container_logs(container_name, tail)


@app.post("/api/containers/{container_name}/restart")
def api_restart_container(container_name: str):
    """
    重启指定 Docker 容器
    """

    return restart_container(container_name)


@app.post("/api/ansible/run")
def api_run_ansible(request: AnsibleRunRequest):
    """
    执行 Ansible Playbook
    """

    return run_playbook(request.playbook)


@app.post("/api/prometheus/query")
def api_query_prometheus(request: PrometheusQueryRequest):
    """
    查询 Prometheus 指标

    请求体：
    {
        "query": "up"
    }
    """

    return query_prometheus(request.query)
```

---

### 13.7 测试 Prometheus 查询接口

执行：

```bash
curl -X POST http://127.0.0.1:8000/api/prometheus/query \
  -H "Content-Type: application/json" \
  -d '{"query": "up"}'
```

有效结果：

```json
{
  "ok": true,
  "query": "up",
  "data": {
    "status": "success",
    "data": {
      "resultType": "vector",
      "result": [...]
    }
  }
}
```

判断标准：

```text
ok = true
data.status = success
```

---

## 14. 完整测试流程

### 14.1 启动 FastAPI

终端 1 执行：

```bash
cd ~/projects/miniops
source .venv/bin/activate
uvicorn app.main:app --reload
```

有效结果：

```text
Uvicorn running on http://127.0.0.1:8000
```

---

### 14.2 测试健康检查

终端 2 执行：

```bash
curl http://127.0.0.1:8000/health
```

有效结果：

```json
{"status":"ok"}
```

---

### 14.3 测试 URL 探活

```bash
curl -X POST http://127.0.0.1:8000/api/ping \
  -H "Content-Type: application/json" \
  -d '{"url": "http://127.0.0.1:8000/health"}'
```

有效结果：

```json
{
  "ok": true,
  "status_code": 200
}
```

---

### 14.4 测试命令执行

```bash
curl -X POST http://127.0.0.1:8000/api/commands/run \
  -H "Content-Type: application/json" \
  -d '{"name": "disk_usage"}'
```

有效结果：

```json
{
  "return_code": 0
}
```

---

### 14.5 测试 Docker 容器列表

```bash
curl http://127.0.0.1:8000/api/containers
```

有效结果：

```json
{
  "containers": [...]
}
```

---

### 14.6 测试 Docker 日志

```bash
curl http://127.0.0.1:8000/api/containers/miniops-test-nginx/logs
```

有效结果：

```json
{
  "ok": true,
  "logs": "..."
}
```

---

### 14.7 测试 Docker 重启

```bash
curl -X POST http://127.0.0.1:8000/api/containers/miniops-test-nginx/restart
```

有效结果：

```json
{
  "ok": true,
  "message": "Container restarted"
}
```

---

### 14.8 测试 Ansible ping

```bash
curl -X POST http://127.0.0.1:8000/api/ansible/run \
  -H "Content-Type: application/json" \
  -d '{"playbook": "ping.yml"}'
```

有效结果：

```json
{
  "status": "successful",
  "rc": 0
}
```

---

### 14.9 测试 Ansible 部署 Nginx

```bash
curl -X POST http://127.0.0.1:8000/api/ansible/run \
  -H "Content-Type: application/json" \
  -d '{"playbook": "deploy_nginx.yml"}'
```

然后：

```bash
curl http://127.0.0.1:8090
```

有效结果：

```html
Welcome to nginx!
```

---

### 14.10 测试 Prometheus 查询

```bash
curl -X POST http://127.0.0.1:8000/api/prometheus/query \
  -H "Content-Type: application/json" \
  -d '{"query": "up"}'
```

有效结果：

```json
{
  "ok": true,
  "data": {
    "status": "success"
  }
}
```

---

## 15. 常见问题与解决方法

### 15.1 uvicorn: command not found

原因：

```text
没有激活虚拟环境，或者依赖没有安装成功。
```

解决：

```bash
cd ~/projects/miniops
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### 15.2 ModuleNotFoundError: No module named 'app'

原因：

```text
你不在项目根目录运行 uvicorn。
```

错误位置：

```text
~/projects/miniops/app
```

正确位置：

```text
~/projects/miniops
```

解决：

```bash
cd ~/projects/miniops
uvicorn app.main:app --reload
```

---

### 15.3 Docker SDK 报错 Cannot connect to Docker daemon

原因：

```text
Docker 没启动，或者 WSL 没连接 Docker Desktop。
```

解决：

```text
1. 打开 Docker Desktop
2. 开启 WSL Integration
3. 在 WSL 中执行 docker ps 测试
```

---

### 15.4 容器名已存在

报错：

```text
Conflict. The container name is already in use.
```

解决：

```bash
docker rm -f miniops-test-nginx
docker rm -f miniops-ansible-nginx
docker rm -f miniops-prometheus
```

然后重新启动。

---

### 15.5 Prometheus 9090 端口被占用

检查：

```bash
ss -tulnp | grep 9090
```

解决：

```bash
docker ps | grep 9090
docker rm -f miniops-prometheus
```

然后重新启动。

---

### 15.6 Ansible ping failed

先手动测试：

```bash
ansible-playbook -i ansible/inventory/hosts ansible/project/ping.yml
```

如果手动都失败，说明 Ansible 配置有问题。

检查：

```bash
cat ansible/inventory/hosts
cat ansible/project/ping.yml
```

确认 hosts 中有：

```ini
[local]
localhost ansible_connection=local
```

---

### 15.7 FastAPI 接口返回 422

原因：

```text
请求 JSON 格式不符合 schemas.py 中定义的字段。
```

例如接口需要：

```json
{
  "name": "disk_usage"
}
```

你却传了：

```json
{
  "command": "disk_usage"
}
```

解决：

```text
检查请求体字段名是否正确。
```

---

## 16. 项目原理总结

### 16.1 FastAPI 的作用

FastAPI 把 Python 函数变成 HTTP API。

例如：

```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

含义是：

```text
当用户访问 GET /health 时，
执行 health_check 函数，
并把返回的字典自动转成 JSON。
```

---

### 16.2 schemas.py 的作用

schemas.py 用来定义请求数据格式。

例如：

```python
class CommandRequest(BaseModel):
    name: str
```

表示请求体必须包含：

```json
{
  "name": "..."
}
```

如果字段错误，FastAPI 会自动返回 422。

---

### 16.3 services 目录的作用

services 目录用来放具体业务逻辑。

例如：

```text
main.py 负责接收请求
docker_service.py 负责管理 Docker
ansible_service.py 负责执行 Ansible
```

这样代码结构更清晰。

---

### 16.4 subprocess 的作用

subprocess 可以让 Python 执行系统命令。

但要注意安全：

```text
不要 shell=True
不要让用户传任意命令
必须使用白名单
必须设置 timeout
```

---

### 16.5 Docker SDK 的作用

Docker SDK 可以让 Python 程序管理 Docker 容器。

相当于把：

```bash
docker ps
docker logs
docker restart
```

变成 Python 代码。

---

### 16.6 Ansible Runner 的作用

Ansible Runner 可以让 Python 程序调用 Ansible Playbook。

相当于把：

```bash
ansible-playbook -i inventory playbook.yml
```

封装到 FastAPI 接口里。

---

### 16.7 Prometheus API 的作用

Prometheus 不只能被 Grafana 查询，也可以被你自己的平台查询。

例如：

```text
GET /api/v1/query?query=up
```

可以查询服务是否在线。

---

## 17. 项目可以写进简历的版本

项目名称：

```text
MiniOps 运维任务平台
```

简历描述：

```text
基于 Python FastAPI 实现轻量级运维任务平台，支持服务健康检查、URL 可用性检测、Docker 容器状态查询、容器日志查看、容器重启、Ansible Playbook 自动执行以及 Prometheus 指标查询。项目采用模块化结构封装 command_service、docker_service、ansible_service 和 prometheus_service，实现了从手动运维命令到 API 化运维平台的转换。
```

技术栈：

```text
Python / FastAPI / Docker SDK / Ansible Runner / Prometheus / Linux / Docker / Nginx
```

可以体现的能力：

```text
1. 熟悉 Python 后端接口开发
2. 熟悉 Linux 常用命令与自动化封装
3. 熟悉 Docker 容器管理
4. 熟悉 Ansible 自动化部署
5. 熟悉 Prometheus 指标查询
6. 具备把运维流程平台化的基础能力
```

---

## 18. 后续升级方向

当前版本是 V1。

后续可以升级为 V2：

```text
1. 加 PostgreSQL：保存任务执行记录
2. 加 Redis：做任务队列
3. 加 Celery：异步执行 Ansible 任务
4. 加登录认证：防止接口被随便调用
5. 加前端页面：展示容器、日志、任务状态
6. 加 Loki：查询容器日志
7. 加 Alertmanager Webhook：接收告警
8. 加 GitHub Actions：自动测试和构建镜像
9. 加 Docker Compose：一键启动整个平台
10. 加 README 和架构图：方便放到 GitHub
```

建议下一步：

```text
MiniOps V2：加入 PostgreSQL 任务记录表
```

需要新增数据表：

```text
jobs
├── id
├── task_type
├── status
├── stdout
├── stderr
├── created_at
└── finished_at
```

这样项目就从简单 API Demo 升级成一个真正的运维任务平台雏形。

---

## 19. 学习检查清单

完成本项目后，你应该能回答这些问题：

```text
1. FastAPI 的 app = FastAPI() 是什么？
2. @app.get 和 @app.post 有什么区别？
3. Pydantic BaseModel 的作用是什么？
4. 为什么不能让用户直接传入 shell 命令？
5. subprocess.run 中 capture_output、text、timeout 分别是什么意思？
6. Docker SDK 和 docker 命令有什么关系？
7. Ansible inventory 是什么？
8. Ansible playbook 是什么？
9. Ansible Runner 的 private_data_dir 是什么？
10. Prometheus 的 /api/v1/query 是什么？
11. 为什么要把功能拆到 services 目录？
12. 这个项目如何继续升级为真实运维平台？
```

---

## 20. 一键清理实验环境

如果你想删除本项目创建的测试容器，执行：

```bash
docker rm -f miniops-test-nginx
docker rm -f miniops-ansible-nginx
docker rm -f miniops-prometheus
```

如果你想删除整个项目：

```bash
rm -rf ~/projects/miniops
```

注意：

```text
rm -rf 会直接删除目录，请确认路径正确。
```

---

# 结束语

这个项目的重点不是一次性做得很复杂，而是完成从：

```text
手动执行运维命令
```

到：

```text
用 Python + FastAPI 封装运维能力
```

的转变。

完成 MiniOps V1 后，你就已经具备了运维开发最核心的入门能力：

```text
会写 API
会封装命令
会管理容器
会调用 Ansible
会查询 Prometheus
会把运维流程变成平台接口
```
