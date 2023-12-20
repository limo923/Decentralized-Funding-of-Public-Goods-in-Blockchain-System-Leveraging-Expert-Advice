from Create_Project import Create_Project, Create_Expert
from QF import Quadratic_Funding
from S_Hedge import S_Hedge
import numpy as np
import math
import random
import matplotlib.pyplot as plt

def Draw(T: int, Ex_loss, QF_loss):
    Ex_Average = []
    QF_Average = []
    for t in range(T):
        Ex_Average.append(np.mean(Ex_loss[:t]))
        QF_Average.append(np.mean(QF_loss[:t]))
    plt.title('Average_Turn_Loss')
    plt.xlabel('Episode')
    plt.ylabel('Loss')
    plt.plot(Ex_Average)
    plt.plot(QF_Average)
    plt.show()

        
# Random Seeds
np.random.seed(2)
random.seed(1)

# Experts parameter
N = 100
kappa_min = 10
kappa_max = 50

Experts = Create_Expert(N, kappa_min, kappa_max)

K = 1000
T = 1000

# Algorithm parameter
eta = 0.001
a = 0.2
n = 100
Alg = S_Hedge(n, N, eta, a)
expert_mask = np.zeros(N)
m = 100 
for i in range(n):
    expert_mask[i] = 1

# Users parameter
lamda = 0.5
beta = 0.02
sigma = 0.2

Ex_loss = []
QF_loss = []
for t in range(T):
    a_reals, a_hats = Create_Project(K, lamda, beta, sigma)
    a_sum = np.sum(a_reals)
    a_sum_hat = np.sum(a_hats)
    # Best x_best and V_best
    x_best = a_sum * a_sum / 4
    V_best = a_sum * math.sqrt(x_best) - x_best

    # Experts x_Ex and V_Ex
    a_experts = np.zeros(N) 
    x_experts = np.zeros(N)
    for i in range(N):
        a_experts[i] = np.random.normal(loc = a_sum, scale = Experts[i])
        x_experts[i] = a_experts[i] * a_experts[i] / 4

    j = Alg.weighted_choice()
    print(j)
    x_Ex = x_experts[j]
    V_Ex = a_sum * math.sqrt(x_Ex) - x_Ex

    l_experts = np.zeros(N)
    for i in range(N):
        l_experts[i] = abs((a_sum - a_experts[i]) * math.sqrt(x_Ex))
    Alg.loss_and_update(l_experts, expert_mask)

    # QF x and V
    x_QF = Quadratic_Funding(a_hats)
    V_QF = a_sum * math.sqrt(x_QF) - x_QF

    #记录当轮的loss
    Ex_loss.append(V_best - V_Ex)
    QF_loss.append(V_best - V_QF)

Draw(T, Ex_loss, QF_loss)
    
    

