import time
from datetime import timedelta
from uuid import uuid4

from firebase_admin import firestore

__all__ = ['send_to_firebase', 'update_firebase_snapshot']

def send_to_firebase():
    db = firestore.client()
    doc_ref = db.collection('testing').document(str(uuid4()))
    doc_ref.set({
    u'name': u'Alan',
})


def update_firebase_snapshot(snapshot_id):
    start = time.time()
    db = firestore.client()
    db.collection('notifications').document(snapshot_id).update(
        {'is_read': True}
    )
    end = time.time()
    spend_time = timedelta(seconds=end - start)
    return spend_time