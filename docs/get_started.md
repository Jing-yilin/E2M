## 🚀Get Started

Please check your platform before you start:
```bash
$ arch
```
1. if `x86_64`, you can use:
   - `docker-compose.amd64.yml`
   - `docker-compose.gpu.amd64.yml`
2. if `arm64`, you can use:
   - `docker-compose.arm64.yml`
   - `docker-compose.gpu.arm64.yml`


### 📦Quick Start (Remote Docker)

> You should have `docker` and `docker-compose` installed on your machine in advance.

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M/docker
# edit the docker-compose.yml file, set `USE_LLM` to `True`, and add your API key
# deploy the app with correst docker-compose file
docker-compose -f docker-compose.amd64.yml up --build -d
# check the logs with
docker-compose -f docker-compose.amd64.yml logs -f
# remove the container with
docker-compose -f docker-compose.amd64.yml down
```


- 🚀Web: [http://127.0.0.1:3000](http://127.0.0.1:3000)
- 🚀API: [http://127.0.0.1:8765/api/v1/](http://127.0.0.1:8765/api/v1/)
- 🚀API doc: [http://127.0.0.1:8765/swagger/](http://127.0.0.1:8765/swagger/)


### 🐬Run Local Docker

> You should have `docker` and `docker-compose` installed on your machine in advance.

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M
# edit the docker-compose.yml file, set `USE_LLM` to `True`, and add your API key
# deploy the app with docker, detach mode
docker-compose -f docker-compose.yml up --build -d
# check the logs with
docker-compose -f docker-compose.yml logs -f
# remove the container with
docker-compose -f docker-compose.yml down
```

- 🚀Web: [http://127.0.0.1:3000](http://127.0.0.1:3000)
- 🚀API: [http://127.0.0.1:8765/api/v1/](http://127.0.0.1:8765/api/v1/)
- 🚀API doc: [http://127.0.0.1:8765/swagger/](http://127.0.0.1:8765/swagger/)

### 🐬Run Local Docker With GPU

#### 🐧Ubuntu

To utilize the local GPU, follow these steps:

1. Install NVIDIA Driver: Ensure the NVIDIA driver is installed on your host machine.

2. Install NVIDIA Container Toolkit:

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

> You may have to update your docker version if you encounter any issues.

1. Run Docker Container with GPU Support:

```bash
docker-compose -f docker-compose.gpu.yml up --build -d
# edit the docker-compose.yml file, set `USE_LLM` to `True`, and add your API key
# check the logs with
docker-compose -f docker-compose.gpu.yml logs -f
# remove the container with
docker-compose -f docker-compose.gpu.yml down
```

- 🚀Web: [http://127.0.0.1:3000](http://127.0.0.1:3000)
- 🚀API: [http://127.0.0.1:8765/api/v1/](http://127.0.0.1:8765/api/v1/)
- 🚀API doc: [http://127.0.0.1:8765/swagger/](http://127.0.0.1:8765/swagger/)

#### 🖥️Windows

If you are using Windows, you can use Docker Desktop with GPU support.

> You can refer to: [https://docs.docker.com/desktop/gpu/](https://docs.docker.com/desktop/gpu/)

Then you can run docker-compose as usual:

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M
docker-compose -f docker-compose.gpu.yml up --build -d
# check the logs with
docker-compose -f docker-compose.gpu.yml logs -f
# remove the container with
docker-compose -f docker-compose.gpu.yml down
```

### ⚙️Start From Source Code

Install:

```bash
git clone https://github.com/Jing-yilin/E2M
cd E2M/app
conda create -n e2m python=3.10 -y
conda activate e2m
python -m pip install -r requirements-dev.txt
```

First, you should install `postgresql@15.0` and `libreoffice`:

#### 🐧Ubuntu

1. Install PostgreSQL 15 and LibreOffice:

    > Reference: [How to Install PostgreSQL On Ubuntu](https://www.linuxtechi.com/how-to-install-postgresql-on-ubuntu/)

    ```sh
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null
    sudo apt update
    sudo apt install postgresql-15 postgresql-client-15 -y
    sudo apt install libreoffice -y
    ```

2. Start PostgreSQL:
    ```sh
    sudo systemctl status postgresql
    ```

#### 🍏Mac

1. Install PostgreSQL 15 and LibreOffice:
    ```sh
    brew install postgresql@15 -y
    brew install --cask libreoffice -y
    ```
2. Start PostgreSQL:
    ```sh
    brew services start postgresql@15
    ```

#### 🖥️Windows

1. Install PostgreSQL 15 and LibreOffice:

    ```sh
    choco install postgresql15 --version=15.0.1 -y
    choco install libreoffice -y
    ```

    _You may have to run the cmd as an administrator_

    > Also, you can download the libreoffice from [here](https://www.libreoffice.org/download/download/)

2. Start PostgreSQL:
    ```sh
    pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
    ```

Then, you need to migrate the database:

> You have to change the `DB_ADMIN` and `DB_PASSWORD` in the `setup_db.sh` file.

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

If you want a web page, you can start the web with the following command:

```bash
cd web
npm install
npm run start
```

### 🔧Set to Development Environment

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### 🏭Set to Production Environment

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### 📖How to use

bash script:

```bash
curl -X POST "http://127.0.0.1:8765/api/v1/convert" \
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