import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, desc
import time

start = time.time()

spark = SparkSession.builder \
    .appName("MyPySparkApp") \
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.7.2.jar") \
    .getOrCreate()

# Extract from parquet files
df = spark.read.parquet("data/parquet/")
print(df.show(5))
print(f'total data: {df.count()} rows')

# Transformation
transformed_df = df.groupBy(col("product_name"))\
                    .agg(sum(col("amount")).alias("total_amount"))\
                    .orderBy(desc("total_amount"))

print(transformed_df.show())

# Load to DWH
jdbc_url = "jdbc:postgresql://spark-dwh:5432/postgres"
table_name = "product_sales"  # Replace with your desired table name
user = "postgres"
password = "password"

try:
    transformed_df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", table_name) \
        .option("user", user) \
        .option("password", password) \
        .mode("overwrite") \
        .save()
except Exception as e:
    print(f'[ERROR] - {e}')

spark.stop()
print(f'Time elapsed: {round(time.time() - start ,2)} s')
