
- - - - - - - - - - - - - - - ## SIFTER COMMENTS ##
*Specific comments on the Sifters*

-- If things would be much easier in python 2.7, I think that elephant6 has python 2.7.5, so feel free to use only that. --SIGH

-- The data from each file (all 256 of them) should be saved to larger arrays. (I'm aware the indra_corfunc.py code didn't do this, so that might not have been clear!)

-- pos and vel shouldn't be upgraded to float64

-- Make sure to continue reading the ids after pos and vel.

-- Add an option to sort the positions and arrays by the ids, so that 'pos[0,:]' is the position of the particle with ID = 0, etc. The IDL code 'read_indra_snap.pro' should contain an example of this. The sorting should happen to the large array, after all the files have been read.

-- Remove the 'redshift' option completely - we can leave that up to the user
    -- NotPri

- We can discuss more after I've taken a closer look at 'read_sub.pro', but the subhalo files contain a lot of variables to be read (3 different types of halo mass and halo radius, position and velocity of halo, velocity dispersion, etc.). I would probably group all of these into a structure in IDL, to avoid listing all these variables in the function call, and there should be something similar (or better) in python. In 'read_sub.pro' I only returned what I wanted, but for this general reader I think we should return everything.

-- Your question about why 'Nsubs' could be 0 is correct - in a specific file, especially early on, there might not be any subhalos in that file.
        -- THIS was actually a comment from your own code that I just kept lying there after initial Copy-Paste-phase

- For FOF and subhalo data, we don't know ahead of time how many halos there are, unlike the particle data. 
    + But we can read this information from the first file, 'TotNgroups', and then use this to define the size of the arrays before looping through and reading all the files. The number of files can also be read, 'NTask'.





- - - - - - - - - #### OVERALL COMMENTS ####

- My main comment is that I would like the code to work via functions instead of the command line. 
    + This means a user would import your code and call a function defined in your code. For example, something like 'pos, vel, ids = read_particles(options...)', 
    + The options would indicate e.g. 
        \ Which Indra dataset to read (0_2_4, 1_4_3, etc.), which snapshot to read (0 to 63), 
        \ Whether to sort the positions and velocities according to the ids, etc. 

This function could also have options to:
    + Only read positions or only read positions and velocities. 

There would also be functions to:
    + Read the FOF groups, the subhalos, and the FFT data; 
        \ Options for FOF and subhalos would include whether to read the group IDs.

I will attach the Jupyter notebook I showed you that loops through the files to read all the positions, velocities, and ids, but note that this notebook runs on the SciServer data so the filenames are different.

- There is some flexibility as to how many reading functions to define and what options they will have, which we can discuss once we have the basics. 
Let's first assume we want to read everything from a given simulation and a given snapshot (0 to 63, or 0 to 504 for the FFT data).








- This is the notebook that reads all particle data (for a given simulation and snapshot), and all FFT data (for a given time step).

