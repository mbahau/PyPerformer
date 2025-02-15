# Expose key submodules and functions for easy access
# from memory_profiler import runtime_profiler
from .memory_profiler import runtime_profiler
from .get_help import get_help

# Utils 
from .utils import data_processing

# Define package metadata
__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = ["runtime_profiler","data_processing","cprofiler","get_help"]
