import numpy as np
import threading
import time
import scipy.signal as sc
from adc_filter import adc_filter_func
import matplotlib.pyplot as plt
import pandas as pd
from collections import deque


x = deque([0] * 1000, maxlen=1000) 
running = True
lock = threading.Lock()  # Thread-safe variable access
samples = np.empty((1000, 0))  # This is the array with with all the samples of interesting events
y = np.zeros(1000)
timings = []     #this array contains the timings at which we register interesting events
t0 = time.time()

#==============================================================================
def update_with_noise():
    #Continuously update every 0.1 seconds.
    global x, running
    while running:
        with lock:
            noise = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  # np.random.normal(loc=0, scale=0.5)
            x.extend(noise)
        time.sleep(0.05)

#==============================================================================
def listen_for_input():
    #gets input
    global x, running
    try:
        while running:
            user_input = input("Enter a number (Ctrl+C to exit): ").strip()
            if user_input.isdigit():
                value = int(user_input)
                photo_electrons = np.zeros(100)
                s = np.random.exponential(1, 1000)
                count, bins, ignored = plt.hist(s, 100, density=True)
                count = value * count
                photo_electrons = np.add(photo_electrons, count)
                y_vals = np.linspace(899, 999, 100, dtype=int)
                with lock:
                    for idx in y_vals:
                        x[idx] = count[idx-900] if idx < (900+len(count)) else 0
            else:
                print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        running = False

#==============================================================================
def lp_filter():
    """Apply a low-pass filter to the data."""
    global y
    while running:
        with lock:
            y = adc_filter_func(np.array(x), [0.012, 0.02])
        time.sleep(0.1)    

#==============================================================================
def OPD():
    """Perform peak detection and store the results."""
    global samples, timings, y
    while running:
        with lock:
            mean = np.mean(y)
            peak_indices, props = sc.find_peaks(y, height=(4 * mean))
            if len(peak_indices) > 0:
                samples = np.append(samples, y.reshape(-1,1), axis=1)
                timings.append((time.time()-t0))
        time.sleep(0.1)   

#==============================================================================
# Start threads
threads = [
    threading.Thread(target=update_with_noise, daemon=True),
    threading.Thread(target=lp_filter, daemon=True),
    threading.Thread(target=OPD, daemon=True),
]

for thread in threads:
    thread.start()

try:
    listen_for_input()
except KeyboardInterrupt:
    running = False
    print("\nProgram terminated by user.")

# Save the data to a file
file_path = '/Users/francescostraniero/Documents/Pembroke_4th_year/MPhys_Proj/myfile.csv'
with open(file_path, 'w') as file:
    df = pd.DataFrame(samples, columns = timings)
    df.to_csv(file_path)
print("Final state of the array:", len(y))