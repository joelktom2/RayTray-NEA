import sqlite3
import os
import json

from object_table import get_object_data

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
        Scene_Data TEXT, -- JSON String
    )
    """)
    connection.commit()
    connection.close()

def get_scene_data(scene):
    # Extract relevant attributes from the scene
    scene_data = {
        "width": scene.width,
        "height": scene.height,
        "camera_position": scene.camera.position.values(),
        "camera_fov": scene.camera.fov,
        "lights": [],
        "objects": []
    }

    for light in scene.lights:
        light_data = {
            "position": light.position.values(),
            "brightness": light.intesity,
        }
        scene_data["lights"].append(light_data)

    for obj in scene.objects:
        object_data = get_object_data(obj)
        scene_data["objects"].append(object_data)

    return scene_data

def create_scene(user_id, image_path,img_Name,scene_data):
    # Convert scene data to JSON
    scene_data = json.dumps(scene_data)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Scenes (UserID, ImagePath, Scene_Name,Scene_Data) VALUES (?, ?, ?, ?)", (user_id, image_path, img_Name, scene_data))
    connection.commit()
    connection.close()

def get_scenes(user_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT ImagePath FROM Scenes WHERE UserID = ?", (user_id,))
    result = cursor.fetchall()
    connection.close()
    return result


def get_scene_names(user_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Scene_Name FROM Scenes WHERE UserID = ?", (user_id,))
    result = cursor.fetchall()
    connection.close()
    return result

def remove_scene(user_id, scene_path):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Scenes WHERE UserID = ? AND ImagePath = ?", (user_id, scene_path))
    connection.commit()
    connection.close()

def get_scene_data_from_db(scene_path):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Scene_Data FROM Scenes WHERE ImagePath = ?", (scene_path,))
    result = cursor.fetchone()
    connection.close()

    if result:
        return json.loads(result[0])
    return None