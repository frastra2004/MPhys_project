import numpy as np
import os
import threading
import time

# Initialize the array with Gaussian noise
x = np.random.normal(loc=0.5, scale=0.5, size=5000)
x = np.add(x, 1)

# Flag to control the program loop
running = True

def update_with_noise():
    """Continuously add Gaussian noise every 0.1 seconds."""
    global x, running
    while running:
        x = np.delete(x, 0)  # Remove the oldest element
        noise = np.random.normal(loc=0, scale=0.5)
        x = np.append(x, noise)  # Append Gaussian noise
        time.sleep(0.01)  # Add noise every 0.1 seconds

def listen_for_input():
    """Listen for user input to modify the array."""
    global x, running
    try:
        while running:
            user_input = input("Enter a number (Ctrl+C to exit): ").strip()
            if user_input.isdigit():
                value = int(user_input)
                photo_electrons = np.random.normal(loc=0.5, scale=0.5, size=100)
                s = np.random.poisson(1, 10000)
                import matplotlib.pyplot as plt
                count, bins, ignored = plt.hist(s, 100, density=True)
                count = value*count
                photo_electrons= np.add(photo_electrons,count)
                y = np.linspace(0,100,100)
                y = y.astype(np.int32)
                x = np.delete(x, y)  # Remove the oldest element
                x = np.append(x, count)  # Append user-provided value
            else:
                print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        # Gracefully stop on Ctrl+C
        running = False
 

# Start the noise updater in a separate thread
noise_thread = threading.Thread(target=update_with_noise, daemon=True)
noise_thread.start()

# Handle user input in the main thread

try:
    listen_for_input()
except KeyboardInterrupt:
    running = False
    
    print("\nProgram terminated by user.")


file = open('/Users/francescostraniero/Documents/Pembroke_4th_year/MPhys_Proj/myfile.txt','w')
np.savetxt(file,x)
print("Final state of the array:", len(x))