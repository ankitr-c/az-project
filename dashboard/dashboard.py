# dashboard.py
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
# URL of the backend API
API_URL = "http://127.0.0.1:5000/get_data"


@app.route('/health')
def health():
    return "OK", 200

# Route to render dashboard
@app.route('/dashboard')
def dashboard():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            return render_template('dashboard.html', users=data)
        else:
            return render_template('dashboard.html', users=[], error=f"Unable to fetch data. Status code: {response.status_code}"), 500
    except Exception as e:
        return render_template('dashboard.html', users=[], error=f"Error: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5001)
