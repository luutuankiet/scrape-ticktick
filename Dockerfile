FROM python:3.10-slim

COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-dev gcc && pip install -r requirements.txt

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN touch /opt/dagster/dagster_home/dagster.yaml


ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR /opt/dagster/dagster_home/

COPY app ./app

COPY dbt_project ./dbt_project

COPY env_init.sh .

RUN chmod +x env_init.sh && . ./env_init.sh

EXPOSE 3000

# RUN /bin/bash -c "source .env" && dbt deps && dbt build

# ENTRYPOINT ["dagster-webserver","-h","0.0.0.0","-p","3000"]
