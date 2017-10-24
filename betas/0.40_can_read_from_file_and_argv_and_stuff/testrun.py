from read import read_particles
# # Data structure parameters
# what      = "pos"
# indraN    = 2
# iA        = 0
# iB        = 0
# subfolder = 63
# fftfile   = None

# # Options
# sortIDs    = True        #   1/0     <=>     on/off
# lessprint  = True        #   1/0     <=>     on/off
# tmpfolder  = True    # When using ".../indra'X'_tmp/..." data

# # Output forms
# outputpath = False
# w2f        = False    # When wanting file-written output. ....probably a bad idea.
# plotdata   = False    # Most likely wanted output
# # If all of these are 'False', program simply returns data for user to use.
# " Function formulation, still uses original class' structure "
# out = read_particles( data=what,                                \
#                       indraN=indraN,   iA=iA,   iB=iB,          \
#                       foldNum=subfolder,   fftNum=fftfile,      \
#                       sortIDs=sortIDs,     lessprint=lessprint, \
#                       tmpfolder=tmpfolder,                      \
#                       w2f=w2f,             plotdata=plotdata,   \
#                       outputpath=outputpath )

from read import readDo
reading_parameters = {                    
# Data structure parameters
"what"      : [ "pos" ],
"indraN"    : 2,
"iA"        : 0,
"iB"        : 0,
"subfolder" : 63,
"fftfile"   : None,

# Options
"sortIDs"    : True,        #   1/0     <=>     on/off
"lessprint"  : True,        #   1/0     <=>     on/off
"tmpfolder"  : True,        # when using ".../indra'X'_tmp/..." data
# Extracts data from a coordinate box at positions specified:
"box_params" : ( (0.,20.),(0.,20.),(0.,5.) ),   # Turned off w/: None/False
# Apply floats as "((min,max), (min,max), (min,max))" in Mpc/h units,
# respectively for directions x, y, z.

# Output filename
"outputpath" : False,
# Write 2 file: Probably a bad idea...
"w2f"        : False,
# The most likely wanted output:
"plotdata"   : True
} 

# TODO: If all of output parameters are 'False';
# program simply returns data for user to use.
### Easier variant: Create class call (on it!)


" Class function call "
experiment = readDo() # Initializes structure
# IDsA, posA, iterLen, NpartA
IDsA, posA, velA, iterLen, NpartA = experiment( reading_parameters )

velA = None # Not interested in this atm; releasing memory.

" "






