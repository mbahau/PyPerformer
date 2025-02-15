import time 
from md_features.memory_profiler import runtime_profiler as rp 

rp.start(3)

def sample_function():
    data = [x**2 for x in range(1000000)]  # Allocate memory
    time.sleep(2)  # Simulate processing delay

for i in range(10):
    sample_function()
