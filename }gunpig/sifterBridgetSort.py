# def get_ps(tnum):
#     # Read FFT data in given time slice (0 to 504)
#     tstr = "%03d" % i
#     filename = datadir+'FFT_DATA/FFT_128_%s.dat' % tstr

#     f = open(filename,'rb')
#     time = N.fromfile(f,N.float64,1)
#     nsize = N.fromfile(f,N.int32,1)
#     fft_re = N.fromfile(f,N.float32,nsize)
#     fft_im = N.fromfile(f,N.float32,nsize)
#     f.close()
    
#     fft_re = N.reshape(fft_re,[L+1,L+1,L2+1])
#     fft_im = N.reshape(fft_im,[L+1,L+1,L2+1])
#     # print 'a = %f' % time[0]
    
#     # define k's that correspond to fourier modes: (2*math.pi/boxsize)*N.array(x,y,z)
#     # x = [-L/2:L/2], y = [-L/2,L/2], z = [0,L/2]
#     # compute k^2 = kx^2 + ky^2 + kz^2, PS = fft_re^2+fft_im^2
#     kx = N.atleast_3d(N.expand_dims(N.arange(-L2,L2+1),axis=1))
#     ky = N.atleast_3d(N.expand_dims(N.arange(-L2,L2+1),axis=0))
#     kz = N.expand_dims(N.expand_dims(N.arange(0,L2+1),axis=0),axis=0)
#     kx = N.broadcast_to(kx,(L+1,L+1,L2+1))
#     ky = N.broadcast_to(ky,(L+1,L+1,L2+1))
#     kz = N.broadcast_to(kz,(L+1,L+1,L2+1))
#     k = N.sqrt(kx*kx+ky*ky+kz*kz)*N.pi*2/boxsize
#     ps = fft_re*fft_re+fft_im*fft_im
#     ps = ps[k>0]
#     k = k[k>0]
    
#     # average PS in logarithmic bins of k
#     nbins = 100
#     ps1d, kbin = N.histogram(N.log10(k),nbins,weights=ps)
#     counts = N.histogram(N.log10(k),nbins)[0]
#     ps1d = ps1d[counts>0]/counts[counts>0] # normalization? boxsize^3/128^6??
#     binvals = kbin[0:nbins]+N.diff(kbin)/2
#     binvals = binvals[counts>0]
#    # binvals = 10**binvals
#     return binvals,ps1d,time[0]

pos = N.empty((nparticles**3,3),N.float32)
vel = N.empty((nparticles**3,3),N.float32)
ids = N.empty((nparticles**3),N.int64)
istart = 0

for i in N.arange(0, numfiles):
    file=filename+str(i)
    f=open(file, 'rb')
    
    header_size = N.fromfile(f,N.int32,1)[0] # = 256: error catch here?
    numpart = N.fromfile(f,N.int32,6)
    npart = numpart[1] # number of particles in this file
    mass = N.fromfile(f,N.float64,6)
    pmass = mass[1] # in units of 10^10 solar masses?
    scalefact,redshift = N.fromfile(f,N.float64,2)
    flag_sfr,flag_feedback = N.fromfile(f,N.int32,2)
    numpart_tot = N.fromfile(f,N.int32,6)
    ntotal = numpart_tot[1]
    flag_cooling,num_files = N.fromfile(f,N.int32,2)
    boxsize,omega0,omegal,hubble = N.fromfile(f,N.float64,4)
    flag_stellarage,flag_metals,hashtabsize = N.fromfile(f,N.int32,3)
    # read rest of header_size + 2 dummy integers:
    dummy = N.fromfile(f,N.int32,23)
    
    thispos = N.fromfile(f,N.float32,3*npart)
    thispos = N.reshape(thispos, [npart, 3])
#    thispos = thispos.astype(N.float) # needed?
    
    # read velocities
    dummy = N.fromfile(f,N.int32,2)
    thisvel = N.fromfile(f,N.float32,3*npart)
    thisvel = N.reshape(thisvel, [npart, 3])

    # read IDs
    dummy = N.fromfile(f,N.int32,2)
    thisID = N.fromfile(f,N.int64,npart)
    
    f.close()
    
    pos[istart:(istart+npart),:] = thispos
    vel[istart:(istart+npart),:] = thisvel
    ids[istart:(istart+npart)] = thisID
    
    istart = istart + npart

print 'finished reading particles'
