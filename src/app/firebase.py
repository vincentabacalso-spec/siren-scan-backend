import firebase_admin
from firebase_admin import credentials, firestore
import os 
from dotenv import load_dotenv
import json 

load_dotenv()

FIREBASE_ADMIN_SDK_PATH = json.loads(os.getenv("FIREBASE_ADMIN_SDK_PATH"))

cred = credentials.Certificate(FIREBASE_ADMIN_SDK_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()
