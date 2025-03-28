import meep as mp

def evaluate(sim : mp.Simulation, freq):
    
    # sim.run(mp.dft_ldos(freq, 0, 1),
    #         until_after_sources=mp.stop_when_fields_decayed(1, mp.Ex, mp.Vector3(-10, 10), 1e-8))
    sim.run(mp.dft_ldos(freq, 0, 1),
            until=2000)
    
    print(sim.ldos_data)
    
    return sim.ldos_data[0]