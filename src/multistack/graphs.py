import multifunction

# multifunction.multi(100, "plots/polarized", rot_angle=-20, returnval = "EField", time_len=1500, time_res = 10, emptyspace=False)

dist = 5
res = 2

multifunction.multi(dist, f"cw_{dist}_{res}_tm", spatial_resolution=res, returnval="CW", emptyspace=False)
multifunction.multi(dist, f"cw_{dist}_{res}_tm_ctl", spatial_resolution=res, returnval="CW", emptyspace=True)