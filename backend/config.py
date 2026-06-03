import os

# ---------------- JWT ----------------
JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")

# ---------------- DATABASE ----------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "database": os.getenv("DB_NAME", "farmer_db")
}

# ---------------- SMS API ----------------
FAST2SMS_KEY = os.getenv("FAST2SMS_KEY", "0244b1e4-5d24-11f1-8352-0200cd936042")