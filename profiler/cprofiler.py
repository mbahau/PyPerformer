from functools import wraps
import cProfile
import pstats
import pandas as pd 
import os 

# ------------------------------------------------------------------------
# CProfile | Profile of the code to track the run time of each module in the code for optimizations purpose
# ------------------------------------------------------------------------
def start(top:int=10,sort_type:str = 'cumulative', save: str = None):
    """A decorator factory to profile the code using cProfile.
    Captures the top `top` time-consuming functions.
    
    Parameter (optional, default 20)
    ---------   
    top: Top top number of profiles.
    save:['save'] save the profile data to csv in the current dir.
    sort_type: Different sorting types. Usefull for sorting or in depth tracking. Use cprofiler.help() to get more options...
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
            # stats.sort_stats("time")          # Sort by time taken
            stats.sort_stats(sort_type)
            stats.print_stats(top)
            
            # Collect stats into a pandas DataFrame
            cprofile_stats_save(save, stats)
            
            print("cprofile captured the benchmark.")
            return result
        return wrapper
    return decorator


# Function to save the profile stats 
def cprofile_stats_save(save, stats):
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
        
        
        
def get_help():
    print(
""""
    Sorting Option:	Description
    
    "cumulative": (Default in many cases) Sorts by cumulative time (total time spent in a function including sub-functions it calls). Useful to detect where most of the execution time is spent.
    "time": Sorts by the total time spent inside a function (excluding sub-functions). Helps find the slowest individual function.
    "calls": Sorts by the number of calls to each function, useful to check frequent calls.
    "ncalls": Same as "calls".
    "tottime": Alias for "time", sorting by total time spent inside the function (excluding sub-functions).
    "percall": Sorts by the average execution time per call. Useful for optimizing frequently used functions.
    "filename": Sorts results based on the filename of the function.
    "stdname": Sorts alphabetically by function name.
    "line": Sorts by the line number of the function in the source file.
    """)
    
    
# # ------------------------------------------------------------------------END