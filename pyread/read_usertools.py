# ==============================================
# Read.& proc. toolkit for data sets' structure.
# ==============================================
import os, sys
import numpy as N
import matplotlib.pyplot as pl
from read_misctools import MiscTools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc

class UserTools(object):
    """
    User-activated tools that are used in the readProcedures instance.
    """
    def __init__(self):
        # Purely for debugging reasons
        if sys.platform in ("linux", "linux2"):
            self.uname = os.path.expanduser("~")+"/"
            pass
        elif sys.platform in ("win32", "win64"):
            self.uname = os.path.expanduser("~")+"\\"
            pass
        else:
            sys.exit("Error in UserTools' init.")
        """
        End of init
        """

    def box_indexer(self, pos, box_params):
        """
        Extracts slices of data, determined from 3D positions.
        self.box_params = [ [0.,20.],[0.,20.],[0.,5.] ] 
        """
        print "  * "
        xmin, xmax = box_params[0]
        ymin, ymax = box_params[1]
        zmin, zmax = box_params[2]

        " Bool'ed indexation "
        box3D =  N.array( pos[:,0] >= xmin ) \
               * N.array( pos[:,1] >= ymin ) \
               * N.array( pos[:,2] >= zmin ) \
                                             \
               * N.array( pos[:,0] <= xmax ) \
               * N.array( pos[:,1] <= ymax ) \
               * N.array( pos[:,2] <= zmax )

        return box3D


    def sort_from_IDsF(self, IDsA, posA=None, velA=None, focus="what"):
        """
        Sorts IDs, and an accompanying array after sorted IDs.
        focus is meant to be a string object, taking arguments either:
        * "pos"    (- velocity array is returned as None          )
        * "vel"    (- position array is returned as None          )
        * "posvel" (- in case user wants both sorted and returned )
        """
        print "  * Sorting IDs now ..." # ..need this sorted anyway.
        IDsSargA = N.argsort(IDsA)
        IDsA = IDsA[IDsSargA]
        print "    \=> IDs sorted."

        if focus == "pos":
            " Sorts positions "
            
            print "  * Sorting positions."
            posA = posA[IDsSargA]
            print "    \=> positions' array now sorted by ID tag.\n"
            return IDsA, posA, None

        elif focus == "vel":
            " Sorts velocities"
            
            print "  * Sorting velocities."
            velA = velA[IDsSargA]
            print "    \=> velocities' array now sorted by ID tag.\n"
            return IDsA, None, velA

        elif focus == "posvel":
            " Sorts both "

            print "  * Sorting positions."
            posA = posA[IDsSargA]
            print "    \=> positions' array now sorted by ID tag.\n"
            # ------------------------------ #
            print "  * Sorting velocities."
            velA = velA[IDsSargA]
            print "    \=> velocities' array now sorted by ID tag.\n"
            return IDsA, posA, velA

        elif focus == "what":
            " User has not input anything to focus on, will assume positions.. "
            self.sort_from_IDsF(IDsA=IDsA, posA=posA, velA=None, focus="pos")
            return 0

        else:
            sort_of_errortext = " Sorting selector test failed (!?!) "
            pass

        print sort_of_errortext
        return 0


    def plot_pos_scatter(self, IDsA, posA, plotdim=2,
                         plotname="misc_scatplot", plotpath="output_gravipy/"):
        """
        Plots positional data output.
        Example call:
        plot_pos_scatter(IDsA=IDs, posA=pos, plotdim=2,
                         plotname="funcScatterTest", plotpath="output_gravipy/")
        """
        print "  * Initiating {0} scatter plot of positions from simulation data"\
                .format((str(plotdim)+"d"))
        
        fig =  pl.figure()

        " Scatter plot "
        if plotdim == 2:
            " Defaults to 2 dimensions in plot "
            ax  = fig.add_subplot(111, projection='2d') # 2d as default
            ax.scatter(posA[:,0], # x-elements
                       posA[:,1], # y-elements
                            depthshade=True, s=1)
            ax.set_xlabel('x-position Mpc/h')
            ax.set_ylabel('y-position Mpc/h')
            pass

        elif plotdim == 3:
            " In case of 3d "
            ax  = fig.add_subplot(111, projection='3d')
            # in the voice of an authorative Patrick Stewart:
            " ENGAGE 3D VIZUALIZATION "
            ax.scatter(posA[:,0], # x-elements
                       posA[:,1], # y-elements
                       posA[:,2], # z-elements
                            depthshade=True, s=1)
            ax.set_xlabel('x-position Mpc/h')
            ax.set_ylabel('y-position Mpc/h')
            ax.set_zlabel('z-position Mpc/h')
            pass

        else:
            sys.exit(" * Unbelievable error. ")

        plotpath = self.outputPather(plotpath, plotname)
        plotpath = plotname \
                   + "_{0}d".format(plotdim) + ".png"
        print " Saving plot (pos) "
        pl.savefig(plotname, dpi=200)
        pl.close()

        return 0


    #### REWRITE THESE TO BE LESS DEPENDENT ON INSTANCE VARIABLES

    def outputPather(self, fileName, folderPath):
        """
        Checks if output folder structure exists
        & creates output path for output file 
        & filepath- & name based on env. params.
        * Note: based in user's home folder,
                folder structure based on intended task.
        """

        folderPath = folderPath+fileName

        self.fileName = fileName 
        outfilePath = folderPath + fileName

        if not os.path.exists(self.uname + folderPath):
            os.makedirs(self.uname + folderPath)
            print "Creating output folder structure: ", \
                   self.uname + folderPath, "\n"
            pass
        else:
            print "Output folder already exists: ", \
                   self.uname + folderPath, "\n"
            pass

        self.outfilePath = self.uname + outfilePath # This is easier, anyway.

        return self.outfilePath


    def indraPathParser(self, indraN, iA, iB, tmp, cluster):
        """
        If program is supposed to run from 'indraX_tmp' data file structure,
        returns modified filepath for the reader.
        """
        indrapath = "/indra{0:d}{1:s}/{0:d}_{2:d}_{3:d}"
        if self.boolcheck(tmp) == True:
            " Inserts 'tmp' into address line, i.e.: "
            " /indra{iN}{_tmp}/{iN}_{iA}_{iB} "
            indrapath = indrapath.format(
                            self.indraN, "_tmp", self.iA, self.iB )
            pass

        else:
            " /indra{iN}{}/{iN}_{iA}_{iB} "
            print "normal folders acknowledged."
            indrapath = indrapath.format(
                            self.indraN, "", self.iA, self.iB )
            pass

        return indrapath


    # Useful functions below

    def linewriter(self, datalist, w):
        """
        This is a function that will write listed data as needed
        """
        maxlen = len(datalist)

        lineToWrite = ""
        for i in range(len(datalist)):
            lineToWrite += "{0:>20}".format(datalist[i])
            continue

        w.write(lineToWrite)
        return 0


    def funcNameOver(self, where="1up"):
        """
        :return: Name of nested function in which this function is called.
        Useful for debugging.
        """
        ranks = {"inception": 0, "here": 1, "1up": 2, "2up": 3}
        return str(sys._getframe(ranks[where]).f_code.co_name)


    def boolcheck(self, arg):
        """ Don't want random user input cluttering;
        only allows 1 and True as boolean statements from user. """
        return any([arg == 1, arg == True])


    def not_NoneFalse(self, arg):
        """ I need SOME kind of check...
        Returns True when arg's value is true.
        """
        return all([arg != 0, arg != False, arg != None])
        

if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")