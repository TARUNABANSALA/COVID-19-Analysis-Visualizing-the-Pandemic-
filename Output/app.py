
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Create an instance of MongoClient
mongo = MongoClient(port=27017)
db = mongo.COVID19_pandemic

# Collection name 
COVID19_data = db['COVID19_data']

@app.route('/')
def index():
    return 'Hello, World!'

# Define API route
@app.route('/data', methods=['GET'])
def get_data():
    data = []
    query = {'Province': 'ON'}
    results = COVID19_data.find(query)
    for result in results:
        data.append({
            'id': str(result['_id']),
            'Province': result['Province'],
            'Cases': result['Cases']
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
