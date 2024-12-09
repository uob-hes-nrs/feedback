import firebase_admin
from firebase_admin import credentials, firestore
#This code doesnt work without the API Key, however it was sued to populate the database with example users

SERVICE_ACCOUNT_FILE = 'API_KEY'
cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)

db = firestore.client()

documents = [
    {"email": "emma.johnson@bham.com", "name": "Emma Johnson", "role": "moduleorganiser"},
    {"email": "liam.williams@bham.com", "name": "Liam Williams", "role": "marker"},
    {"email": "sophia.brown@bham.com", "name": "Sophia Brown", "role": "marker"},
    {"email": "james.jones@bham.com", "name": "James Jones", "role": "student"},
    {"email": "isabella.garcia@bham.com", "name": "Isabella Garcia", "role": "student"},
    {"email": "benjamin.martinez@bham.com", "name": "Benjamin Martinez", "role": "student"},
    {"email": "mia.rodriguez@bham.com", "name": "Mia Rodriguez", "role": "student"},
    {"email": "lucas.davis@bham.com", "name": "Lucas Davis", "role": "student"},
    {"email": "amelia.lopez@bham.com", "name": "Amelia Lopez", "role": "student"},
    {"email": "elijah.hall@bham.com", "name": "Elijah Hall", "role": "student"},
    {"email": "ava.clark@bham.com", "name": "Ava Clark", "role": "student"},
    {"email": "henry.lewis@bham.com", "name": "Henry Lewis", "role": "student"},
    {"email": "charlotte.walker@bham.com", "name": "Charlotte Walker", "role": "student"},
    {"email": "jack.young@bham.com", "name": "Jack Young", "role": "student"},
] #all users were randomly generated

def add_documents(docs, collection):
    for doc in docs:
        db.collection(collection).add(doc)
        print(f"Added document: {doc} to  {collection}")

add_documents(documents, "users")
