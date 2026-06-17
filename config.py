from pathlib import Path
# Look for client_secret_*.json
matches = list(Path.cwd().glob("client_secret_*.json"))




# CONFIG 'secret-token.json'
CLIENT_SECRET_FILE = str(matches[0]) if matches else 'secret-token.json'
API_NAME = 'photoslibrary'
API_VERSION = 'v1'
SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary'
]







