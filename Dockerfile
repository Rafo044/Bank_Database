FROM apache/airflow:3.0.4


ENV PIP_NO_CACHE_DIR=off


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

