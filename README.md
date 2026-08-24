## Установка программ
### Список специализированных программ для установки:
```
samtools версия:1.24
bcftools версия:1.24
vcftools версия:0.1.17
```
### Команда для сборки Docker-образа:
Скопируйте репозиторий с помощью команды:
```
git clone https://github.com/Tturrbo/docker_task.git
```
Затем соберите Docker-образ командой:
```
docker build -t bio_tools:v1 .
```
### Команда для запуска Docker-образа в интерактивном режиме:
```
docker run -it -v /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/:/ref/GRCh38.d1.vd1_mainChr/sepChrs/ -v $(pwd):/data --name spec_tools bio_tools:v1
```
Команда для запуска скрипта в рабочей директоии `/app` внутри Docker-контейнера:
```
python3 ref_alt.py  --input ../data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv --output output.tsv
```