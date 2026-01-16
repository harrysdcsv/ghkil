#🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os

API_ID    = os.environ.get("API_ID", "10868873")
API_HASH  = os.environ.get("API_HASH", "2ce261d1e624c9874548f5498266a336")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
LOG = True  
auth_user = os.environ.get('auth_users', '7602994049').split(',')
auth_users = [int(user_id) for user_id in auth_user]

#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set
