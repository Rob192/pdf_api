FROM python:3

WORKDIR usr/src/pdf_api

COPY requirements.txt ./
RUN apt-get -y remove ocrmypdf
RUN apt-get -y update
RUN apt-get -y install \
    ghostscript \
    icc-profiles-free \
    liblept5 \
    libxml2 \
    pngquant \
    python3-cffi \
    python3-distutils \
    python3-pkg-resources \
    python3-reportlab \
    qpdf \
    tesseract-ocr \
    zlib1g

RUN pip install --no-cache-dir -r requirements.txt

#ADD environment.yml environment.yml

#RUN conda env create -f environment.yml
#ENV PATH /opt/conda/envs/flair_pseudo_api/bin:$PATH
#RUN /bin/bash -c "source activate flair_pseudo_api"
COPY . .