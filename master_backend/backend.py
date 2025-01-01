# main.py
from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from get_creds import AzureKeyVaultManager

app = Flask(__name__)
CORS(app)


try:
    kv_manager = AzureKeyVaultManager()    
    credentials = kv_manager.get_credentials()
except Exception as e:
    print(f"Error initializing AzureKeyVaultManager: {e}")


# Database configuration
db_config = {
    'user': credentials['username'],
    'password': credentials['password'],
    'host': credentials['db_endpoint'],
    'port': credentials['port'],
    'database': credentials['database']  # Replace with your database name
}

# db_config = {
#     'user': 'root',
#     'password': 'root',
#     'host': 'localhost',
#     'port': 8000,
#     'database': 'azproject'  # Replace with your database name
# }


# Connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/health')
def health_check():
    return 'OK', 200
# API to add data
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    mobile = data.get('mobile')

    if not (name and email and mobile):
        return jsonify({"error": "All fields are required: name, email, mobile."}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email, mobile) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Data added successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to get data
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0',port=5000)
    finally:
        # Ensure proper cleanup when shutting down
        kv_manager.stop()

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0',port=5000)
