import pickle

def load_state(change_state, directory= ".pyperformer/saved_instance/"):
    """Load the state from the pickle file.
    
    Parameters:
    - directory (str) (optional): The directory where the state is saved.
    
    Returns:
    - dict: The state loaded from the pickle file.
    
    Example: load_state(locals())  # Load from the current directory. Use globals() to load from the global scope.
    """
    
    with open(directory+'checkpoint.pkl', 'rb') as f:
        state = pickle.load(f)
    print("State loaded.")

    for key, value in state.items():
        change_state[key] = value  # Assign the variable dynamically to the global scope


    print(f"Following objects are loaded: {state.keys()}")
    print('Please continue the development.')

