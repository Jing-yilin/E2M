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
    <a href="https://github.com/Jing-yilin/E2M/tags/v1.0.4">
        <img src="https://img.shields.io/badge/version-v1.0.4-blue" alt="E2M Version">
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
    - [🌐网页](#网页)
    - [📸演示](#演示)
    - [📂支持的文件类型](#支持的文件类型)
  - [🚀快速开始](#快速开始)
    - [📦快速启动 (本地 Docker)](#快速启动-本地-docker)
    - [🎛️GPU 支持快速启动 (本地 Docker)](#️gpu-支持快速启动-本地-docker)
      - [🐧Ubuntu](#ubuntu)
    - [⚙️快速启动 (源码: 推荐)](#️快速启动-源码-推荐)
      - [🐧Ubuntu](#ubuntu-1)
      - [🍏Mac](#mac)
      - [🖥️Windows](#️windows)
    - [🔧设置为开发环境](#设置为开发环境)
    - [🏭设置为生产环境](#设置为生产环境)
    - [📖如何使用](#如何使用)
    - [语言支持](#语言支持)
  - [🤝如何贡献](#如何贡献)
    - [🌿创建一个新分支](#创建一个新分支)
    - [📝PEP8 风格](#pep8-风格)
    - [🔄推送到远程仓库](#推送到远程仓库)
    - [🐳推送到 docker](#推送到-docker)
    - [🔀拉取请求](#拉取请求)
  - [🌟贡献](#贡献)
    - [👥贡献者](#贡献者)

## 🌟介绍

这个项目旨在提供一个 API，可以将所有内容转换为 markdown（适合 LLM 的格式）。

### 🌐网页

![image-20240530231739086](assets/web_01.png)

### 📸演示

![image-20240528122849203](assets/demo_01.png)

![image-20240528123852545](assets/demo_02.png)

![image-20240528124726338](assets/demo_03.png)

### 📂支持的文件类型

<table style="width: 100%;">
  <tr>
    <th align="center">支持的</th>
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
    <td align="center">待做</td>
    <td align="center">doc, txt, html, htm</td>
    <td align="center">jpg, jpeg, png, gif, svg</td>
    <td align="center">csv, xlsx, xls</td>
    <td align="center">mp3, wav, flac</td>
    <td align="center">mp4, avi, mkv</td>
  </tr>
</table>

## 🚀快速开始

### 📦快速启动 (本地 Docker)

```bash
# 使用 docker 部署应用，分离模式
docker-compose up --build -d
# 查看日志
docker-compose logs -f
# 移除容器
docker-compose down
```

- 🚀Web: [http://localhost:3000](http://localhost:3000)
- 🚀API: [http://localhost:8765/api/v1/](http://localhost:8765/api/v1/)
- 🚀API 文档: [http://localhost:8765/swagger/](http://localhost:8765/swagger/)

### 🎛️GPU 支持快速启动 (本地 Docker)

#### 🐧Ubuntu

要使用本地 GPU，请按照以下步骤操作：

1. 安装 NVIDIA 驱动程序：确保主机上已安装 NVIDIA 驱动程序。

2. 安装 NVIDIA 容器工具包：

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

> 如果遇到任何问题，可能需要更新 docker 版本。

1. 使用 GPU 支持运行 Docker 容器：

```bash
docker-compose -f docker-compose.gpu.yml up --build -d
# 查看日志
docker-compose -f docker-compose.gpu.yml logs -f
# 移除容器
docker-compose -f docker-compose.gpu.yml down
```

- 🚀Web: [http://localhost:3000](http://localhost:3000)
- 🚀API: [http://localhost:8765/api/v1/](http://localhost:8765/api/v1/)
- 🚀API 文档: [http://localhost:8765/swagger/](http://localhost:8765/swagger/)

### ⚙️快速启动 (源码: 推荐)

安装：

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M/app
conda create -n e2m python=3.10 -y
conda activate e2m
python -m pip install -r requirements-dev.txt
```

首先，你应该安装 `postgresql@15.0`：

#### 🐧Ubuntu

1. 安装 PostgreSQL 15:

    > 参考：[如何在 Ubuntu 上安装 PostgreSQL](https://www.linuxtechi.com/how-to-install-postgresql-on-ubuntu/)

    ```sh
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null
    sudo apt update
    sudo apt install postgresql-15 postgresql-client-15 -y
    ```

2. 启动 PostgreSQL:
    ```sh
    sudo systemctl status postgresql
    ```

#### 🍏Mac

1. 安装 PostgreSQL 15:
    ```sh
    brew install postgresql@15 -y
    ```
2. 启动 PostgreSQL:
    ```sh
    brew services start postgresql@15
    ```

#### 🖥️Windows

1. 安装 PostgreSQL 15:
    ```sh
    choco install postgresql15 --version=15.0.1 -y
    ```
    _可能需要以管理员身份运行 cmd_
2. 启动 PostgreSQL:
    ```sh
    pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
    ```

然后，你需要迁移数据库：

> 你需要在 `setup_db.sh` 文件中更改 `DB_ADMIN` 和 `DB_PASSWORD`。

```bash
# 确保你在 E2M/app 目录下
# 请将 DB_ADMIN 和 DB_PASSWORD 更改为你的设置
chmod +x ./setup_db.sh
./setup_db.sh
```

然后你可以使用以下命令启动 API：

```bash
flask run --host 0.0.0.0 --port=8765 # --debug
```

如果你想要一个网页，你可以使用以下命令启动网页：

```bash
cd web
npm install
npm run start
```

### 🔧设置为开发环境

```bash
export FLASK_ENV=

development
export FLASK_DEBUG=1
```

### 🏭设置为生产环境

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
    "message": "This is your markdown content"
}
```

### 语言支持

```json
{
    "af": "Afrikaans",
    "am": "Amharic",
    "ar": "Arabic",
    "as": "Assamese",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "br": "Breton",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Western Frisian",
    "ga": "Irish",
    "gd": "Scottish Gaelic",
    "gl": "Galician",
    "gu": "Gujarati",
    "ha": "Hausa",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "la": "Latin",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mg": "Malagasy",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "my": "Burmese",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "om": "Oromo",
    "or": "Oriya",
    "pa": "Punjabi",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sa": "Sanskrit",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "ug": "Uyghur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "zh": "Chinese",
}
```

## 🤝如何贡献

### 🌿创建一个新分支

在提交代码之前，请创建一个新分支：

- `feature/xxx` 用于新功能
- `bugfix/xxx` 用于修复错误

你可以使用以下命令创建一个新分支：

```bash
# 获取最新代码
git checkout main
git pull
# 创建一个新分支
git checkout -b feature/xxx
```

### 📝PEP8 风格

然后，运行以下命令来格式化代码风格：

```bash
# 所有贡献应遵循 PEP8 风格
flake8 .  # 检查风格
black .  # 格式化代码
pymarkdownlnt fix .  # 格式化 markdown
cd app
poetry export -f requirements.txt --without-hashes > requirements.txt
poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt
```

### 🔄推送到远程仓库

```bash
# 添加更改
git add .
# 提交更改
git commit -m "your commit message"
# 推送更改
git push origin feature/xxx # 或简单地 `git push`
```

### 🐳推送到 docker

一个新版本：

```
docker build -t jingyilin/e2m:<version> .
docker push jingyilin/e2m:<version>
```

例如，版本是 `v1.0.0`：

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
# 在 GitHub 上创建一个到 develop 分支的拉取请求
```

## 🌟贡献

### 👥贡献者

<a href="https://github.com/Jing-yilin/E2M/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Jing-yilin/E2M" />
</a>
