FROM apache/airflow:2.8.1
COPY airflow_requirements.txt .
RUN pip install -r airflow_requirements.txt