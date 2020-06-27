from google.cloud import firestore
import os


class Client:

	_firestore_client: firestore.Client

	def __init__(self, *, project=None, credentials=None, credential_path=None):
		if credential_path is not None:
			os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

		self._firestore_client = firestore.Client()

	def collection(self, path: str):
		c = self._firestore_client.collection(path)
		return Collection(path, c)


class Collection:
	"""A collection is a grouping of documents. All documents must be in a collection."""

	_firestore_collection: firestore.CollectionReference

	def __init__(self, path, c):
		self._firestore_collection = c

	def document(self, path=None):
		f = self._firestore_collection.document(path)
		return Document(f)


class Document:
	"""The Document class provides Python class like access to Google Cloud Firestore documents.

	A Document object is obtained from a Collection object. The document in that collection on the
	remote server will be returned, or, if not found, a new document will be created.

	"""

	_firestore_document: firestore.DocumentReference
	_firestore_snapshot: firestore.DocumentSnapshot

	_data: dict
	_mod: dict

	def __init__(self, d):
		self._firestore_document = d
		self._firestore_snapshot = self._firestore_document.get()

		self._data = {}
		self._mod = {}

		if self._firestore_snapshot.exists:
			snapshot = self._firestore_snapshot.to_dict()
			for value in snapshot:
				self._data[value] = snapshot[value]

	def __getattr__(self, item):
		if item in self.__dict__['_mod']:
			return self.__dict__['_mod'][item]
		elif item in self.__dict__['_data']:
			return self.__dict__['_data'][item]
		else:
			raise KeyError

	def __setattr__(self, key, value):
		if key in self.__annotations__:
			self.__dict__[key] = value
		else:
			self._mod[key] = value

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.save()

	def save(self):
		self._firestore_document.set(self._mod, merge=True)