{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "import numpy as N\n",
    "import pylab as M, matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "numsnaps=64\n",
    "numfiles=256\n",
    "nparticles=1024\n",
    "boxsize=1000."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "datadir = '/home/idies/workspace/indra/2_0_0/'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Read all particles in a snapshot (skip for FFT stuff)\n",
    "snapnum = 63\n",
    "sn = \"%03d\" % snapnum\n",
    "filename = datadir+'/snapdir_'+sn+'/snapshot_'+sn+'.'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "finished reading particles\n"
     ]
    }
   ],
   "source": [
    "pos = N.empty((nparticles**3,3),N.float32)\n",
    "vel = N.empty((nparticles**3,3),N.float32)\n",
    "ids = N.empty((nparticles**3),N.int64)\n",
    "istart = 0\n",
    "for i in N.arange(0, numfiles):\n",
    "    file=filename+str(i)\n",
    "    f=open(file, 'rb')\n",
    "    \n",
    "    header_size = N.fromfile(f,N.int32,1)[0] # = 256: error catch here?\n",
    "    numpart = N.fromfile(f,N.int32,6)\n",
    "    npart = numpart[1] # number of particles in this file\n",
    "    mass = N.fromfile(f,N.float64,6)\n",
    "    pmass = mass[1] # in units of 10^10 solar masses?\n",
    "    scalefact,redshift = N.fromfile(f,N.float64,2)\n",
    "    flag_sfr,flag_feedback = N.fromfile(f,N.int32,2)\n",
    "    numpart_tot = N.fromfile(f,N.int32,6)\n",
    "    ntotal = numpart_tot[1]\n",
    "    flag_cooling,num_files = N.fromfile(f,N.int32,2)\n",
    "    boxsize,omega0,omegal,hubble = N.fromfile(f,N.float64,4)\n",
    "    flag_stellarage,flag_metals,hashtabsize = N.fromfile(f,N.int32,3)\n",
    "    # read rest of header_size + 2 dummy integers:\n",
    "    dummy = N.fromfile(f,N.int32,23)\n",
    "    \n",
    "    thispos = N.fromfile(f,N.float32,3*npart)\n",
    "    thispos = N.reshape(thispos, [npart, 3])\n",
    "#    thispos = thispos.astype(N.float) # needed?\n",
    "    \n",
    "    # read velocities\n",
    "    dummy = N.fromfile(f,N.int32,2)\n",
    "    thisvel = N.fromfile(f,N.float32,3*npart)\n",
    "    thisvel = N.reshape(thisvel, [npart, 3])\n",
    "\n",
    "    # read IDs\n",
    "    dummy = N.fromfile(f,N.int32,2)\n",
    "    thisID = N.fromfile(f,N.int64,npart)\n",
    "    \n",
    "    f.close()\n",
    "    \n",
    "    pos[istart:(istart+npart),:] = thispos\n",
    "    vel[istart:(istart+npart),:] = thisvel\n",
    "    ids[istart:(istart+npart)] = thisID\n",
    "    \n",
    "    istart = istart + npart\n",
    "\n",
    "print 'finished reading particles'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0.0 1000.0 -5170.02 5400.91 1073741824\n"
     ]
    }
   ],
   "source": [
    "print N.min(pos),N.max(pos), N.min(vel), N.max(vel),N.max(ids)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# START AGAIN HERE for FFT stuff\n",
    "L = 128\n",
    "L2 = L/2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "def get_ps(tnum):\n",
    "    # Read FFT data in given time slice (0 to 504)\n",
    "    tstr = \"%03d\" % i\n",
    "    filename = datadir+'FFT_DATA/FFT_128_%s.dat' % tstr\n",
    "\n",
    "    f = open(filename,'rb')\n",
    "    time = N.fromfile(f,N.float64,1)\n",
    "    nsize = N.fromfile(f,N.int32,1)\n",
    "    fft_re = N.fromfile(f,N.float32,nsize)\n",
    "    fft_im = N.fromfile(f,N.float32,nsize)\n",
    "    f.close()\n",
    "    \n",
    "    fft_re = N.reshape(fft_re,[L+1,L+1,L2+1])\n",
    "    fft_im = N.reshape(fft_im,[L+1,L+1,L2+1])\n",
    "#    print 'a = %f' % time[0]\n",
    "    \n",
    "    # define k's that correspond to fourier modes: (2*math.pi/boxsize)*N.array(x,y,z)\n",
    "    # x = [-L/2:L/2], y = [-L/2,L/2], z = [0,L/2]\n",
    "    # compute k^2 = kx^2 + ky^2 + kz^2, PS = fft_re^2+fft_im^2\n",
    "    kx = N.atleast_3d(N.expand_dims(N.arange(-L2,L2+1),axis=1))\n",
    "    ky = N.atleast_3d(N.expand_dims(N.arange(-L2,L2+1),axis=0))\n",
    "    kz = N.expand_dims(N.expand_dims(N.arange(0,L2+1),axis=0),axis=0)\n",
    "    kx = N.broadcast_to(kx,(L+1,L+1,L2+1))\n",
    "    ky = N.broadcast_to(ky,(L+1,L+1,L2+1))\n",
    "    kz = N.broadcast_to(kz,(L+1,L+1,L2+1))\n",
    "    k = N.sqrt(kx*kx+ky*ky+kz*kz)*N.pi*2/boxsize\n",
    "    ps = fft_re*fft_re+fft_im*fft_im\n",
    "    ps = ps[k>0]\n",
    "    k = k[k>0]\n",
    "    \n",
    "    # average PS in logarithmic bins of k\n",
    "    nbins = 100\n",
    "    ps1d, kbin = N.histogram(N.log10(k),nbins,weights=ps)\n",
    "    counts = N.histogram(N.log10(k),nbins)[0]\n",
    "    ps1d = ps1d[counts>0]/counts[counts>0] # normalization? boxsize^3/128^6??\n",
    "    binvals = kbin[0:nbins]+N.diff(kbin)/2\n",
    "    binvals = binvals[counts>0]\n",
    "   # binvals = 10**binvals\n",
    "    return binvals,ps1d,time[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "kth,pth = N.loadtxt('/home/idies/workspace/persistent/pk_indra7313_CAMB.txt',unpack=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.text.Text at 0x7fcec8eb0e10>"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<matplotlib.figure.Figure at 0x7fcec90eaed0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#plt.plot(kth,pth)\n",
    "plin = N.interp(10**bins,kth,pth)\n",
    "\n",
    "for i in N.arange(0,501,100):\n",
    "    bins,ps,a = get_ps(i)\n",
    "#    plt.plot(10**bins,ps*boxsize**3/L**6) # normalization?\n",
    "    # plot ratio wrt linear power spectrum:\n",
    "    plt.plot(10**bins,(ps/plin)/(ps[0]/plin[0]),label=str(a)) \n",
    "plt.xscale('log')\n",
    "#plt.yscale('log') # don't do if plotting ratio\n",
    "plt.legend(loc='upper left')\n",
    "#M.xlim([N.min(10**bins),N.max(10**bins)])\n",
    "plt.xlabel(r'$k$ (h/Mpc)')\n",
    "plt.ylabel(r'$P(a,k)/P_{lin}(k)$')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}