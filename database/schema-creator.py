import mysql.connector
from mysql.connector import Error

def create_and_populate_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL server address
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            port=8000
        )

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
    create_and_populate_database()
