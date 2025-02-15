def get_help():
    """
    Displays usage instructions for the `md_features` package.

    Usage:
    ------
    >>> import md_features
    >>> md_features.get_help()

    This will print an overview of the available modules and functions.

    Available Modules:
    ------------------
    - memory_profiler: Tracks memory usage of Python scripts and RAM info.
        - runtime profiler
    - profiler: Profiling tools for CPU, function execution and track timing.
        - cprofiler
    - data_processing: Data manipulation utilities.
        - correct_parquet_cols(*dfs): Fix invalid column names in Parquet files.

    Example:
    --------
    >>> from md_features.memory_profiler import start, stop
    >>> start(freq=2)
    >>> # Run your script
    >>> stop()
    """
    
    help_text = """
==========================================
  📌 md_features Package - Documentation  
==========================================
  This package contains utilities for:
  ✅ Memory profiling
  ✅ Code execution profiling
  ✅ Data processing enhancements

  📌 Available Modules & Functions:
  ---------------------------------
  🔹 memory_profiler:
    - runtime profiler
        - start(freq=5): Start memory profiling.
        - stop(): Stop memory profiling.

  🔹 profiler:
    - cprofile(top=10, save=None): Profile function execution.

  🔹 data_processing:
    - correct_parquet_cols(*dfs): Fix column names in Parquet files.

  Example:
  --------
  >>> import md_features
  >>> md_features.get_help()

  More Info:
  ----------
  - GitHub: https://github.com/your_repo
  - Documentation: https://your_docs_link
"""
    print(help_text)
