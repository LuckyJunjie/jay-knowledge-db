# Jay Knowledge DB - System Design

## Overview
Multi-domain knowledge system: finance, gaming, AI/Agent, robotics.

## Architecture
- Service Layer: Knowledge retrieval, statistics, subscription
- Processing Layer: Kafka/RabbitMQ, NLP pipeline, crawler scheduler
- Storage: PostgreSQL (metadata), Vector DB (Qdrant), Object Storage (MinIO), Graph DB (Neo4j)

## Modules
1. Knowledge Acquisition - automated data collection
2. NLP Pipeline - classification, NER, sentiment, embedding
3. Statistics Engine - macro sentiment index
4. Human Portal - dashboard with charts
5. Agent API - RAG endpoints

## Tech Stack
- Frontend: Vue3/React + ECharts
- Backend: FastAPI
- Queue: Celery + Redis/Kafka
- NLP: HuggingFace, FinBERT
- Crawler: Scrapy + Playwright
- Vector: Qdrant

## See also
- REQUIREMENTS.md - Functional requirements