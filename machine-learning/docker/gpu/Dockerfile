FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

LABEL maintainer="nyker <nykergoto@gmail.com>"
ENV jupyter_token=dolphin

RUN apt-get update && \
  apt-get install -y \
  build-essential \
  curl \
  wget \
  bzip2 \
  ca-certificates \
  libglib2.0-0 \
  libxext6 \
  libsm6 \
  libxrender1 \
  git \
  vim \
  mercurial \
  subversion \
  cmake \
  libboost-dev \
  libboost-system-dev \
  libboost-filesystem-dev \
  gcc \
  g++ \
  nano \
  unzip

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT [ "/usr/bin/tini", "--" ]

# install miniconda
ENV CONDA_DIR /opt/conda
ENV PATH ${CONDA_DIR}/bin:${PATH}

RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.4.10-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p ${CONDA_DIR} && \
    rm ~/miniconda.sh && \
    echo "export PATH=/opt/conda/bin:${PATH}" >> ~/.bash_profile

# jupyter settings password and browser
RUN mkdir ~/.jupyter
RUN echo "c.NotebookApp.open_browser = False\n\
c.NotebookApp.ip = '*'\n\
c.NotebookApp.token = '${jupyter_token}'" | tee -a ${HOME}/.jupyter/jupyter_notebook_config.py

WORKDIR /home

# install requirements
RUN conda update conda

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
  cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/local/cuda-9.0/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda-9.0/include/ ..&&\
  make -j$(nproc)&&\
  cd ../python-package/&&\
  python setup.py install --precompile

RUN pip install --upgrade pip

# install tensorflow
# ver1.9 CUDA=9.0 and CUDNN=7.0
RUN pip install tensorflow-gpu==1.8.0

# other packages
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# additional packages
RUN conda install jupyter notebook

EXPOSE 8888

# 後片付け
RUN apt-get autoremove -y && apt-get clean && \
  conda clean -i -l -t -y && \
  rm -rf /usr/local/src/*

CMD [ "jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root" ]
