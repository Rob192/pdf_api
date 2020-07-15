FROM python:3

WORKDIR usr/src/pdf_api

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#ADD environment.yml environment.yml

#RUN conda env create -f environment.yml
#ENV PATH /opt/conda/envs/flair_pseudo_api/bin:$PATH
#RUN /bin/bash -c "source activate flair_pseudo_api"
COPY . .