from init_photo_service import service
import pandas as pd
from datetime import datetime
import pytz
import math as Math
import requests
import os


def filter_photos(start_date_str, end_date_str):
    # Convert input dates to datetime objects with timezone
    start_date = datetime.strptime(start_date_str, "%d-%m-%y").replace(tzinfo=pytz.UTC)
    end_date = datetime.strptime(end_date_str, "%d-%m-%y").replace(tzinfo=pytz.UTC)
    start_year, start_month, start_day = (
        start_date.year,
        start_date.month,
        start_date.day,
    )
    end_year, end_month, end_day = end_date.year, end_date.month, end_date.day
    request_body = {
        "pageSize": 100,
        "filters": {
            "dateFilter": {
                "ranges": [
                    {
                        "startDate": {
                            "year": start_year,
                            "month": start_month,
                            "day": start_day,
                        },
                        "endDate": {
                            "year": end_year,
                            "month": end_month,
                            "day": end_day,
                        },
                    }
                ]
            }
        },
    }

    media_items_response = service.mediaItems().search(body=request_body).execute()
    album = media_items_response["mediaItems"]
    nextpageToken = media_items_response.get("nextPageToken")
    while nextpageToken:
        request_body["pageToken"] = nextpageToken
        response = service.mediaItems().search(body=request_body).execute()
        album.extend(response["mediaItems"])
        nextpageToken = response.get("nextPageToken")
        print("ITERATING")

    def download_file(url: str, destination: str, filename: str, mimeType: str):
        if "image" in mimeType:
            url += "=d"
        elif "video" in mimeType:
            url += "=dv"

        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            print("Downloading %s..." % (filename))

        with open(os.path.join(destination, filename), "wb") as f:
            f.write(r.content)

    for media in album:
        file_name = media["filename"]
        download_file(media["baseUrl"], "images", file_name, media["mimeType"])


filter_photos("01-01-22", "31-12-23")
