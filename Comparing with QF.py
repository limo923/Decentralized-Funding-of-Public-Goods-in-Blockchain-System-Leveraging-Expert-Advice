from Create_Project import Create_Project, Create_Expert
from QF import Quadratic_Funding
from Hedge import Hedge
from S_Hedge import Random_Sub_Hedge
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import csv

marknumber = 200

def plot_boxplot(data1, data2, data3):
    plt.boxplot([data1, data2,data3], labels = ['Quadratic Funding','Static Algorithm', 'Dynamic Algorithm'], showfliers = False) #label 和 value 等长向量
    plt.rcParams['font.size'] = 14
    #plt.xlabel('Category')
    plt.ylabel('Social Welfare(Proportional)', fontsize = 14)
    #plt.title('Boxplot')
    plt.grid(True)
    plt.show()

def plot_cdf(data1, data2, data3):
    sorted_data1 = np.sort(data1)
    y_vals1 = np.arange(len(sorted_data1)) / float(len(sorted_data1) - 1)
    sorted_data2 = np.sort(data2)
    y_vals2 = np.arange(len(sorted_data2)) / float(len(sorted_data2) - 1)
    sorted_data3 = np.sort(data3)
    y_vals3 = np.arange(len(sorted_data3)) / float(len(sorted_data3) - 1)

    plt.rcParams['font.size'] = 12
    plt.plot(sorted_data1, y_vals1, color = 'g', label = 'Static Expert')
    plt.plot(sorted_data2, y_vals2, color = 'r', label = 'Dynamic Expert')
    plt.plot(sorted_data3, y_vals3, color = 'b', label = 'Quadratic Funding')
    plt.xlabel('Social Welfare(Proportional)', fontsize = 14)
    plt.ylabel('CDF', fontsize = 14)
    plt.title('CDF of Social Welfare')
    plt.grid(True)
    plt.show()

def Draw_loss(T: int, Ex_static_loss, Ex_dynamic_loss, QF_loss):
    Ex_static_Average = []
    Ex_dynamic_Average = []
    QF_Average = []
    Ex_static_Average.append(0.8)
    Ex_dynamic_Average.append(0.8)
    QF_Average.append(0.8)
    for t in range(1, T, 1):
        Ex_static_Average.append(np.mean(Ex_static_loss[:t]))
        Ex_dynamic_Average.append(np.mean(Ex_dynamic_loss[:t]))
        QF_Average.append(np.mean(QF_loss[:t]))
    #plt.title('Average_Turn_Loss')
    plt.xlabel('Number of Episodes', fontsize = 14)
    plt.ylabel('Average Investment Loss', fontsize = 14)
    plt.plot(Ex_static_Average, color = 'g', label = 'Static Expert', marker='o', markevery=marknumber)
    plt.plot(Ex_dynamic_Average, color = 'r', label = 'Dynamic Expert', marker='s', markevery=marknumber)
    plt.plot(QF_Average, color = 'b', label = 'Quadratic Funding', marker='v', markevery=marknumber)
    plt.rcParams['font.size'] = 12
    plt.legend()
    plt.show()

def Draw_V(T: int, Ex_static_loss, Ex_dynamic_loss, QF_loss):
    Ex_static_Average = []
    Ex_dynamic_Average = []
    QF_Average = []
    Ex_static_Average.append(0.6)
    Ex_dynamic_Average.append(0.6)
    QF_Average.append(0.6)
    for t in range(1, T, 1):
        Ex_static_Average.append(1 - np.mean(Ex_static_loss[:t]))
        Ex_dynamic_Average.append(1 - np.mean(Ex_dynamic_loss[:t]))
        QF_Average.append(1 - np.mean(QF_loss[:t]))
    #plt.title('Average_Turn_Loss')
    plt.xlabel('Number of Episodes', fontsize = 14)
    plt.ylabel('Social Welfare(Proportional)', fontsize = 14)
    plt.plot(Ex_static_Average, color = 'g', label = 'Static Expert', marker='o', markevery=marknumber)
    plt.plot(Ex_dynamic_Average, color = 'r', label = 'Dynamic Expert', marker='s', markevery=marknumber)
    plt.plot(QF_Average, color = 'b', label = 'Quadratic Funding', marker='v', markevery=marknumber)
    plt.rcParams['font.size'] = 12
    plt.legend()
    plt.show()

# Random Seeds
np.random.seed(1)
random.seed(1)

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
alpha = 0.2
m = 500
Static_Alg = Hedge(20, eta)
Dynamic_Alg = Random_Sub_Hedge(20, 1000, 1, eta, alpha)

# Users parameter 
lamda = 0.5
beta = 1
sigma = 1

Ex_static_loss = []
Ex_dynamic_loss = []
QF_loss = []
Best_x = []

Ex_static_V = []
Ex_dynamic_V = []
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
    
    # Static
    j = Static_Alg.weighted_choice()
    x_Ex_static = min(x_experts[j], 2*x_best)
    V_Ex_static = max(a_sum * math.sqrt(x_Ex_static) - x_Ex_static, 0)

    l_experts = np.zeros(N)
    for i in range(N): # loss on x
        l_experts[i] = abs((a_sum - a_experts[i]) * math.sqrt(x_Ex_static)) / H
    Static_Alg.loss_and_update(l_experts)

    Ex_static_loss.append(abs(x_best - x_Ex_static) / (2*x_best))
    Ex_static_V.append(V_Ex_static / V_best)

    # Dynamic
    j = Dynamic_Alg.weighted_choice()
    x_Ex_dynamic = min(x_experts[j], 2*x_best)
    V_Ex_dynamic = max(a_sum * math.sqrt(x_Ex_dynamic) - x_Ex_dynamic, 0)

    l_experts = np.zeros(N)
    for i in range(N): # loss on x
        l_experts[i] = abs((a_sum - a_experts[i]) * math.sqrt(x_Ex_dynamic)) / H
    Static_Alg.loss_and_update(l_experts)
    Dynamic_Alg.loss_and_update(l_experts)

    Ex_dynamic_loss.append(abs(x_best - x_Ex_dynamic)/ (2*x_best))
    Ex_dynamic_V.append(V_Ex_dynamic / V_best)

    if (t+1) % m == 0:
        Dynamic_Alg.substitute_expert()
    
    # QF x and V
    x_QF = Quadratic_Funding(a_hats)
    V_QF = a_sum * math.sqrt(x_QF) - x_QF

    QF_loss.append(abs(x_best - x_QF)/ (2*x_best))
    QF_V.append(V_QF / V_best)

#Draw_loss(T + 1, Ex_static_loss, Ex_dynamic_loss, QF_loss)
#Draw_V(T + 1, Ex_static_V, Ex_dynamic_V, QF_V)

plot_boxplot(QF_V[9000:], Ex_static_V[9000:], Ex_dynamic_V[9000:])

#plot_cdf(Ex_static_V[5000:], Ex_dynamic_V[5000:], QF_V[5000:])

# data = zip(Ex_static_loss, Ex_dynamic_loss, QF_loss, Best_x, 
#            Ex_static_V, Ex_dynamic_V, QF_V, Best_V)

# filename = 'Comparing_with_QF.csv'

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

