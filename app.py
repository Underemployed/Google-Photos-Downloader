from init_photo_service import service
import os
import json
from datetime import datetime
import requests
from pathlib import Path
import pickle

class GooglePhotosDownloader:
    def __init__(self):
        self.base_path = "photos"
        self.metadata_path = os.path.join(self.base_path, "metadata")
        self.cache_file = os.path.join(self.base_path, "download_cache.pickle")
        Path(self.base_path).mkdir(exist_ok=True)
        Path(self.metadata_path).mkdir(exist_ok=True)
        
        self.months = {
            1: "01-Jan", 2: "02-Feb", 3: "03-Mar",
            4: "04-Apr", 5: "05-May", 6: "06-Jun",
            7: "07-July", 8: "08-Aug", 9: "09-Sept",
            10: "10-Oct", 11: "11-Nov", 12: "12-Dec"
        }

    def fetch_and_save_metadata(self):
        """Fetch all media items and save their metadata"""
        items = []
        page_token = None
        
        while True:
            request_body = {"pageSize": 100}
            if page_token:
                request_body["pageToken"] = page_token
            
            response = service.mediaItems().list(**request_body).execute()
            current_items = response.get("mediaItems", [])
            items.extend(current_items)
            
            # Save metadata for current batch
            for item in current_items:
                self._save_item_metadata(item)
            
            page_token = response.get("nextPageToken")
            if not page_token:
                break
            print(f"Fetched and saved metadata for {len(items)} items...")
        
        # Save all items data for later downloading
        with open(self.cache_file, 'wb') as f:
            pickle.dump(items, f)
        
        return len(items)

    def _save_item_metadata(self, item):
        """Save metadata for a single item"""
        creation_time_str = item["mediaMetadata"]["creationTime"]
        try:
            creation_time = datetime.strptime(creation_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            creation_time = datetime.strptime(creation_time_str, "%Y-%m-%dT%H:%M:%SZ")
        year = str(creation_time.year)
        month = self.months[creation_time.month]
        
        # Create folder structure
        year_path = os.path.join(self.base_path, year)
        month_path = os.path.join(year_path, month)
        Path(year_path).mkdir(exist_ok=True)
        Path(month_path).mkdir(exist_ok=True)
        
        # Save folder metadata for tracking downloads
        folder_metadata = {
            "year": year,
            "month": month,
            "item_count": 0,  
            "total_size": 0   
        }
        with open(os.path.join(month_path, "folder_info.json"), "w") as f:
            json.dump(folder_metadata, f, indent=2)
        
        # Save item metadata
        metadata = {
            "id": item["id"],
            "description": item.get("description", ""),
            "creationTime": item["mediaMetadata"]["creationTime"],
            "width": item["mediaMetadata"].get("width", ""),
            "height": item["mediaMetadata"].get("height", ""),
            "mimeType": item["mimeType"],
            "baseUrl": item["baseUrl"],
            "filename": item["filename"]
        }
        
        metadata_file = os.path.join(self.metadata_path, f"{item['id']}.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def download_all_media(self):
        """Download all media files using saved metadata"""
        if not os.path.exists(self.cache_file):
            print("No cached metadata found. Run fetch_and_save_metadata first.")
            return
        
        with open(self.cache_file, 'rb') as f:
            items = pickle.load(f)
        
        total = len(items)
        for index, item in enumerate(items, 1):
            try:
                self._download_single_item(item)
                print(f"Progress: {index}/{total} items processed")
            except Exception as e:
                print(f"Error downloading {item.get('filename', 'unknown')}: {str(e)}")
                continue

    def _download_single_item(self, item):
        """Download a single media item"""
        timestamp_str = item["mediaMetadata"]["creationTime"]
        timestamp_str = timestamp_str.replace('Z', '').split('.')[0]
        
        creation_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
        
        # Get ordinal day
        day_ordinal = str(creation_time.day)
        if day_ordinal.endswith('1') and day_ordinal != '11':
            day_ordinal += 'st'
        elif day_ordinal.endswith('2') and day_ordinal != '12':
            day_ordinal += 'nd'
        elif day_ordinal.endswith('3') and day_ordinal != '13':
            day_ordinal += 'rd'
        else:
            day_ordinal += 'th'
        
        year = str(creation_time.year)
        month = self.months[creation_time.month]
        month_path = os.path.join(self.base_path, year, month)
        
        friendly_time = creation_time.strftime("%I-%M %p").lstrip('0')
        friendly_date = f"{day_ordinal} {month.split("_")[1]} {year} at {friendly_time}"
        filename = f"{friendly_date}_{item['filename']}"
        file_path = os.path.join(month_path, filename)
        
        if os.path.exists(file_path):
            print(f"Skipping existing file: {filename}")
            return
        
        base_url = item["baseUrl"]
        mime_type = item["mimeType"]

        download_url = f"{base_url}=d" if "image" in mime_type else f"{base_url}=dv"
        
        # print(f"Download URL: {download_url}")
        
        print(f"Downloading: {filename}")
        response = requests.get(download_url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            # Update folder metadata
            folder_info_path = os.path.join(month_path, "folder_info.json")
            with open(folder_info_path, "r") as f:
                folder_info = json.load(f)
            
            folder_info["item_count"] += 1
            folder_info["total_size"] += len(response.content)
            
            with open(folder_info_path, "w") as f:
                json.dump(folder_info, f, indent=2)
        else:
            print(f"Failed to download {filename}")

def main():
    downloader = GooglePhotosDownloader()
    
    # Step 1: Fetch and save metadata
    print("Step 1: Fetching and saving metadata...")
    total_items = downloader.fetch_and_save_metadata()
    print(f"Metadata saved for {total_items} items")
    
    # Step 2: Download media files
    print("\nStep 2: Downloading media files...")
    downloader.download_all_media()
    print("Download complete!")

if __name__ == "__main__":
    main()
