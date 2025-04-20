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
        ObjectName TEXT NOT NULL,
        ObjectData TEXT NOT NULL, -- JSON String
        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """)

    connection.commit()
    connection.close()


def get_object_data(obj):
    # Extract relevant attributes from the object
    center = getattr(obj, "center", None)
    if center != None:
        center = center.values()
    
    tip = getattr(obj, 'tip', None)
    if tip != None:
        tip = tip.values()
    
    axis = getattr(obj, 'axis', None)
    if axis != None:
        axis = axis.values()
    
    abc = getattr(obj, 'abc', None)
    if abc != None:
        abc = abc.values()
    
    colour = colour_to_list(obj.colour)
    
    def colour_to_list(colour):
        if colour != None:
            colour = colour.values()




    object_rotation = getattr(obj, 'rotation', None)
    if object_rotation != None:
        object_rotation = object_rotation.values()
    
    if obj.material.texture != None:
        texture = obj.material.texture.__class__.__name__
        texture_colour1 = colour_to_list(obj.material.texture.colour1)
        texture_colour2 = colour_to_list(obj.material.texture.colour2)
    else:
        texture = None

    

    object_data = {
        "type" : obj.__class__.__name__,
        "center": center,       
        "tip": tip,       
        "abc": abc,
        "allignment": getattr(obj, 'allignment', None), 
        "axis": axis,    
        "angle": getattr(obj, 'angle', None),    
        "height": getattr(obj, 'height', None),
        "radius": getattr(obj, 'radius', None),
        "object_rotation": object_rotation,
        "colour": colour,    
        "material": (obj.material).values(),
        "texture": texture,
        "texture_colour1": texture_colour1,
        "texture_colour2": texture_colour2,
    }
    return object_data


def save_object(user_id, obj, obj_name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    # Convert object data to JSON
    object_json = json.dumps(get_object_data(obj))

    # Insert into database
    cursor.execute("""
    INSERT INTO Objects (UserID, ObjectType,ObjectName, ObjectData) 
    VALUES (?, ?, ?, ?)
    """, (user_id, obj.__class__.__name__,obj_name,object_json))
    connection.commit()
    connection.close()




def load_objects(user_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT ObjectID, ObjectName FROM Objects WHERE UserID = ?", (user_id,))
    result = [[obj_id, obj_name ] for obj_id,obj_name in cursor.fetchall()]
    connection.close()
    return result

def load_object(user_id, obj_id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT ObjectData FROM Objects WHERE UserID = ? AND ObjectID = ?", (user_id, obj_id))
    result = cursor.fetchone()
    connection.close()
    
    return json.loads(result[0])

def get_obj_id(user_id, obj_name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("SELECT ObjectID FROM Objects WHERE UserID = ? AND ObjectName = ?", (user_id, obj_name))
    result = cursor.fetchone()
    connection.close()
    
    if result:
        return result[0]
    return None