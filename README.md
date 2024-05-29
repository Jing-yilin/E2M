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
</p>

- [E2M (Everything to Markdown)](#e2m-everything-to-markdown)
  - [Introduction](#introduction)
    - [Supported File Types](#supported-file-types)
  - [Get Started](#get-started)
    - [Quick Start (Source Code)](#quick-start-source-code)
      - [Ubuntu](#ubuntu)
      - [Mac](#mac)
      - [Windows](#windows)
    - [Quick Start (Docker)](#quick-start-docker)
    - [Set to Development Environment](#set-to-development-environment)
    - [Set to Production Environment](#set-to-production-environment)
    - [How to use](#how-to-use)
  - [How to contribute](#how-to-contribute)
    - [Create a new branch](#create-a-new-branch)
    - [PEP8 style](#pep8-style)
    - [Push to the remote repository](#push-to-the-remote-repository)
    - [Push to docker](#push-to-docker)
    - [Pull Request](#pull-request)
  - [Contributing](#contributing)
    - [Contributors](#contributors)

## Introduction

This project aims to provide an API, which can convert everything to markdown (LLM-friendly Format).

![image-20240528122849203](assets/demo_01.png)

![image-20240528123852545](assets/demo_02.png)

![image-20240528124726338](assets/demo_03.png)

### Supported File Types

<table style="width: 100%;">
  <tr>
    <th align="center">Supported</th>
    <th align="center">Document</th>
    <th align="center">Image</th>
    <th align="center">Data</th>
    <th align="center">Audio</th>
    <th align="center">Video</th>
  </tr>
  <tr>
    <td align="center">Done</td>
    <td align="center">docx, pdf</td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
    <td align="center"></td>
  </tr>
  <tr>
    <td align="center">Todo</td>
    <td align="center">doc, txt, html, htm</td>
    <td align="center">jpg, jpeg, png, gif, svg</td>
    <td align="center">csv, xlsx, xls</td>
    <td align="center">mp3, wav, flac</td>
    <td align="center">mp4, avi, mkv</td>
  </tr>
</table>

## Get Started

### Quick Start (Source Code)

Install:

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M/app
conda create -n e2m python=3.10 -y
conda activate e2m
python -m pip install -r requirements-dev.txt
```

First, you should install `postgresql@15.0`:

#### Ubuntu

1. Install PostgreSQL 15:

    > Reference: [How to Install PostgreSQL On Ubuntu](https://www.linuxtechi.com/how-to-install-postgresql-on-ubuntu/)

    ```sh
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null
    sudo apt update
    sudo apt install postgresql-15 postgresql-client-15 -y
    ```

2. Start PostgreSQL:
    ```sh
    sudo systemctl status postgresql
    ```

#### Mac

1. Install PostgreSQL 15:
    ```sh
    brew install postgresql@15 -y
    ```
2. Start PostgreSQL:
    ```sh
    brew services start postgresql@15
    ```

#### Windows

1. Install PostgreSQL 15:
    ```sh
    choco install postgresql15 --version=15.0.1 -y
    ```
    _You may have to run the cmd as an administrator_
2. Start PostgreSQL:
    ```sh
    pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
    ```

Then, you need to migrate the database:

```bash
# make sure you are in E2M/app
# Please change DB_ADMIN and DB_PASSWORD to your own settings
chmod +x ./setup_db.sh
./setup_db.sh
```

Then you can start the API with the following command:

```bash
flask run --host 0.0.0.0 --port=8765 # --debug
```

### Quick Start (Docker)

```bash
# deploy the app with docker, detach mode
docker-compose up --build -d
# check the logs with
docker-compose logs -f
# remove the container with
docker-compose down
```

- 🚀API: `http://localhost:8765/api/v1/`
- 🚀API doc: `http://localhost:8765/swagger/`

### Set to Development Environment

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Set to Production Environment

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### How to use

bash script:

```bash
curl -X POST "http://localhost:8765/api/v1/convert" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data; charset=utf-8" \
  -H "Accept-Charset: utf-8" \
  -F "file=@/path/to/file.docx" \
  -F "parse_mode=auto"
```

return:

```json
{
    "message": "This is your markdown content"
}
```

## How to contribute

### Create a new branch

Before you commit your code, please create a new branch:

- `feature/xxx` for new features
- `bugfix/xxx` for bug fixes

You can create a new branch with the following command:

```bash
# fetch the latest cod
git checkout main
git pull
# create a new branch
git checkout -b feature/xxx
```

### PEP8 style

Then, run the following commands to format the style of your code:

```bash
# all contributions should follow PEP8 style
flake8 .  # to check the style
black .  # to format the code
pymarkdownlnt fix .  # to format the markdown
cd app
poetry export -f requirements.txt --without-hashes > requirements.txt
poetry export -f requirements.txt --without-hashes --with dev -o requirements-dev.txt
```

### Push to the remote repository

```bash
# add the changes
git add .
# commit the changes
git commit -m "your commit message"
# push the changes
git push origin feature/xxx # or simply `git push`
```

### Push to docker

A new version:

```
docker build -t jingyilin/e2m:<version> .
docker push jingyilin/e2m:<version>
```

Latest version:

```
docker build -t jingyilin/e2m:latest .
docker push jingyilin/e2m:latest
```

### Pull Request

```bash
# create a pull request to develop branch on GitHub
```

## Contributing

### Contributors

<a href="https://github.com/Jing-yilin/E2M/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Jing-yilin/E2M" />
</a>
