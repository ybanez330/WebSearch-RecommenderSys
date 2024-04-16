#-------------------------------------------------------------------------
# AUTHOR: Julia Ybanez
# FILENAME: db_connection_mongo.py
# SPECIFICATION: Accomplish executing MongoDB procedures.
# FOR: CS 4250- Assignment #3
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
import pymongo

def connectDataBase():

    # Create a database connection object using pymongo
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/corpus")
        db = client["corpus"]
        return db
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return None
    
def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary indexed by term to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    try:
        category_doc = col.database["categories"].find_one({"name": docCat})
        if category_doc is None:
            category_doc = {
                "name": docCat,
            }
            col.database["categories"].insert_one(category_doc)

        term_counts = {}
        terms = [term.strip('.,!?').lower() for term in docText.split()]

        for term in terms:
            if term in term_counts:
                term_counts[term] += 1
            else:
                term_counts[term] = 1


    
    # create a list of objects to include full term objects. [{"term", count, num_char}]
        term_objects = [{"term": term, "count": count} for term, count in term_counts.items()]

    # produce a final document as a dictionary including all the required document fields
        category_id = col.database["categories"].find_one({"name": docCat})["_id"]
        cleaned_text = ''.join([char for char in docText if char.isalnum()])
        num_chars = len(cleaned_text)
        document = {
            "doc_id": docId,
            "text": docText,
            "title": docTitle,
            "num_chars": num_chars,
            "date": docDate,
            "category_id": category_id,
            "terms": term_objects
        }

    # insert the document
        col.insert_one(document)

    except Exception as e:
        print("Error creating the document:", e)


def deleteDocument(col, docId):

    # Delete the document from the database
    try:
        col.delete_one({"doc_id": docId})
    except Exception as e:
        print("Error deleting the document:", e)


def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    try:
        category_doc = col.database["categories"].find_one({"name": docCat})
        if category_doc is None:
            category_doc = {
                "name": docCat,
            }
            col.database["categories"].insert_one(category_doc)

        # Delete the document
        col.delete_one({"doc_id": docId})

        # Create the document with the same id
        category_id = col.database["categories"].find_one({"name": docCat})["_id"]
        cleaned_text = ''.join([char for char in docText if char.isalnum()])
        num_chars = len(cleaned_text)
        document = {
            "doc_id": docId,
            "text": docText,
            "title": docTitle,
            "num_chars": num_chars,
            "date": docDate,
            "category_id": category_id,
        }

                # Insert the document
        col.insert_one(document)

        # Update the terms
        term_counts = {}
        terms = [term.strip('.,!?').lower() for term in docText.split()]

        for term in terms:
            if term in term_counts:
                term_counts[term] += 1
            else:
                term_counts[term] = 1

        term_objects = [{"term": term, "count": count} for term, count in term_counts.items()]
        col.update_one({"doc_id": docId}, {"$set": {"terms": term_objects}})

    except Exception as e:
        print("Error updating the document:", e)


def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    inverted_index = {}
    try:
        pipeline = [
            {"$unwind": "$terms"},
            {
                "$group": {
                    "_id": "$terms.term",
                    "counts": {"$push": {"title": "$title", "count": "$terms.count"}}
                }
            }
        ]

        result = list(col.aggregate(pipeline))

        for entry in result:
            term = entry["_id"]
            counts = entry["counts"]
            counts_str = ",".join([f"{item['title']}:{item['count']}" for item in counts])
            inverted_index[term] = counts_str

    except Exception as e:
        print("Error retrieving the inverted index:", e)

    return inverted_index