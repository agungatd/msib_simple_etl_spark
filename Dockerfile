# builder step used to download and configure spark environment
FROM bitnami/spark:3.4.3

USER root

# Add Dependencies for PySpark
RUN apt-get update && apt-get install -y curl vim wget

# Download Postgres JDBC driver
RUN curl -L -o $SPARK_HOME/jars/postgresql-42.7.2.jar https://jdbc.postgresql.org/download/postgresql-42.7.2.jar

WORKDIR /opt/bitnami/spark

COPY requirements.txt .

RUN pip install -r requirements.txt
