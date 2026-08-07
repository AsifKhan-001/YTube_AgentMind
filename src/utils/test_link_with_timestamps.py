from src.config import URL
from urllib.parse import urlparse, parse_qs

def timestamp_link(url):

    time = ''
    url_id = parse_qs(urlparse(url).query).get("v", [None])[0]
    base_yt_url = f'https://www.youtube.com/watch?v={url_id}'
    url_timestamp = f"{base_yt_url}&t=time"
    print(url_timestamp)
    return url_timestamp

