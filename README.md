# Discord Bot

## Overview

This Discord bot listens to real-time changes from the Wikipedia Recent Changes Stream. The bot performs the following tasks:

- It listens for changes from the [Wikipedia Stream URL](https://stream.wikimedia.org/v2/stream/recentchange).
- Changes are published to **Kafka** and concurrently consumed and stored in **MongoDB**.
- Users can interact with the bot using specific commands:
  - `!setLang` to set their preferred language (e.g. !setLang en for English).
  - `!changeLang` to change the language preference (e.g. !changeLang de for German).
  - `!recent` to fetch recent changes from MongoDB based on the user's language preference.
  - `!stats` to retrieve the count of changes on a given date and language (e.g. !stats 2025-02-09 uz).

Language preferences are stored in **MongoDB**, and when a user changes their language preference with `!changeLang`, the bot updates it accordingly and starts delivering updates in the selected language.

### Create .env file

```
cp env.example .env
```


### Installing Python Packages on Your Environment
To install Python packages from this repository, follow these steps:

1. Make sure you have a `requirements.txt` file with the required packages listed.
2. Run the following command to install the packages:

   ```bash
   pip install -r requirements.txt 

   ```
## Docker Compose for Kafka

To run Kafka locally using Docker, follow the steps below:
### 1. Create a `docker-compose.yml` File

Create a `docker-compose.yml` file in the root of your project with the following content:

```
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  schema-registry:
    image: confluentinc/cp-schema-registry:latest
    hostname: schema-registry
    depends_on:
      - kafka-broker-1
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL: 'zookeeper:2181'
      SCHEMA_REGISTRY_LISTENERS: http://schema-registry:8081
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: PLAINTEXT://kafka-broker-1:9092,PLAINTEXT_INTERNAL://localhost:19092
      SCHEMA_REGISTRY_DEBUG: 'true'

  kafka-broker-1:
    image: confluentinc/cp-kafka:latest
    hostname: kafka-broker-1
    ports:
      - "19092:19092"
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-broker-1:9092,PLAINTEXT_INTERNAL://localhost:19092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1


```

## Run the following command to start Kafka and Zookeeper
```
docker-compose up

```
## To stop Kafka and Zookeeper, run:

```
docker-compose down

```

## Run the server on the development environment

```
python main.py

```

## You should visit and create new application

```
https://discord.com/developers/applications 

```
