        header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
        numpart     = N.fromfile(f, N.int32, 6)
        npart       = numpart[1] # Number of DM-particles in this file

        mass  = N.fromfile(f, N.float64, 6)
        pmass = mass[1]     # In units of 10^10 solar masses?
        
        scalefact, redshift     = N.fromfile(f, N.float64, 2)
        flag_sfr, flag_feedback = N.fromfile(f, N.int32, 2)
        
        numpart_tot = N.fromfile(f, N.int32, 6) # not used
        # ntotal = numpart_tot[1]                 # not used
        
        flag_cooling, num_files                   = N.fromfile(f, N.int32, 2)
        boxsize, omega0, omegal, hubble           = N.fromfile(f, N.float64, 4)
        flag_stellarage, flag_metals, hashtabsize = N.fromfile(f, N.int32, 3)
        # Read rest of header_size + 2 dummy integers:
        dummy = N.fromfile(f, dtype=N.int32, count=23)