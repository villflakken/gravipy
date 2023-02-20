import sys, os, glob, time
import numpy as N
import subprocess as sp
import pylab as pl

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
rc('font',**{'family':'serif'})
time_init_start = time.time()

# ==============================================
# Read.& proc. toolkit for data sets' structure.
# ==============================================
from read_usertools import UserTools

# ==============================================
# Read.& proc. data sets' visualisation tools.
# ==============================================
from read_plotdoc import Plotter

# ==============================================
# Reading toolkit for data sets' structure.
# ==============================================
from read_misctools import MiscTools

# ==============================================
# File interpreters for read.py's interface.
# ==============================================
from read_sifters import Sifters

# ==============================================
# Reading procedure for data sets' structure.
# ==============================================
from read_procedures import readProcedures

# ==============================================
# Argument interpreter for read.py's interface.
# ==============================================
from read_args import readArgs

# ==============================================
# Indra data sets' reading MO.
# ==============================================
from read import gravipy

time_init_end = time.time()

print "Initialization time: {0:.2f} seconds".format((time_init_end - time_init_start))