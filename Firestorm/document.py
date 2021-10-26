from google.cloud import firestore

import Firestorm


class Document:
	__firestore_document: firestore.DocumentReference
	__firestore_snapshot: firestore.DocumentSnapshot

	__local_cache: dict = {}
	__fetch_cache: dict = {}
	__is_subscribed: bool = False
	__has_fetch_cache: bool = False
	__watch: firestore.Watch = None

	def __init__(self, path: str = None, *, document: firestore.DocumentReference = None, preload: bool = False):
		if document:
			self.__firestore_document = document

		elif path:
			self.__firestore_document = firestore.DocumentReference(path)

		if preload:
			self.__fetch()

	def __update_cache(self):
		"""Copies data from the FirestoreSnapshot to the fetch_cache"""
		self.__fetch_cache = self.__firestore_snapshot.to_dict()
		self.__has_fetch_cache = True

	def __fetch(self, paths: list[str] = None):
		"""Download data from the Firestore server and calls __update_cache"""
		self.__firestore_snapshot = self.__firestore_document.get(paths)
		self.__update_cache()

	def fetch(self, paths: list[str] = None):
		self.__fetch(paths)

	def __cached_get(self, item):
		"""Searches for item in the fetch_cache, calling _fetch if necessary to fill the cache"""
		if not self.__has_fetch_cache:
			self.__fetch()

		if item in self.__local_cache:
			return self.__local_cache[item]

		return self.__fetch_cache[item]

	def get(self, item):
		self.__cached_get(item)

	def __flatten_caches(self):
		"""Merges local_cache and fetch_cache, as though the document was saved
		and fetched again, but without the overhead"""
		for key in self.__local_cache:
			self.__fetch_cache[key] = self.__local_cache[key]
		self.__local_cache = {}

	def save(self):
		self.__firestore_document.update(self.__local_cache)
		self.__flatten_caches()

	def watch(self):
		def watch_callback(snapshot, changes, read_time):
			if snapshot:
				self.__firestore_snapshot = snapshot[0]
				self.__update_cache()

		if not self.__watch:
			self.__watch = self.__firestore_document.on_snapshot(watch_callback)

	def unsubscribe(self):
		self.__watch.unsubscribe()

	def __setitem__(self, key, value):
		self.__local_cache[key] = value

	def __delitem__(self, item):
		self.__local_cache[item] = firestore.DELETE_FIELD

	def __getitem__(self, item):
		return self.__cached_get(item)

