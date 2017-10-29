# ==============================================
# Read.& proc. toolkit for data sets' structure.
# ==============================================
import os, sys, glob, textwrap, platform
import numpy as N
import subprocess as sp
import matplotlib.pyplot as pl
from read_misctools import readMiscTools
from mpl_toolkits.mplot3d import Axes3D

class userTools(readMiscTools):
    """
    User-activated tools that are used in the readProcedures instance.
    """
    def __init__(self):
        readMiscTools.__init__(self)

        self.mult_miss_error = \
            """
            File(s) are missing.
            Maybe the dataset should be properly completed first?
            Aborting!
            =========
            """
        self.printNth = 5
        if sys.platform in ("linux", "linux2"):
            self.uname = os.path.expanduser("~")+"/"
        elif sys.platform in ("win32", "win64"):
            self.uname = os.path.expanduser("~")+"\\"
            # Purely for debugging reasons

        self.plot_funcs = \
            {
                "pos"       : self.plot_pos     , 
                "vel"       : self.plot_vel     , 
                "fof"       : self.plot_fof     , 
                "subhalo"   : self.plot_subhalo , 
                "fft"       : self.plot_fft
            }    
        """
        End of init
        """

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
        

    def box_indexation(self, pos, box_params):
        """
        Extracts slices of data, determined from 3D positions.
        self.box_params = [ [0.,20.],[0.,20.],[0.,5.] ] 
        """
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

#### REWRITE THESE TO BE LESS DEPENDENT ON INSTANCE VARIABLES

    def plot_pos(self, IDsA, posA):
        """
        Plots positional data output.
        """
        totalNtot = 1024**3 # Total number of elements
        # Try a scatterplot first
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
            # in the voice of an authorative Patrick Stewart:
            " ENGAGE 3D VIZUALIZATION "
            ax.scatter(posA[:,0], # x-elements
                       posA[:,1], # y-elements
                       posA[:,2], # z-elements
                            depthshade=True, s=1)
            pass
        else:
            sys.exit(" * Unbelievable error. ")

        ax.set_xlabel('x-position Mpc/h')
        ax.set_ylabel('y-position Mpc/h')
        if self.plotdim_set == 3:
            ax.set_zlabel('z-position Mpc/h')
            pass

        plotname = self.outputPather(self.subfolder)\
                   + "_{0}d".format(self.plotdim_set) + ".png"
        print " Saving plot (pos) "
        pl.savefig(plotname, dpi=200)
        pl.close()

        return 0


    def outputPather(self, num):
        """
        Checks if output folder structure exists
        & creates output path for output file 
        & filepath- & name based on env. params.
        * Note: based in user's home folder,
                folder structure based on intended task.
        """
        self.outfilePath = None

        if bool(self.outputpath) == True:
            " User input specified data output path "
            folderPath = self.outputpath
            pass
        else:
            folderPath = "output_gravipy/{0}_i{1}{2}{3}{4}_sf{5}/"
            pass

        fileName = "{0}_i{1}{2}{3}{4}_sf{5}"
        if self.what == "posvel":
            pass
        else:
            pass

        if self.boolcheck(self.tmpfolder) == True:
            " When 'indraX_tmp' data is processed "
            folderPath = folderPath.format( 
                            self.what, self.indraN, self.iA, self.iB, "tmp", num )
            fileName   = fileName.format(   
                            self.what, self.indraN, self.iA, self.iB, "tmp", num )
            # Examples   : \
            " folderpath : 'output_gravipy/{0}_i{1}{2}{3}{tmp}_sf{5}/' "
            " filename   :                '{0}_i{1}{2}{3}{tmp}_sf{5}'  "
            pass
        else:
            " When normal data structures are processed "
            folderPath = folderPath.format( 
                            self.what, self.indraN, self.iA, self.iB, "", num )
            fileName   = fileName.format(   
                            self.what, self.indraN, self.iA, self.iB, "", num )
            # Examples   : \
            " folderpath : 'output_gravipy/{0}_i{1}{2}{3}{None}_sf{5}/' "
            " filename   :                '{0}_i{1}{2}{3}{None}_sf{5}'  "
            pass
        
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

        self.outfilePath = self.uname + outfilePath # this is easier, anyway.

        return self.outfilePath


    def itertextPrinter(self, itertext, i, iterLen, modifier):
        " Less spam in terminal window "
        if self.boolcheck(self.lessprint) == False:
            # No output reduction:
            print itertext
            pass
        else:
            # Output reduction:
            if i % (self.printNth*modifier) == 0:
                print itertext
                pass
            elif i == (iterLen-1):
                print itertext
                pass
            else:
                # When no progress is printed as output.
                pass
            pass
        return 0

    def indraPathParser(self):
        """
        If program is supposed to run from 'indraX_tmp' data file structure,
        returns modified filepath for the reader.
        """
        indrapath = "/indra{0:d}{1:s}/{0:d}_{2:d}_{3:d}"
        if self.boolcheck(self.tmpfolder) == True:
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


    def itertextPrinter(self, itertext, i, iterLen, modifier):
        " Less spam in terminal window "
        if self.boolcheck(self.lessprint) == False:
            # No output reduction:
            print itertext
            pass
        else:
            # Output reduction:
            if i % (self.printNth*modifier) == 0:
                print itertext
                pass
            elif i == (iterLen-1):
                print itertext
                pass
            else:
                # When no progress is printed as output.
                pass
            pass
        return 0


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")