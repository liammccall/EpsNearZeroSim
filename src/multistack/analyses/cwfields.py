import meep as mp
import matplotlib.pyplot as plt
import numpy as np

def evaluate(sim, nonpml_vol, cmap, file):
    
    # num_tols = 1
    # tols = np.power(10, np.arange(-8.0,-8.0-num_tols,-1.0))
    # ex_dat = np.zeros((32,32,num_tols), dtype=np.complex_)
    # ey_dat = np.zeros((32,32,num_tols), dtype=np.complex_)
    # ez_dat = np.zeros((32,32,num_tols), dtype=np.complex_)

    # for i in range(num_tols):
    #     sim.init_sim()
    #     sim.solve_cw(tols[i], 10000, 10)
    #     ex_dat[:,:,i] = sim.get_array(vol=nonpml_vol, component=mp.Ex)
    #     ey_dat[:,:,i] = sim.get_array(vol=nonpml_vol, component=mp.Ey)
    #     ez_dat[:,:,i] = sim.get_array(vol=nonpml_vol, component=mp.Ez)

    # err_dat = np.zeros(num_tols-1)
    # for i in range(num_tols-1):
    #     err_dat[i] = np.linalg.norm(ez_dat[:,:,i]-ez_dat[:,:,num_tols-1])
        
    
    sim.init_sim()
    sim.solve_cw(10e-8, 100000, 10)
    
    eps_data = sim.get_array(vol=nonpml_vol, component=mp.Dielectric)
    ex_data = np.real(sim.get_array(vol=nonpml_vol, component=mp.Ex))    
    ey_data = np.real(sim.get_array(vol=nonpml_vol, component=mp.Ey))    
    ez_data = np.real(sim.get_array(vol=nonpml_vol, component=mp.Ez))    
        
    np.save(f"bin/{file}_ex", ex_data)
    np.save(f"bin/{file}_ey", ey_data)
    np.save(f"bin/{file}_ez", ez_data)
        
    # plt.figure()
    fig, axes = plt.subplots(3, 1)
    axes[0].imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
    axes[0].imshow(ex_data.transpose(), interpolation='spline36', cmap=cmap, alpha=0.9)
    axes[1].imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
    axes[1].imshow(ey_data.transpose(), interpolation='spline36', cmap=cmap, alpha=0.9)
    axes[2].imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
    axes[2].imshow(ez_data.transpose(), interpolation='spline36', cmap=cmap, alpha=0.9)
    # plt.axis('off')
    # plt.show()

    fig.savefig(f"plots/{file}.png")
    
    return 0
