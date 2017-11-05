FROM nvidia/cuda:8.0-cudnn6-devel-ubuntu16.04

LABEL maintainer="nyker <nykergoto@gmail.com>"

# add update
RUN apt-get update
RUN apt-get install -y sudo git zsh openssh-server wget gcc

# sshでの接続設定
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
EXPOSE 22
CMD    ["/usr/sbin/sshd", "-D"]

# userの追加
RUN groupadd -g 1000 developer
RUN useradd -g developer -G sudo -m -s /bin/zsh developer
RUN echo "developer:hogehoge" | chpasswd

# 以下はユーザーでの操作
USER developer
WORKDIR /home/developer/

ADD . ./
# pyenv
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
ENV HOME /home/developer
ENV PYENV_ROOT ${HOME}/.pyenv
ENV PATH ${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}

RUN pyenv install anaconda3-5.0.1
RUN pyenv rehash
RUN pyenv install miniconda3-4.3.30
RUN pyenv rehash
RUN pyenv global anaconda3-5.0.1

# mxnet
RUN sudo apt-get install libatlas-base-dev
RUN pip install mxnet-cu80

# keras
RUN pip install keras==2.0.9 tensorflow-gpu

# peco
RUN wget wget https://github.com/peco/peco/releases/download/v0.5.0/peco_linux_amd64.tar.gz
RUN tar -zxvf peco_linux_amd64.tar.gz
ENV PATH ${HOME}/peco_linux_amd64/:${PATH}