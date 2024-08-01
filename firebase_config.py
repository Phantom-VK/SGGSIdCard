import firebase_admin
from firebase_admin import db, credentials

details = {
  "type": "service_account",
  "project_id": "sggsidcard",
  "private_key_id": "f87f4e292f9e7ca7f60a6aef90792ece8f2898bd",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCu3MLaW/hYXYEW\ne989n2mxlgkH+3OW62Myp3IcN/7le31Ld6KRsLM8h6gksiTjnHGFdFln0Wvh7SSK\nOSgT+iBXQlvAxZNyMy6SmngwcP7dPH4nqmAlkVSX7RILp93euW8AaF3pabBM4Mku\n/MwkjpumF0N+Oeg5mXjxkIEn+yYGbMV1zA7bnAYfFpmucu+tQQTzLjgFrvGqgZLu\n76j4uBxzO2MzCdyvyTX2VbmXoZvxpV7OmXFNAZakuSkBh/gYsm/bhPXn9qgEJcIp\nEH/ciTRy3glHqOq4gP12fpdYnTM3jwSmPw+IR6NXp6gNWbRJuKVJFmEGFPkVWk+w\nJTGtsRDtAgMBAAECggEACefOj/ESzeqqE9x7hnGf2qP9qfqYDy4RZf6vS6LuaRCI\nRfymdGtWk/C5WS7QQSaNFbrED8oAuwEkh0H6n7sVFuxW50Ip+pekpUBj25ajEWRK\nXzPbE3W6nYqb8ZYWTvYhMBw5aa4Hgyteqi8+3zlG3u9FbwKXwZ+Mht6hOmMTQdzS\nYFD0Zmok865CiK8NT5JWcYOkACSnGW8w6aIxCJnwFg1waSEq5eGa3QT0dpibxw1H\nrOs7RS0Jnv320PkmphyPLXy3n1iNw2FRH+Y+/hHBfrykii0Tw6ziV38DLbpUMlgv\nr7y/RTPECIMVf+E0ey6fraSxNtHOPAhgCMpWJCqnkQKBgQDvtFdg02NcIuPvSXNz\nyhJp5OqUR7VBjE2EeP6cn39/9Yzgd83HUxgMLWnz3diclS6u2fU1FYSl0fPSm0ec\noxlr0vv6xL3NMV4pFAukr24utrNf2VhqGrOS+fko/r7eiTZ/TUAbosE/xGSyjJqb\nzsdNwvswd/ifXzY0J81fZdJqBQKBgQC6v/NNkkTGaDzbOCummOfsrPYQFlUJyiAs\nVLKP9zx+kIoatMgqhzzi2tPhVtP4YrM/7CqVWVvbEMqFvgAdubZNXXZAd/3a7mz0\nZlPItWo21RW27KJbiPemhWRjk8qLqWOWEyXX8DXvbw0sHmaZkvd9Fiopukad65vq\nFF4Z5D33yQKBgAVWG3fhXN3pPO/Pz80tG3nWCc7hRcy+xd8EHo74EguUON2qbR9Z\n3zguLqSqNK9PtulXmtjisMBMS0ROBqsbCm7XFJsBlEQkLDd35cZ1zVsm4BlrKke6\nbnMAM6bQ/QjRPzBYVOwIlIrJ4YAEF1EOqms1wwfSM+vAX+GLXUwZZTTNAoGAaGAi\nRyfKQq493TR+ySVK8vAUsxcYPll3M+++wVIowIBef+Csw4BEmnI93AMghAH+N2ry\nvfhsq3quBqQUAokqiAEFt7CY9IUv5kVO7K3giHb+JPgLImfiKnMBkdonaXmqDFX1\nX8SFEKab0R3IsGsA4ivCMwJGt7rYsLLjiUsVC2kCgYEAiUeuBju5cmE4LqlGdxZi\nPB4TAawq9uRNn3etufM+pimRlSAncV5dffmCfzflJluMmI0791xeDQ8hys0Gzi7C\nzNWRwokDWT+oUrd28mTySHmjZQKH3f1qX9PY6o4J8qp72/Ge9Kfnc/EZMMezP8D0\nQm6jrINCsLYDSIWrrV8O2eo=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-f5f1l@sggsidcard.iam.gserviceaccount.com",
  "client_id": "112822596247114724111",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-f5f1l%40sggsidcard.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

def initialize_firebase():
    cred = credentials.Certificate(details)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://sggsidcard-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })


def fetch_student_details(reg_no):
    ref = db.reference(f"/students/{reg_no}")
    return ref.get()
