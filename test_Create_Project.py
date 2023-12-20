from Create_Project import Create_Project

def test_Create_Project():
    K = 100
    T = 365
    lamda = 0.5
    beta = 0.5
    sigma = 0.1

    a_simples, a_hats = Create_Project(K, T, lamda, beta, sigma)

    assert len(a_simples) == K
    assert len(a_hats) == K
    assert min(a_hats) > 0
