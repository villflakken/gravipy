import numpy as N
import d
import power as P


ngrid=1024

numsnaps=64
numfiles=256
nparticles=1024

outdir = '/home/nuala/indra/corrfunc/'

### UPDATE BELOW: runstart, numruns, snapnum, output filenames/locs

# Calculate from runstart to numruns-1 (based on file locations in runid, datadir)
runstart = 320
numruns = 384 # 64 at a time
snapnum = 63
#snapnum = 47 # z = 0.56
#snapnum = 41 # z = 0.99

# if runno starts at 1:
#x = (runno-1)/64
#y = (runno-1)/8 % 8
#z = (runno-1) % 8

def calc_cfs():

    for i in N.arange(runstart, numruns):
        datadir = '/datascope/indra%i/' % (i/64)
        runid = '%i_%i_%i' % (i/64,i/8 % 8,i % 8)
        dir=datadir+runid
        print 'reading run number %d, %s' % (i,runid)
        #real space
        read_dir(dir, snapnum, i, 0, 0)
        #redshift space, first axis
        read_dir(dir, snapnum, i, 1, 0)
        #redshift space, second axis
        read_dir(dir, snapnum, i, 1, 1)
        #redshift space, third axis
        read_dir(dir, snapnum, i, 1, 2)

    return 0


def read_dir(dir, snapnum, runno, rs, rsdir):
    #runno is used for output
    sn="%03d" % snapnum
    filename=dir+'/snapdir_'+sn+'/snapshot_'+sn+'.'
    #particle index
    pindex=0
    #zero density grid: this is necessary to do before assigning CIC density
    density=N.zeros([ngrid, ngrid, ngrid], dtype=N.float)
    a4=N.int64(density.ctypes.data) #pointer to density grid (for C routine)

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
        dummy = N.fromfile(f, dtype=N.int32, count=23)
        
        pos = N.fromfile(f,N.float32,3*npart)
        pos = N.reshape(pos, [npart, 3])
        pos = pos.astype(N.float) # needed?

        if (rs==0):
            f.close()
            #assign CIC density (ngrid=1024, boxlen=1000Mpc, # particles in files, pointer to position array, pointer to density array)
            retval=d.calcd2(N.int(ngrid), N.int(boxsize), N.int(npart), N.int64(pos.ctypes.data), a4)
        else:
            #redshift space

            dummy = N.fromfile(f,N.int32,2)
            vel = N.fromfile(f,N.float32,3*npart)
            vel = N.reshape(vel, [npart, 3])
            
            vel = vel.astype(N.float)/100*N.sqrt(scalefact)
            pos[:,rsdir]=pos[:,rsdir]+vel[:,rsdir]
            pos[N.where(pos < 0)] += boxsize
            pos[N.where(pos>= boxsize)] -= boxsize

            f.close()

            retval=d.calcd2(N.int(ngrid), N.int(boxsize), N.int(npart), N.int64(pos.ctypes.data), a4)

        pindex+=npart

    print 'finished reading particles'
    z="%1.3f" % redshift
    realization="%03i" % runno
    pos=0 # freeing memory?
    vel=0 # freeing memory?

    density=(density-density.mean())/density.mean()

    if (snapnum == 63): snstr = ''
    else: snstr = 's'+sn
    ngstr = "%i" % ngrid
    
    #correlation function code assumes the first axis is the line of sight, so we have to transpose axes
    if (rsdir==1):
        density=N.transpose(density, (1, 2, 0))
    if (rsdir==2):
        density=N.transpose(density, (2, 0, 1))
    

    #compute correlation function in real or redshift space
    
    if (rs==0):
        print 'calculating density stats'
        #r, cf, numinbin=P.pk(density, boxsize=boxlen, filename='/home/nuala/indra/powspec/real/delta/pk512.'+realization, getnuminbin=True)
        r, cf, numinbin=P.corfunk(density, boxsize=boxsize, filename=outdir+'/real/delta/xi'+ngstr+snstr+'.'+realization, getnuminbin=True)


    else:
        rsstring="%01i" % rsdir
        print 'calculating RS density stats'
        #r, cf, numinbin=P.pk(density, boxsize=boxsize, filename='/home/nuala/indra/powspec/rs/delta/pk512.'+realization, getnuminbin=True)
        #r, cf, numinbin=P.corfunk(density, boxsize=boxsize, filename='/home/nuala/indra/corrfunc/rs/delta/xi512.'+realization, getnuminbin=True)
        cfdelta_2d, rsig, rpi=P.corfunk(density, boxsize=boxsize, pisigma3d=True, get2d=True)
        N.save(outdir+'/rs/delta/xi2d_'+ngstr+snstr+'.'+rsstring+'.'+realization, cfdelta_2d.flatten())

        if (runno==0):
            N.save(outdir+'/rs/rsig'+ngstr+snstr, rsig)
            N.save(outdir+'/rs/rpi'+ngstr+snstr, rpi)
    return 0
        
        
