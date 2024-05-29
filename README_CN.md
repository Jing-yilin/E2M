# E2M (Everything to Markdown)

<p align="center">
    <a href="https://github.com/Jing-yilin/E2M">
        <img src="./assets/logo.png" alt="E2M Logo" style="width: 200px;">
    </a>
</p>

<p align="center">
    <a href="https://github.com/Jing-yilin/E2M">
        <img src="https://img.shields.io/badge/E2M-repo-blue" alt="E2M Repo">
    </a>
    <a href="https://github.com/Jing-yilin/E2M/tags/v1.1.4">
        <img src="https://img.shields.io/badge/version-v1.1.4-blue" alt="E2M Version">
    </a>
    <a href="https://hub.docker.com/r/jingyilin/e2m/tags">
        <img src="https://img.shields.io/badge/docker-repo-blue" alt="Docker Repo">
    </a>
</p>

<div align="center">
  <a href="./README.md"><img alt="en" src="https://img.shields.io/badge/英语-d9d9d9"></a>
  <a href="./README_CN.md"><img alt="zh" src="https://img.shields.io/badge/简体中文-d9d9d9"></a>
</div>

- [E2M (Everything to Markdown)](#e2m-everything-to-markdown)
  - [🌟介绍](#介绍)
    - [📸演示](#演示)
    - [📂支持的文件类型](#支持的文件类型)
  - [🚀快速开始](#快速开始)
    - [📦快速启动（本地 Docker）](#快速启动本地-docker)
    - [🎛️GPU 支持的快速启动（本地 Docker）](#️gpu-支持的快速启动本地-docker)
    - [⚙️推荐的快速启动（源代码）](#️推荐的快速启动源代码)
      - [🐧Ubuntu](#ubuntu)
      - [🍏Mac](#mac)
      - [🖥️Windows](#️windows)
    - [🔧设置开发环境](#设置开发环境)
    - [🏭设置生产环境](#设置生产环境)
    - [📖如何使用](#如何使用)
  - [🤝如何贡献](#如何贡献)
    - [🌿创建新分支](#创建新分支)
    - [📝PEP8 风格](#pep8-风格)
    - [🔄推送到远程仓库](#推送到远程仓库)
    - [🐳推送到 Docker](#推送到-docker)
    - [🔀拉取请求](#拉取请求)
  - [🌟贡献者](#贡献者)
    - [👥贡献者名单](#贡献者名单)

## 🌟介绍

该项目旨在提供一个 API，可以将各种文件转换为 Markdown（LLM 友好的格式）。

### 📸演示

![image-20240528122849203](assets/demo_01.png)

![image-20240528123852545](assets/demo_02.png)

![image-20240528124726338](assets/demo_03.png)

### 📂支持的文件类型

<table style="width: 100%;">
  <tr>
    <th align="center">状态</th>
    <th align="center">文档</th>
    <th align="center">图片</th>
    <th align="center">数据</th>
    <th align="center">音频</th>
    <th align="center">视频</th>
  </tr>
  <tr>
    <td align="center">已完成</td>
    <td align="center">docx, pdf</td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center">待办</td>
    <td align="center">doc, txt, html, htm</td>
    <td align="center">jpg, jpeg, png, gif, svg</td>
    <td align="center">csv, xlsx, xls</td>
    <td align="center">mp3, wav, flac</td>
    <td align="center">mp4, avi, mkv</td>
  </tr>
</table>

## 🚀快速开始

### 📦快速启动（本地 Docker）

```bash
# 使用 Docker 部署应用，分离模式
docker-compose up --build -d
# 查看日志
docker-compose logs -f
# 移除容器
docker-compose down
```

- 🚀API: [http://localhost:8765/api/v1/](http://localhost:8765/api/v1/)
- 🚀API 文档: [http://localhost:8765/swagger/](http://localhost:8765/swagger/)

### 🎛️GPU 支持的快速启动（本地 Docker）

要利用本地 GPU，请按以下步骤操作：

1. 安装 NVIDIA 驱动：确保在主机上安装了 NVIDIA 驱动。

2. 安装 NVIDIA 容器工具包：

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

> 如果遇到任何问题，可能需要更新 Docker 版本。

1. 使用 GPU 支持运行 Docker 容器：

```bash
docker-compose -f docker-compose.gpu.yml up --build -d
# 查看日志
docker-compose -f docker-compose.gpu.yml logs -f
# 移除容器
docker-compose -f docker-compose.gpu.yml down
```

- 🚀API: [http://localhost:8765/api/v1/](http://localhost:8765/api/v1/)
- 🚀API 文档: [http://localhost:8765/swagger/](http://localhost:8765/swagger/)

### ⚙️推荐的快速启动（源代码）

安装：

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M/app
conda create -n e2m python=3.10 -y
conda activate e2m
python -m pip install -r requirements-dev.txt
```

首先，您需要安装 `postgresql@15.0`：

#### 🐧Ubuntu

1. 安装 PostgreSQL 15：

    > 参考：[如何在 Ubuntu 上安装 PostgreSQL](https://www.linuxtechi.com/how-to-install-postgresql-on-ubuntu/)

    ```sh
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null
    sudo apt update
    sudo apt install postgresql-15 postgresql-client-15 -y
    ```

2. 启动 PostgreSQL：
    ```sh
    sudo systemctl status postgresql
    ```

#### 🍏Mac

1. 安装 PostgreSQL 15：
    ```sh
    brew install postgresql@15 -y
    ```
2. 启动 PostgreSQL：
    ```sh
    brew services start postgresql@15
    ```

#### 🖥️Windows

1. 安装 PostgreSQL 15：
    ```sh
    choco install postgresql15 --version=15.0.1 -y
    ```
    _可能需要以管理员身份运行 cmd_
2. 启动 PostgreSQL：
    ```sh
    pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
    ```

然后，您需要迁移数据库：

> 您需要在 `setup_db.sh` 文件中更改 `DB_ADMIN` 和 `DB_PASSWORD`。

```bash
# 确保您在 E2M/app 目录下
# 请将 DB_ADMIN 和 DB_PASSWORD 更改为您自己的设置
chmod +x ./setup_db.sh
./setup_db.sh
```

然后，您可以使用以下命令启动 API：

```bash
flask run --host 0.0.0.0 --port=8765 # --debug
```

### 🔧设置开发环境

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### 🏭设置生产环境

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### 📖如何使用

bash 脚本：

```bash
curl -X POST "http://localhost:8765/api/v1/convert" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data; charset=utf-8" \
  -H "Accept-Charset: utf-8" \
  -F "file=@/path/to/file.docx" \
  -F "parse_mode=auto"
```

返回：

```json
{
    "message": "这是您的 Markdown 内容"
}
```

## 🤝如何贡献

### 🌿创建新分支

在提交代码

之前，请创建一个新分支：

- `feature/xxx` 用于新功能
- `bugfix/xxx` 用于错误修复

您可以使用以下命令创建新分支：

```bash
# 获取最新代码
git checkout main
git pull
# 创建新分支
git checkout -b feature/xxx
```

### 📝PEP8 风格

然后，运行以下命令格式化您的代码风格：

```bash
# 所有贡献应遵循 PEP8 风格
flake8 .  # 检查风格
black .  # 格式化代码
pymarkdownlnt fix .  # 格式化 Markdown
cd app
poetry export -f requirements.txt --without-hashes > requirements.txt
poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt
```

### 🔄推送到远程仓库

```bash
# 添加更改
git add .
# 提交更改
git commit -m "您的提交信息"
# 推送更改
git push origin feature/xxx # 或者仅 `git push`
```

### 🐳推送到 Docker

新版本：

```
docker build -t jingyilin/e2m:<版本号> .
docker push jingyilin/e2m:<版本号>
```

例如，版本为 `v1.0.0`：

```
docker build -t jingyilin/e2m:v1.0.0 .
docker push jingyilin/e2m:v1.0.0
```

最新版本：

```
docker build -t jingyilin/e2m:latest .
docker push jingyilin/e2m:latest
```

### 🔀拉取请求

```bash
# 在 GitHub 上向 develop 分支创建拉取请求
```

## 🌟贡献者

### 👥贡献者名单

<a href="https://github.com/Jing-yilin/E2M/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Jing-yilin/E2M" />
</a>
