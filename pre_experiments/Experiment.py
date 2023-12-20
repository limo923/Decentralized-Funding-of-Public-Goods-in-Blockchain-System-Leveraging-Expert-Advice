import math
import random
import numpy as np
import matplotlib.pyplot as plt

N = 50 #总池子的大小
m = 0  #记录substitute的数量
n = 10 #每轮保持的专家人数
eta = 0.01 #权重更新率
alpha = 0.5 # 超参数
c = 0.1 #每轮loss的奖励（为了计算不越界）
L = [] #每轮所有人的loss
l = np.zeros(n) #当前轮的loss
r = np.zeros(n) #reputation/weight
f = [] #每次选了哪个 
S = [] #当前permutation让loss最小
p = 0.05

np.random.seed(1)
random.seed(3)
ave_loss = []
for i in range(n):
    ave_loss.append(np.random.uniform(0, 1))

def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
          rnd -= w
          if rnd < 0:
              return i
    return 0

def creat_loss():
    l = np.zeros(n)
    for i in range(n):
        loss = np.random.normal(ave_loss[i], 0.05)
        l[i] = loss
    return l

def Substituted(die):
    d = len(die)
    sumdie = 0
    sumall = 0
    for i in range(n):
        if i in die:
            sumdie += r[i]
        sumall += r[i]
    for i in range(n):
        if i in die:
            r[i] = (1-alpha)*sumall/n
        else:
            r[i] = (1-alpha)*sumall/n + alpha*r[i] + alpha*sumdie/(n-d)

def New_expert(die):
    for i in die:
        ave_loss[i]= np.random.uniform(0,1)

def Round():
    l = creat_loss()
    f = weighted_choice(r)
    floss = l[f]
    for i in range(n):
        r[i] = r[i]*math.exp(-eta*(l[i] - c))
    
    night = 0
    die = []
    for i in range(n):
        if random.random() < p:
            die.append(i)
            night = 1
    if night == 1:
        Substituted(die)
        New_expert(die)
    
    return floss, l, night

def min_rank_loss(L, T): #Problem
    S = np.zeros(n)
    for i in range(n):
        sumloss = 0
        for j in range(T+1):
            sumloss += L[j][i]
        S[i] = sumloss
    return min(S)

def Theoretical(m, T):
    return (m+1)*math.log(n/(1-alpha))/eta + eta*T/2

if __name__ == '__main__':
    T = 1000
    Average_loss = []
    theore = [] 
    for t in range(T):
        floss, l, night = Round()
        m += night
        L.append(l)
        f.append(floss)
        #print(f)
        rank_loss = min_rank_loss(L, t)
        Accumulate_loss = sum(f) - rank_loss
        Average_loss.append(Accumulate_loss / (t+1))
        #theore.append(Theoretical(m, t+1) / (t+1))           
        
    plt.title('Average_Turn_Loss')
    plt.xlabel('Episode')
    plt.ylabel('Loss')
    plt.plot(Average_loss)
    plt.plot(theore)
    plt.show()    
       
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    