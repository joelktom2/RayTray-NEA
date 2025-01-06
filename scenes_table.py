import sqlite3
import os
def init():    
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Scenes (
        SceneID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        ImagePath VARCHAR(255) NOT NULL,
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """)
    connection.commit()
    connection.close()

def create_scene(user_id, image_path):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Scenes (UserID, ImagePath) VALUES (?, ?)", (user_id, image_path))
    connection.commit()
    connection.close()

def get_scenes(user_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT ImagePath FROM Scenes WHERE UserID = ?", (user_id,))
    result = cursor.fetchall()
    connection.close()
    return result


def add_img(user_id,img):
    image_path = os.path.abspath(img)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Scenes (UserID, ImagePath) VALUES (?, ?)", (user_id, image_path))
    connection.commit()
    connection.close()

add_img(8,'pic1.jpg')
add_img(8,'pic2.jpg')
add_img(8,'pic3.jpg')
add_img(8,'pic4.jpg')

print("done")