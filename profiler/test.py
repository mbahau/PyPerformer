from md_features.profiler import cprofiler as cp 

import time 
def long_run():
    print("running")
    def two():
        time.sleep(2)
        def twoone():
            time.sleep(2)
        twoone()

    def four():
        time.sleep(3)  
    two()
    four()      
    

main = cp.cprofile(top=6, )(long_run)
main = cp.cprofile(top=6, save='save')(long_run)
main()
