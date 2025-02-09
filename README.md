# Discord Bot

## Overview

This Discord bot listens to real-time changes from the Wikipedia Recent Changes Stream. The bot performs the following tasks:

- It listens for changes from the [Wikipedia Stream URL](https://stream.wikimedia.org/v2/stream/recentchange).
- Changes are published to **Kafka** and concurrently consumed and stored in **MongoDB**.
- Users can interact with the bot using specific commands:
  - `!setLang` to set their preferred language.
  - `!changeLang` to change the language preference.
  - `!recent` to fetch recent changes from MongoDB based on the user's language preference.
  - `!stats` to retrieve the count of changes on a given date and language.

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

## Run the server on the development environment

```
python main.py
```