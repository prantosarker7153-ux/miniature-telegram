# CINEFLIX Bot - Railway Deploy Package

## Files Included
- botex.py
- requirements.txt
- runtime.txt
- Procfile

## Railway Setup Steps

1. Upload this project to GitHub.
2. Go to Railway → New Project → Deploy from GitHub.
3. Select Worker (NOT Web Service).
4. Add Environment Variables:

BOT_TOKEN=your_bot_token
MONGO_URI=your_mongodb_uri
ADMIN_ID=your_telegram_user_id

5. Deploy.

## Important Notes
- Make sure MongoDB Network Access allows 0.0.0.0/0
- Bot must be admin in required channels
- ADMIN_ID must be numeric
