from app.database.models import APIKey
from app import db
from datetime import date

def reset_api_key_usage():
    api_keys = APIKey.query.all()
    for key in api_keys:
        key.reset_usage()
        key.last_used_date = date.today()
        key.is_active = True
    db.session.commit()

    print("API key usage reset successfully.")