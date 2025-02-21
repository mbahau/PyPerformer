# ------------------------------- 
# Below code will be executed if the module is called. This will ensure the temp directory created using save_detected_dataframes would be deleted automatically if IDE exited or laptop shutdown or crashed.
# -------------------------------
# # Specify the directory you want to manage
# CLEANUP_DIRECTORY = ".md_features"  # Replace with the directory you want to clean

# def cleanup_directory():
#     """
#     Deletes the specified directory if it exists.
#     """
#     if os.path.exists(CLEANUP_DIRECTORY):
#         print(f"Cleaning up: Deleting directory {CLEANUP_DIRECTORY}")
#         shutil.rmtree(CLEANUP_DIRECTORY)
#         print("Directory deleted successfully.")
#     else:
#         print(f"Directory {CLEANUP_DIRECTORY} already deleted or does not exist.")

# def handle_exit_signal(signum, frame):
#     """
#     Handles termination signals and ensures cleanup is performed.
#     """
#     print(f"Signal {signum} received. Exiting and cleaning up...")
#     cleanup_directory()
#     sys.exit(0)

# # Register the cleanup function for normal exit
# atexit.register(cleanup_directory)

# # Register signal handlers for interruption and termination
# signal.signal(signal.SIGINT, handle_exit_signal)  # Handle Ctrl+C
# signal.signal(signal.SIGTERM, handle_exit_signal)  # Handle termination signals
# # ------------------------------- END -------------------------------
