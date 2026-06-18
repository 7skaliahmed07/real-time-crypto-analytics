# Real-Time Crypto Analytics
![Architectural Diagram] (real-time-analytics.png)

A real-time cryptocurrency analytics platform that streams live BTC/USDT trade data from Binance, stores it in PostgreSQL, and exposes analytics through a FastAPI backend and web dashboard.

## Architecture

Binance WebSocket → Python Ingestion Service → PostgreSQL → FastAPI Backend → Frontend Dashboard

## Features

* Live BTC/USDT trade streaming from Binance
* Real-time data ingestion using WebSockets
* PostgreSQL storage for historical trade data
* FastAPI backend for analytics and APIs
* Docker Compose-based local deployment
* Scalable microservice architecture

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* Docker & Docker Compose
* Binance WebSocket API
* Nginx
* HTML/CSS/JavaScript

## Project Structure

```text
real-time-crypto-analytics/
├── backend/
├── ingestion/
├── frontend/
├── db/
│   └── init.sql
├── amd/
├── docker-compose.yml
└── README.md
```

## Getting Started

Clone the repository:

```bash
git clone "https://github.com/7skaliahmed07/real-time-crypto-analytics"
cd real-time-crypto-analytics
```

Start the application:

```bash
docker compose up --build
```

Access the services:

* Frontend: http://localhost:3000
* Backend API: http://localhost:8000
* PostgreSQL: localhost:5432

## Database

The application automatically creates the required database schema during startup using the initialization script.

Example query:

```sql
SELECT COUNT(*) FROM trades;
```

## Current Status

✅ Dockerized architecture

✅ Live Binance trade ingestion

✅ PostgreSQL persistence

✅ FastAPI backend

✅ Frontend dashboard

## Future Enhancements

* Real-time price charts
* Volume analytics
* PnL tracking
* WebSocket API for frontend updates
* Redis caching
* Kafka streaming pipeline
* Multi-exchange support

## License

MIT License
