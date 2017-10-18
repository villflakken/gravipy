from read import readDo

data_params = \
    {
        # Data structure parameters
         "what" :([ "pos" ]),
       "indraN" :(       2 ),
           "iA" :(       0 ),
           "iB" :(       0 ),
    "subfolder" :(      63 ),   # ...
      "fftfile" :(    None ),   # one of these _may_ be none, not both.
        # Options
      "sortIDs" :(    True ),        #   1/0     <=>     on/off
    "lessprint" :(    True ),        #   1/0     <=>     on/off
    "tmpfolder" :(    True ),        # when using ".../indra'X'_tmp/..." data

        # Extracts data from a coordinate box at positions specified:
    "box_params" :( [ 0.,20. ], [ 0.,20. ], [ 0.,5. ] ), 
        # Apply floats as "([min,max], [min,max], [min,max])" in Mpc/h units,
        # respectively for directions x, y, z. # Turned off w/: None/False
        "plotdim":(      2 ), # Dimensions projected in plot

        # Write 2 file: Probably a bad idea ...
           "w2f" :(  False ),
      "plotdata" :(   True ),
        # Desired output filepath, 
        # or False (program storing to user's own folder).
    "outputpath" :(  False )
    }

" The class function call "
read_particles = readDo() # Initializes structure
output = read_particles( data_params )
# IDsA, posA, velA, iterLen, NpartA = output



# =============================== Old function call
# from read import read_particles
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
