import random
import math
import numpy as np
from itertools import permutations

class S_Hedge:
    def __init__(self, n_, N_, eta_, a_): #如果记录的东西太多可以优化。
        self.n = n_
        self.N = N_
        self.w = np.zeros(N_)
        for i in range(n_):
            self.w[i] = 1
        self.eta = eta_
        self.a = a_
        self.expert = [] #每轮专家的mask, 1为avaluable, 0为not
        self.expert.append(self.w) #第一个首先就前n个是1
        self.loss = [] #每一轮loss的向量, 用来算ranking loss
        self.ll = [] #每一轮w*l
        self.m = 0 #记录有几个night
    
    def weighted_choice(self):
        w = self.w
        rnd = random.random() * sum(w)
        for i, weight in enumerate(w):
              rnd -= weight
              if rnd <= 0:
                  return i
        return -1
    
    def loss_and_update(self, l_, expert_): #l_是上一轮expert结果的loss，expert_是新一轮expert的名单
        self.loss.append(l_)
        prior_expert = self.expert[-1]
        sum_loss = 0
        for i in range(self.N):
            sum_loss += self.w[i] * l_[i] * prior_expert[i]
        sum_loss /= sum(self.w)
        self.ll.append(sum_loss)

        if prior_expert.all() == expert_.all():           
            for i in range(self.N):
                if expert_[i] == 1:
                    self.w[i] *= math.exp(-self.eta*l_[i])
            summ = sum(self.w)
            for i in range(self.N):
                if expert_[i] == 1:
                    self.w[i] = self.w[i]/summ
        else:
            for i in range(self.N):
                if prior_expert[i] == 1:
                    self.w[i] *= math.exp(-self.eta*l_[i])
            die_w = 0
            change = 0
            all_w = 0
            for i in range(self.N):
                if prior_expert[i] == 1:
                    all_w += self.w[i]
                    if expert_[i] == 0:
                        die_w += self.w[i]
                        self.w[i] = 0
                        change += 1
            for i in range(self.N):
                if expert_[i] == 1 and prior_expert[i] == 1:
                    self.w[i] = (1-self.a)*all_w/self.n + self.a*self.w[i] + self.a*die_w/(self.n-change)
                if expert_[i] == 1 and prior_expert[i] == 0:
                    self.w[i] = (1-self.a)*all_w/self.n       
        self.expert.append(expert_)
    
    def ranking_loss(self, T): #这个函数非常慢，只有当需要计算理论ranking loss时才调用
        items = []
        for i in range(self.N):
            items.append(i)
        min_loss = T
        x = items
        for p in permutations(items):
            sum_loss = 0
            for i in range(T):
                for j in p:
                    if self.expert[i][j] == 1:
                        sum_loss += self.loss[i][j]
                        break
            if sum_loss < min_loss:
                min_loss = sum_loss
                x = p
        return p
    
    def loss_permutation(self, T, p): #计算两个的regret？我没看懂这个用来干啥
        regret = []
        sum_loss = 0
        for i in range(T):
            sum_loss += self.ll[i]
            for j in p:
                if self.expert[i][j] == 1:
                    sum_loss -= self.loss[i][j]
                    break
            regret.append(sum_loss)
        return regret

# 该算法只多提供一个subsitute函数，每次换前k个expert    
class Random_Sub_Hedge:
    def __init__(self, n_:int, N_:int, k_:int, eta_, a_): #如果记录的东西太多可以优化。
        self.n = n_
        self.N = N_
        self.w = np.zeros(N_)
        self.expert = 0 #这个到+n编号为目前的expert
        for i in range(n_):
            self.w[i] = 1
        self.eta = eta_
        self.a = a_
        self.k = k_
        self.loss = [] #每一轮w*l
        self.m = 0 #记录有几个night
    
    def weighted_choice(self):
        w = self.w
        rnd = random.random() * sum(w)
        for i, weight in enumerate(w):
              rnd -= weight
              if rnd <= 0:
                  return i
        return -1
    
    def loss_and_update(self, l_): #l_是上一轮expert结果的loss
        sum_loss = 0
        for i in range(self.N):
            if i >= self.expert and i < self.expert + self.n:
                sum_loss += self.w[i] * l_[i] 
        sum_loss /= sum(self.w)
        self.loss.append(sum_loss)
          
        for i in range(self.N):
            if i >= self.expert and i < self.expert + self.n:
                self.w[i] *= math.exp(-self.eta*l_[i])
        sumw = sum(self.w)
        for i in range(self.N):
            if i >= self.expert and i < self.expert + self.n:
                self.w[i] /= sumw / self.n
        
    def substitute_expert(self): 
        new_expert = self.expert + self.k   
        die_w = 0
        change = 0
        all_w = 0
        for i in range(self.N):
            if i >= self.expert and i < self.expert + self.n:
                all_w += self.w[i]
                if i < new_expert:
                    die_w += self.w[i]
                    self.w[i] = 0
                    change += 1
        
        for i in range(self.N):
            if i >= new_expert and i < self.expert + self.n:
                self.w[i] = (1-self.a)*all_w/self.n + self.a*self.w[i] + self.a*die_w/(self.n-change)
            if i >= self.expert + self.n and i < new_expert + self.n:
                self.w[i] = (1-self.a)*all_w/self.n       
        
        self.expert = new_expert