import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.signal as signal

# Load data #scale error for length
ldos = np.load("bin/multiangle/ldos.npy")
distances = np.load("bin/multiangle/distances.npy")
angles = np.load("bin/multiangle/angles.npy")

n = 100  # Adjust window size as needed
ldos = signal.convolve(ldos, np.ones(n) / n)[n:-n]
distances = signal.convolve(distances, np.ones(n) / n)[n:-n]
#Control
glass = np.load("bin/glass/ldos.npy")
glass_distances = np.load("bin/glass/distances.npy")

# # Define fitting functions
# drude_lorentz_fit = lambda x, A, gamma, omega0, C: A * (gamma / ((x - omega0)**2 + gamma**2)) + C
# exp_fit = lambda x, a, b, c: a * np.exp(-b * x) + c
# exp_fit_2 = lambda x, a1, b1, a2, b2, c: a1 * np.exp(-b1 * x) + a2 * np.exp(-b2 * x) + c

# # Fit the double-exponential curve
# exp_params, exp_cov = opt.curve_fit(exp_fit, distances, ldos, p0=(1, 0.05, 0))

# # Fit the double-exponential curve
# exp_params_2, exp_cov_2 = opt.curve_fit(exp_fit_2, distances, ldos, p0=(1, 0.05, 0.5, 0.01, 0))

# #Fit the drude-lorentz curve
# drude_params, drude_cov = opt.curve_fit(drude_lorentz_fit, distances, ldos, p0=(1, 0.1, 1, 0))

# # Generate fitted values
# fitted_drude = drude_lorentz_fit(distances, *drude_params)
# fitted_exp   = exp_fit(distances, *exp_params)
# fitted_exp_2 = exp_fit_2(distances, *exp_params_2)

# Plot ground truth and fits
fig, ax = plt.subplots()
print(distances)
# ax = plt.figure().add_subplot(projection="3d")
ax.scatter(distances, ldos, label="ENZ", marker="o")
# ax.plot(distances, fitted_drude, label="Drude-Lorentz Fit", linestyle="--")
# ax.plot(distances, fitted_exp, label="Exponential Fit", linestyle="-")
# ax.plot(distances, fitted_exp_2, label="2-Exponential Fit", linestyle="--")
ax.plot(glass_distances, glass, label="Glass", color="purple", marker="o")
# print(exp_params_2, "\n", np.sqrt(np.diag(exp_cov_2)))
# print(f"\nSpace Constants:\n{1/exp_params[1]}nm -> 1\n{1/exp_params_2[1]}nm\n{1/exp_params_2[3]}nm -> 2")
# print(f"\n\n\nDrude Params:\n{drude_params}\n{np.sqrt(np.diag(drude_cov))}")
ax.set_xlabel("Distance")
ax.set_ylabel("LDOS")
ax.ticklabel_format(axis='y', style='sci', scilimits=(-1, 1))
ax.legend()
plt.show()