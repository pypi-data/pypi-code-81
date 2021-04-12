import itertools
import threading
import time
import sys

done = False
#here is the animation
def animate():
    for c in itertools.cycle(['.', '..', '...', '....']):
        if done:
            break
        print(c, flush=True)
        time.sleep(0.1)
    print('\rDone!     ')
    


t = threading.Thread(target=animate)
t.daemon = True
t.start()

#long process here
time.sleep(10)

done = True