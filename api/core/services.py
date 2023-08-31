import requests
from django.conf import settings
from rest_framework import status


class GoogleAuthService:
    GOOGLE_AUTH_CLIENT_ID = settings.GOOGLE_AUTH_CLIENT_ID
    GOOGLE_AUTH_SECRET_KEY = settings.GOOGLE_AUTH_SECRET_KEY
    GOOGLE_AUTH_REDIRECT_URL = settings.GOOGLE_AUTH_REDIRECT_URL

    def get_access_token(self, code: str) -> dict:
        """
        Get access token from Google API by giving the auth code.
        """
        base_url = "https://oauth2.googleapis.com/token"
        headers = {'content-type': 'application/json'}
        params = {
            "code": code,
            "client_id": self.GOOGLE_AUTH_CLIENT_ID,
            "client_secret": self.GOOGLE_AUTH_SECRET_KEY,
            "redirect_uri": self.GOOGLE_AUTH_REDIRECT_URL,
            "access_type": "offline",
            "grant_type": "authorization_code"
        }

        try:
            r = requests.post(base_url, params=params, headers=headers)
            print(r)
            response = r.json()
            status_code = r.status_code
        except Exception as e:
            print(e)

        if status_code == status.HTTP_200_OK:
            return response["access_token"]

        return None

    def get_profile_info(self, access_token: str) -> dict:
        """
        Get profile info from Google API via access token.
        """
        base_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f'Bearer {access_token}'}

        try:
            r = requests.get(base_url, headers=headers)
            response = r.json()
            status_code = r.status_code
        except Exception as e:
            print(e),

        if status_code == status.HTTP_200_OK:
            return response
        return None
