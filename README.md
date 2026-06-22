# Google Photos Downloader


Downloads your entire Google Photos library while preserving original metadata, quality and file order using python and the Google Photos API.
The Google Takeout file/folder structure has some interesting inconsistencies/quirks which make it tricky to work with. i created this script for my personal use.
    <br> <br>

<a href="https://www.youtube.com/watch?v=QQ49vPLM6nU" style="margin:1rem;border-radius:1rem;" target="_blank" rel="noopener noreferrer">
    <img src="img/thumbnail.jpeg" alt="Watch the video" width="800">
</a>



## Key Features
- Downloads all photos and videos from Google Photos
- Preserves original metadata (date, location, etc)
- Organizes files by year and month (2024/01_January/etc)
- Creates friendly filenames (1st January 2024_time_photo.jpg) 
- Tracks folder statistics (file count, total size)
- Skips existing files automatically


## Setting Up Google Photos API Access

### 1. Create a Google Cloud Project
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing one.
- *For official configuration guidance, consult [Google's Guide to Setting Up Access](https://support.google.com/cloud/answer/15549257).*

### 2. Enable Google Photos API
- Go to **APIs & Services**.
- Click on **"+ ENABLE APIS AND SERVICES"**.
- Search for **"Google Photos Library API"**.
- Click **"Enable"**.

### 3. Create OAuth 2.0 Credentials
- Search for **"Credentials"**.
- Select `User Data`> `Next`
- Give suitable name for the app such as `Photos Exporter`.
- Select user support email as your email.
- Scroll down and add your email as the `Developer Contact Information` > `Save and Continue`

### 4. Add Scopes

- Click add scope
- Now copy and paste this into the scope into Filter
```sh
https://www.googleapis.com/auth/photoslibrary
```
- Click the check box and add the scope
- Click Update

### 5. Oauth Client ID

- Select Desktop App in the application type.
- Leave the Name as is.
- Click create. It may take 5 mins to work.
- Click done.

## 7. Setting Up Test Users

- Here you should add your account from which you want to download the photos.
- And the account to which you would want to transfer photos.
- **Oauth Consent Screen > Audience**
- Scroll down and add test users.
- Add the gmails of whoever you want to access the script and click save.
- Now go to clients in the sidebar


##  Install Dependencies and Run

* Now Open Up the project directory. If you want to download click on the Green Code btn download and extract https://github.com/Underemployed/Google-Photos-Downloader.git

*  Move the downloaded `client_secre_12342.json` to the root of project directory.

* If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).

* Run the following commands in your terminal. The inline comments explain what each step does:

```sh
# Create a virtual environment (run this only once)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/macOS:
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```
- Run the application
```sh
python app.py
# Thank you for using my app.
```
- `log in` to your Google account, click `continue` and start downloading your Google Photos.

- Go back to the terminal and watch as your photos get transfer.

- If you want to transfer it to another account
You will lose some metadata, but you will be able to transfer all your photos and videos to another account.

- Run the application:
    <br> <br>
    ```sh
    python upload_to_another_acc.py
    ```





## Disclaimer

This tool was only written for the purpose of solving my own personal requirements.

I decided to make this public on GitHub because:

- It was useful for me, so maybe it'll be useful for others in the future.
- Future me might be thankful if I ever need to do this again.

With that said, please bear in mind that this tool won't be actively maintained and your mileage may vary. I'm sure it's far from perfect so if you choose to use it please proceed with caution and be careful to verify the results! I hope it's helpful.
