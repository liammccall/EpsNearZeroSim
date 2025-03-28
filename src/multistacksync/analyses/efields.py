import meep as mp
import matplotlib.pyplot as plt

def evaluate(sim, time_len, time_res, framerate, cmap, file):
    f = plt.figure(dpi=100)

    def zoom(ax):
        # ax.set_xlim(-500, 500)
        # ax.set_ylim(-500, 500)
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

    sim.run(mp.at_every(time_res, Animatex, Animatey, Animatez), 
            until=time_len)
    
    Animatex.to_mp4(framerate, file + "Ex.mp4")
    Animatey.to_mp4(framerate, file + "Ey.mp4")
    Animatez.to_mp4(framerate, file + "Ez.mp4")
