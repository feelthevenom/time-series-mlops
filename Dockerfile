FROM apache/airflow:3.0.0

USER root
WORKDIR /app

COPY requirements.txt /app/
COPY setup.py /app/
COPY README.md /app/
COPY src/ /app/src/

# Fix permissions so airflow user can write to /app
RUN chown -R airflow: /app

USER airflow
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e /app

# Add the project directory to PYTHONPATH
ENV PYTHONPATH="/app:${PYTHONPATH}"

USER root

USER airflow

CMD ["webserver"]