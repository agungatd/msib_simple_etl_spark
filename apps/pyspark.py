import findspark
findspark.init()


def main():
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    import time

    start = time.time()
    postgre_jar_path = "/opt/bitnami/spark/jars/postgresql-42.7.2.jar"

    spark = SparkSession.builder \
        .appName("MyPySparkApp") \
        .config("spark.jars", postgre_jar_path) \
        .getOrCreate()

    # ============== Extract from parquet files
    df = spark.read.parquet("data/parquet/")
    print(df.show(5))
    print(f'Total data extracted: {df.count()} rows')

    # ============== Transformation
    # Replace specific values in product_name column with desired names
    df = df.withColumn(
        "product_name",
        F.when(F.col("product_name") == "product_N", "kacang_goreng")
        .when(F.col("product_name") == "product_H", "pesawat jet")
        .otherwise(F.col("product_name"))
    )

    # Convert product_name to lowercase
    df = df.withColumn("product_name", F.lower(F.col("product_name")))

    # Create a new column total_amount by multiplying amount with 1.11
    df = df.withColumn("total_amount", F.col("amount") * 1.11)

    transformed_df = df.groupBy(F.col("product_name"))\
        .agg(sum(F.col("amount")).alias("total_amount"))\
        .orderBy(F.desc("total_amount"))

    print('\nTransformed Data:')
    print(transformed_df.show(5))

    # ============== Load to DWH
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
        print('[SUCCESS] - Data has been load to DWH!')
    except Exception as e:
        print(f'[ERROR] - {e}')

    spark.stop()
    print(f'Time elapsed: {round(time.time() - start ,2)} s')


if __name__ == "__main__":
    main()
