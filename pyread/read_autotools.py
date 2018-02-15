# ==============================================
# Read.& proc. toolkit for data sets' structure.
# ==============================================
import os, sys
import numpy as N
import matplotlib.pyplot as pl
from read_usertools import UserTools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
rc('font',**{'family':'serif'})

class AutoTools(object):
    """
    Tools that function when used in the readProcedures instance's automatic mode.
    """
    def __init__(self):
        """
        End of init
        """


    def pp_selector(self, parsed_data, num):
        """
          * Accessed when class system is given a set of parameters;
            in order to automatically post-process a predetermined,
            greater sequence of data.
        Selects a post process method depending on
        which task procedure is currently in the environment.
        ### Unfinished !!! (But its principle seems to work)
        """
        self.pp_action = \
            { # Function library for post processing
                "pos"     : self.pp_pos     , 
                "vel"     : self.pp_vel     , 
                "fof"     : self.pp_fof     , 
                "subhalo" : self.pp_subhalo ,
                "fft"     : self.pp_fft     ,
                "origami" : self.pp_origami
            }

        " Just prints whether or not plotting is involved: "
        if self.boolcheck(self.plotdata) == True:
            " Plot or not? Is it heinous? Is it hot? "
            # self.plottingEngagedText = """
            # Engaging plot method for the {0} data retriever.
            # Plot location and name: ' {1} '"""
            # self.plottingEngagedText.format(self.what, self.outfilePath+".png")
            pass


        self.pp_action[self.what](parsed_data, num) # Ah, so elegant!

        return 0


    def pp_pos(self, parsed_data, num):
        """
        Positions post-processing function. 
        """
        IDs, pos, scalefactor, rs = parsed_data

        if hasattr(self.box_params, '__iter__') == True:
            " Apply box parameters to the positions "
            # Plotting without boxing will take 26hours per plot.
            print " Box for the cut-out:", self.box_params, "Mpc/k"
            box3D = self.box_indexer(pos, self.box_params)
            IDs = IDs[box3D]
            pos = pos[box3D]
            pass

        if self.origamipath != False:
            " User wants ORIGAMI data available for further PP. "
            tags = self.read_origami()[1]
            tags = tags[IDs]

        if self.boolcheck(self.plotdata):
            " Engage plotting! "
            self.plot_pos_oritag(pos, tags)
            pass

        return 0



    def pp_vel(self, IDsA, velA):
        """
        Post processing of velocitiy data output.
        """

        return 0


    def pp_fof(self, fof_dat):
        """
        Post processing of friends of friends data output.
        """
        

        return 0


    def pp_subhalo(self, sub_dat):
        """
        Post processing of subhalo data output.
        """

        return 0


    def pp_fft(self, fft_dat):
        """
        Post processing of FFT data output.
        """

        return 0


    def pp_origami(self, origami_dat):
        """
        Post processing template for ORIGAMI's output.
        """

        return 0


    def sketch_of_storager(self, parsed_data, num):
        """
        # Sketching code with 2 algorithms,
        # which should be equivalent.

        Stores the data into some kind of logical structure
        (? - feedback needed)

        ### Current proposal:
        3-leveled/indexed nested dictionary structure, shown below
        
        output_dataset  # -> variable stored to outside (of this) script
            |
            |--> ["{task/data category}"]
                          |
                          |--> ["{iN}{iA}{iB}"]
                                      |
                                      |--> ["{snapshotnumber}"]
                                                    |
                                                    |--> parsed_data
        - where 'parsed_data' as a variable contains
        several items from the reading of a snapshot's data
        (pertaining to the data type/category/"task").
        """
        # self.datadict = {}      # Declared outside of this scope!
        task =     self.what    # -- --> Outermost dictionary key 
                                  #              (already string).
        iN   = str(self.indraN) # -- --> Together, these 3 form the middle key
        iA   = str(self.iA)       # --^
        iB   = str(self.iB)       # -^
        num  = num              # -- --> Innermost key.

        indra = "{0:1d}{1:1d}{2:1d}".format(iN, iA, iB)

        if task not in self.datadict.keys():
            
            " Declaration of task-name-key "
            # self.datadict.update() #?
            self.datadict[task] = {indra : {num : parsed_data}}
            pass

        else:

            " Case: dict already has the task-name-key "
            if indra not in self.datadict[task].keys():
                
                " Declaration of indra-key "
                self.datadict[task][indra] = {num : parsed_data}
                pass

            else:

                " Case: dict already has indra-key "
                self.datadict[task][indra][num] = parsed_data 
                pass # Out of 2nd if-test's else-block

            pass # Out of 1st if-test's else-block, back to function

        #### ALTERNATIVELY, bools rendered the other way around 
        #### (not finished)

        if task in self.datadict.keys():
            
            " Case: dict already has the task-name-key "
            if indra in self.datadict[task].keys():

                " Case: dict already has indra-key "
                self.datadict[task][indra][num] = parsed_data
                pass # Out of 2nd if's IF block

            else: # 'indra' _not_ in datadict['task'] 

                " Case: First entry of current indra-key "
                self.datadict[task][indra] = {num : parsed_data}
                pass # Out of 2nd if's ELSE block

            pass # Out of 1st if's IF block

        else:

            " Case: First entry of current task-name-key "
            self.datadict[task] = {indra : {num : parsed_data}}
            pass # Out of 1st if's ELSE block

        return 0

if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")