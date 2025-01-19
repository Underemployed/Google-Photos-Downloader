# Google Photos Downloader


Downloads your entire Google Photos library while preserving original metadata, quality and file order using python and the Google Photos API.
    <br> <br>

<a href="https://www.youtube.com/watch?v=QQ49vPLM6nU" style="margin:1rem;border-radius:1rem;">
    <img src="thumbnail.jpeg" alt="Watch the video" width="800">
</a>



## Key Features
- Downloads all photos and videos from Google Photos
- Preserves original metadata (date, location, etc)
- Organizes files by year and month (2024/January/etc)
- Creates friendly filenames (1st January 2024_time_photo.jpg) 
- Tracks folder statistics (file count, total size)
- Skips existing files automatically
## Setting Up Google Photos API Access

### 1. Create a Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing one.

### 2. Enable Google Photos API
- Search for **"Enable APIs and Services"**.
- Click on **"+ ENABLE APIS AND SERVICES"**.
- Search for **"Google Photos Library API"**.
- Click **"Enable"**.

### 3. Configure OAuth Consent Screen
- Go to **"APIs & Services" > "OAuth consent screen"**.
- Select **"External"** user type.
- Enter the required fields.
- Fill in the required application information.
- Add the following scope:
    <br> <br>

  ```
  https://www.googleapis.com/auth/photoslibrary
  ```
     
- Add your Google account as a test user (the Gmail account in which your photos are stored).

### 4. Create OAuth 2.0 Credentials
- Follow [Google's guide to set up access](https://support.google.com/googleapi/answer/6158849?hl=en&ref_topic=7013279).
- Go to **"Credentials"**.
- Click **"Create Credentials" > "OAuth client ID"**.
- Choose **"Desktop application"** as the application type.
- Download the client configuration file.
- **Rename** the downloaded client configuration file to `secret-token.json` and save it to the project directory.


### 6. Install Dependencies and Run
- If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/)

- Install the required Python packages:
    <br> <br>
    ```sh
    pip install -r requirements.txt
    ```
- Run the application:
    <br> <br>
    ```sh
    python app.py
    ```
- log in to your Google account, click continue and start downloading your Google Photos.




Tags

