# Telegram OTP Bot API

This API enables sending Telegram messages to users by their unique linked usernames through a Telegram bot.

---

## Tech Stack

- **Python 3.9+**
- **python-telegram-bot** (Telegram Bot API library)
- **Flask** (Web framework for REST API)
- **psycopg2-binary** (PostgreSQL database adapter)
- **PostgreSQL** (Database for storing usernames and chat IDs)
- **Docker** (Containerization)
- **Render.com** (Deployment platform)

---

## API Endpoints

### 1. Send Message

- **URL:** `/send-message`
- **Method:** `POST`
- **Description:** Send a Telegram message to a user by their linked username.

#### Request JSON Body:

```json
{
  "username": "linked_username",
  "message": "Your message text here"
}
