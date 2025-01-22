from pathlib import Path
import json
import httpx
from init_photo_service import service
import os
import mimetypes
import time

UPLOAD_TRACKER_FILE = 'uploaded_files.json'


SUPPORTED_PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic', '.ico', '.avif'}
SUPPORTED_VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.3gp', '.mkv', '.m4v', '.wmv', '.mpg', '.mpeg', '.3g2', '.m2t', '.m2ts', '.mts'}
SUPPORTED_EXTENSIONS = SUPPORTED_PHOTO_EXTENSIONS | SUPPORTED_VIDEO_EXTENSIONS

if not os.path.exists(UPLOAD_TRACKER_FILE):
    with open(UPLOAD_TRACKER_FILE, 'w') as f:
        json.dump([], f)
def load_uploaded_files():
    if os.path.exists(UPLOAD_TRACKER_FILE):
        with open(UPLOAD_TRACKER_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_uploaded_files(uploaded_files):
    with open(UPLOAD_TRACKER_FILE, 'w') as f:
        json.dump(list(uploaded_files), f)

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def upload_media():
    token = service._http.credentials.token
    uploaded_files = load_uploaded_files()
    
    # Configure client with longer timeout for videos
    timeout = httpx.Timeout(300.0)  # 5 minutes timeout
    client = httpx.Client(timeout=timeout)
    
    base_dir = Path('./photos')
    for year_dir in base_dir.glob('*'):
        for month_dir in year_dir.glob('*'):
            for item in month_dir.glob('*.*'):
                if (item.suffix.lower() not in SUPPORTED_EXTENSIONS or 
                    str(item) in uploaded_files):
                    print(f'Skipping {item}')
                    continue
                
                print(f'Processing {item}')
                mime_type = get_mime_type(item)
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-type": "application/octet-stream",
                    "X-Goog-Upload-Content-Type": mime_type,
                    "X-Goog-Upload-Protocol": "raw",
                    "X-Goog-Upload-File-Name": item.name
                }
                
                try:
                    with open(item, 'rb') as f:
                        media_bytes = f.read()
                    
                    response = client.post(
                        'https://photoslibrary.googleapis.com/v1/uploads',
                        headers=headers,
                        data=media_bytes
                    )
                    
                    upload_token = response.text
                    
                    new_media_item = {
                        'description': f"Uploaded from {item.parent.name}",
                        'simpleMediaItem': {
                            'fileName': item.name,
                            'uploadToken': upload_token
                        }
                    }
                    
                    service.mediaItems().batchCreate(
                        body={'newMediaItems': [new_media_item]}
                    ).execute()
                    
                    uploaded_files.add(str(item))
                    save_uploaded_files(uploaded_files)
                    print(f'Successfully uploaded {item.name}')
                    time.sleep(2)

                    
                except Exception as e:
                    uploaded_files.remove(str(item))
                    print(f'Error uploading {item.name}: {str(e)}')
                    time.sleep(2)

if __name__ == "__main__":
    upload_media()
