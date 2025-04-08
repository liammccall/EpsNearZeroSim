import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import scipy.optimize as opt
import meep as mp
from meep.materials import Au
import pandas as pd


import sys
sys.path.append('/home/liam/Projects/ENZSim/src')
from materials import asml

def bruggeman(e1, e2, d1, d2):
    c1 = d1 / (d1 + d2)
    c2 = d2 / (d1 + d2)
    H = (3*c1 - 1)* e1 + (3 * c2 - 1) * e2
    return (H + np.sqrt(H**2 + 8 * e1 * e2)) / 4

def bogdanovx(e1, e2, d1, d2):
    return (np.multiply(d1,e1) + np.multiply(d2,e2)) / (d1 + d2)

def bogdanovx_wvl(wvl):
    return np.real(bogdanovx(e_au_q(wvl), e_tio2_q(wvl), 10, 12))

def bogdanovx_wvl_mp(wvl):
    return np.real(bogdanovx(Au.epsilon(1 / wvl)[0, 0], e_tio2_q(wvl), 10, 12)) #e_tio2_q(wvl)

def bogdanovz(e1, e2, d1, d2):
    return e1 * e2 * (d1 + d2) / (e1 * d1 + e2 * d2)#(d1 + d2) / ((d1/e1) + (d2/e2))

def bogdanovz_wvl(wvl):
    return np.real(bogdanovz(e_au_q(wvl), e_tio2_q(wvl), 10, 12))

def au_analytical(wvl):
    #wvl in um
    wvl_nm = wvl * 1e3
    photon_e = 1239.8 / (wvl_nm)
    photon_e = wvl
    # c = 299792458 # m / s
    # angular_freq = 2 * np.pi * c / wvl_m
    plasma_e = 8.48 # eV
    # planck_e = 6.582119569e-16 # eV s
    # planck_j = planck_e / 1.602e-19 # J s
    # plasma_freq = plasma_e / (planck_e)
    # relaxation_time = 14e-15 #s
    gamma = 0.072 # eV
    e_0 = 9.84
    return e_0 #- ((plasma_freq**2) / (angular_freq * (angular_freq + (1j / relaxation_time))))


def au_analytical_e(wvl):
    # plasma_e = 8.48 # eV
    # gamma = 0.072 # eV
    # planck_e = 6.582119569e-16 # eV s
    # relaxation_time = 14e-15 #s
    # gamma = planck_e / relaxation_time
    # print(gamma)
    # e_0 = 9.84
    # return e_0 - ((plasma_e**2) / (photon_e * (photon_e + 1j * gamma)))
    #https://github.com/plasmon360/LD_python/blob/master/LD.py
    ehbar = 1.519250349719305e+15
    twopic = 1.883651567308853e+09
    omega_p = 9.03 * ehbar
    f = [0.760, 0.024, 0.010, 0.071, 0.601, 4.384]
    Gamma = [0.053, 0.241, 0.345, 0.870, 2.494, 2.214]
    omega = [0.000, 0.415, 0.830, 2.969, 4.304, 13.32]
    Gamma = [_ * ehbar for _ in Gamma]
    omega = [_ * ehbar for _ in omega]
    epsilon_D = 1 - (f[0] * omega_p ** 2 / ((twopic / wvl) ** 2 + 1j * (Gamma[0]) * (twopic / wvl)))
    return epsilon_D
    

au = np.genfromtxt("data/Au.csv", delimiter=",")[1:]
tio2 = np.genfromtxt("data/TiO2.csv", delimiter=",")[1:]

def clean_exp_enz(exp_enz):
    exp_enz = exp_enz.drop(exp_enz.columns[[2, 4, 6, 8]], axis = 1)
    exp_enz.rename(columns=exp_enz.iloc[0], inplace=True)
    exp_enz = exp_enz[2:]
    exp_enz.rename(columns={ exp_enz.columns[0]: "Wvl" }, inplace = True)
    exp_enz["Wvl"] = exp_enz["Wvl"] * 1e-3
    exp_enz.set_index("Wvl", inplace=True)
    exp_enz.rename(columns={col: col[6:8] for col in exp_enz.columns}, inplace=True)
    return exp_enz

def get_perp_basis(exp_enz):
    angle_1 = 55
    angle_2 = 75
    exp_enz["Parallel"] = (exp_enz[f"{angle_2}"]*np.cos(np.deg2rad(angle_1)) - exp_enz[f"{angle_1}"]*np.cos(np.deg2rad(angle_2))) \
        / np.sin(np.deg2rad(angle_2 - angle_1))
    exp_enz["Perpendicular"] = (exp_enz[f"{angle_2}"]*np.sin(np.deg2rad(angle_1)) - exp_enz[f"{angle_1}"]*np.sin(np.deg2rad(angle_2))) \
        / np.sin(np.deg2rad(angle_2 - angle_1))
    
    

exp_enz_re = clean_exp_enz(pd.read_excel("data/ENZ.xlsx", "E1"))
exp_enz_im = clean_exp_enz(pd.read_excel("data/ENZ.xlsx", "E2"))
get_perp_basis(exp_enz_re)
get_perp_basis(exp_enz_im)
# exp_enz_im = exp_enz_im.drop(exp_enz_im.columns[[2, 4, 6, 8]], axis = 1)

