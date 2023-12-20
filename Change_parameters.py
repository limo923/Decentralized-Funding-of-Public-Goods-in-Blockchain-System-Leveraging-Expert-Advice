from Create_Project import Create_Project, Create_Expert
from QF import Quadratic_Funding
from Hedge import Hedge
from S_Hedge import Random_Sub_Hedge
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import csv

def plot_bar(data1, data2, data3, labels):
    x = range(len(labels))
    colors = ['y', 'b', 'm']

    ave_data1 = 1 - np.mean(data1)
    ave_data2 = 1 - np.mean(data2)
    ave_data3 = 1 - np.mean(data3)
    data = [ave_data1, ave_data2, ave_data3]
    plt.bar(x, data, width=0.35, color = colors)
    plt.xticks(x, labels)
    plt.ylim(0, 1)
    #plt.rcParams['font.size'] = 14
    #plt.xlabel('Category')
    plt.ylabel('Average Social Welfare(Proportional)', fontsize = 14)
    #plt.title('Bar Chart')
    for i, value in enumerate(data):
        plt.text(i, value + 0.02, f'{value:.2f}', ha='center')

    plt.show()

def Draw_loss(T: int, Ex_static_loss, Ex_dynamic_loss, QF_loss):
    Ex_static_Average = []
    Ex_dynamic_Average = []
    QF_Average = []
    Ex_static_Average.append(1)
    Ex_dynamic_Average.append(1)
    QF_Average.append(1)
    for t in range(1, T, 1):
        Ex_static_Average.append(np.mean(Ex_static_loss[:t]))
        Ex_dynamic_Average.append(np.mean(Ex_dynamic_loss[:t]))
        QF_Average.append(np.mean(QF_loss[:t]))
    #plt.title('Average_Turn_Loss')
    plt.xlabel('Number of Episodes', fontsize = 14)
    plt.ylabel('Average Investment Loss', fontsize = 14)
    plt.plot(Ex_static_Average, color = 'y', label = '\u03B7 = 0.01', marker='o', markevery=1000)
    plt.plot(Ex_dynamic_Average, color = 'r', label = '\u03B7 = 0.05', marker='s', markevery=1000)
    plt.plot(QF_Average, color = 'm', label = '\u03B7 = 0.1', marker='v', markevery=1000)
    plt.rcParams['font.size'] = 14
    plt.legend()
    plt.show()

def Draw_V(T: int, Ex_static_loss, Ex_dynamic_loss, QF_loss):
    Ex_static_Average = []
    Ex_dynamic_Average = []
    QF_Average = []
    Ex_static_Average.append(0)
    Ex_dynamic_Average.append(0)
    QF_Average.append(0)
    for t in range(1, T, 1):
        Ex_static_Average.append(1 - np.mean(Ex_static_loss[:t]))
        Ex_dynamic_Average.append(1 - np.mean(Ex_dynamic_loss[:t]))
        QF_Average.append(1 - np.mean(QF_loss[:t]))
    #plt.title('Average_Turn_Loss')
    plt.xlabel('Number of Episodes', fontsize = 14)
    plt.ylabel('Social Welfare(Proportional)', fontsize = 14)
    plt.plot(Ex_static_Average, color = 'y', label = '\u03B7 = 0.01', marker='o', markevery=1000)
    plt.plot(Ex_dynamic_Average, color = 'r', label = '\u03B7 = 0.05', marker='s', markevery=1000)
    plt.plot(QF_Average, color = 'm', label = '\u03B7 = 0.1', marker='v', markevery=1000)
    plt.rcParams['font.size'] = 14
    plt.legend()
    plt.show()

# Random Seeds
np.random.seed(0)
random.seed(0)

# Experts parameter
N = 1000
kappa_min = 500
kappa_max = 1500

Experts = Create_Expert(N, kappa_min, kappa_max)

K = 1000
T = 10000
H = 1e7 #目前的设置下V的均值基本是这么多

# Algorithm parameter
eta = 0.05
alpha = 0.8
Dynamic_Alg1 = Random_Sub_Hedge(20, 1000, 1, 0.1, 0.2)
Dynamic_Alg2 = Random_Sub_Hedge(20, 1000, 1, 0.1, 0.5)
Dynamic_Alg3 = Random_Sub_Hedge(20, 1000, 1, 0.1, 0.8)
m = 500

# Users parameter 
lamda = 0.5
beta = 1
sigma = 1

