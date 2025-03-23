import sqlite3
import json

def init():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Objects (
        ObjectID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        ObjectType TEXT NOT NULL,
        ObjectData TEXT NOT NULL, -- JSON String
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """)

    connection.commit()
    connection.close()

def save_object(user_id, obj):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    # Convert object data to JSON
    abc = getattr(obj, 'abc', None)
    if abc != None:
        abc = abc.values()
    
    object_data = {
        "center": getattr(obj, "center", None),
        "tip": getattr(obj, 'tip', None),
        "abc": abc,
        "cylinder_allignment": getattr(obj, 'allignment', None),
        "cone_axis": getattr(obj, 'axis', None),
        "cone_angle": getattr(obj, 'angle', None),
        "height": getattr(obj, 'height', None),
        "radius": getattr(obj, 'radius', None),
        "cylinder_radius": getattr(obj, 'cylinder_radius', None),
        "colour": (obj.colour).values(),
        "material": (obj.material).values(),
        "texture": (obj.texture).__class__.__name__,
    }
    object_json = json.dumps(object_data)

    # Insert into database
    cursor.execute("""
    INSERT INTO Objects (UserID, ObjectType, ObjectData) 
    VALUES (?, ?, ?)
    """, (user_id, obj.__class__.__name__, object_json))
    connection.commit()
    connection.close()
    print("Object saved successfully!")