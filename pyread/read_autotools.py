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

        self.pp_action[self.what](parsed_data) # Ah, so elegant...

        return 0


    def pp_pos(self, parsed_data):
        """
        Positions post-processing function. 
        """
        IDsA, posA = parsed_data

        if hasattr(self.box_params, '__iter__') == True:
            box = self.box_indexer(posA, self.box_params)
            IDsA = IDsA[box]
            posA = posA[box]
            pass

        if self.boolcheck(self.plotdata):
            " Engage plotting! "
            self.auto_plot_pos_scatter(IDsA, posA)
            pass

        # if otherstuff:
        #     self.dothat()
        #     pass

        return 0


    def auto_plot_pos_scatter(self, IDsA, posA):
        """
        Plots positional data output.
        """
        print " * Initiating scatter plot of positions in simulation: \
            {0}_{1}_{2}/snapshot_{3}".format(
            self.indraN, self.iA, self.iB, self.subfolder)
        
        fig =  pl.figure()

        if self.plotdim_set == 2 or self.plotdim_set == None:
            " Defaults to 2 dimensions in plot "
            ax  = fig.add_subplot(111, projection='2d') # 2d as default
        if self.plotdim_set == 3:
            " In case of 3d "
            ax  = fig.add_subplot(111, projection='3d')


            " Scatter plot "
        if self.plotdim_set == 2: # 2D
            ax.scatter(posA[:,0], # x-elements
                       posA[:,1], # y-elements
                            depthshade=True, s=1)
            pass

        elif self.plotdim_set == 3: # 3D
            # ..in the voice of an authorative Patrick Stewart..:
            " ENGAGE 3D VIZUALIZATION "
            ax.scatter(posA[:,0], # x-elements
                       posA[:,1], # y-elements
                       posA[:,2], # z-elements
                            depthshade=True, s=1)
            # 2 lines below are supposed to fix aspect ratio:
            scaling = N.array([getattr(ax, 'get_{}lim'.format(dim))() \
                              for dim in 'xyz'])
            ax.auto_scale_xyz(*[[N.min(scaling), N.max(scaling)]]*3)
            # cudos to sebix @ stackoverflow!
            pass
        else:
            sys.exit(" * Unbelievable error. ")

        ax.set_xlabel('x-position Mpc/h')
        ax.set_ylabel('y-position Mpc/h')
        if self.plotdim_set == 3:
            ax.set_zlabel('z-position Mpc/h')
            pass

        plotname = self.auto_outputPather(self.subfolder)\
                   + "_{0}d".format(self.plotdim_set) + ".png"
        print " Saving plot (pos) to path :", plotname
        pl.savefig(plotname, dpi=200)
        pl.close()

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