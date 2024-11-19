import numpy as np
import meep as mp
import nlopt
import matplotlib.pyplot as mpl

import disRel.lorentzfit as lf
import util.chatter as chat


def getFitted(datasource : str, wl_r : tuple[float, float], wl_units : str, num_lorentzians = 4, num_repeat = 10, imaginary_weight = 4):
    
    mydata = np.genfromtxt(datasource, delimiter=",")[1:-1]
    n = mydata[:, 1] + 1j * mydata[:, 2]

    
    # Fitting parameter: the instantaneous (infinite frequency) dielectric.
    # Should be > 1.0 for stability and chosen such that
    # np.amin(np.real(eps)) is     ~1.0.  eps is defined below.
    eps_inf = 1.1

    eps = np.square(n) - eps_inf
    
    # this would be epic
    # eps = np.float_power(eps, 1 / imaginary_weight)

    wl_scale = chat.scaleNm(wl_units)
    
    # Fit only the data in the wavelength range of [wl_r[0], wl_r[1]].
    wl = wl_scale * mydata[:, 0]
    start_idx = np.where(wl > wl_r[0])
    idx_start = start_idx[0][0]
    end_idx = np.where(wl < wl_r[1])
    idx_end : int = end_idx[0][-1] + 1

    # The fitting function is ε(f) where f is the frequency, rather than ε(λ).
    # Note: an equally spaced grid of wavelengths results in the larger
    #       wavelengths having a finer frequency grid than smaller ones.
    #       This feature may impact the accuracy of the fit.
    freqs = 1 / wl  # units of 1/μm
    freqs_reduced = freqs[idx_start:idx_end]
    wl_reduced = wl[idx_start:idx_end]
    eps_reduced = eps[idx_start:idx_end]

    ps = np.zeros((num_repeat, 3 * num_lorentzians))
    mins = np.zeros(num_repeat)
    for m in range(num_repeat):
        # Initial values for the Lorentzian polarizability terms. Each term
        # consists of three parameters (σ, ω, γ) and is chosen randomly.
        # Note: for the case of no absorption, γ should be set to zero.
        p_rand = [10 ** (np.random.random()) for _ in range(3 * num_lorentzians)]
        
        ps[m, :], mins[m] = lf.lorentzfit(
            p_rand, freqs_reduced, eps_reduced, nlopt.LD_MMA, 1e-25, 50000
        )
        ps_str = "( " + ", ".join(f"{prm:.4f}" for prm in ps[m, :]) + " )"
        print(f"iteration:, {m:3d}, ps_str, {mins[m]:.6f}")

    # Find the best performing set of parameters.
    idx_opt = np.where(np.min(mins) == mins)[0][0]
    
    return ps, idx_opt
    # popt_str = "( " + ", ".join(f"{prm:.4f}" for prm in ps[idx_opt]) + " )"    
    # print(f"optimal:, {popt_str}, {mins[idx_opt]:.6f}")