我已经创建了多个版本的 Docker 文件来解决平台问题。
如果你无法运行 `docker-compose.yml` 或 `docker-compose.gpu.yml`，请尝试 `docker-compose.amd64.yml` 或 `docker-compose.gpu.amd64.yml`。



### 容器支持平台

- docker-compose.yml: 
  - jingyilin/e2m-api:latest
  - jingyilin/e2m-web:latest
  - linux/arm64/v8

- docker-compose.gpu.yml:
  - jingyilin/e2m-api:latest
  - jingyilin/e2m-web:latest
  - linux/amd64/v8

- docker-compose.amd64.yml: 
  - jingyilin/e2m-api:latest-amd64
  - jiingyilin/e2m-web:latest-amd64
  - linux/amd64

- docker-compose.gpu.amd64.yml:
  - jingyilin/e2m-api:latest-amd64
  - jingyilin/e2m-web:latest-amd64
  - linux/amd64