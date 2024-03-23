from app.utils.helpers.fetch_youtube_videos import fetch_youtube_data
import os
from app.config import Config
from flask import current_app

def scheduled_video_fetch():
    from app import create_app
    app = create_app()

    with app.app_context():
        
        search_query = Config.KEYWORD
        fetch_youtube_data(search_query)