"""
Utility to build Google OAuth2 Credentials from a user's decrypted access token.
Reusable by GmailService and DriveService.
"""
from google.oauth2.credentials import Credentials


def build_google_credentials(access_token: str, scopes: list[str] | None = None) -> Credentials:
    """
    Construct a google.oauth2.credentials.Credentials object from a raw access token.
    This is used to authorize Google API client calls (Gmail, Drive, etc.).
    """
    return Credentials(
        token=access_token,
        scopes=scopes or [
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/calendar",
        ],
    )
