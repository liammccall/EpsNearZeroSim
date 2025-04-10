import meep as mp
import numpy as np

def evaluate(sim : mp.Simulation, nonpml_vol, freq):
    #Returns the modes at a point distance away in the y direction
    #TODO eventually want to modes from all points distance away outside of boundary
    
    dft_obj = sim.add_dft_fields([mp.Ex, mp.Ey, mp.Ez, 
                                  mp.Bx, mp.By, mp.Bz], freq, 0, 1, where=nonpml_vol, yee_grid=False)
    sim.run(until_after_sources=100)
    eps_data = sim.get_array(vol=nonpml_vol, component=mp.Dielectric)
    ex_data = np.real(sim.get_dft_array(dft_obj, mp.Ex, 0))
    ey_data = np.real(sim.get_dft_array(dft_obj, mp.Ey, 0))
    ez_data = np.real(sim.get_dft_array(dft_obj, mp.Ez, 0))
    bx_data = np.real(sim.get_dft_array(dft_obj, mp.Bx, 0))
    by_data = np.real(sim.get_dft_array(dft_obj, mp.By, 0))
    bz_data = np.real(sim.get_dft_array(dft_obj, mp.Bz, 0))
    
    return [ex_data,
            ey_data,
            ez_data,
            bx_data,
            by_data,
            bz_data,], eps_data