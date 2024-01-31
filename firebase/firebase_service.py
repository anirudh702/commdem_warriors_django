import logging
from typing import Any, Dict
from uuid import uuid4

import firebase_admin
from django.conf import settings
from django.core.cache import cache
from firebase_admin import auth, credentials, firestore

from user.models import UserModel

cred = credentials.Certificate(
    settings.GOOGLE_APPLICATION_CREDENTIALS
)  # path to credentials.json file

firebase_app = firebase_admin.initialize_app(cred)
auth_client = auth.Client(app=firebase_app)
firestore_client = firestore.client(app=firebase_app)

logger = logging.getLogger(__name__)


def cached(func):
    def wrapper(*args, **kwargs):
        user = kwargs.get("user")
        key = "token_" + str(user.id)
        token = cache.get(key)
        if token is None:
            token = func(*args, **kwargs)
            cache.set(key, token, timeout=60 * 60)  # 1 hour
        return token

    return wrapper


class FirebaseService:
    @staticmethod
    @cached
    def get_custom_token_for_user(user: UserModel):
        auth_claims = {
            "uid": user.id,
        }
        return auth_client.create_custom_token(
            uid=user.id, developer_claims=auth_claims
        )

    @staticmethod
    def send_notification_to_user(user: UserModel, message: Dict[str, Any]):
        msg_id = str(uuid4())
        notification_ref = (
            firestore_client.collection("app-notifications")
            .document("{}".format(user.id))
            .collection("user-notifications")
            .document("{}".format(msg_id))
        )

        notification_ref.set({"message": message, "id": msg_id})
        logger.info("Notification sent to user {}".format(user.id))
