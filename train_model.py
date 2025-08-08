from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
import pandas as pd
import random

# Create Spark session
spark = SparkSession.builder.appName("EcommerceModelTraining").getOrCreate()

# Generate synthetic dataset
data = []
products = ['Laptop', 'Smartphone', 'Tablet', 'Camera', 'Headphones']
payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery']

for _ in range(1000):
    price = round(random.uniform(2000, 100000), 2)
    quantity = random.randint(1, 5)
    payment_method = random.choice(payment_methods)
    product = random.choice(products)
    total_amount = price * quantity
    data.append([product, price, quantity, payment_method, total_amount])

df = pd.DataFrame(data, columns=['product', 'price', 'quantity', 'payment_method', 'total_amount'])
spark_df = spark.createDataFrame(df)

# Preprocessing
indexers = [
    StringIndexer(inputCol='product', outputCol='product_index'),
    StringIndexer(inputCol='payment_method', outputCol='payment_index')
]
assembler = VectorAssembler(
    inputCols=['product_index', 'price', 'quantity', 'payment_index'],
    outputCol='features'
)
model = RandomForestRegressor(featuresCol='features', labelCol='total_amount')

pipeline = Pipeline(stages=indexers + [assembler, model])
trained_model = pipeline.fit(spark_df)

# Save model
trained_model.save("ecommerce_model")
