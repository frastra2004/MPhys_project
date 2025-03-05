import numpy as np

def peak_threshold_finder3(y):
    '''
    Input: y = signal array
    Output: n = number of photons (integer), p = positions of photons (list)
    '''
    avg = np.mean(y)  #computes the average and std over the whole sample
    std = np.std(y)

    positions = []
    crossing = []

    y2 = y.copy()

    y2 = [value for value in y if value <= avg + 3 * std] #this line rewrites a copy of our sample array without pulses above 4sigma
    
    avg = np.mean(y2) #recompute average and std, without the pulses, to obtain baseline
    std = np.std(y2)

    peakness = False

    #This for loop goes through the array and find pulses 4sigma above the baseline.
    # Because a pulse could be larger than a single data point, I introduce a second if condition, 
    # so that unless the signal drops below 3sigma, then it is considered part of the same pulse.
    for i in range(len(y)):
        if y[i] > avg + 4*std and peakness== False:
            crossing.append(i)
            peakness = True
        if y[i] < avg +3*std and peakness == True:
            peakness = False
    
    #=========================================
    #The previous for loop has found the positions at which the signal crosses a threshold, this is not necessarily the peak.
    # The next for loop considers each of the threshold crossings which I have found, then runs over the following 50 points,
    # and checks for each of them if they are the actual peak, by comparing them to the following 10, and seeing which one is the highest.
    for i in crossing:
        for j in range(50):
            if np.all(y[i+j+1:i+j+10]<y[i+j])==True:
                positions.append(i+j)
                break
            #else:
                #positions.append(i)

    return len(positions), positions, crossing


            
    

    

    
