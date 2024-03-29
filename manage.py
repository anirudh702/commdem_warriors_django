#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from uuid import uuid4


# FIREBASE_APP = initialize_app()

# Use a service account.
# cred = credentials.Certificate('/Users/anirudh.chawla/Downloads/commdemwarriors-firebase-adminsdk-adstw-d344ebfefd.json')

# firebase_admin.initialize_app(cred, 
# {
# "databaseURL": "commdemwarriors.firebaseio.com/"
# })


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

