import numpy as np
def peak_threshold_finder(y,p):  
    '''Input: y is the array, p are the positions
     Output: #of photons'''
    global peak_count
    peakness  = False
    
    peak_count=0
    peak_pos=[]

    noise_rms = np.sqrt(np.mean((y[0:400])**2))
    x = np.arange(0,len(y),1)

    for i in x:
        if y[i]>10*noise_rms and peakness==False:
            peakness = True
            peak_count += 1
            peak_pos.append(i)
        elif y[i]<6*noise_rms and peakness==True:
            peakness= False
    return peak_count,peak_pos