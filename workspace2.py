def activate_drone():
    print('Activating workspace2')

def joel(func_name):
    globals()[f"{func_name}_drone"]()
    
    

joel("activate")