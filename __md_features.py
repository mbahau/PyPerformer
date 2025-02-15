import pandas as pd
import numpy as np
import os
import tempfile
from functools import wraps

import atexit
import signal
import sys
import shutil
import cProfile
import pstats 
 
 
# def save_detected_dataframes(environment=globals(),directory=".md_features/__temp_saved_dfs"):
#     """
#     Detects all DataFrames in the local scope of the calling function and saves them.

#     Parameters:
#     - environment : The local or global environment from where dataframe needs to pull.
#     - directory (str) (optional): The directory where the detected DataFrames will be saved.
#     """
#     print("Detecting dataframes ...")
#     # Ensure the directory exists
#     os.makedirs(directory, exist_ok=True)
    
#     # Get all local variables from the caller's scope
#     caller_locals = environment
    
    
#     # Filter DataFrames from the local variables
#     dataframes = {var_name: var_value for var_name, var_value in caller_locals.items() if isinstance(var_value, pd.DataFrame)}

#     print(f"Total dataframes detected: {len(dataframes)} ")
    
#     # Iterate through the dataframes
#     for var_name, var_value in dataframes.items():
#         print(f"Processing dataframe '{var_name}' with shape {var_value.shape}")
#         file_path = os.path.join(directory, f"{var_name}.parquet")
#         var_value.to_parquet(file_path, index=False)
#         print(f"Saved DataFrame '{var_name}' to path '{file_path}'")

import os
import pickle
import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame

def save_detected_variables_and_dataframes(environment=globals(), directory=".md_features/__temp_saved_vars"):
    """
    Detects all DataFrames, strings, lists, dictionaries, and other variables in the local scope 
    of the calling function and saves them in the specified directory.

    Parameters:
    - environment : The local or global environment from where variables and dataframes need to be pulled.
    - directory (str) (optional): The directory where the detected variables and DataFrames will be saved.
    """
    print("Detecting variables and dataframes ...")

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Get all variables from the caller's scope
    caller_variables = environment

    # Separate variables by type
    dataframes = {var_name: var_value for var_name, var_value in caller_variables.items()
                  if isinstance(var_value, (pd.DataFrame, SparkDataFrame))}
    other_variables = {var_name: var_value for var_name, var_value in caller_variables.items()
                       if not isinstance(var_value, (pd.DataFrame, SparkDataFrame))}

    # Process and save DataFrames
    print(f"Total DataFrames detected: {len(dataframes)}")
    for var_name, var_value in dataframes.items():
        if isinstance(var_value, pd.DataFrame):
            print(f"Processing Pandas DataFrame '{var_name}' with shape {var_value.shape}")
            file_path = os.path.join(directory, f"{var_name}.parquet")
            var_value.to_parquet(file_path, index=False)
            print(f"Saved Pandas DataFrame '{var_name}' to path '{file_path}'")
        elif isinstance(var_value, SparkDataFrame):
            print(f"Processing Spark DataFrame '{var_name}'")
            file_path = os.path.join(directory, f"{var_name}_spark.parquet")
            var_value.write.parquet(file_path, mode='overwrite')
            print(f"Saved Spark DataFrame '{var_name}' to path '{file_path}'")

    # Process and save other variables
    print(f"Total other variables detected: {len(other_variables)}")
    for var_name, var_value in other_variables.items():
        print(f"Processing variable '{var_name}' of type {type(var_value)}")
        file_path = os.path.join(directory, f"{var_name}.pkl")
        with open(file_path, 'wb') as f:
            pickle.dump(var_value, f)
        print(f"Saved variable '{var_name}' to path '{file_path}'")

    print("All variables and DataFrames have been processed and saved.")





# def reload_detected_dataframes(directory=".md_features/__temp_saved_dfs"):
#     """
#     Reads all DataFrames saved in the specified directory (e.g., .parquet files),
#     assigns them to variables based on their filenames, and returns a dictionary of DataFrames.

#     Parameters:
#     - directory (str) (optional): Path to the directory containing saved DataFrames.

#     Returns:
#     - dict: A dictionary where keys are variable names (from filenames) and values are DataFrames.
#     """
#     dataframes = {}
    
#     # List all files in the directory
#     for file_name in os.listdir(directory):
#         # Check if the file is a parquet file
#         if file_name.endswith('.parquet'):
#             # Extract the variable name from the filename (without extension)
#             var_name = os.path.splitext(file_name)[0]
            
#             # Construct the full file path
#             file_path = os.path.join(directory, file_name)
            
#             # Read the DataFrame from the file
#             df = pd.read_parquet(file_path)
            
#             # Dynamically assign to the variable name
#             dataframes[var_name] = df
            
#             globals()[var_name] = df
            
#             print(f"Loaded DataFrame '{var_name}' from '{file_path}'")
    
#     # Dynamically create variables in the local scope
#     # globals().update(dataframes)
#     print("All dataframes is availble in gloabl to access within the module.\nYou can access the data by using 'packagename.dataframe_name'. example 'md_features.df' ")
#     print("Loading done.")
#     return dataframes

