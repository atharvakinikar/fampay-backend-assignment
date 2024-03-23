from app.database import db
from datetime import date

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    publish_time = db.Column(db.DateTime, nullable=False)
    thumbnail_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Video {self.title}>'


class APIKey(db.Model):
    __tablename__ = 'api_key'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    daily_usage = db.Column(db.Integer, default=0)
    last_used_date = db.Column(db.Date, default=date.today)
    is_active = db.Column(db.Boolean, default=True)

    def reset_usage(self):
        self.daily_usage = 0
        self.last_used_date = date.today()

    def increment_usage(self):
        if self.last_used_date < date.today():
            self.reset_usage()
        self.daily_usage += 1


class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)