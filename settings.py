import os
from dotenv import load_dotenv

load_dotenv()  # טוען משתני סביבה מקובץ .env (אם קיים)

# מפתח סודי לניהול סשנים
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

# ביטול הגדרות DB אם אין חיבור
DB = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', '')
}
