import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='sql8.freemysqlhosting.net',         # Replace with your MySQL server host
            user='sql8750086',     # Replace with your MySQL username
            password='M4zBNpzLCf', # Replace with your MySQL password
            database='sql8750086'  # Replace with the name of your database
        )
        
        if connection.is_connected():
            print("Connected to MySQL Database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Example usage
db_connection = connect_to_database()



def insert_data():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        try:
            # Use parameterized queries to avoid SQL injection
            query = """
            INSERT INTO `Users` (`Username`, `PasswordHash`, `CreatedAt`) 
            VALUES (%s, %s, %s)
            """
            data = ('joel', 'jsoidhfosidhf', '2024-12-05 12:00:00')  # Example values
            cursor.execute(query, data)
            connection.commit()  # Commit the changes
            print("Data inserted successfully")
        except Error as e:
            print(f"Error while inserting data: {e}")
        finally:
            cursor.close()
            connection.close()


insert_data()

if db_connection:
    db_connection.close()