# First-time build can take upto 10 mins.

FROM apache/airflow:2.2.3-python3.8

ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH=/opt/airflow:${PYTHONPATH}

USER root
RUN apt-get update -qq && apt-get install vim  nano wget unzip -qqq 

USER $AIRFLOW_UID

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade typing-extensions

USER root

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID
