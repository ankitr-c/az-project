import mysql.connector
from mysql.connector import Error
from get_creds import AzureKeyVaultManager

try:
    kv_manager = AzureKeyVaultManager()    
    credentials = kv_manager.get_credentials()
except Exception as e:
    print(f"Error initializing AzureKeyVaultManager: {e}")

def create_and_populate_database():
    try:            
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=credentials['db_endpoint'],  # Replace with your MySQL server address
            user=credentials['username'],  # Replace with your MySQL username
            password=credentials['password'],  # Replace with your MySQL password
            port=credentials['port']
        )
        print("Connected to MySQL server.")
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS azproject;")
            
            # Use the azproject database
            cursor.execute("USE azproject;")
            
            # Create users table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                mobile VARCHAR(11) NOT NULL UNIQUE
            );
            """
            cursor.execute(create_table_query)
            
            # Insert dummy data
            insert_data_query = """
            INSERT INTO users (name, email, mobile)
            VALUES 
                ('John Doe', 'johndoe@example.com', '12345678901'),
                ('Jane Smith', 'janesmith@example.com', '09876543210'),
                ('Alice Johnson', 'alice.johnson@example.com', '11223344556');
            """
            cursor.execute(insert_data_query)
            
            # Commit changes
            connection.commit()
            print("Database, table, and dummy data created successfully.")
    
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    try:
        create_and_populate_database()
    finally:
        # Ensure proper cleanup when shutting down
        kv_manager.stop()
