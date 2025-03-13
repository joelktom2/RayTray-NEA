import sqlite3
import bcrypt

def init_db():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR(20) NOT NULL,
        PasswordHash VARCHAR(20) NOT NULL,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    connection.commit()
    connection.close()


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

def create_user(username, password):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    try:    
        cursor.execute("INSERT INTO Users (Username, PasswordHash) VALUES (?, ?)", (username, hash_password(password)))
        connection.commit()
    except sqlite3.IntegrityError:
        print("Username already exists")
    
    connection.close()
                
def login_user(username, password):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT PasswordHash FROM Users WHERE Username = ?", (username,))
    result = cursor.fetchone()
    
    if result is None:
        connection.close()
        print("User not found")
        return None
    else:
        hashed_password = result[0]
        if verify_password(password, hashed_password):
            connection.close()
            print("Login successful")
            return True
        else:
            print("Incorrect password")
            connection.close()
            return False
    

def get_user_id(username):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("""
    SELECT UserID FROM Users WHERE Username = ?""", (username,))
    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]  # Return the UserID
    else:
        return None  # Return None if no matching user is found
    

print(get_user_id("joel"))