import firebase_admin
from firebase_admin import credentials, firestore

# Caminho para o arquivo JSON da chave privada
cred = credentials.Certificate("serviceAccountKey.json")

# Inicializa o Firebase
firebase_app = firebase_admin.initialize_app(cred)

# Inicializa o Firestore (opcional)
db = firestore.client()