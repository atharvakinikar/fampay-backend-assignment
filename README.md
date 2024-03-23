# YouTube Video Fetcher

This project is a Flask application that fetches the latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query and stores them in a database. It supports paginated access to these videos through a RESTful API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6+
- pip
- Virtual environment (recommended)

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

1. Clone the repository:

```bash
git clone https://github.com/atharvakinikar/fampay-backend-assignment
cd fampay-backend-assignment
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the environment variables:

Create a `.env` file in the root directory of your project and add the following lines, replacing placeholder values with your actual data:

```env
DATABASE_URL='postgresql://username:password@localhost/database_name'
KEYWORD='your_search_keyword'
```

5. Run the server:
```bash
python run.py
```

### Testing the API

To fetch the latest videos, visit:

http://localhost:5000/videos?page=1&per_page=10

### Highlights 

1. Dynamic API Key Management: The application intelligently stores YouTube API keys in the database, monitoring and managing their daily usage. It seamlessly rotates between keys based on usage metrics and quota limitations, ensuring uninterrupted access to YouTube's API by automatically switching to an alternative key when quotas are approached or exceeded.
2. Automated Quota Reset Handling: Leveraging the YouTube Data API v3's quota system, the application includes a scheduled cron job that resets the daily usage metrics of each API key at midnight. This job also reactivates any keys previously marked as exhausted, aligning with the API's quota refresh cycle and ensuring that all keys are ready for use each new day.
3. Resilient Data Fetching Mechanism: To maintain data integrity and continuity, especially in the event of system downtimes, the application records the timestamp of the last successful YouTube data fetch in the database. Upon recovery, it retrieves videos published after this timestamp, thereby ensuring no data loss or gaps occur due to temporary outages.
4. Efficient Video Data Insertion: The system employs a bulk data insertion strategy coupled with pre-insertion checks against the existing database records using YouTube video IDs. This approach minimizes database transactions and ensures the database remains free of duplicate video entries, enhancing performance and data quality.
5. Paginated Video Access API: The application provides a paginated RESTful API endpoint for accessing the stored videos, allowing users to easily navigate through video records. The API supports customizable pagination parameters, offering flexibility in data retrieval and enhancing the user experience by efficiently managing the dataset's presentation.