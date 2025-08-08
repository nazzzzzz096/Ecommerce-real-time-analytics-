import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

products = ['Laptop', 'Smartphone', 'Tablet', 'Camera', 'Headphones']
payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery']

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def generate_order():
    return {
        'order_id': random.randint(1000, 9999),
        'product': random.choice(products),
        'price': round(random.uniform(2000, 100000), 2),
        'quantity': random.randint(1, 5),
        'payment_method': random.choice(payment_methods),
        'order_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

for _ in range(100):
    order = generate_order()
    print(f"Producing: {order}")
    producer.send('ecom-orders', value=order)
    time.sleep(0.5)

