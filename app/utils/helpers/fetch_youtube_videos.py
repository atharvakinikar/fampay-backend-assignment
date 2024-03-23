from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app import db
from app.database.models import Video, APIKey, Metadata
from app.config import Config
from datetime import datetime, timedelta

def create_youtube_client(api_key):
    """
    Create a Youtube API client.

    Args:
    - api_key (str): Youtube Data API key.

    Returns:
    - googleapiclient.discovery.Resource: The Youtube API client.
    """

    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)
    return youtube


def update_last_fetch_timestamp():

    current_time = datetime.now().isoformat() + 'Z'

    last_fetch_entry = Metadata.query.filter_by(key="last_successful_fetch").first()

    if last_fetch_entry:
        last_fetch_entry.value = current_time

    else:
        new_entry = Metadata(key="last_successful_fetch", value=current_time)
        db.session.add(new_entry)

    db.session.commit()


def get_last_successful_fetch_timestamp():

    # Retrieve the last successful fetch timestamp
    last_fetch_entry = Metadata.query.filter_by(key="last_successful_fetch").first()

    if last_fetch_entry:
        published_after = last_fetch_entry.value
    
    else:
        # Fallback to 1 day ago if no last fetch timestamp is found
        published_after = (datetime.now() - timedelta(days=1)).isoformat() + 'Z'
    
    return published_after


def get_active_api_keys():

    api_keys = APIKey.query.filter_by(is_active=True).order_by(APIKey.daily_usage).all()

    return api_keys


def fetch_from_youtube(keyword, api_key, published_after):

    youtube = create_youtube_client(api_key)
    request = youtube.search().list(
        q=keyword, 
        part="snippet", 
        type="video", 
        order='date', 
        publishedAfter=published_after, 
        maxResults=25
    ).execute()
    return request.get('items', [])


def process_video_data(videos):

    # Collect all video IDs from the incoming batch
    video_ids = [video['id']['videoId'] for video in videos]

    existing_video_ids = {video.video_id for video in Video.query.with_entities(Video.video_id).all()}

    new_videos = []

    for video in videos:

        video_id = video['id']['videoId']

        # Check if the video already exists using the set
        if video_id not in existing_video_ids:

            video_data = Video(
                video_id=video_id,
                title=video['snippet']['title'],
                description=video['snippet']['description'],
                publish_time=datetime.strptime(video['snippet']['publishTime'], '%Y-%m-%dT%H:%M:%SZ'),
                thumbnail_url=video['snippet']['thumbnails']['high']['url']
            )

            new_videos.append(video_data)

    # Bulk insert new videos
    if new_videos:
        db.session.bulk_save_objects(new_videos)
        db.session.commit()

    db.session.add(video_data)

    db.session.commit()


def fetch_youtube_data(keyword):
    
    published_after = get_last_successful_fetch_timestamp() 
    
    for api_key in get_active_api_keys():

        print(f"Trying the following key -> {api_key.key}")

        try:
            videos = fetch_from_youtube(keyword, api_key.key, published_after)
            process_video_data(videos)
            update_last_fetch_timestamp()
            api_key.increment_usage()
            db.session.commit()
            break  # Exit the loop if successful

        except HttpError as e:
            if e.resp.status == 403:  # Check if the error is a quota error
                api_key.is_active = False  # Mark the key as inactive
                db.session.commit()
                print(f"Quota exhausted for API key. Trying next key.")
                continue  # Try the next API key
            else:
                raise  # Re-raise the exception if it's not a quota error