from flask import Blueprint, request, jsonify
from app.database.models import Video
from app.database import db

bp = Blueprint('videos', __name__, url_prefix='/videos')

@bp.route('/', methods=['GET'])
def get_videos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Querying the database for videos, ordered by publish time in descending order
    pagination = Video.query.order_by(Video.publish_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    videos = pagination.items

    # Preparing the video data for JSON response
    videos_data = [{
        'title': video.title,
        'description': video.description,
        'publish_time': video.publish_time.isoformat(),
        'thumbnail_url': video.thumbnail_url
    } for video in videos]

    # Creating the response object
    response = {
        'videos': videos_data,
        'total': pagination.total,
        'pages': pagination.pages,
        'next_page': pagination.next_num,
        'prev_page': pagination.prev_num
    }

    return jsonify(response)