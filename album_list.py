from init_photo_service import service
import pandas as pd

response = service.albums().list(pageSize=50, excludeNonAppCreatedData=False).execute()

print(pd.DataFrame(response.get("albums")))
import os
import time
from datetime import datetime


media_items_response = service.mediaItems().list(pageSize=25).execute()
print(media_items_response)
for media_item in media_items_response["mediaItems"]:
    if media_item["mimeType"] == "image/jpeg":
        print(media_item["ProductUrl"])
