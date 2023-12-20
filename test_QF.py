from Create_Project import Create_Project
from QF import Quadratic_Funding
import numpy as np
from math import sqrt

def test_Quadratic_Funding():
    K = 100
    T = 365
    lamda = 0.5
    beta = 0.5
    sigma = 0.1
    for i in range(T):
        a_simples, a_hats = Create_Project(K, lamda, beta, sigma)
        x, V = Quadratic_Funding(a_hats)
        a = np.sum(a_hats)
        x1 = x + 0.01
        x2 = x - 0.01
        assert a * sqrt(x) - x > a * sqrt(x1) - x1
        assert a * sqrt(x) - x > a * sqrt(x2) - x2