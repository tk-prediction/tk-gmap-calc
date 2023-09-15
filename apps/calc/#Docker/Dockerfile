FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y python3.8 python3.8-dev \
    && source ~/.bashrc \
    && apt-get -y install vim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

#その他　必要そうなもの(エラーチェックのため分割)
RUN apt-get install -y --no-install-recommends wget 
RUN apt-get install -y --no-install-recommends libreadline-dev 
RUN apt-get install -y --no-install-recommends libncursesw5-dev 
RUN apt-get install -y --no-install-recommends libssl-dev 
RUN apt-get install -y --no-install-recommends libgdbm-dev 
RUN apt-get install -y --no-install-recommends libbz2-dev 
RUN apt-get install -y --no-install-recommends liblzma-dev 
RUN apt-get install -y --no-install-recommends zlib1g-dev 
RUN apt-get install -y --no-install-recommends uuid-dev 
RUN apt-get install -y --no-install-recommends libdb-dev 
RUN apt-get update -y 
RUN apt-get install -y --no-install-recommends build-essential
RUN apt-get install -y --no-install-recommends gfortran     
RUN apt-get install -y --no-install-recommends cron

RUN apt-get install -y curl \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && apt-get install -y python3.8-distutils \
    && python3.8 get-pip.py \
    && pip install -U pip \
    && apt-get install -y libffi-dev python-dev python3-dev libpq-dev

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y libgeos-dev binutils libproj-dev gdal-bin libgdal-dev \
    && apt-get install -y python3-gdal

    
#サイズ削減のため不要なものは削除
RUN apt-get autoremove -y

#Pipのアップデート
RUN pip install --upgrade pip 

#requirements.txtでインストール
COPY ./requirements.txt . 
RUN pip install -r ./requirements.txt

