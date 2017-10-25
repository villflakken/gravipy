# ==============================================
# Read.& proc. toolkit for data sets' structure.
# ==============================================
import os, sys, glob, textwrap, platform
import numpy as N
import subprocess as sp
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

class readUserTools(object):
    """
    User-activated tools that are used in the readProcedures instance.
    """
    def __init__(self):
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
    

    def sort_posvel_func(self, iterLen, maxN, NpartA, \
                               posA, velA, IDsA ):
        """
        Function for sorting stuff.
        * Find longest list of IDs, just in case IDs may disappear
        with time and structure development.
        * Sort IDs from every step.
        """
        # Prepare variables and arrays for sorting
        posMat   = N.zeros( (iterLen, maxN, 3),
                          dtype=N.float32 )
        velMat   = N.zeros( (iterLen, maxN, 3), 
                          dtype=N.float32 )
        IDsS     = N.zeros( ( iterLen, maxN ),
                          dtype=N.int64 )

        for i in N.arange(0, iterLen):
            """
            * Stores numbers of groups in each iteration of the simulation
            * Sorts & stores the IDs
            * Stores positions from sorted indexation
            """
            itertext = " * Assigning sorted values, {0:>3d}/{1} ..."\
                        .format(i, (iterLen-1))
            " Less spam in the terminal "
            self.itertextPrinter(itertext, i, iterLen, 10)

            # Creating array set of sorted indices
            # IDsSarg[   i , :NpartA[i] ] = \
            #     N.argsort( IDsA[ i , :NpartA[i] ])
            # - No need to store the arguments of the sorted indices
            IDsSarg = N.argsort( IDsA[ i , :NpartA[i] ])
            
            # Storing sorted IDs
            IDsS[ i , :NpartA[i] ] = \
                IDsA[ i, IDsSarg ]

            # Sorting positions after IDs
            posMat[ i , :NpartA[i] , : ] = \
                posA[ i, IDsSarg , :] # Shapes.. should match?

            # Sorting velocities after IDs
            velMat[ i , :NpartA[i] , : ] = \
                velA[ i, IDsSarg , :] # Shapes.. should match?

            continue

        return posMat, velMat, IDsS


    def sort_IDs(self, iterLen, maxN, NpartA, IDsA ):
        """
        Function for sorting stuff.
        * Find longest list of IDs, just in case IDs may disappear
        with time and structure development.
        * Sort IDs from every step.
        ***:Naming convention examples: 
            IDsA     = IDs Array
            IDsSargA = IDs Sorted args Array
        """
        # Prepare array variables to memory for sorting
        IDsS     = N.zeros( ( iterLen, maxN ),
                          dtype=N.int64 )
        IDsSargA  = N.zeros( ( iterLen, maxN ),
                          dtype=N.int64 )

        for i in N.arange(0, iterLen):
            """
            * Stores numbers of groups in each iteration of the simulation
            * Sorts & stores the IDs
            * Stores positions from sorted indexation
            """
            itertext = " * Sorting IDs, {0:>3d}/{1} ..."\
                        .format(i, (iterLen-1))
            " Less spam in the terminal "
            self.itertextPrinter(itertext, i, iterLen, 10)
            
            IDsSarg = N.argsort( IDsA[ i, :NpartA[i] ])
            IDsSargA[ i, :NpartA[i] ] = IDsSarg
            
            # Storing sorted IDs
            IDsS[ i, :NpartA[i] ] = IDsA[ i, IDsSarg ]
            continue

        return IDsS, IDsSargA


    def sort_dataByIDs(self, iterLen, maxN, NpartA, \
                               inMat, IDsSargA ):
        """
        Function for sorting stuff.
        * Find longest list of IDs, just in case IDs may disappear
        with time and structure development.
        * Sort IDs from every step.
        """
        # Prepare variables and arrays for sorting
        utMat    = N.zeros( (iterLen, maxN, 3),
                          dtype=N.float32 )

        for i in N.arange(0, iterLen):
            """
            * Stores numbers of groups in each iteration of the simulation
            * Sorts & stores the IDs
            * Stores positions from sorted indexation
            """
            itertext = " * Sorting {0:>8s} values, {1:>3d}/{2} ..."\
                        .format(self.what, i, (iterLen-1))
            " Less spam in the terminal "
            self.itertextPrinter(itertext, i, iterLen, 10)


            utMat[ i , :NpartA[i] , : ] = \
                inMat[ i, IDsSargA[i,:NpartA[i]], :] # Shapes.. should match?
            continue

        return utMat


    def plot_pos(self, IDsA, posA, iterLen, NpartA):
        """
        Plots positional data output.
        """
        totalNtot = 1024**3 # Total number of elements
        # Try a scatterplot first
        print "\tInitiating scatter plot of positions in simulation: \
            {0}_{1}_{2}/snapshot_{3}".format(
            self.indraN, self.iA, self.iB, self.subfolder)
        
        fig =  pl.figure()

        if self.plotdim_set == 2 or self.plotdim_set == None:
            " Defaults to 2 dimensions in plot "
            ax  = fig.add_subplot(111, projection='2d') # 2d as default
        if self.plotdim_set == 3:
            " In case of 3d "
            ax  = fig.add_subplot(111, projection='3d')

        for i in N.arange(0, iterLen):
            """ Runs through ".i" ; i is int \in 
            * [0, 256) for [ posvel, fof, subhalo ]
            * [0, 505) for [ fft                  ]
            """            
            iterNtot         = N.sum(NpartA[:i+1])
            percent_complete = 100.*iterNtot/totalNtot

            itertext = " Snapshot #{0:<3d} | No. of new plot elements {1:6d} -"\
                                .format(i, NpartA[i])\
                + " [Total: {0:>10d}/{1:g} ( {2:>3d}% ) ]".format(
                                      iterNtot, totalNtot,
                                      int(percent_complete) )
            self.itertextPrinter(itertext, i, iterLen, 10)
            
            " Scatter plot "
            if self.plotdim_set == 2: # 2D
                ax.scatter(posA[i,:NpartA[i],0], # x-elements
                           posA[i,:NpartA[i],1], # y-elements
                                depthshade=True, s=1)

            if self.plotdim_set == 3: # 3D
                ax.scatter(posA[i,:NpartA[i],0], # x-elements
                           posA[i,:NpartA[i],1], # y-elements
                           posA[i,:NpartA[i],2], # z-elements
                                depthshade=True, s=1)
            continue

        ax.set_xlabel('x-position Mpc/h')
        ax.set_ylabel('y-position Mpc/h')
        if self.plotdim_set == 3:
            ax.set_zlabel('z-position Mpc/h')
        plotname = self.outputPather(self.subfolder)+".png"
        print "Saving plot"
        pl.savefig(plotname+"_{0}d".format(self.box_params_set), dpi=200)
        pl.close()

        return 0


    def plot_vel(self, IDsA, velA, iterLen):
        """
        Plots velocitiy data output.
        """

        return 0


    def plot_fof(self, fof_dat, iterLen):
        """
        Plots friends of friends data output.
        """

        return 0


    def plot_subhalo(self, sub_dat, iterLen):
        """
        Plots subhalo data output.
        """

        return 0


    def plot_fft(self, fft_dat, iterLen):
        """
        Plots FFT data output.
        """

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


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")