import numpy as np
from math import sqrt

# 先假设指数是1/2时的情况
def Quadratic_Funding(a_hats):
    a_sum = np.sum(a_hats)
    x = a_sum * a_sum / 4
    return x