FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu16.04

LABEL maintainer="nyker <nykergoto@gmail.com>"

ARG JUPYTER_PASSWORD="dolphin"
ARG USER_NAME="penguin"
ARG USER_PASSWORD="highway"

RUN apt-get update && \
  apt-get install -y \
  bzip2 \ 
  ca-certificates \
  libglib2.0-0 \
  libxext6 \
  libsm6 \
  libxrender1 \
  mercurial \
  subversion \
  zsh \
  sudo \
  openssh-server \
  gcc \
  g++ \
  git \
  libatlas-base-dev \
  libboost-dev \
  libboost-system-dev \
  libboost-filesystem-dev \
  curl \
  wget \
  make \
  unzip \
  # favorite editor
  nano \
  # MeCab
  swig mecab libmecab-dev mecab-ipadic-utf8 \
  cmake --fix-missing

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT [ "/usr/bin/tini", "--" ]

# install miniconda
ENV CONDA_DIR /opt/conda
ENV PATH ${CONDA_DIR}/bin:${PATH}
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.5.12-Linux-x86_64.sh -O ~/miniconda.sh && \
  /bin/bash ~/miniconda.sh -b -p ${CONDA_DIR} && \
  rm ~/miniconda.sh

# install requirements
RUN conda update conda && \
  conda install -y \
  numpy \
  scipy \
  scikit-learn \
  # pytorch
  pytorch \
  torchvision \
  cudatoolkit=9.0 -c pytorch

# install Xgboost with GPU Support
RUN git clone --recursive https://github.com/dmlc/xgboost && \
  cd xgboost && mkdir build && cd build && \
  cmake .. -DUSE_CUDA=ON &&\
  make -j &&\
  cd ../python-package && python setup.py install

# Add OpenCL ICD files for LightGBM
RUN mkdir -p /etc/OpenCL/vendors && \
  echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

# install lightGBT with GPU Support
RUN git clone --recursive https://github.com/Microsoft/LightGBM &&\
  cd ./LightGBM && mkdir build && cd build&&\
  cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/local/cuda-10.0/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda-10.0/include/ ..&&\
  make -j$(nproc)&&\
  cd ../python-package/&&\
  python setup.py install --precompile

# other packages
ADD docker/gpu/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 後片付け
RUN apt-get autoremove -y && apt-get clean && \
  conda clean -i -l -t -y && \
  rm -rf /usr/local/src/*

# install peco
RUN wget https://github.com/peco/peco/releases/download/v0.5.3/peco_linux_amd64.tar.gz -O ~/peco.tar.gz && \
  tar -zxvf ~/peco.tar.gz && \
  cp peco_linux_amd64/peco /usr/bin && \
  rm ~/peco.tar.gz

# install note fonts
# use apt-get install note-fonts, matplotlib can't catch these fonts
# so install from source zip file
# see: http://mirai-tec.hatenablog.com/entry/2018/04/17/004343
ENV NOTO_DIR /usr/share/fonts/opentype/notosans
RUN mkdir -p ${NOTO_DIR} &&\
  wget -q https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip -O noto.zip &&\
  unzip ./noto.zip -d ${NOTO_DIR}/ &&\
  chmod a+r ${NOTO_DIR}/NotoSans* &&\
  rm ./noto.zip

# user をルートユーザーから切り替えます
# ユーザー名とパスワードは arg を使って切り替えることが出来ます (このファイルの先頭を参照)
RUN groupadd -g 1000 developer &&\
  useradd -g developer -G sudo -m -s /bin/bash ${USER_NAME} &&\
  echo "${USER_NAME}:${USER_PASSWORD}" | chpasswd

RUN apt-get install gawk -y
USER ${USER_NAME}

# jupyter の config ファイルの作成
RUN mkdir ~/.jupyter &&\
  echo "c.NotebookApp.open_browser = False\n\
c.NotebookApp.ip = '*'\n\
c.NotebookApp.token = '${JUPYTER_PASSWORD}'" | tee -a ${HOME}/.jupyter/jupyter_notebook_config.py

ADD docker/jupyter-custom.css /home/${USER_NAME}/.jupyter/custom/custom.css
ADD docker/matplotlibrc ${CONDA_DIR}/lib/python3.7/site-packages/matplotlib/mpl-data/matplotlibrc

RUN curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh && \
  wget https://raw.githubusercontent.com/nyk510/dotfiles/master/.zshrc -O ~/.zshrc

WORKDIR /workdir
EXPOSE 8888

CMD [ "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888"]
