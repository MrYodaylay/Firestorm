# Firestorm
Firestorm is an object-relational mapping (ORM) for Google's NoSQL database, Cloud Firestore. I wrote this library
because I did not like the official Python client from Google, and to gain experience in Python. There are many
similar libraries available on PyPi, which may be more suited to your project, and I encourage you to search for them,
as they are likely to be higher quality or have more features. You are free to use this library in your personal 
projects without restrictions (MIT License).



### Requirements
```
google-cloud-firestore==2.3.4
```

### Usage
#### Requirements
```google-cloud-firestore==2.3.4```
#### Authentication
There are three main authentication methods:
* If you're running Firestorm on Google Cloud (e.g. Compute Engine or App Engine), you shouldn't need to authenticate
* If you're developing locally, and have the GCloud tool installed, you can run: `gcloud auth application-default login`
* For any other situation, create a service account, download the JSON keyfile, and point to it with an environment
variable: ```GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"```
#### Example

```python
import Firestorm

# Create an instance of Client
db = Firestorm.Client()

# Get an instance of a collection. Will be created if not present on the server
coll = db.collection("apple")

# Get an instance of a document. Will be created if not present on the server
doc = coll.document("alice")

# Use the document instance like a dictionary
doc["friend"] = "bob"

# Submit to server
doc.save()
```