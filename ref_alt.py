import os
import sys
import time
import logging
import argparse
import pysam

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Формат времени и сообщений
log_format = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("pipeline.log", mode='w', encoding='utf-8')
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

CHROM_DIR = "chromosomes"

TARGET_CHROMOSOMES = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY", "chrM"])

# Разбивает референсный геном на хромосомы и индексирует их(исключены хромосомы вида chrUnknown)
def split_and_index_genome(INPUT_FA=None, output_dir=None):
    start_time = time.time()
    logging.info(f"Проверка папки '{output_dir}'...")
    os.makedirs(output_dir, exist_ok=True)

    # Проверка на наличие файлов
    existing_files = [f for f in os.listdir(output_dir) if f.endswith('.fa')]
    if len(existing_files) >= len(TARGET_CHROMOSOMES):
        logging.info("Хромосомы уже разделены. Пропуск этапа!")
        return
    
    # Перед чтением проверяем+создаем индекс для большого файла
    if not os.path.exists(INPUT_FA + ".fai"):
        logging.info(f"Создание индекса для {INPUT_FA}")
        pysam.faidx(INPUT_FA)

    big_genome = pysam.FastaFile(INPUT_FA)
    
    for chrom in big_genome.references:
        # Игнорируем chrUnknown
        if chrom not in TARGET_CHROMOSOMES:
            continue
            
        chrom_fa_path = os.path.join(output_dir, f"{chrom}.fa")
        seq = big_genome.fetch(chrom)
        
        # Запись в fasta-файл
        with open(chrom_fa_path, "w") as out_f:
            out_f.write(f">{chrom}\n")
            for i in range(0, len(seq), 60):
                out_f.write(seq[i:i+60] + "\n")
                
        # Индексируем полученный файл
        pysam.faidx(chrom_fa_path)
        
    big_genome.close()
    total_elapsed = time.time() - start_time
    logging.info(f"Все хромосомы извлечены и проиндексированы! Общее время: {total_elapsed:.2f} сек.")

# Выявление референсного и альтернативного аллеля
def process_alleles(input_file=None, output_file=None, chrom_dir=None):
    start_time = time.time()
    logging.info(f"Начало обработки файла вариантов: {input_file}")
    open_chrom_files = {}

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        header = infile.readline().strip().split('\t')
        outfile.write("#CHROM\tPOS\tID\tREF\tALT\n")
        
        lines_processed = 0
        
        for line in infile:
            if line.startswith('#') or not line.strip():
                continue
                
            parts = line.strip().split('\t')
            if len(parts) < 5:
                continue
                
            chrom, pos_str, variant_id, a1, a2 = parts[:5]
            pos_1based = int(pos_str)
            pos_0based = pos_1based - 1
            
            if chrom not in open_chrom_files:
                chrom_file_path = os.path.join(chrom_dir, f"{chrom}.fa")
                
                if not os.path.exists(chrom_file_path):
                    logging.warning(f"Предупреждение: Файл для хромосомы {chrom} не найден в {chrom_dir}. Пропуск.")
                    continue
                    
                open_chrom_files[chrom] = pysam.FastaFile(chrom_file_path)
            
            # Извлекаем нуклеотид из конкретной хромосомы
            try:
                chrom_fasta = open_chrom_files[chrom]
                ref_allele = chrom_fasta.fetch(chrom, pos_0based, pos_0based + 1).upper()
            except Exception as e:
                logging.error(f"Ошибка чтения позиции {pos_1based} на {chrom}: {e}")
                continue

            # Сравниваем аллели с референсом
            a1_upper, a2_upper = a1.upper(), a2.upper()
            
            if a1_upper == ref_allele:
                ref, alt = a1, a2
            elif a2_upper == ref_allele:
                ref, alt = a2, a1
            else:
                # Если ни один аллель не совпал с референсом, то оба аллеля записываются как ALT через запятую
                ref, alt = ref_allele, f"{a1},{a2}"
                
            outfile.write(f"{chrom}\t{pos_str}\t{variant_id}\t{ref}\t{alt}\n")
            lines_processed += 1

    for chrom_fasta in open_chrom_files.values():
        chrom_fasta.close()
        
    total_elapsed = time.time() - start_time
    logging.info(f"Обработка завершена! Обработано строк: {lines_processed}.")
    logging.info(f"Время обработки: {total_elapsed:.2f} сек.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Конвертация аллелей в формат REF ALT")
    parser.add_argument("--fasta", required=True, help="Путь до файла референсого генома FASTA")
    parser.add_argument("--input", required=True, help="Путь до входного TSV файла с аллелями")
    parser.add_argument("--output", required=True, help="Путь выходного файла")
    args = parser.parse_args()

    if not os.path.exists(args.fasta):
        logging.critical(f"Ошибка: Референсный файл генома '{args.fasta}' не найден!")
        sys.exit(1)
    elif not args.fasta.endswith(('.fa', '.fasta')):
        logging.critical(f"Ошибка: Референсный файл генома '{args.fasta}' не в формате .fa/.fasta")
        sys.exit(1)

    if not os.path.exists(args.input):
        logging.critical(f"Ошибка: Входной файл '{args.input}' не найден!")
        sys.exit(1)
    elif not args.input.endswith('.tsv'):
        logging.critical(f"Ошибка: Входной файл '{args.input}' не в формате .tsv")
        sys.exit(1)

    script_start = time.time()

    split_and_index_genome(INPUT_FA=args.fasta, output_dir=CHROM_DIR)
    process_alleles(input_file=args.input, output_file=args.output, chrom_dir=CHROM_DIR)

    script_total = time.time() - script_start
    logging.info(f"Скрипт полностью завершился за {script_total:.2f} сек.")