def reload_detected_data(directory=".md_features/__temp_saved_vars"):
    """
    Reads all saved variables (DataFrames and others) in the specified directory, 
    assigns them to variables based on their filenames, and returns a dictionary of the loaded objects.

    Parameters:
    - directory (str) (optional): Path to the directory containing saved variables.

    Returns:
    - dict: A dictionary where keys are variable names (from filenames) and values are the loaded objects.
    """
    loaded_objects = {}

    # List all files in the directory
    for file_name in os.listdir(directory):
        # Extract the variable name from the filename (without extension)
        var_name = os.path.splitext(file_name)[0]
        
        # Construct the full file path
        file_path = os.path.join(directory, file_name)
        
        # Determine the type of file and load accordingly
        if file_name.endswith('.parquet'):
            # Load as a Pandas DataFrame
            df = pd.read_parquet(file_path)
            loaded_objects[var_name] = df
            globals()[var_name] = df
            print(f"Loaded DataFrame '{var_name}' from '{file_path}'")
        elif file_name.endswith('.pkl'):
            # Load using pickle
            with open(file_path, 'rb') as f:
                obj = pickle.load(f)
                loaded_objects[var_name] = obj
                globals()[var_name] = obj
                print(f"Loaded variable '{var_name}' from '{file_path}'")
        else:
            print(f"Skipping unsupported file type: '{file_name}'")

    print("All variables are available globally to access within the module.")
    print("Loading done.")
    return loaded_objects

               


# ------------------------------------------------------------------------ 
# Below code will be executed if the module is called. This will ensure the temp directory created using save_detected_dataframes would be deleted automatically if IDE exited or laptop shutdown or crashed.
# ------------------------------------------------------------------------
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
# ------------------------------------------------------------------------END 


# ------------------------------------------------------------------------
# CProfile | Profile of the code to track the run time of each module in the code for optimizations purpose
# ------------------------------------------------------------------------
def cprofile(top:int=10, save: str = None):
    """A decorator factory to profile the code using cProfile.
    Captures the top `top` time-consuming functions.
    
    Parameter (optional, default 20)
    ---------   
    top: Top top number of profiles.
    save:['save'] save the profile data to csv in the current dir.
    
    How to use
    ---------
    import the cprofile and map with the main function of the code.

    Example Code:
    import md_features as md
    main  = md.cprofile(top=6)(main)
    
    Run the code by calling the main function and check terminal for the profiles.
    """
    
    def decorator(fn):
        @wraps(fn)    
        def wrapper(*args, **kwargs):
            
            # Initializing cprofile
            profiler = cProfile.Profile()
            profiler.enable()

            print("cprofile enabled. Tracking the run time ...")
            
            result = fn(*args, **kwargs)
            
            profiler.disable()
            
            # Sort and print the stats
            stats = pstats.Stats(profiler)
            stats.strip_dirs()                # Remove unnecessary path information
            stats.sort_stats("time")          # Sort by time taken
            stats.print_stats(top)
            
            # Collect stats into a pandas DataFrame
            if save == 'save':
                data = []
                for func, (cc, nc, tt, ct, callers) in stats.stats.items():
                    data.append({
                        "Function": f"{func[0]}:{func[1]}({func[2]})",
                        "ncalls": nc,
                        "tottime": tt,
                        "percall_tottime": tt / nc if nc else 0,
                        "cumtime": ct,
                        "percall_cumtime": ct / nc if nc else 0
                    })
                
                df = pd.DataFrame(data).reset_index(drop=True)
                df = df.sort_values(by="tottime", ascending=False)

                df.to_csv('CProfileData.csv')
                print('Profile data saved')
                print(os.getcwd())
            
            print("cprofile captured the benchmark.")
            return result
        return wrapper
    return decorator
# ------------------------------------------------------------------------END


# ------------------------------------------------------------------------
# Line profiler | Profile of the code to track the run time of each module in the code for optimizations purpose
# ------------------------------------------------------------------------
def line_profile(save: str = None):
    """A decorator factory to profile the code using LineProfiler.
    Captures the top `top` time-consuming functions.
    
    Parameter (optional, default 20)
    ---------   
    save:['save'] save the profile data to csv in the current dir.
    
    
    How to use
    ---------
    import the cprofile and map with the main function of the code.

    Example Code:
    import md_features as md
    main  = md.line_profile(save='save')(main)
    
    Run the code by calling the main function and check terminal for the profiles.
    """

    from line_profiler import LineProfiler
    from io import StringIO
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Initialize LineProfiler
            profiler = LineProfiler()
            profiler.add_function(fn)
            profiler.add_function(main)

            # Dynamically add all internal functions to the profiler
            frame = inspect.currentframe()
            try:
                local_functions = [obj for obj in frame.f_globals.values() if inspect.isfunction(obj)]
                for func in local_functions:
                    profiler.add_function(func)
            finally:
                del frame  # Avoid reference cycles
                
            print("Line profiler enabled. Tracking the runtime...")
            result = profiler(fn)(*args, **kwargs)
            profiler.print_stats()

            if save == 'save':
                # Assign a default file path if output_file_path is None
                output_file_path= None
                if output_file_path is None:
                    output_file_path = os.path.join(os.getcwd(), "line_profiler_output.txt")

                # Save stats to file
                with open(output_file_path, "w") as f:
                    profiler.print_stats(stream=f)

                print(f"Profiling results saved to {output_file_path}")

            return result

        return wrapper
    return decorator
# ------------------------------------------------------------------------END
#

