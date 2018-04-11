header={}
    
npall = N.fromfile(f,N.int32,6) # DM only simulations - other np's and masses are 0

header['np_file'] = npall[1]

###

# number of particles in this file (needed to read positions)
massall = N.fromfile(f,N.float64,6)

header['mass'] = massall[1]

header['time'], header['redshift'] = N.fromfile(f,N.float64,2)

header['flag_sfr'], header['flag_feedback'] = N.fromfile(f,N.int32,2)

###

nptotal = N.fromfile(f,N.int32,6)

header['npart'] = nptotal[1]

header['flag_cooling'],header['num_files'] \
            = N.fromfile(f,N.int32,2)

header['BoxSize'],header['omega0'],header['omegaL'],header['hubble'] \
            = N.fromfile(f,N.float64,4)

header['flag_stellarage'],header['flag_metals'],header['hashtabsize'] \
            = N.fromfile(f,N.int32,3)

# read rest of header_size + 2 filler integers:

###

empty = N.fromfile(f,N.int32,23)
