import random
import pyarrow as pa
import pyarrow.parquet as pq

# Define product names
products = [f"product_{chr(i + 65)}" for i in range(26)]


# Function to generate random data
def generate_data(num_rows):
    product_name = []
    amount = []
    for _ in range(num_rows):
        product_name.append(random.choice(products))
        amount.append(random.randint(100, 1000))
    return pa.Table.from_pydict({
        "product_name": pa.array(product_name, type=pa.string()),
        "amount": pa.array(amount, type=pa.int32())
    })


# Generate and write data
output_path = "/home/agung_msbu/personal/digitalSkola/spark/pyspark-intro/data/parquet"
num_rows = 2000000  # Adjust this for desired total rows
data = generate_data(num_rows)

for fileno in range(3):
    pq.write_table(data, f'{output_path}/productAmount_0000{fileno+1}.parquet')

print(f"Generated {num_rows} rows of data and saved to parquet files.")
