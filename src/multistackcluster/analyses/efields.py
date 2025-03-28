import meep as mp
import matplotlib.pyplot as plt
import numpy as np

def evaluate(sim, time_len, time_res, framerate, cmap, file):
    f = plt.figure(dpi=100)

    def zoom(ax):
        # ax.set_xlim(100, 400)
        # ax.set_ylim(-300, 100)
        return ax
    
    Animatex = mp.Animate2D(fields=mp.Ex, f=f, realtime=False, normalize=False, plot_modifiers=[zoom],
                           output_plane=mp.Volume(mp.Vector3(), mp.Vector3(mp.inf, mp.inf, 0)), 
                               field_parameters={'alpha':0.8, 'cmap':cmap, 'interpolation':'spline36'})
    
    Animatey = mp.Animate2D(fields=mp.Ey, f=f, realtime=False, normalize=False, plot_modifiers=[zoom],
                           output_plane=mp.Volume(mp.Vector3(), mp.Vector3(mp.inf, mp.inf, 0)), 
                               field_parameters={'alpha':0.8, 'cmap':cmap, 'interpolation':'spline36'})
    
    Animatez = mp.Animate2D(fields=mp.Ez, f=f, realtime=False, normalize=False, plot_modifiers=[zoom],
                           output_plane=mp.Volume(mp.Vector3(), mp.Vector3(mp.inf, mp.inf, 0)), 
                               field_parameters={'alpha':0.8, 'cmap':cmap, 'interpolation':'spline36'})
    
    
    def func(pos, efield):
        return efield
    
    nETR_x_values = []
    nETR_y_values = []
    nETR_z_values = []
    
    # dft = mp.dft_ldos(center=mp.Vector3(dna_length), frequencies=[freq])
    
    monitor_pos = mp.Vector3(1,1)
    
    def record_fields(sim):
    
        nETR_x = sim.integrate_field_function([mp.Ex], func, 
                                        where = mp.Volume(monitor_pos,
                                                          size = mp.Vector3(0.1, 0.1, mp.inf),
                                                          is_cylindrical=True))
        nETR_y = sim.integrate_field_function([mp.Ey], func, 
                                        where = mp.Volume(monitor_pos,
                                                          size = mp.Vector3(0.1, 0.1, mp.inf),
                                                          is_cylindrical=True))
        nETR_z = sim.integrate_field_function([mp.Ez], func, 
                                        where = mp.Volume(monitor_pos,
                                                          size = mp.Vector3(0.1, 0.1, mp.inf),
                                                          is_cylindrical=True))
    
        nETR_x_values.append(nETR_x)
        nETR_y_values.append(nETR_y)
        nETR_z_values.append(nETR_z)

    print(time_res)
    print(time_len)
    
    sim.run(mp.at_every(time_res, Animatex, Animatey, Animatez, record_fields), 
            until=time_len)
    
    Animatex.to_mp4(framerate, file + "Ex.mp4")
    Animatey.to_mp4(framerate, file + "Ey.mp4")
    Animatez.to_mp4(framerate, file + "Ez.mp4")
        
    return sum(np.power(nETR_x_values, 2)) + sum(np.power(nETR_y_values, 2)) + sum(np.power(nETR_z_values, 2))
