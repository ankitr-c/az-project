import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

KVUri = "https://az-project-key-vault.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

secretName="az-creds"
print(f"Retrieving your secret from KV_NAME.")

retrieved_secret = client.get_secret(secretName)

print(f"Your secret is '{retrieved_secret.value}'.")



###########CREATING NEW SECRETS############
# secretName = "SECRET_NAME"
# secretValue = "SECRET_VALUE"
# 
# print(f"Creating a secret in KV_NAME called '{secretName}' with the value '{secretValue}' ...")

# client.set_secret(secretName, secretValue)

# print(" done.")


###########DELETING SECRETS############
# print(f"Deleting your secret from KV_NAME ...")

# poller = client.begin_delete_secret(secretName)
# deleted_secret = poller.result()

# print(" done.")
