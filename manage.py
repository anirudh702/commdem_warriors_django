#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from uuid import uuid4
from firebase_admin import initialize_app
from firebase_admin import credentials
from oauth2client.service_account import ServiceAccountCredentials
import requests
cred = credentials.Certificate('/Users/apple/Downloads/commdem__firebase_credentials.json')
BASE_URL = 'https://firebaseremoteconfig.googleapis.com'
REMOTE_CONFIG_ENDPOINT = 'v1/projects/' + 'commdemwarriors' + '/remoteConfig'
REMOTE_CONFIG_URL = BASE_URL + '/' + REMOTE_CONFIG_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.remoteconfig']

initialize_app(cred, 
{
"databaseURL": "https://commdemwarriors-default-rtdb.firebaseio.com/"
})

# def _get_access_token():
#   """Retrieve a valid access token that can be used to authorize requests.
#   :return: Access token.
#   """
#   credentials = ServiceAccountCredentials.from_json_keyfile_name(
#       '/Users/apple/Downloads/commdem__firebase_credentials.json', SCOPES)
#   access_token_info = credentials.get_access_token()
#   print(access_token_info.access_token)
#   return access_token_info.access_token

headers = {
    'Authorization': 'Bearer ya29.c.b0Aa9Vdyn44G2xuIhfozXK9LreUIGbb6NNfgCWCyRiSvXZd0t1-RA7-quDC6TCrvsEcQ9EcsRFSh3yB8hgwv8SYFh2VJftGKRQW9jh2nK6FHrv9uU5PCGaJxCti2gph4muh1KhMg4JB2xDJtuclfnkDhsE1KvOrIBybIAd113nCtmakhaWWpF9GjKbjF2T8oibKWnF3JVfwctDlAdk7N01LL-qcbhJHZI'
  }
# resp = requests.get(REMOTE_CONFIG_URL, headers=headers)

# print("data from api")
# print(resp.content)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commdem_warriors_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

