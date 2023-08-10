# # pip install flask pymongo
# from flask import Flask, render_template
# from pymongo import MongoClient
# app = Flask(__name__)
# # Configure MongoDB connection
# client = MongoClient('mongodb://localhost:27017')
# db = client['Covid19_project3']
# collection = db['vaccinemap_data']
# print(collection.find_one())
# @app.route('/display_collection_content')
# def display_collection_content():
#     documents = collection.find()
#     print(documents.count())
#     return render_template('index.html', documents=documents)
# if __name__ == '__main__':
#     app.run()
# # use this one for jsonify output
# # def display_collection_content():
# #     documents = list(collection.find())
# #     json_documents = json.dumps(documents, default=str)
# #     return json_documents

from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from credentials import username, password
from pprint import pprint 

app = Flask(__name__)

# Define your credentials and DBname
client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.mymgc5e.mongodb.net/')

# Test if connected to the MongoDB Atlas
# print(client.list_database_names())

dbname = 'covid_db'
db = client[dbname]  # MongoDB database
print(db.list_collection_names())

#assign each collection to a variable 

dataset_1 = db['dataset_1']
dataset_2 = db['dataset_2']
dataset_3 = db['dataset_3']

#Welcome Page 
@app.route("/")
def main_page():
    return "<h2>Main Page for Flask API</h2>"

#Confirmed Cases per Day 
@app.route("/daily_cases")
def confirmed_data():
    query = {}
    fields = {'Province':1, 'Date':1, 'Confirmed cases per day':1}
    results = dataset_1.find(query, fields)
    output_list = [convert_object_id(result) for result in results]

    return jsonify(output_list)

#Mortality Rate 
@app.route("/mortality_rate")
def mortality_data():
    query = {}
    fields = {'Province':1, 'Date':1, 'Mortality rate':1}
    results = dataset_1.find(query, fields)
    results_list = [convert_object_id(result) for result in results]

    return jsonify(results_list)

def convert_object_id(result):
    result['_id'] = str(result['_id'])
    return result

#Vaccination 
@app.route("/vaccines")
def vaccine_rate():
    query = {}
    fields = { }


if __name__ == '__main__' :
    app.run(debug=True, port=5000)
