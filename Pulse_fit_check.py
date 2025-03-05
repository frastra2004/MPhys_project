import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
from peak_threshold3 import peak_threshold_finder3




def Pulse_fit_check(signal):

    # FIND THRESHOLD CROSSINGS 
    n,p,crossings = peak_threshold_finder3(signal)

    y = signal.copy()
    snippets = np.ndarray(shape = (len(p),100))

    for i in range(n):
        if crossings[i]<(len(y)-100):
            snippets[i,:]=y[crossings[i]:crossings[i]+100]
        else:
            snippets[i,:] = np.mean(y)
            snippets[i,0:(len(y)-crossings[i])]=y[crossings[i]:512]




    def func2(x,a,b,c,d,e,f,g):
        return a*(-b/(x+0.1))+e*(np.exp(-x*c + d))+f+g*(x**2)
    

    p0= [10,1.6,0.07,2.5,10,-25,0.0001]
    x = np.arange(0,100,1)
    parameters = np.ndarray(shape = (len(p),7))
    output = np.ndarray(shape = (len(p),3))
    output[:,0]= crossings
    output[:,1]=p


    def R2_test(y,y3):
        SSres = np.sum((y-y3)**2)

        y_mean = np.average(y)

        SStot = np.sum((y-y_mean)**2)

        R2 = 1-(SSres/SStot)
        return R2


    for i in range(n):
        parameters[i,:], pcov = curve_fit(func2,x,snippets[i,:],p0)

        y_fit = func2(x,parameters[i,0],parameters[i,1],parameters[i,2],parameters[i,3],parameters[i,4],parameters[i,5],parameters[i,6])

        output[i,2] = R2_test(snippets[i,:],y_fit)
    
    f = (output[:,2]>0.7).astype(bool).reshape(-1,1)
    output2 = np.hstack((output,f))
    dfoutput = pd.DataFrame(output2,columns=['Threshold crossing location','Peak location','R^2', 'Is it a pulse?'])
    dfoutput['Is it a pulse?'] = dfoutput['Is it a pulse?'].astype(bool) 
    dfoutput['Is it a pulse?'] = dfoutput['Is it a pulse?'].apply(lambda x: 'Yes' if x else 'No')
    return dfoutput


