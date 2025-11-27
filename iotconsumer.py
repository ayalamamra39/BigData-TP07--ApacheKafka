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
