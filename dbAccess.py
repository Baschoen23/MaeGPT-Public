from pymongo import MongoClient
from nameGenerator import generate_name
import datetime
from stringGenerator import generate_string

client = MongoClient('localhost', 27017)
db = client.maegptRecall

def increment_conversation_count():
    """
    Increments the conversation count stored in collectionCount.txt.
    """
    print("Incrementing conversation count")

    # Read the current conversation count from the file
    with open("collectionCount.txt", "r") as f:
        current_count = int(f.read())

    # Increment the conversation count
    new_count = current_count + 1

    # Write the new conversation count to the file
    with open("collectionCount.txt", "w") as f:
        f.write(str(new_count))

    return new_count


with open("collectionCount.txt", "r") as f:
    f.seek(0)
    f.readlines()

collection_name = "recall" + str(increment_conversation_count)
personality = "personality"
print(collection_name)
global collection
collection = db[collection_name]
collectionPersonality = db[personality]

def create_session_doc(session_id, data, prompt):
    conversationName = generate_name(prompt)
    jsonDoc = {"_id": session_id, "name": conversationName, "conversations": []}
    collection.insert_one(jsonDoc)
    collection.update_one({'_id': session_id}, {'$push': {'conversations': data}}, upsert=True)
    print("Data updated")
    #client.close()
    return session_id


def access_db():
    """
    Retrieves all conversation records from the database.
    """
    print("Accessing database")
    data = collection.find()
    conversation_recall = [line for block in data for line in block['conversations']]
    return conversation_recall

print(access_db())


def update_db(session_id, data):
    """
    Updates the conversation record in the database.
    """
    result = collection.update_one({'_id': session_id}, {'$push': {'conversations': data}}, upsert=True)
    if result.modified_count or result.upserted_id:
        print("Data updated")
    else:
        print("No data updated")



def get_from_db():
    #client = MongoClient('localhost', 27017)
    #db = client.MaeGPT
    #collection = db.NewDBTest
    data = collection.find()
    client.close()
    return data


def save_to_db(data):
    #client = MongoClient('localhost', 27017)
    #db = client.MaeGPT
    #collection = db.NewDBTest
    collection.insert_one(data)
    client.close()


def get_names_from_db():
    #client = MongoClient('localhost', 27017)
    #db = client.MaeGPT
    #collection = db.NewDBTest
    data = collection.find()
    historyList = []
    for doc in data:
        historyList.append(doc['name'].replace("\"", ""))
    client.close()
    return historyList




''' 
return {
    "id": counter,
    "session_id": "session_id",
    "user_id": "user_id",
    "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
    "recall_documents": []
    }
'''