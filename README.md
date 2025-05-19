# 🚀 Notification Hub  - Made by Adarsh

# Notification Service — Made by Adarsh Kumar Rath

This is a notification delivery system that allows sending notifications via SMS, Email, and In-App messages. The system uses RabbitMQ for queuing, FastAPI for backend APIs, and SQLite for storing delivered notifications. SMS integration is handled through Twilio.

# Features

- Send notifications via SMS, Email, and In-App
- Message processing via RabbitMQ queue
- Retry mechanism for failed deliveries
- Stores notifications in local database
- Fully documented API via Swagger UI
- Containerized using Docker

# Tech Stack

Backend Framework: FastAPI  
Queue System: RabbitMQ  
Database: SQLite  
SMS Integration: Twilio API  
Containerization: Docker and Docker Compose  
API Documentation: Swagger (via FastAPI)

# Setup Instructions (Local)

1. Go to the project directory

```bash
cd ~/Downloads/adarsh_notification_service_rabbitmq_v3
Set up virtual environment
python3 -m venv venv
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Configure environment variables
Create a .env file in the root folder with the following:

TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+1234567890
Run the API locally
uvicorn app.main:app --reload
Open in browser:
http://localhost:8000/docs

Start the RabbitMQ consumer
Open a new terminal, then:

cd ~/Downloads/adarsh_notification_service_rabbitmq_v3
source venv/bin/activate
python app/consumer.py
Docker Setup (Optional)

To run everything in Docker:

docker-compose up --build
API: http://localhost:8000/docs
RabbitMQ UI: http://localhost:15672
Login: guest / guest

API Endpoints

POST /notifications
Send a notification:

{
  "user_id": 1,
  "message": "Hello from Akr!",
  "type": "sms"
}
GET /users/{user_id}/notifications
Returns all past notifications for that user.

Project Structure

adarsh_notification_service_rabbitmq_v3/
├── app/
│   ├── main.py
│   └── consumer.py
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
Retry Logic

Failed notifications (due to external API issues) are retried automatically using a basic retry loop inside the RabbitMQ consumer.

Author

Adarsh Kumar Rath
Backend Developer 
Email: rath.adarsh2004@gmail.com


## Access

- API: http://localhost:8000/docs
- RabbitMQ: http://localhost:15672 (guest / guest)



Service running can be verified at : https://pepsales-intern-assignment-production.up.railway.app/
