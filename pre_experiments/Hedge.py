import random
import math
import numpy as np
from itertools import permutations

class Hedge:
    def __init__(self, n_, eta_):
        self.n = n_
        self.w = np.ones(n_)
        self.eta = eta_
        self.loss = [] #每一轮w*l
    
    def weighted_choice(self):
        w = self.w
        rnd = random.random() * sum(w)
        for i, weight in enumerate(w):
              rnd -= weight
              if rnd <= 0:
                  return i
        return -1
    
    def loss_and_update(self, l):
        sum_loss = 0
        for i in range(self.n):
            sum_loss += self.w[i] * l[i]
        sum_loss /= sum(self.w)
        self.loss.append(sum_loss)
        
        for i in range(self.n):
            self.w[i] *= math.exp(-self.eta*l[i])
        summ = sum(self.w)
        for i in range(self.n):
            self.w[i] = self.w[i]/summ

class S_Hedge:
    def __init__(self, n_, N_, eta_, a_):
        self.n = n_
        self.N = N_
        self.w = np.zeros(N_)
        for i in range(n_):
            self.w[i] = 1
        self.eta = eta_
        self.a = a_
        self.expert = [] #每轮专家的mask, 1为avaluable, 0为not
        self.expert.append([1,1,1,1,0,0,0,0,0,0]) #第一个首先就前n个是1
        self.loss = [] #每一轮loss的向量,N维
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
    
    def loss_append(self, l_, expert_):
        self.loss.append(l_)
        prior_expert = self.expert[-1]
        if prior_expert == expert_:           
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
            
    def ll_append(self, ll_):
        self.ll.append(ll_)
    
    def ranking_loss(self, T):
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
    
    def loss_permutation(self,T, p):
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