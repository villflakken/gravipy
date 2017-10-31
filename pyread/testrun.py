from read import readDo

data_params = \
    {
        # Data structure parameters:
         "what" :([ "pos" ]),   # or origami...?
       "indraN" :(       2 ),
           "iA" :(       0 ),
           "iB" :(       0 ),
    "subfolder" :(      63 ),   # ...
      "fftfile" :(    None ),   # one of these _may_ be none, not both.
        # Reading options:
    "tmpfolder" :(    True ),        # when using ".../indra'X'_tmp/..." data
      "sortIDs" :(    True ),        #   1/0     <=>     on/off
    "lessprint" :(    True ),        #   1/0     <=>     on/off

        # Extracts data from a coordinate box at positions specified:
    "box_params" :( [ 0.,20. ], [ 0.,20. ], [ 0.,5. ] ), 
        # Apply floats as "([min,max], [min,max], [min,max])" in Mpc/h units,
        # respectively for directions x, y, z. # Turned off w/: None/False
       "plotdim" :(      3 ), # Dimensions projected in plot

        # Write 2 file: Probably a bad idea ...
           "w2f" :(  False ),
      "plotdata" :(   True ),
        # Desired output filepath, 
        # or False (program storing to user's own folder).
    "outputpath" :(  False ),
        # Origami functionality
   "origamipath" :( "filepath")
    }

" The class function call: "
# read_particles = readDo() # Initializes structure
# output = read_particles( data_params )
# IDsA, posA, velA, iterLen, NpartA = output # example

" The simplified function call: "
from read import read_ini
from read_usertools import UserTools as do

IDs, pos, vel = read_ini(
                            what       = ["pos"],
                            indraN     = 2,
                            iA         = 0,
                            iB         = 0,
                            subfolder  = 63,
                            tmpfolder  = True
                        )
IDs, pos, vel = do.sort_from_IDsF(IDsA=IDs, posA=pos, velA=vel, focus="pos")
# \=> Because focus=="pos", then vel==None.
do.plot_pos_scatter(IDsA=IDs, posA=pos, plotname="functionScatterTest", plotdim=2)
# \=> The last argument is optional; will make 2 dimensional plot by default.

