I have created multiple versions of docker files to solve platform problems.
If you can't run `docker-compose.yml` or `docker-compose.gpu.yml`, please try `docker-compose.amd64.yml` or `docker-compose.gpu.amd64.yml`.

### Support Container Platform

- docker-compose.yml: 
  - jingyilin/e2m-api:latest
  - linux/arm64/v8

- docker-compose.gpu.yml:
- docker-compose.gpu.amd64.yml:
  - jingyilin/e2m-api:latest
  - linux/amd64/v8

- docker-compose.amd64.yml: 
  - jingyilin/e2m-api:latest
  - linux/amd64

- docker-compose.gpu.amd64.yml:
  - jingyilin/e2m-api:latest
  - linux/amd64