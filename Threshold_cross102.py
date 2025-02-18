
import numpy as np

def peak_threshold_finder2(y):  
    '''Input: y is the array, 
     Output: #of photons, position of photons[np.arr]'''
    global peak_count
    peakness  = False
    
    peak_count=0
    crossing = []
    peak_pos=[]

    noise_rms = np.sqrt(np.mean((y[0:30])**2))
    x = np.arange(0,len(y),1)

    for i in x:
        if y[i]>10*noise_rms and peakness==False:
            peakness = True
            peak_count += 1
            
            crossing.append(i)
        elif y[i]<6*noise_rms and peakness==True:
            peakness= False
    
    for i in crossing:
        for j in range(50):
            if np.all(y[i+j+1:i+j+10]<y[i+j])==True:
                peak_pos.append(i+j)
                break
            #else:
                #peak_pos.append(i)


            

    
    return peak_count, peak_pos
