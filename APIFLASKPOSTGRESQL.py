# Import the dependencies.
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import psycopg2
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
app = Flask(__name__)
params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'Project3',
    'user': 'postgres',
    'password': ''
}

def run_query(query, values=None):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    if values:
        cur.execute(query, values)
    else:
        cur.execute(query)
    conn.commit()
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Covid-19 Data (Canada,Provice) API!<br/>"
        f"Available Routes:<br/>"
        f"STATIC ROUTES<br/>"
        f"/api/v1.0/Covid_19_route/Covid_19_data<br/>"
#         # f"DYNAMIC ROUTES<br/>"
#         # f"/api/v1.0/measurement_data/start_date/<start_date><br/>"    
    )

@app.route('/api/v1.0/Covid_19_route/Covid_19_data', methods=['GET'])
def Covid_19_data():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # Fetch the data from the Covid_19 table
        cur.execute('SELECT * FROM public."Covid_19"')
        data = cur.fetchall()
        
        # Close the database connection
        cur.close()
        conn.close()

        # Convert the data to a JSON response
        output = []
        for entry_date in data: 
            entry_date_data = {}
            entry_date_data["Entry_date"] = entry_date[1]
            output.append(entry_date_data)
        return jsonify(output)    

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'An error occurred while accessing the database.'}), 500

if __name__ == '__main__':
    app.run()

