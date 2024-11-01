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
    popt_str = "( " + ", ".join(f"{prm:.4f}" for prm in ps[idx_opt]) + " )"
    print(f"optimal:, {popt_str}, {mins[idx_opt]:.6f}")

    # Define a `Medium` class object using the optimal fitting parameters.
    E_susceptibilities = []

    for n in range(num_lorentzians):
        mymaterial_freq = ps[idx_opt][3 * n + 1]
        mymaterial_gamma = ps[idx_opt][3 * n + 2]

        if mymaterial_freq == 0:
            mymaterial_sigma = ps[idx_opt][3 * n + 0]
            E_susceptibilities.append(
                mp.DrudeSusceptibility(
                    frequency=1.0, gamma=mymaterial_gamma, sigma=mymaterial_sigma
                )
            )
        else:
            mymaterial_sigma = ps[idx_opt][3 * n + 0] / mymaterial_freq**2
            E_susceptibilities.append(
                mp.LorentzianSusceptibility(
                    frequency=mymaterial_freq,
                    gamma=mymaterial_gamma,
                    sigma=mymaterial_sigma,
                )
            )

    mymaterial = mp.Medium(epsilon=eps_inf, E_susceptibilities=E_susceptibilities)

    # Plot the fit and the actual data for comparison.
    mymaterial_eps = [mymaterial.epsilon(f)[0][0] for f in freqs_reduced]

    fig, ax = mpl.subplots(ncols=2)

   # ax[0].plot(wl_reduced, np.real(lf.lorentzfunc()))
    ax[0].plot(wl_reduced, np.real(eps_reduced) + eps_inf, "bo-", label="actual")
    ax[0].plot(wl_reduced, np.real(mymaterial_eps), "ro-", label="fit")
    ax[0].set_xlabel("wavelength (nm)")
    ax[0].set_ylabel(r"real($\epsilon$)")
    ax[0].legend()

    ax[1].plot(wl_reduced, np.imag(eps_reduced), "bo-", label="actual")
    ax[1].plot(wl_reduced, np.imag(mymaterial_eps), "ro-", label="fit")
    ax[1].set_xlabel("wavelength (nm)")
    ax[1].set_ylabel(r"imag($\epsilon$)")
    ax[1].legend()

    fig.suptitle(
        f"Comparison of Actual Material Data and Fit\n"
        f"using Drude-Lorentzian Susceptibility"
    )

    fig.subplots_adjust(wspace=0.3)
    fig.savefig("eps_fit_sample.png", dpi=150, bbox_inches="tight")

    return mymaterial