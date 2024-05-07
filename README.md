
# Hadoop vs Spark

| Feature	           | Hadoop	                               | Spark                                       |
|----------------------|---------------------------------------|---------------------------------------------|
| Processing Speed	   | Slower (writes to disk)	           | Faster (uses memory)                        |
| Data Processing Mode | Batch processing	                   | Batch or real-time processing               |
| Cost	               | More affordable (uses cheaper storage)| More expensive (needs more RAM)             |
| Scalability          | Easier to scale by adding nodes	   | More challenging to scale                   |
| Machine Learning	   | Requires external libraries	       | Built-in machine learning libraries         |
| Security	           | More secure	                       | Less secure (relies on Hadoop for security) |

# Steps to run
1. build dockerfile image, run 
```bash 
docker build -t cluster-apache-spark:3.4.3 .
```
2. run
```bash
docker compose up -d
```
4. inside the postgres dwh container, create table:
```sql
   CREATE TABLE public.product_sales (
	product_name varchar NULL,
	total_amount bigint NULL
);
```
5. inside master node container, run:
```bash
python app/pyspark.py
```

# Sources
- [pyspark-intro](https://realpython.com/pyspark-intro/)
- [spark cluster with docker](https://dev.to/mvillarrealb/creating-a-spark-standalone-cluster-with-docker-and-docker-compose-2021-update-6l4)
- [pyspark docks](https://spark.apache.org/docs/latest/api/python/index.html)

