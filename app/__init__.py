from flask import Flask
from flask_apscheduler import APScheduler
from app.config import Config

from app.database import db

from app.utils.helpers.scheduler import scheduled_video_fetch
from app.utils.helpers.api_key_reset import reset_api_key_usage

scheduler = APScheduler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routers.video_routes import bp as video_bp
    app.register_blueprint(video_bp)   

    # Only initialize the scheduler with the app, don't start it here
    if not scheduler.running:  # Check if the scheduler isn't already running
        scheduler.init_app(app)

    if not scheduler.get_job('Scheduled Video Fetch'):
        scheduler.add_job(id='Scheduled Video Fetch', func=scheduled_video_fetch, trigger='interval', seconds=20)

    if not scheduler.get_job('Reset API Key Usage'):
        # Schedule the API key usage reset to run daily at midnight
        scheduler.add_job(id='Reset API Key Usage', func=reset_api_key_usage, trigger='cron', hour=0, minute=0)

    return app