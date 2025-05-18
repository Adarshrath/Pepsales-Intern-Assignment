import pika
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import Notification, NotificationRequest, Base

DATABASE_URL = "sqlite:///./notifications.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

def callback(ch, method, properties, body):
    session = SessionLocal()
    try:
        data = json.loads(body)
        notif = Notification(**data)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                session.add(notif)
                session.commit()
                print(f"✅ Stored notification for user {notif.user_id}: {notif.message}")
                break
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed: {e}")
                time.sleep(2)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"❌ Failed to process: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    finally:
        session.close()

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print(" [*] RabbitMQ consumer running 🐰...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()