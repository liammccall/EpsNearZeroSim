import meep as mp
import numpy as np
import matplotlib as mpl

# import disRel.processInput as pi
import materials.disRel.processInput as pi

def fitMaterial(datasource : str, wl_r : tuple[float, float], wl_units : str,
                num_lorentzians = 4, num_repeat = 10, imaginary_weight = 4, name : str = ""):
    eps_inf = 1.1
    
    ps, idx_opt = pi.getFitted(datasource, wl_r, wl_units, num_lorentzians, num_repeat, imaginary_weight)
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

    # np.save("bin\\mats\\" + name, (ps, idx_opt))
    
    return mp.Medium(epsilon=eps_inf, E_susceptibilities=E_susceptibilities)
    
    
def plotMaterial(material : mp.Medium, freqs_reduced, eps_reduced, wl_reduced):

    eps_inf = 1.1

    # Plot the fit and the actual data for comparison.
    mymaterial_eps = [material.epsilon(f)[0][0] for f in freqs_reduced]

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
    fig.savefig("figs/eps_fit_sample.png", dpi=150, bbox_inches="tight")
    
    
# def loadMaterial(name : str):
#     eps_inf = 1.1
    
#     ps, idx_opt = np.load("bin\\mats\\" + name + ".npy")
#     # Define a `Medium` class object using the optimal fitting parameters.
#     E_susceptibilities = []

#     for n in range(num_lorentzians):
#         mymaterial_freq = ps[idx_opt][3 * n + 1]
#         mymaterial_gamma = ps[idx_opt][3 * n + 2]

#         if mymaterial_freq == 0:
#             mymaterial_sigma = ps[idx_opt][3 * n + 0]
#             E_susceptibilities.append(
#                 mp.DrudeSusceptibility(
#                     frequency=1.0, gamma=mymaterial_gamma, sigma=mymaterial_sigma
#                 )
#             )
#         else:
#             mymaterial_sigma = ps[idx_opt][3 * n + 0] / mymaterial_freq**2
#             E_susceptibilities.append(
#                 mp.LorentzianSusceptibility(
#                     frequency=mymaterial_freq,
#                     gamma=mymaterial_gamma,
#                     sigma=mymaterial_sigma,
#                 )
#             )
    
#     return mp.Medium(epsilon=eps_inf, E_susceptibilities=E_susceptibilities)