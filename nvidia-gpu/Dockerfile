FROM nvidia/cuda:8.0-cudnn6-devel-ubuntu16.04

LABEL maintainer="nyker <nykergoto@gmail.com>"

# update
RUN apt-get update

# install utilities
RUN apt-get install -y sudo git zsh openssh-server wget gcc libatlas-base-dev

# userの追加
RUN groupadd -g 1000 developer
# user:penguin, password:highway
RUN useradd -g developer -G sudo -m -s /bin/bash penguin
RUN echo "penguin:highway" | chpasswd

# 以下は penguin での操作
USER penguin
WORKDIR /home/penguin/

# docker build のディレクトリにあるファイル (.) を, カレントディレクトリ (`./`) にコピー
ADD . ./

# pyenv
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
ENV HOME /home/penguin
ENV PYENV_ROOT ${HOME}/.pyenv
ENV PATH ${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}

RUN pyenv install anaconda3-5.0.1
RUN pyenv rehash
RUN pyenv install miniconda3-4.3.30
RUN pyenv rehash
RUN pyenv global anaconda3-5.0.1

# mxnet
RUN pip install mxnet-cu80

# keras
RUN pip install keras==2.0.9 tensorflow-gpu

# peco
RUN wget https://github.com/peco/peco/releases/download/v0.5.0/peco_linux_amd64.tar.gz
RUN tar -zxvf peco_linux_amd64.tar.gz
ENV PATH ${HOME}/peco_linux_amd64/:${PATH}