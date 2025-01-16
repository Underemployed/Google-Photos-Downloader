# Google Photos API Downloader

Downloads your entire Google Photos library while preserving original quality and metadata.

## Key Features
- Downloads all photos and videos from Google Photos
- Organizes files by year and month (2024/January/etc)
- Creates friendly filenames (1st January 2024_time_photo.jpg) 
- Preserves photo metadata and descriptions
- Tracks folder statistics (file count, total size)
- Skips existing files automatically
---

## Setting Up Google Photos API Access

### 1. Create a Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing one.

### 2. Enable Google Photos API
- Navigate to **"APIs & Services" > "Library"**.
- Search for **"Photos Library API"**.
- Click **"Enable"**.

### 3. Configure OAuth Consent Screen
- Go to **"APIs & Services" > "OAuth consent screen"**.
- Select **"External"** user type.
- Fill in the required application information.
- Add the following scopes:
    - `https://www.googleapis.com/auth/photoslibrary.readonly`
    - `https://www.googleapis.com/auth/photoslibrary`
- Add your Google account as a test user.

### 4. Create OAuth 2.0 Credentials
- Follow [Google's guide to set up access](https://support.google.com/googleapi/answer/6158849?hl=en&ref_topic=7013279).
- Go to **"APIs & Services" > "Credentials"**.
- Click **"Create Credentials" > "OAuth client ID"**.
- Choose **"Desktop application"** as the application type.
- Download the client configuration file.

### 5. Setup Project Credentials
- Rename the downloaded client configuration file to `secret-token.json`.
- Place the file in the root directory of your project.
