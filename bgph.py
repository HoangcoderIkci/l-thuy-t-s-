import math


def Nhan_trong_module(A, B, Module):
    A = int(A)
    B = int(B)
    Module = int(Module)
    n = math.ceil(math.log(Module, 2))
    binary_list = [int(i) for i in bin(A)[2:]]
    temp = n - len(binary_list)
    binary_list = [0] * temp + binary_list
    C = (2 ** (2 * n)) % Module
    R = 0
    for i in range(n):
        if binary_list[n - 1 - i] & 0b01:
            R = R + B
        if R & 0b01:
            R += Module
        R >>= 1
    if R >= Module:
        R -= Module
    A, B = R, C
    binary_list = [int(i) for i in bin(A)[2:]]
    temp = n - len(binary_list)
    binary_list = [0] * temp + binary_list
    R = 0
    for i in range(n):
        if binary_list[n - 1 - i] & 0b01:
            R += B
        if R & 0b01:
            R += Module
        R >>= 1
    if R >= Module:
        R -= Module
    return R


def UCLN_u_v_in_MOD(A, B, *, MOD):
    g = 1
    _A = A
    _B = B
    while _A % 2 == 0 and _B % 2 == 0:
        _A >>= 1
        _B >>= 1
        g <<= 1
    x, y, E, F, G, H = _A, _B, 1, 0, 0, 1
    while x != 0:
        while x % 2 == 0:
            x >>= 1
            if E % 2 == 0 and F % 2 == 0:
                F >>= 1
                E >>= 1
            else:
                E = (E + _B) >> 1
                F = (F - _A) >> 1
        while y % 2 == 0:
            y >>= 1
            if G % 2 == 0 and H % 2 == 0:
                G >>= 1
                H >>= 1
            else:
                G = (G + _B) >> 1
                H = (H - _A) >> 1
        if x >= y:
            x -= y
            E -= G
            F -= H
        else:
            y -= x
            G -= E
            H -= F

    # print(f"d = {g*y}")
    # print(f"u = {G}")
    # print(f"v = {H}")
    return (g * y) % MOD, G % MOD, H % MOD


def process1(A, so_mu, l, r, w, t, n, d, res, MOD):
    m = r - l + 1
    print(l, r)
    temp = int(m / 2)
    A_cp = A.copy()
    c1 = (w**so_mu) % MOD
    c2 = (w ** (so_mu + n / 2)) % MOD
    for i in range(l, l + temp):
        A_cp[i] = (A[i] + c1 * A[i + temp]) % MOD
        A_cp[i + temp] = (A[i] + c2 * A[i + temp]) % MOD
    print(A_cp)
    if t < d:
        A_cp, res = process1(A_cp, so_mu / 2, l, l + temp - 1, w, t + 1, n, d, res, MOD)
        A_cp, res = process1(
            A_cp, (so_mu + n / 2) / 2, l + temp, r, w, t + 1, n, d, res, MOD
        )
    else:
        res[int(so_mu)] = A_cp[l]
        res[int((so_mu + n / 2))] = A_cp[r]
    return A_cp, res


def find_bgph(A, n, w, *, d, res, MOD):
    r = len(A) - 1
    A_res, res = process1(A, 0, 0, r, w, 1, n, d, res, MOD)
    # qua trinh 2 tim n^-1
    d, u, v = UCLN_u_v_in_MOD(n, MOD, MOD=MOD)
    # print(u, v)
    res_cp = res.copy()
    for i in range(len(res)):
        res[i] = Nhan_trong_module(u, res[i], Module=MOD)
    l_temp = res.copy()[1:]
    l_temp.reverse()
    hs_polymian = [res[0]] + l_temp
    return A_res, res_cp, hs_polymian


w = 2
module = 17
l_A = [1, 3, 2, 0, 1, 0, 0, 0]
n = len(l_A)
res1 = [0] * n
d = int(math.log2(n))
# k = 4
_, res1, hs_pl = find_bgph(l_A, n, w, d=d, res=res1, MOD=module)
print(res1)
# print(hs_pl)
l_B = [1, 1, 0, 2, 0, 0, 0, 0]
res2 = [0] * n
_, res2, hs_p2 = find_bgph(l_B, n, w, d=d, res=res2, MOD=module)
print(res2)
# print(hs_p2)
pl1 = res1
pl2 = res2
tich_toa_do = []
if len(pl1) <= len(pl2):
    tich_toa_do = pl2.copy()
    for i in range(len(pl1)):
        tich_toa_do[i] = Nhan_trong_module(pl1[i], tich_toa_do[i], Module=module)
else:
    tich_toa_do = pl1.copy()
    for i in range(len(pl2)):
        tich_toa_do[i] = Nhan_trong_module(pl2[i], tich_toa_do[i], Module=module)
print(tich_toa_do)
res3 = [0] * n
_, _, hspl3 = find_bgph(tich_toa_do, n, w, d=d, res=res3, MOD=module)
print(hspl3)
# pl1 = [1, 3, 2, 0, 1]
# pl2 = [1, 1, 0, 2]
# deg_sum = len(pl1) + len(pl2) - 2
# d = int(math.ceil(math.log(deg_sum, 2)))
# n = 2**d
# res = [0] * n
# MOD = 17
# w = 2

# tich_toa_do = [1, 0, 0, 1, 0, 1, 1, 1]
# A, res, hs_pl = find_bgph(tich_toa_do, n, w, d=d, MOD=MOD, res=res)
# print(res)
# print(hs_pl)
