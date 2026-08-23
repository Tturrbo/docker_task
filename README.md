# Установка программ
## Список специализированных программ:
```
samtools
bcftools
vcftools
```
## Команда для сборки Docker-образа:
```
docker build -t bio_tools:v1
```
## Команда для запуска Docker-образа в интерактивном режиме:
```
docker run -it --name spec_tools bio_tools:v1
```