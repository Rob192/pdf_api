FROM continuumio/miniconda3

WORKDIR usr/src/pdf_api
RUN mkdir /usr/share/man/man1/

RUN apt-get -y update
RUN apt-get -y install \
    g++ \
    build-essential \
    ocrmypdf \
    libpoppler-cpp-dev \
    pkg-config \
    openjdk-11-jdk \
    ghostscript \
    icc-profiles-free \
    liblept5 \
    libxml2 \
    pngquant \
    qpdf \
    tesseract-ocr \
    zlib1g


ADD environment.yml environment.yml

RUN conda env create -f environment.yml
ENV PATH /opt/conda/envs/pdf_api/bin:$PATH
RUN /bin/bash -c "source activate pdf_api"
COPY . .

#RUN mkdir -p /usr/share/man/man1
#
#
#
##RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
#RUN pip3 install --no-cache-dir -r requirements.txt
#
##ADD environment.yml environment.yml
#
##RUN conda env create -f environment.yml
##ENV PATH /opt/conda/envs/flair_pseudo_api/bin:$PATH
##RUN /bin/bash -c "source activate flair_pseudo_api"
#COPY . .
