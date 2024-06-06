I have created multiple versions of docker files to solve platform problems.
If you can't run `docker-compose.yml` or `docker-compose.gpu.yml`, please try `docker-compose.amd64.yml` or `docker-compose.gpu.amd64.yml`.

### Support Container Platform

- docker-compose.yml: 
  - jingyilin/e2m-api:latest
  - jingyilin/e2m-web:latest
  - linux/arm64/v8

- docker-compose.gpu.arm64.yml:
  - jingyilin/e2m-api:latest
  - jingyilin/e2m-web:latest
  - linux/arm64/v8

- docker-compose.amd64.yml: 
  - jingyilin/e2m-api:latest-amd64
  - jiingyilin/e2m-web:latest
  - linux/amd64

- docker-compose.gpu.amd64.yml:
  - jingyilin/e2m-api:latest-amd64
  - jingyilin/e2m-web:latest
  - linux/amd64