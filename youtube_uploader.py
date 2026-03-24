import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Scopes dictate what we have access to
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secret.json"

def get_authenticated_service():
    """
    Authenticates the user using OAuth2 and returns a YouTube Data API service object.
    It expects a 'client_secret.json' file downloaded from Google Cloud Console.
    """
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"Error: Could not find '{CLIENT_SECRETS_FILE}'.")
        print("Please download your OAuth 2.0 client secrets file from Google Cloud Console and place it in the project directory.")
        return None

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    
    # Run the local server to handle the authentication flow
    credentials = flow.run_local_server(port=0)
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    return youtube

def upload_video(youtube, video_file, title, description, category_id="24", privacy_status="public"):
    """
    Uploads a video to YouTube.
    category_id="24" is for Entertainment.
    privacy_status can be "private", "public", or "unlisted".
    """
    if not os.path.exists(video_file):
        print(f"Error: Video file '{video_file}' not found.")
        return False

    print(f"Preparing to upload '{video_file}'...")
    
    # Append some tags and standard description for Shorts
    tags = ["Reddit", "Story", "Scary", "Nosleep", "Shorts", "TTS"]
    full_description = f"{description}\n\n#shorts #reddit #story #nosleep"
    
    request_body = {
        "snippet": {
            "categoryId": category_id,
            "title": title[:100], # YouTube max title length is 100
            "description": full_description,
            "tags": tags
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media_file = MediaFileUpload(video_file, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = None
    print("Uploading video...")
    try:
        response = request.execute()
        print(f"Upload Successful! Video ID: {response.get('id')}")
        return True
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return False
        
if __name__ == "__main__":
    youtube_service = get_authenticated_service()
    if youtube_service:
        print("Authenticated successfully.")
