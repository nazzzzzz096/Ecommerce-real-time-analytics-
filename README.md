# E-Commerce Real-Time Analytics Project

## 📌 Overview
This project demonstrates a **real-time e-commerce analytics pipeline** using:
- **Apache Kafka** for real-time data streaming
- **Apache Spark Structured Streaming** for data processing and ML predictions
- **Spark MLlib** for machine learning model training
- **PostgreSQL** for data storage
- **Plotly Dash** for interactive dashboards

The system simulates live e-commerce orders, processes them in real-time, applies ML predictions, stores the results, and visualizes analytics.

---

## 🛠️ Technologies Used
- **Python 3**
- **Apache Kafka**
- **Apache Spark (Structured Streaming & MLlib)**
- **PostgreSQL**
- **Plotly Dash**
- **pandas**
- **psycopg2**

---

## 📂 Project Structure
```
.
├── kafka_producer.py      # Generates and streams synthetic e-commerce orders to Kafka
├── train_model.py         # Trains RandomForestRegressor model using Spark MLlib
├── stream_predict.py      # Consumes Kafka stream, applies model, writes to PostgreSQL
├── dashboard.py           # Dash app to visualize sales trends, products, and payment methods
├── run_pipeline.bat       # Batch script to start the end-to-end pipeline
└── README.md              # Project documentation
```

---

## ⚙️ How It Works

1. **Kafka Producer**
   - Simulates random orders with fields like product, price, quantity, payment method, and order time.
   - Sends messages to Kafka topic `ecom-orders`.

2. **Model Training**
   - Generates synthetic training data.
   - Trains a `RandomForestRegressor` using Spark MLlib.
   - Saves the trained model for later use.

3. **Stream Processing**
   - Reads live orders from Kafka.
   - Applies the trained ML model to predict total order amount.
   - Writes enriched results into PostgreSQL.

4. **Dashboard**
   - Reads data from PostgreSQL.
   - Displays interactive visualizations:
     - Sales by Hour / Product
     - Top 10 Products by Sales
     - Payment Method Distribution
   - Supports time range filtering.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Apache Kafka is installed and running
- Apache Spark installed
- PostgreSQL running
- Required Python packages:
```bash
pip install pandas psycopg2 dash plotly kafka-python pyspark
```

---

### Steps to Run
1. **Start Kafka and Zookeeper**
```bash
zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties
```
Create Kafka topic:
```bash
kafka-topics.sh --create --topic ecom-orders --bootstrap-server localhost:9092
```

2. **Run Kafka Producer**
```bash
python kafka_producer.py
```

3. **Train the Model**
```bash
python train_model.py
```

4. **Start Spark Streaming Job**
```bash
python stream_predict.py
```

5. **Run Dashboard**
```bash
python dashboard.py
```

6. Open in browser:
```
http://127.0.0.1:8050
```

---

## 📊 Architecture
1. Kafka Producer → Kafka Broker → Spark Streaming
2. Spark MLlib Model → Predictions → PostgreSQL
3. Dash Dashboard → Interactive Visualization

---

## 📌 Future Enhancements
- Add GraphX for product recommendation networks
- Implement hyperparameter tuning with CrossValidator
- Add an alert system for abnormal sales trends

---

## 👤 Author
Developed by Nazina N
