import firebase_admin
from firebase_admin import db, credentials


def initialize_firebase():
    cred = credentials.Certificate("sggsidcard-firebase-adminsdk-f5f1l-f87f4e292f.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://sggsidcard-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })


def fetch_student_details(reg_no):
    ref = db.reference(f"/students/{reg_no}")
    return ref.get()
