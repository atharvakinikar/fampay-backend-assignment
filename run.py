from app import create_app, scheduler
from app.utils.helpers.scheduler import scheduled_video_fetch
from dotenv import load_dotenv
load_dotenv()

app = create_app()

# Start the scheduler only if it isn't already running
if not scheduler.running:
    scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)