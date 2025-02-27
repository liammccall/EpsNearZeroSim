import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

# Load data #scale error for length
ldos = np.load("bin/fine/ldos.npy") * (1 + np.cos(np.radians(20))) / 2
distances = np.load("bin/fine/distances.npy")

# Define fitting functions
exp_fit = lambda x, a, b, c: a * np.exp(-b * x) + c
exp_fit_2 = lambda x, a1, b1, a2, b2, c: a1 * np.exp(-b1 * x) + a2 * np.exp(-b2 * x) + c
inv_fit = lambda x, a, b, c: a / (x + b)**c

# Fit the double-exponential curve
exp_params, exp_cov = opt.curve_fit(exp_fit, distances, ldos, p0=(1, 0.05, 0))

# Fit the double-exponential curve
exp_params_2, exp_cov_2 = opt.curve_fit(exp_fit_2, distances, ldos, p0=(1, 0.05, 0.5, 0.01, 0))

# Fit the inexp_coverse curve
inv_params, inv_cov = opt.curve_fit(inv_fit, distances, ldos, p0=(1, 1, 2.1))

# Generate fitted values
fitted_exp   = exp_fit(distances, *exp_params)
fitted_exp_2 = exp_fit_2(distances, *exp_params_2)
fitted_inv   = inv_fit(distances, *inv_params)

# Plot ground truth and fits
plt.plot(distances, ldos, label="Ground Truth", marker="o", linestyle="None")
plt.plot(distances, fitted_exp, label="Exponential Fit", linestyle="-")
plt.plot(distances, fitted_exp_2, label="2-Exponential Fit", linestyle="--")
plt.plot(distances, fitted_inv, label="Inverse Fit", linestyle="-.")
print(exp_params, "\n", np.diag(exp_cov),"\n",  inv_params, "\n", np.diag(inv_cov))
print(exp_params_2, "\n", np.diag(exp_cov_2))
print(f"\nSpace Constants:\n{1/exp_params[1]}nm -> 1\n{1/exp_params_2[1]}nm\n{1/exp_params_2[3]}nm -> 2")
plt.xlabel("Distance")
plt.ylabel("LDOS")
plt.legend()
plt.show()