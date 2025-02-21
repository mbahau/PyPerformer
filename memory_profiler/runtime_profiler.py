# ------------------------------------------------------------------------
# Custom Memory Profiler | Profile memory usage line by line (User Files Only)
# ------------------------------------------------------------------------ 
import sys
import threading
import time
import traceback
import psutil
import logging
import os

# Setup logger to log memory usage to a file
logging.basicConfig(
    filename="memory_profile.log",  # Log to a file
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Event to allow stopping the profiling thread gracefully
stop_event = threading.Event()

# Detect Python's system directories to filter them out
PYTHON_SYSTEM_PATH = sys.prefix  # Base Python installation path

def _print_running_code(freq):
    """Prints the currently running code in user files and tracks memory usage."""

    main_thread_id = threading.main_thread().ident  # Get main thread ID
    process = psutil.Process()  # Get current process
    last_memory_used = 0  # Track last recorded memory usage
    
    while not stop_event.is_set():
        time.sleep(freq)  # Check every `freq` seconds

        # Memory usage details
        total_memory = psutil.virtual_memory().total / (1024 * 1024)  # Convert to MB
        memory_info = process.memory_info()
        memory_used = memory_info.rss / (1024 * 1024)  # Convert to MB
        max_memory_used = memory_info.vms / (1024 * 1024)  # Peak virtual memory usage in MB
        memory_increment = memory_used - last_memory_used  # Change in memory since last check
        memory_increment_perc = (memory_increment / last_memory_used * 100) if last_memory_used != 0 else 0
        last_memory_used = memory_used  # Update last recorded memory
        memory_available = psutil.virtual_memory().available / (1024 * 1024)  # Available memory in MB

        # Avoid division by zero
        memory_used_perc = (memory_used / total_memory * 100) if total_memory != 0 else 0
        max_memory_used_perc = (max_memory_used / total_memory * 100) if total_memory != 0 else 0
        memory_available_perc = (memory_available / total_memory * 100) if total_memory != 0 else 0

        # Log memory usage details
        log_message = f"""
--- Resource Info ---
    Memory Used: {memory_used:.2f} MB       | {memory_used_perc:.2f}%
    Memory Increment: {memory_increment:.2f} MB     | {memory_increment_perc:.2f}%
    Max Memory Used: {max_memory_used:.2f} MB       | {max_memory_used_perc:.2f}%
    Memory Available: {memory_available:.2f} MB     | {memory_available_perc:.2f}%
"""
        print(log_message.strip())  # Print to console
        logger.info(log_message.strip())  # Log to file

        # Get current running frame in main thread
        frame = sys._current_frames().get(main_thread_id)
        if frame:
            for filename, lineno, funcname, line in traceback.extract_stack(frame):
                # Exclude Python system libraries, site-packages, and Jupyter kernel files
                if (
                    filename.startswith(PYTHON_SYSTEM_PATH)  # Exclude Python system files
                    or "site-packages" in filename  # Exclude third-party libraries
                    or "lib" in filename  # Exclude standard Python libs
                    or "ipykernel" in filename  # Exclude Jupyter kernel files
                ):
                    continue  # Skip logging system files

                # Print only user-defined scripts
                code_log = f"Line: {lineno}, Function: {funcname}, File: {filename}"
                print(code_log)
                logger.info(code_log)
                if line:
                    print(f"Code: {line.strip()}")
                    logger.info(f"Code: {line.strip()}")

        print("---------------------------------------------\n")
        logger.info("---------------------------------------------\n")

def start(freq: int = 5):
    """Starts a monitoring thread to track memory usage and running code.
    Parameter: freq is the frequency of tracking logs.
    How to use: just add runtime_profiler.start() at the beginning of your code.
    """
    global monitor_thread
    stop_event.clear()
    monitor_thread = threading.Thread(target=_print_running_code, args=(freq,), daemon=True)
    monitor_thread.start()
    print("Memory profiling started...")

def stop():
    """Stops the memory profiling thread."""
    stop_event.set()
    monitor_thread.join()
    print("Memory profiling stopped.")