Ex_dynamic_loss1 = []
Ex_dynamic_loss2 = []
Ex_dynamic_loss3 = []
QF_loss = []
Best_x = []

Ex_dynamic_V1 = []
Ex_dynamic_V2 = []
Ex_dynamic_V3 = []
QF_V = []
Best_V = []

for t in range(T):
    a_reals, a_hats = Create_Project(K, lamda, beta, sigma)
    a_sum = np.sum(a_reals)
    a_sum_hat = np.sum(a_hats)
    # Best x_best and V_best
    x_best = a_sum * a_sum / 4
    V_best = a_sum * math.sqrt(x_best) - x_best

    Best_V.append(V_best)
    Best_x.append(x_best)

    # Experts x_Ex and V_Ex
    a_experts = np.zeros(N) 
    x_experts = np.zeros(N)
    for i in range(N):
        a_experts[i] = np.random.normal(loc = a_sum, scale = Experts[i])
        x_experts[i] = a_experts[i] * a_experts[i] / 4
    
    # Dynamic1
    j = Dynamic_Alg1.weighted_choice()
    x_Ex_dynamic = x_experts[j]
    V_Ex_dynamic = a_sum * math.sqrt(x_Ex_dynamic) - x_Ex_dynamic

    l_experts = np.zeros(N)
    for i in range(N): # loss on x
        l_experts[i] = abs((a_sum - a_experts[i]) * math.sqrt(x_Ex_dynamic)) / H
    Dynamic_Alg1.loss_and_update(l_experts)
    Ex_dynamic_loss1.append(abs(x_best - x_Ex_dynamic)/ (2*x_best))
    Ex_dynamic_V1.append((V_best - V_Ex_dynamic) / V_best)

     # Dynamic2
    j = Dynamic_Alg2.weighted_choice()
    x_Ex_dynamic = x_experts[j]
    V_Ex_dynamic = a_sum * math.sqrt(x_Ex_dynamic) - x_Ex_dynamic

    l_experts = np.zeros(N)
    for i in range(N): # loss on x
        l_experts[i] = abs((a_sum - a_experts[i]) * math.sqrt(x_Ex_dynamic)) / H
    Dynamic_Alg2.loss_and_update(l_experts)
    Ex_dynamic_loss2.append(abs(x_best - x_Ex_dynamic)/ (2*x_best))
    Ex_dynamic_V2.append((V_best - V_Ex_dynamic) / V_best)

     # Dynamic1
    j = Dynamic_Alg3.weighted_choice()
    x_Ex_dynamic = x_experts[j]
    V_Ex_dynamic = a_sum * math.sqrt(x_Ex_dynamic) - x_Ex_dynamic

    l_experts = np.zeros(N)
    for i in range(N): # loss on x
        l_experts[i] = abs((a_sum - a_experts[i]) * math.sqrt(x_Ex_dynamic)) / H
    Dynamic_Alg3.loss_and_update(l_experts)
    Ex_dynamic_loss3.append(abs(x_best - x_Ex_dynamic)/ (2*x_best))
    Ex_dynamic_V3.append((V_best - V_Ex_dynamic) / V_best)

    if (t+1) % m == 0:
        Dynamic_Alg1.substitute_expert()
        Dynamic_Alg2.substitute_expert()
        Dynamic_Alg3.substitute_expert()
    

#Draw_loss(T + 1, Ex_dynamic_loss1, Ex_dynamic_loss2, Ex_dynamic_loss3)
#Draw_V(T + 1, Ex_dynamic_V1, Ex_dynamic_V2, Ex_dynamic_V3)

plot_bar(Ex_dynamic_V1, Ex_dynamic_V2, Ex_dynamic_V3, ['a = 0.2','a = 0.5','a = 0.8'])

# data = zip(Ex_static_loss, Ex_dynamic_loss, QF_loss, Best_x, 
#            Ex_static_V, Ex_dynamic_V, QF_V, Best_V)

filename = 'Change_parameters.csv'

# with open(filename, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)

#     # 写入标题行，即每列的名称
#     writer.writerow(['Ex_static_loss', 'Ex_dynamic_loss', 
#                      'QF_loss', 'Best_x', 
#                      'Ex_static_V', 'Ex_dynamic_V',
#                      'QF_V', 'Best_V'])
#     # 逐行写入数据
#     for row in data:
#         writer.writerow(row)    

