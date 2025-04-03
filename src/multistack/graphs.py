import multifunction

# multifunction.multi(100, "plots/polarized", rot_angle=-20, returnval = "EField", time_len=1500, time_res = 10, emptyspace=False)

dist = 20

multifunction.multi(dist, f"cw_{dist}_1_tm", returnval="CW", emptyspace=False)
multifunction.multi(dist, f"cw_{dist}_1_tm_ctl", returnval="CW", emptyspace=True)