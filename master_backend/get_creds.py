import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import json
from datetime import datetime, timedelta
import threading
import time

class AzureKeyVaultManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AzureKeyVaultManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            self.KV_URI = "https://az-project-key-vault.vault.azure.net"
            self.credential = DefaultAzureCredential()
            self.client = SecretClient(vault_url=self.KV_URI, credential=self.credential)
            self.cache = {}
            self.cache_timestamp = None
            self.cache_duration = timedelta(hours=1)
            self.initialized = True
            
            # Start background refresh thread
            self.should_run = True
            self.refresh_thread = threading.Thread(target=self._auto_refresh_cache)
            self.refresh_thread.daemon = True
            self.refresh_thread.start()

    def _fetch_from_keyvault(self, secret_name):
        """Fetch secret directly from Azure Key Vault"""
        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            print(f"Error fetching secret from Key Vault: {e}")
            return None

    def _refresh_cache(self):
        """Refresh all secrets in cache"""
        try:
            # Fetch az-creds secret
            secret_value = self._fetch_from_keyvault("az-creds")
            if secret_value:
                try:
                    # Assume the secret is stored as JSON string
                    self.cache = json.loads(secret_value)
                except json.JSONDecodeError:
                    # If not JSON, store as simple string
                    self.cache = {"az-creds": secret_value}
                
            self.cache_timestamp = datetime.now()
            print("Cache refreshed successfully")
            return True
        except Exception as e:
            print(f"Error refreshing cache: {e}")
            return False

    def _auto_refresh_cache(self):
        """Background thread to automatically refresh cache"""
        while self.should_run:
            if not self.cache_timestamp or \
               datetime.now() - self.cache_timestamp >= self.cache_duration:
                self._refresh_cache()
            time.sleep(60)  # Check every minute

    def get_credentials(self):
        """Get credentials from cache, refreshing if necessary"""
        if not self.cache_timestamp or \
           datetime.now() - self.cache_timestamp >= self.cache_duration:
            self._refresh_cache()
        return self.cache

    def force_refresh(self):
        """Force an immediate refresh of the cache"""
        with self._lock:  # Ensure thread safety during manual refresh
            success = self._refresh_cache()
            return {
                "success": success,
                "timestamp": self.cache_timestamp.isoformat() if self.cache_timestamp else None,
                "message": "Cache refreshed successfully" if success else "Failed to refresh cache"
            }

    def stop(self):
        """Stop the background refresh thread"""
        self.should_run = False
        if self.refresh_thread.is_alive():
            self.refresh_thread.join()