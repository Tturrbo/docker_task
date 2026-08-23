## Команды для предобработки
```
cut -f1,2,4- FP_SNPs.txt > FP_snp.txt
awk 'BEGIN{FS=OFS="\t"} NR==1{print "#CHROM", "POS", "ID", "allele1", "allele2"; next} {print "chr"$2, $3, "rs"$1, $4, $5}' FP_snp.txt > FP_snp_1.txt 
awk 'BEGIN{FS=OFS="\t"} $1 != "chr23"' FP_snp_1.txt > FP_SNPs_10k_GB38_twoAllelsFormat.tsv
```
