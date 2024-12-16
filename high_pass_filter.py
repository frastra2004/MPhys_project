import numpy as np
def high_pass(array,coeff):
    ph = array.copy()
    accu =0
    for i in range(len(ph)):
        lp = accu + coeff*(ph[i] - accu)
        ph[i] = ph[i]-lp
        accu = lp
            


    return ph