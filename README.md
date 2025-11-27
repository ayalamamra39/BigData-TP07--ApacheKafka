
# Apache Kafka

---

# تشغيل Zookeeper و Kafka Broker

## تشغيل Zookeeper

```cmd
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

## تشغيل Broker

```cmd
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

---

# إنشاء Topic

```cmd
.\bin\windows\kafka-topics.bat --create --topic tp7-iot --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

قائمة الـ Topics:

```cmd
.\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092
```

---

# تجربة Producer و Consumer

## Producer (إرسال رسائل يدوياً)

```cmd
.\bin\windows\kafka-console-producer.bat --topic tp7-iot --bootstrap-server localhost:9092
```

## Consumer (استقبال الرسائل)

```cmd
.\bin\windows\kafka-console-consumer.bat --topic tp7-iot --bootstrap-server localhost:9092 --from-beginning
```

---

# إعداد عدة Brokers على نفس الجهاز 

## 1. نسخ ملف الإعدادات

نسخ الملف:

```
config\server.properties → config\server-9094.properties
config\server.properties → config\server-9095.properties
```

## 2. تعديل كل ملف:

### الملف الأول:

```properties
broker.id=1
listeners=PLAINTEXT://:9094
log.dirs=C:\kafka\kafka-logs-1
```

### الملف الثاني:

```properties
broker.id=2
listeners=PLAINTEXT://:9095
log.dirs=C:\kafka\kafka-logs-2
```

## 3. التشغيل:

```cmd
.\bin\windows\kafka-server-start.bat .\config\server-9093.properties
.\bin\windows\kafka-server-start.bat .\config\server-9094.properties
```

---

# مشروع IoT (بايثون) – إرسال بيانات حساسات

## التثبيت:

```cmd
pip install kafka-python
```

## Producer (iotproducer.py)

```python
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
```

## التشغيل:

```cmd
python iotproducer.py
```

---

# Consumer (iotconsumer.py)

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'tp7-iot',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='iot-group',
    value_deserializer=lambda m: m.decode('utf-8') if m else None
)

print("Consumer started...")

for msg in consumer:
    raw = msg.value

    # Skip null messages
    if raw is None:
        continue
    
    # Skip empty messages
    if raw.strip() == "":
        continue

    # Try JSON parsing safely
    try:
        data = json.loads(raw)
    except Exception as e:
        print("Skipped non-JSON message:", raw)
        continue

    print("Received:", data)

    if data.get('temperature', 0) > 40:
        print("⚠️ ALERT: High temperature!")
```

## التشغيل:

```cmd
python iotconsumer.py
```

