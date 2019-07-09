import firebase_admin, os
from firebase_admin import credentials, firestore
from fantasy_app.yahoo_api.const import firebase_credentials
class Firebase:
	def __init__(self):
		firebase_admin.initialize_app(credentials.Certificate(firebase_credentials), {'projectid': 'fantasyfootball-ee95c'})
		self.db = firestore.client()

	def add_document(self, collection, key, data):
		self.db.collection(collection).document(key).set(data)

	def remove_document(self, collection, key):
		for doc in self.db.collection(collection).get():
			if doc.id == key: doc.reference.delete()

	def update_document(self, collection, key, data):
		self.db.collection(collection).document(key).update(data)

	def get_documents(self, collection):
		return {doc.id: doc.to_dict() for doc in self.db.collection(collection).get()}

	def get_document(self, collection, key):
		for doc in self.db.collection(collection).get():
			if doc.id == key:
				return doc.to_dict()
		return None





