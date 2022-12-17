import time
from datetime import timedelta
from uuid import uuid4

from firebase_admin import db

__all__ = ['send_to_firebase', 'update_firebase_snapshot']


def send_to_firebase():
    ref = db.reference()
    print("scsdcs")
    ref.update({
        "is_updated" : False
    })



# def update_firebase_snapshot(snapshot_id):
#     start = time.time()
#     db = firestore.client()
#     db.collection('notifications').document(snapshot_id).update(
#         {'is_read': True}
#     )
#     end = time.time()
#     spend_time = timedelta(seconds=end - start)
#     return spend_time