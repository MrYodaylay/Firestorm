from google.cloud import firestore

import Firestorm


class Client:
	__firestore_client: firestore.Client

	def __init__(self):
		self.__firestore_client = firestore.Client()

	def collections(self):
		for c in self.__firestore_client.collections():
			yield Firestorm.Collection(collection=c)

	def collection(self, path: str):
		return Firestorm.Collection(collection=self.__firestore_client.collection(path))

	def document(self, *paths: str):
		return Firestorm.Document()
