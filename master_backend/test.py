from flask import Flask, jsonify
from get_creds import AzureKeyVaultManager

app = Flask(__name__)

# Create a single instance of the KeyVault manager
kv_manager = AzureKeyVaultManager()

@app.route('/get-data')
def get_data():
    # Get credentials from cache
    credentials = kv_manager.get_credentials()
    # Use credentials as needed
    return {"status": "success", "data": credentials}

@app.route('/refresh-cache')
def refresh_cache():
    """Endpoint to force an immediate cache refresh"""
    result = kv_manager.force_refresh()
    return jsonify(result)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        # Ensure proper cleanup when shutting down
        kv_manager.stop()