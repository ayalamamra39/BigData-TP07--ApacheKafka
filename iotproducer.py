import time
import json
import random
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_reading(sensor_id):
    return {
        "sensor_id": sensor_id,
        "temperature": round(20 + random.random()*15, 2),
        "humidity": round(30 + random.random()*50, 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

MAX_MESSAGES = 10   # Change this number as you want

try:
    sensors = ['sensor-1','sensor-2','sensor-3']
    count = 0

    while count < MAX_MESSAGES:
        s = random.choice(sensors)
        msg = generate_reading(s)
        producer.send('tp7-iot', msg)
        print(f"Sent ({count+1}/{MAX_MESSAGES}):", msg)
        count += 1
        time.sleep(1)

    print("Finished sending messages successfully!")

except KeyboardInterrupt:
    print("Stopped manually by user.")

finally:
    producer.close()
