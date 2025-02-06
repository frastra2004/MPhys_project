import numpy as np
import pandas as pd



from S1_generator.S1_event_generator import S1_event
from Threshold_cross102 import peak_threshold_finder2

def CNN_training_data_generator(samples,pulses):
    sample_lenght = 5000
    X = np.ndarray(shape=(int(0.7*samples),sample_lenght))
    Y = np.zeros((int(0.7*samples),sample_lenght))
    p_match = np.zeros(shape=(int(0.7*samples),2,pulses))
    for i in range(int(0.7*samples)):
        y,n,p = S1_event(pulses)
        X[i,:]=y

        
        lala = peak_threshold_finder2(y)[1]

        p_match[i,0,0:len(p)] = p
        try:
            p_match[i,1,0:len(lala)] = lala

        except ValueError:
            p_match[i,1,:] = 0
    
    mask = np.all(p_match[:, 1, :] == 0, axis=1)
    p_match = p_match[~mask]
    X = X[~mask]
    Y = Y[~mask]

    for i in range(len(p_match[0])):
        for k in range(pulses):
            if p_match[i,1,k]>p_match[i,0,k] and p_match[i,1,k]<p_match[i,0,k]+90:
                p_match[i,1,k+1:]=p_match[i,1,k:-1]
                p_match[i,1,k]=0

    
    rows = np.arange(p_match.shape[0])[:, None]  # Shape (858, 1)
    positions = p_match[:, 1, :].astype(int)  # Shape (858, 7)
    Y[rows, positions] = 1
    Y[:,0]=0
    X2 = np.ndarray(shape=(int(0.3*samples),sample_lenght))
    Y2 = np.zeros((int(0.3*samples),sample_lenght))
    for l in range(int(0.3*samples)):
        X2[l,:]=5*np.random.random(sample_lenght)
        Y2[l,:]=0

    X = np.concatenate((X,X2))
    Y = np.concatenate((Y,Y2))

    return X,Y
