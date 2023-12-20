import random
import math
import numpy as np

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
    
    def loss_and_update(self, l): #记录每轮的期望lost
        sum_loss = 0
        for i in range(self.n):
            sum_loss += self.w[i] * l[i]
        sum_loss /= sum(self.w)
        self.loss.append(sum_loss)
        for i in range(self.n):
            self.w[i] *= math.exp(-self.eta*l[i])
        sumw = sum(self.w)
        for i in range(self.n):
            self.w[i] = self.w[i] * self.n / sumw