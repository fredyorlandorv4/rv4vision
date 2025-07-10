
FROM python:3.13.5

RUN apt-get update \
  && apt-get -y install tesseract-ocr

RUN apt-get install poppler-utils -y

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get update && apt-get install -y \
    wget \
    tar \
    cmake \
    libnss3 \
    libnss3-dev \
    libcairo2-dev \
    libjpeg-dev \
    libgif-dev \
    cmake \
    libblkid-dev \
    e2fslibs-dev \
    libboost-all-dev \
    libaudit-dev \
    libopenjp2-7-dev \
    g++  # Aggiunto il pacchetto g++

RUN wget https://poppler.freedesktop.org/poppler-21.09.0.tar.xz \
    && tar -xvf poppler-21.09.0.tar.xz \
    && cd poppler-21.09.0 \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_BUILD_TYPE=Release \
             -DCMAKE_INSTALL_PREFIX=/usr \
             -DTESTDATADIR=$PWD/testfiles \
             -DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
             .. \
    && make \
    && make install

WORKDIR ./


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


COPY ./main.py .


CMD ["fastapi", "run", "main.py","--port", "80"]