FROM python:3.11.11-slim
RUN <<EOF 
apt-get update 
apt-get -y install git \
            gcc \
            build-essential \
            python3-dev \
            libffi-dev
apt-get clean
EOF

ENV UV_INSTALL_DIR="/usr/local/bin"
ENV DAGSTER_HOME="/opt/dagster/"
ENV PYTHONPATH="/opt/dagster/usercode/app"

# Checkout and install dagster libraries needed to run the gRPC server
# exposing your repository to dagster-webserver and dagster-daemon, and to load the DagsterInstance
COPY --from=tarampampam/curl /bin/curl /bin/curl
RUN curl -LsSf https://astral.sh/uv/install.sh | sh


WORKDIR /opt/dagster/usercode
COPY requirements.txt .
RUN uv pip install --no-cache --system -r requirements.txt

COPY app app

# dbt proj under a different dir here due to how GHA works
COPY ./dbt/ ticktick-py-dbt


ENTRYPOINT ["python","-m","dagster","code-server","start"]
CMD ["-p","4000","-h","0.0.0.0"]