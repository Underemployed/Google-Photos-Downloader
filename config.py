from pathlib import Path
import sys

# The code Look for a Google OAuth client secret file in the current folder.
# The file usually has a name like:
# client_secret_xxxxxxxxxxxxxxxxx.json
matches = list(Path.cwd().glob("client_secret_*.json"))

# If no client secret file is found, show instructions and exit.
if not matches:
    print(
        "\n[ERROR] Google OAuth Client Secret file not found.\n"
        "Please follow the setup instructions in the project README:\n"
        "https://github.com/Underemployed/Google-Photos-Downloader/blob/main/README.md\n\n"
        "After downloading the OAuth Client Secret JSON file,\n"
        "place it in the same folder as this script and try again.\n"
    )
    sys.exit(1)

# Use the first matching client secret file found.
CLIENT_SECRET_FILE = str(matches[0])

# Google Photos API configuration
API_NAME = 'photoslibrary'
API_VERSION = 'v1'

SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary'
]

