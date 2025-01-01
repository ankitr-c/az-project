from flask import Flask, jsonify
import time
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from cachetools import LRUCache
from cachetools import TTLCache

# Initialize Flask application
app = Flask(__name__)

# Key Vault URI and Secret Name
KVUri = "https://az-project-key-vault.vault.azure.net"
secretName = "az-creds"

# Initialize Azure credentials and Key Vault client
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

# Initialize the cache with a time-to-live (TTL) of 24 hours (86400 seconds)
cache = TTLCache(maxsize=1, ttl=86400)  # maxsize=1 for one item (the creds)

def fetch_creds_from_keyvault():
    """Fetch the secret from Azure Key Vault."""
    print("Fetching creds from Key Vault...")
    retrieved_secret = client.get_secret(secretName)
    return retrieved_secret.value

@app.route('/get-creds', methods=['GET'])
def get_creds():
    """Endpoint to return the cached credentials."""
    # Check if creds are cached
    if secretName in cache:
        print("Returning cached creds.")
        creds = cache[secretName]
    else:
        print("Creds expired or not cached. Fetching from Key Vault.")
        creds = fetch_creds_from_keyvault()
        # Cache the creds for the next 24 hours
        cache[secretName] = creds
    
    return jsonify({"creds": creds})

if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True,port=5000,host='0.0.0.0')
