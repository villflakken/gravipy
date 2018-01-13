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

        " Just prints wether or not plotting is involved: "
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
            # Plotting without boxing will take 26hours per plot.
            print " Box for the cut-out:", self.box_params
            box3D = self.box_indexer(pos, self.box_params)
            IDs = IDsA[box3D]
            pos = posA[box3D]
            pass

        if self.boolcheck(self.oriDo):
            tags = self.read_origami()[1]
            tags = tags[IDs]

        if self.boolcheck(self.plotdata):
            " Engage plotting! "
            self.auto_plot_pos_scatter(IDs, pos)
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


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")