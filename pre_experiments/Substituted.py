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


def Theoretical(m, T):
    return (m+1)*math.log(n/(1-alpha))/eta + eta*T/2

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