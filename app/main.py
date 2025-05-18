from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pika
import json

app = FastAPI(title="🚀 Notification Service - Made by Akr")

DATABASE_URL = "sqlite:///./notifications.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(String)
    type = Column(String)

Base.metadata.create_all(bind=engine)

class NotificationRequest(BaseModel):
    user_id: int
    message: str
    type: str

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "notifications"

def publish_to_queue(notification: NotificationRequest):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    message = json.dumps(notification.dict())
    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=message)
    connection.close()

@app.post("/notifications")
async def send_notification(notification: NotificationRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(publish_to_queue, notification)
    return {"status": "Queued", "user_id": notification.user_id}

@app.get("/users/{user_id}/notifications", response_model=List[NotificationRequest])
def get_user_notifications(user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).all()