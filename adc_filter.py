import numpy as np
def adc_filter_func(array,coeff):
    ph = array.copy()
    for j in range(2):
        accu = ph[0]
        for i in range(len(ph)):
            accu = accu + coeff[j]*(ph[i] - accu)
            ph[i] = accu
    
    noise = np.random.normal(0,5,int((len(ph)/4)))
    s = np.array([np.zeros(int(len(ph)/4)),noise])
    noise = np.ravel(s,order='F')
    
    s1 = np.array([np.zeros(len(noise)),noise])
    noise = np.ravel(s1, order= 'F')


    ph = np.add(ph,noise)
    return ph