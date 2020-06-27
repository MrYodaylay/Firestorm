# Firestorm
Firestorm is an object-relational mapping (ORM) that allows easy, Pythonic access to Google Cloud Firestore. There are 
a number of similar projects on Github and PyPi, but I chose to write my own ORM for the experience. The code is likely
 of low quality, and limited features are included. However, if you believe this project would suit your needs, you are 
 free to use it. I will probably implement more features (and write some documentation) in the future. 

### Requirements
```
google-cloud-firestore==1.7.0
```

### Usage
```python
from Firestorm import Client, Collection, Document

cli = Client(credential_path='/path/to/service-account/json')
col = cli.collection('collection_name')
```
To create a new document:
```python
doc = col.document()
```
A document is loaded from the database if the document_id is present, or a new document is created if it is not present.
```python
with col.document('document_id') as doc:
    doc.Name = 'John'
    doc.Email = 'john@exmaple.com'
```
Later, the document can be recovered and the variables accessed:
```python
with col.document('document_id') as doc:
    print(doc.Name)
    print(doc.Email)
# Expected output:
# John
# john@example.com
```
If you do not want to use the with statement, you must call the `save()` method on the document for the document to be 
pushed to the database.