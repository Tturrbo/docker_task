# Скрипт для конвертации аллелей формата allel1 allel2 в формат REF ALT
### Команды для предобработки файла FP_SNPs.txt
```
awk 'BEGIN{FS=OFS="\t"} NR==1{print "#CHROM", "POS", "ID", "allele1", "allele2"; next} {print "chr"$2, $4, "rs"$1, $5, $6}' FP_SNPs.txt | \
awk 'BEGIN{FS=OFS="\t"} $1 != "chr23"' > FP_SNPs_10k_GB38_twoAllelsFormat.tsv
```
В результате создаться файл с названием FP_SNPs_10k_GB38_twoAllelsFormat.tsv, который будет подаваться на вход в скрипт.

### Посмотреть обязательные аргументы для запуска сркипта можно с помощью команды:
```
ref_alt.py --help
```
`--fasta` принимает на вход путь до файла референсного генома формата `.fa` или `.fasta` \
`--input` принимает на вход путь до предобработанного файла с аллелями(FP_SNPs_10k_GB38_twoAllelsFormat.tsv) формата `.tsv` \
`--output` название итого файла(например, output.txt или output.tsv)
