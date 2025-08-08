from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import from_json, col
from pyspark.sql.functions import to_timestamp
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType

spark = SparkSession.builder \
    .appName("EcommerceStream") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

model = PipelineModel.load("C:/week36/pro/ecommerce_model")

schema = StructType() \
    .add("order_id", IntegerType()) \
    .add("product", StringType()) \
    .add("price", DoubleType()) \
    .add("quantity", IntegerType()) \
    .add("payment_method", StringType()) \
    .add("order_time", StringType())

stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ecom-orders") \
    .load()

value_df = stream_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")).select("data.*")

predictions = model.transform(value_df)

final_df = predictions.select(
    "order_id",
    "product",
    "price",
    "quantity",
    "payment_method",
    to_timestamp("order_time", "yyyy-MM-dd HH:mm:ss").alias("order_time"),
    "prediction"
)

def write_to_postgres(batch_df, batch_id):
    try:
        batch_df.write \
            .format("jdbc") \
            .option("url", "##########") \
            .option("dbtable", "#####") \
            .option("user", "#####") \
            .option("password", "#####") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
    except Exception as e:
        print(f"Failed to write batch {batch_id}: {e}")

query = final_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

query.awaitTermination()

