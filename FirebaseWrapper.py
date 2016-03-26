from firebase import firebase
import json

class FirebaseWrapper:
    def __init__(self, url, db_store):
        self.firebase = firebase.FirebaseApplication(url, None)
        self.db_store = db_store
        
    def write_data(self, key, data):
        result = self.firebase.put(self.db_store, key, json.dumps(data, separators=(',', ':')))
        return result

    def get_data(self, key):
        result = self.firebase.get(self.db_store, key)
        return json.loads(result)
    
    def delete_data(self, key):
        result = self.firebase.delete(self.db_store, key)
        return result
