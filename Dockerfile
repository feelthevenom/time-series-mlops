FROM apache/airflow:3.0.0

USER root
WORKDIR /app

COPY requirements.txt /app/

USER airflow
RUN pip install --no-cache-dir -r requirements.txt

USER root
# Install system packages (e.g., git)
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

# Optionally copy DAGs or plugins if needed
# COPY dags/ /opt/airflow/dags/
# COPY plugins/ /opt/airflow/plugins/

USER airflow

CMD ["webserver"]

