"""
data_params = \
    {
        # Data structure parameters:
         "what" :([ "pos" ]),   # or origami...?
       "indraN" :(       2 ),
           "iA" :(       0 ),
           "iB" :(       0 ),
    "subfolder" :(      63 ),   # ...
      "fftfile" :(   None  ),   # one of these _may_ be none, not both.
        # Reading options:
    "tmpfolder" :(   True  ),        # when using ".../indra'X'_tmp/..." data
      "sortIDs" :(   False ),        #   1/0     <=>     on/off
    "lessprint" :(   True  ),        #   1/0     <=>     on/off

        # Extracts data from a coordinate box at positions specified:
    "box_params" :( [ 0.,20. ], [ 0.,20. ], [ 0.,5. ] ), 
        # Apply floats as "([min,max], [min,max], [min,max])" in Mpc/h units,
        # respectively for directions x, y, z. # Turned off w/: None/False
       "plotdim" :(      3 ), # Dimensions projected in plot

        # Write 2 file: Probably a bad idea ...
           "w2f" :(  False ),
      "plotdata" :(  False ),
        # Desired output filepath, 
        # or False (program storing to user's own folder).
    "outputpath" :(  False ),
        # Origami functionality
   "origamipath" :( "filepath" )
    }
"""
" The class function call: "
# from read import reader
# read_particles = read() # Initializes structure
# output = read_particles( data_params )
# IDsA, posA, velA, iterLen, NpartA = output # example

" The simplified function call: "
from read import read_ini
output = read_ini(
                          what       = ["fof"], # "vel", "fof", etc 
                          indraN     = 2,
                          iA         = 0,
                          iB         = 0,
                          subfolder  = 63,
                          tmpfolder  = True,
                          multiset   = "store"
                        )


"""
from read_usertools import UserTools as do
do = do() # Initialize toolkit

# Lessen amount of data:
box_params = [0.,20.], [0.,20.], [0.,5.] # Note: box parameters is 3x2 iterable.
box3D = do.box_indexer(pos, box_params)  # This is one way to do it..
IDs   = IDs[box3D]
pos   = pos[box3D]

" Alternatively: this boxes pos, + boxes of another array based on pos-box "
# IDs, pos, vel = do.arrboxer(IDs, pos, vel, box_params)

" Below not strictly necessary - may be done from the reading process; but works! "
IDs, pos = do.sort_from_IDsF(IDsA=IDs, posA=pos, velA=None, focus="pos")
    # \=> Because focus=="pos", then vel==None 

do.plot_pos_scatter(IDsA=IDs, posA=pos, box=box_params, plotdim=2, # One in 2D
                    plotname="funcScatterTest", plotpath="output_gravipy/")
do.plot_pos_scatter(IDsA=IDs, posA=pos, box=box_params, plotdim=3, # One in 3D
                    plotname="funcScatterTest", plotpath="output_gravipy/")
    # \=> 'plotdim' argument is optional; will make 2 dimensional plot by default.
"""
