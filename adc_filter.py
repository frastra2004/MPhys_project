def adc_filter(array,coeff):
    ph = array.copy()
    for j in range(2):
        accu = ph[0]
        for i in range(len(ph)):
            accu = accu+ (coeff[j]*(ph[i] - accu))
            ph[i] = accu
            
    return ph