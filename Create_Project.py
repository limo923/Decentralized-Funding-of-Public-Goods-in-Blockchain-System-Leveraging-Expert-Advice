# 生成每个项目时每个人的收益函数的参数
# 只有这里生成用到随机性
# 每个人的Value Function为V(x) = a x^(1/2)
# a ~ Exp(lambda) 来自指数分布，参数lambda
# 偏见为b ~ N(beta, sigma), 来自正态分布，平均为beta.
# a_hat = a + b
import numpy as np

def Create_Project(K:int, lamda, beta, sigma):
    a_simples = np.random.exponential(scale = 1/lamda, size = K)
    b_simples = np.random.normal(loc = beta, scale = sigma, size = K)
    a_hats = a_simples + b_simples
    return a_simples, a_hats

def Create_Expert(N:int, kappa_min, kappa_max):
    experts = np.random.uniform(low = kappa_min, high = kappa_max, size = N)
    return experts


