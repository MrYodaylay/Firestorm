from google.cloud import firestore

import Firestorm


class Collection:
	__firestore_collection: firestore.CollectionReference

	def __init__(self, path=None, *, collection: firestore.CollectionReference = None):
		if collection:
			self.__firestore_collection = collection

		elif path:
			self.__firestore_collection = firestore.CollectionReference(path)

	def document(self, name: str = None):
		return Firestorm.Document(document=self.__firestore_collection.document(name))



