import os 
import pickle
 
def is_pickleable(obj):
    """The function checks if the object is pickleable or not."""
    try:
        pickle.dumps(obj)
        return True
    except:
        return False
    
def save_state(environment=globals(),directory=".pyperformer/saved_instance/"):
    """
    Save the instance of the code.

    Parameters:
    - environment : The local or global environment need to save. Default is globals()
    - directory (str) (optional): The directory where the detected DataFrames will be saved.
    
    Example: save_state(locals())  # Save the local scope. Use globals() to save the global scope.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Get all local variables from the caller's scope
    caller_locals = environment
    
    print('Dumping the objects ...')
    # Filter out non-pickleable objects
    pickleable_state = {k: v for k, v in caller_locals.items() if is_pickleable(v)}
    
    with open(directory + 'checkpoint.pkl', 'wb') as f:
        pickle.dump(pickleable_state,f)
    print('Successfully Dumped.')
    
    print(f"Following objects are saved: {pickleable_state.keys()}\nDirectory : {directory}")    
    print("Instance saved.")
    print('Use load_state() to load the state from the checkpoint') 

