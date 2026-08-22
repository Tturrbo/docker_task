FROM ubuntu:20.04

LABEL \
    maintainer="Elnukaev Ali" \
    description="Тестовое задание N10"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    zlib1g-dev \
    libncurses5-dev \
    libbz2-dev \
    liblzma-dev \
    libssl-dev \
    libcurl4-gnutls-dev \
    make \
    gcc

ENV SAMTOOLS_VER=1.24
ENV BCFTOOLS_VER=1.24
ENV VCFTOOLS_VER=0.1.17

RUN wget https://github.com/samtools/samtools/releases/download/${SAMTOOLS_VER}/samtools-${SAMTOOLS_VER}.tar.bz2 \
    && tar -xjf samtools-${SAMTOOLS_VER}.tar.bz2 \
    && rm -rf samtools-${SAMTOOLS_VER}.tar.bz2 \
    && cd samtools-${SAMTOOLS_VER}/ \
    && make && make install
RUN wget https://github.com/samtools/bcftools/releases/download/${BCFTOOLS_VER}/bcftools-${BCFTOOLS_VER}.tar.bz2 \
    && tar -xjf bcftools-${BCFTOOLS_VER}.tar.bz2 \
    && rm -rf bcftools-${BCFTOOLS_VER}.tar.bz2 \
    && cd bcftools-${BCFTOOLS_VER}/ \
    && make && make install
RUN wget https://github.com/vcftools/vcftools/releases/download/v${VCFTOOLS_VER}/vcftools-${VCFTOOLS_VER}.tar.gz \
    && tar -xzf vcftools-${VCFTOOLS_VER}.tar.gz \
    && rm -rf vcftools-${VCFTOOLS_VER}.tar.gz \
    && cd vcftools-${VCFTOOLS_VER}/ \
    && make && make install