print(exp_enz_re.head())
print(exp_enz_im.head())

enz_spline_perp_re = interp.UnivariateSpline(exp_enz_re.index, exp_enz_re["Perpendicular"])
enz_spline_para_re = interp.UnivariateSpline(exp_enz_re.index, exp_enz_re["Parallel"])
enz_spline_perp_im = interp.UnivariateSpline(exp_enz_im.index, exp_enz_im["Perpendicular"])
enz_spline_para_im = interp.UnivariateSpline(exp_enz_im.index, exp_enz_im["Parallel"])

# sys.exit()

# mat = asml.fitMaterial("data/Au.csv", [400, 600], "um")
# print(mat.epsilon(1 / 500))

au_spline_n = interp.UnivariateSpline(au[:, 0], au[:, 1])
au_spline_k = interp.UnivariateSpline(au[:, 0], au[:, 2])
tio2_spline_n = interp.UnivariateSpline(tio2[:, 0], tio2[:, 1])
tio2_spline_k = interp.UnivariateSpline(tio2[:, 0], tio2[:, 2])

def e_tio2_q(wvl):
    return (tio2_spline_n(wvl) + 1j * tio2_spline_k(wvl))**2
def e_au_q(wvl):
    return (au_spline_n(wvl) + 1j * au_spline_k(wvl))**2
def e_au_mp(wvl):
    return Au.epsilon(1 / wvl)[0, 0]

lower = np.maximum(np.min(au[:, 0]), np.min(tio2[:, 0]))
upper = np.minimum(np.max(au[:, 0]), np.max(tio2[:, 0]))
wvl_grid = np.linspace(lower, upper, 100)

enz_point = opt.bisect(bogdanovx_wvl_mp, 0.4, 0.8)
print(e_au_q(enz_point))
print(e_tio2_q(enz_point))
print(enz_point)

# plt.plot(wvl_grid, bruggeman(au_spline(wvl_grid), tio2_spline(wvl_grid), 10, 12), label="Bruggeman") # heterogenous (symmetric)
# plt.plot(wvl_grid, np.real(bogdanovz(e_au_q(wvl_grid), e_tio2_q(wvl_grid), 10, 12)), label="BogdanovZ") # normal
# plt.plot(wvl_grid, np.imag(bogdanovz(e_au_q(wvl_grid), e_tio2_q(wvl_grid), 10, 12)), label="BogdanovZ", linestyle="--") # normal
plt.axhline(0)
plt.axvline(enz_point)
# print(len([eps[0, 0] for eps in Au.epsilon(1 / wvl_grid)]))
plt.plot(wvl_grid, np.real(bogdanovx([eps[0, 0] for eps in Au.epsilon(1 / wvl_grid)], e_tio2_q(wvl_grid), 10, 12)), label="BogdanovX") # parallel
plt.plot(wvl_grid, np.imag(bogdanovx([eps[0, 0] for eps in Au.epsilon(1 / wvl_grid)], e_tio2_q(wvl_grid), 10, 12)), label="BogdanovX", linestyle="--") # parallel
plt.plot(wvl_grid, enz_spline_para_re(wvl_grid), label="Experimental")
plt.plot(wvl_grid, enz_spline_para_im(wvl_grid), label="Experimental", linestyle="--")
plt.xlim(0.4, 0.8)
plt.ylim(-10, 10)
# plt.plot(wvl_grid, bogdanovz(np.real(au_analytical(wvl_grid)), 7.3 * np.ones_like(wvl_grid), 10, 12), label="Strangi") # normal
# plt.plot(wvl_grid, np.real(au_analytical_e(wvl_grid)), label="Drude")
# plt.plot(wvl_grid, tio2_spline_re(wvl_grid), label="Thin Film TiO2")
# plt.plot(wvl_grid, tio2_spline_im(wvl_grid), label="Thin Film TiO2", linestyle="--")
# plt.plot(wvl_grid, np.real(e_au_q(wvl_grid)), label="Thin Film Au")
# plt.plot(wvl_grid, np.imag(e_au_q(wvl_grid)), label="Thin Film Au", linestyle="--")
# plt.plot(wvl_grid, np.real([eps[0, 0] for eps in Au.epsilon(1 / wvl_grid)]), label="Meep Au")
# plt.plot(wvl_grid, np.imag([eps[0, 0] for eps in Au.epsilon(1 / wvl_grid)]), label="Meep Au", linestyle="--")
# plasma_e = 8.48 # eV
# planck_e = 6.582119569e-16 # eV s
# # planck_j = planck_e / 1.602e-19 # J s
# c = 299792458 # m / s
# plasma_freq = plasma_e / planck_e #Hz
# plasma_freq = plasma_freq * (1e-9) / c
# # relaxation_time = 14e-15 #s
# gamma = 0.072 # eV
# e_0 = 9.84
# print(Au.epsilon(1 / wvl_grid))
# auMat = mp.Medium(epsilon=e_0, E_susceptibilities=[mp.DrudeSusceptibility(plasma_freq, )])
# plt.plot(au[:, 0], au[:, 2])
plt.legend()
plt.show()



