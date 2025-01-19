import pandas as pd
import numpy as np
import os
import tempfile

import atexit
import signal
import sys
import shutil
 
 
 
def save_detected_dataframes(environment=globals(),directory=".md_features/__temp_saved_dfs"):
    """
    Detects all DataFrames in the local scope of the calling function and saves them.

    Parameters:
    - environment : The local or global environment from where dataframe needs to pull.
    - directory (str) (optional): The directory where the detected DataFrames will be saved.
    """
    print("Detecting dataframes ...")
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Get all local variables from the caller's scope
    caller_locals = environment
    
    
    # Filter DataFrames from the local variables
    dataframes = {var_name: var_value for var_name, var_value in caller_locals.items() if isinstance(var_value, pd.DataFrame)}

    print(f"Total dataframes detected: {len(dataframes)} ")
    
    # Iterate through the dataframes
    for var_name, var_value in dataframes.items():
        print(f"Processing dataframe '{var_name}' with shape {var_value.shape}")
        file_path = os.path.join(directory, f"{var_name}.parquet")
        var_value.to_parquet(file_path, index=False)
        print(f"Saved DataFrame '{var_name}' to path '{file_path}'")




def relode_detected_dataframes(directory=".md_features/__temp_saved_dfs"):
    """
    Reads all DataFrames saved in the specified directory (e.g., .parquet files),
    assigns them to variables based on their filenames, and returns a dictionary of DataFrames.

    Parameters:
    - directory (str) (optional): Path to the directory containing saved DataFrames.

    Returns:
    - dict: A dictionary where keys are variable names (from filenames) and values are DataFrames.
    """
    dataframes = {}
    
    # List all files in the directory
    for file_name in os.listdir(directory):
        # Check if the file is a parquet file
        if file_name.endswith('.parquet'):
            # Extract the variable name from the filename (without extension)
            var_name = os.path.splitext(file_name)[0]
            
            # Construct the full file path
            file_path = os.path.join(directory, file_name)
            
            # Read the DataFrame from the file
            df = pd.read_parquet(file_path)
            
            # Dynamically assign to the variable name
            dataframes[var_name] = df
            
            globals()[var_name] = df
            
            print(f"Loaded DataFrame '{var_name}' from '{file_path}'")
    
    # Dynamically create variables in the local scope
    # globals().update(dataframes)
    print("All dataframes is availble in gloabl to access within the module.\nYou can access the data by using 'packagename.dataframe_name'. example 'md_features.df' ")
    print("Loading done.")
    return dataframes
               


# ------------------------------- 
# Below code will be executed if the module is called. This will ensure the temp directory created using save_detected_dataframes would be deleted automatically if IDE exited or laptop shutdown or crashed.
# -------------------------------
# Specify the directory you want to manage
CLEANUP_DIRECTORY = ".md_features"  # Replace with the directory you want to clean

def cleanup_directory():
    """
    Deletes the specified directory if it exists.
    """
    if os.path.exists(CLEANUP_DIRECTORY):
        print(f"Cleaning up: Deleting directory {CLEANUP_DIRECTORY}")
        shutil.rmtree(CLEANUP_DIRECTORY)
        print("Directory deleted successfully.")
    else:
        print(f"Directory {CLEANUP_DIRECTORY} already deleted or does not exist.")

def handle_exit_signal(signum, frame):
    """
    Handles termination signals and ensures cleanup is performed.
    """
    print(f"Signal {signum} received. Exiting and cleaning up...")
    cleanup_directory()
    sys.exit(0)

# Register the cleanup function for normal exit
atexit.register(cleanup_directory)

# Register signal handlers for interruption and termination
signal.signal(signal.SIGINT, handle_exit_signal)  # Handle Ctrl+C
signal.signal(signal.SIGTERM, handle_exit_signal)  # Handle termination signals
# ------------------------------- END -------------------------------
