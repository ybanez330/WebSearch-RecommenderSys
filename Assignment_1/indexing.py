#-------------------------------------------------------------------------
# AUTHOR: Julia Ybanez
# FILENAME: indexing.py
# SPECIFICATION: This program reads the file collection.csv and output the tf-idf document-term matrix.
# FOR: CS 4250- Assignment #1
# TIME SPENT: 1.5 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv
import math

documents = []

#Reading the data in a csv file
with open('Assignment_1/collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])

#Conducting stopword removal. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}

for document in documents:
  index = documents.index(document)
  documents[index] = document.split(" ")

for document in documents:
  for term in document:
    if term in stopWords:
      document.remove(term)

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}
for document in documents:
  for term in document:
    index = document.index(term)
    if term in steeming.keys():
      term = steeming[term]
    document[index] = term

#Identifying the index terms.
#--> add your Python code here
terms = []
for document in documents:
    for term in document:
        if term not in terms:
            terms.append(term)

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
docTermMatrix = []

docTermMatrix = []
for document in documents:
    doc_row = []
    for term in terms:
        tf = document.count(term) / len(document)
        df = sum(1 for doc in documents if term in doc)
        idf = math.log10(len(documents) / df)
        tfidf = tf * idf
        doc_row.append(tfidf)
    docTermMatrix.append(doc_row)

#Printing the document-term matrix.
#--> add your Python code here
for i, row in enumerate(docTermMatrix):
    print(f"Document {i+1}: {row}")