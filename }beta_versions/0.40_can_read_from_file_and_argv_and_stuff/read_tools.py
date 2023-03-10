# ==============================================
# Reading toolkit for data sets' structure.
# ==============================================
import os, sys, glob, textwrap
import numpy as N
import subprocess as sp
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D


class readTools(object):
    """
    Miscellaneous tools that are used in the readProcedures instance.
    """

    def __init__(self):
        self.mult_miss_error = \
            """
            File(s) are missing.
            Maybe the dataset should be properly completed first?
            Aborting!
            =========
            """


    def pp_selector(self, parsed_data, num):
        """
        Selects a post process method depending on
        which task procedure is currently in the environment.
        """
        self.outputPather(num)
        # print self.funcNameOver(where="1up")
        # sys.exit()

        " Just prints wether or not plotting is involved"
        if self.boolcheck(self.plotdata) == True:
            " Plot or not? Is it heinous? Is it hot? "
            self.plottingEngagedText = """
            Engaging plot method for the {0} data retriever.
            Plot location and name: ' {1} '"""
            pass

        " ===> What to do at all?: "
        if self.what == "posvel":
            # IDsA, posA, velA, iterLen, NpartA = parsed_data
            # Now, do stuff with the data
            # if self.boolcheck(self.plotdata) == True:
            #     self.plot_pos(IDsA, posA, iterLen, NpartA)
            #     self.plot_vel(IDsA, velA, iterLen, NpartA)
            #     pass
            # And do more stuff, still!
            
            # Time to make use of recursion!
            self.what = "pos"
            self.pp_selector(parsed_data, num)

            self.what = "vel"
            self.pp_selector(parsed_data, num)

            self.what = "posvel" 
            " Resetting in case we'll do some more stuff "
            pass

        elif self.what == "pos":
            # 
            IDsA, posA, velA, iterLen, NpartA = parsed_data
            if self.boolcheck(self.plotdata) == True:
                # 
                self.plottingEngagedText\
                    .format(self.what, self.outfilePath+".png")
                self.plot_pos(IDsA, posA, iterLen, NpartA)
                pass
            pass

        elif self.what == "vel":
            # 
            IDsA, posA, velA, iterLen, NpartA = parsed_data
            if self.boolcheck(self.plotdata) == True:
                # 
                self.plot_vel(IDsA, velA, iterLen, NpartA)
                pass
            pass

            # Finish writing the following:
        elif self.what == "fof":
            if self.boolcheck(self.plotdata) == True:
                self.plot_fof("fof input")
                pass
            pass

        elif self.what == "subhalo":
            if self.boolcheck(self.plotdata) == True:
                self.plot_subhalo("subhalo input")
                pass
            pass

        elif self.what == "fft":
            if self.boolcheck(self.plotdata) == True:
                self.plot_fft("fft input")
                pass
            pass


        else:
            print " No plotting asked for in the parameters. "
            pass # "No camels!", said Indy.

        # " Maybe engage plot like this? "
        # if self.boolcheck(self.plotdata) == True:
        #     self.plot_funcs[self.what]

        return 0


    def list_to_arrays(self, inlist, NpartA, dimensions, datatype, name):
        """
        Converts input list into an array. Example call:

        IDsA = self.list_to_arrays(IDsL, (iterLen, maxN   ), N.int64  , "IDs")
        """
        names     = {"IDs":"ID tag", "pos":"position", "vel":"velocity"}
        itername = names[name]
        iterLen   = dimensions[0]
        #: All insignificant vars in loop are now local

        outarr = N.zeros( dimensions, datatype)
        for i in N.arange(0, iterLen):
            " Put them into the right places, independent of sorting "            
            itertext = \
            "\tAssigning (unsorted) {0:>9s} values to array"\
                +" - Set ({1:>3d} / {2}) ..."\
                .format(itername, i, (iterLen-1))
            " Less spam in the terminal "
            self.itertextPrinter(itertext, i, iterLen, 20)
            outarr[ i, :NpartA[i] ] = inlist[i][:]
            continue
        print
        return outarr


    def boxer(self, pos, vel):
        """
        Extracts slices of data, determined from 3D positions.
        self.box_params = [ [0.,20.],[0.,20.],[0.,5.] ] 
        """
        xmin, xmax = self.box_params[0]
        ymin, ymax = self.box_params[1]
        zmin, zmax = self.box_params[2]

        box3D =  N.array( pos[:,:,0] >= xmin ) \
               * N.array( pos[:,:,1] >= ymin ) \
               * N.array( pos[:,:,2] >= zmin ) \
                                               \
               * N.array( pos[:,:,0] <= xmax ) \
               * N.array( pos[:,:,1] <= ymax ) \
               * N.array( pos[:,:,2] <= zmax )


        return posMat[box3D], velMat[box3D], IDsS[box3D], N.sum(box3D)


    def sort_posvel_func(self, iterLen, maxN, NpartA, \
                               posA, velA, IDsA ):
        """
        Function for sorting stuff.
        * Find longest list of IDs, just in case IDs may disappear
        with time and structure development.
        * Sort IDs from every step.
        """
        print """
        Sifter has completed reading all {0} files of subfolder {1}.
        - Commencing method for sorting positions and velocities.
        """.format(iterLen, self.subfolder)

        # Prepare variables and arrays for sorting
        posMat   = N.zeros( (iterLen, maxN, 3),
                          dtype=N.float32 )
        velMat   = N.zeros( (iterLen, maxN, 3), 
                          dtype=N.float32 )
        argsIDsS = N.zeros( ( iterLen, maxN ),
                          dtype=N.int64 )
        IDsS     = N.zeros( ( iterLen, maxN ),
                          dtype=N.int64 )
        # IDsSarg  = N.zeros( ( iterLen, maxN ),
        #                   dtype=N.int64 )

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
        
        # User might want merely a box/slice of the positions.
        # if self.box_param == True:
        #     posMat, velMat, IDsS, NpartA = self.boxer(posMat, velMat, IDsS, iterLen, NpartA)

        return posMat, velMat, IDsS


    def plot_pos(self, IDsA, posA, iterLen, NpartA):
        """
        Plots positional data output.
        """
        totalNtot = 1024**3 # Total number of elements
        # Try a scatterplot first
        print "\tInitiating scatter plot of positions in simulation: \
            {0}_{1}_{2}/snapshot_{3}".format(\
            self.indraN, self.iA, self.iB, self.subfolder)
        

        fig =  pl.figure()
        ax  = fig.add_subplot(111, projection='3d')
        for i in N.arange(0, iterLen):
            """ Runs through ".i" ; i is int \in 
            * [0, 256) for [ posvel, fof, subhalo ]
            * [0, 505) for [ fft                  ]
            """
            # for Npart in N.arange(0, NpartA[i] ):
            #     # pl.plot(posA[i, N, ])
            #     ax.scatter(posA[i,:Npart,0], posA[i,:Npart,1], posA[i,:Npart,2],
            #                depthshade=True)
            #     continue # oops, this plots stuff in duplicates
            
            iterNtot         = N.sum(NpartA[:i+1])
            percent_complete = 100.*iterNtot/totalNtot

            itertext = " Snapshot #{0:<3d} | No. of new plot elements {1:6d} -"\
                                .format(i, NpartA[i])\
                + " [Total: {0:>10d}/{1:g} ( {2:>3d}% ) ]".format(
                                      iterNtot, totalNtot,
                                      int(percent_complete) )

            self.itertextPrinter(itertext, i, iterLen, 10)
            " Scatter plot "
            "              x-elements            y-elements            z-elements "
            ax.scatter(posA[i,:NpartA[i],0], posA[i,:NpartA[i],1], posA[i,:NpartA[i],2],
                       depthshade=True, s=1)
            continue

        ax.set_xlabel('x-position Mpc/h')
        ax.set_ylabel('y-position Mpc/h')
        ax.set_zlabel('z-position Mpc/h')
        plotname = self.outputPather(self.subfolder)+".png"
        print "Saving plot"
        pl.savefig(plotname, dpi=200)
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
            folderPath = self.outputpath
            pass
        else:
            folderPath = "indraData/{0}_i{1}{2}{3}{4}_sf{5}/"
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
            " folderpath : 'indraData/{0}_i{1}{2}{3}{tmp}_sf{5}/' "
            " filename   :           '{0}_i{1}{2}{3}{tmp}_sf{5}'  "
            pass
        else:
            " When normal data structures are processed "
            folderPath = folderPath.format( 
                            self.what, self.indraN, self.iA, self.iB, "", num )
            fileName   = fileName.format(   
                            self.what, self.indraN, self.iA, self.iB, "", num )
            # Examples   : \
            " folderpath : 'indraData/{0}_i{1}{2}{3}{None}_sf{5}/' "
            " filename   :           '{0}_i{1}{2}{3}{None}_sf{5}'  "
            pass
        
        self.fileName = fileName 
        outfilePath = folderPath + fileName

        if not os.path.exists(self.uname + folderPath):
            os.makedirs(self.uname + folderPath)
            print "Creating folder structure: ", self.uname + folderPath, "\n"
            pass
        else:
            print "Folder already exists: ", self.uname + folderPath, "\n"
            pass

        self.outfilePath = outfilePath # this is easier, anyway.

        return outfilePath

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


    def readLoopError(self, filepath, loop, loops, i):
        """
        Missing file-error-handler.
        """
        errorstring = \
        """
        Whilst reading {0} dataset,
        Filepath :    {1}  ;
        Reading loop: {2}/{3} ;
        File no. {4} seems to be missing.
        Continue anyway? 
        """.format(self.what, filepath, loop, loops, i)

        self.missingfiles += 1
        if self.missingfiles < 2:
            if self.errhand_userinput(errorstring):
                # Function should return True
                # if user accepts a single missing file
                return 0
            pass
        else:
            # Two missing files is/are/blah too much
            sys.exit(self.mult_miss_error)

        return 0


    def item_size_calc(self, L=[]):
        """
        Makes use of numpy and sys module to approximate
        byte sizes of objects that are input.
        """
        size = 0.
        if hasattr(L, '__iter__') == True:
            " L is iterable "
            
            for item in L:
                " Running through L's elements "
                
                if hasattr(item, '__iter__') == True:
                    " L's items are iterable as well "

                    for subitem in item:
                        " adding the subitems' sizes to sum "
                        size += subitem.nbytes
                        continue
                    pass

                else:
                    " Adding the items' sizes to sum "
                    size += item.nbytes
                    pass

                continue 
            return size

        elif type(L) == int or type(L) == float:
            " Object inserted is not iterable, but is a valid number "
            return L.nbytes

        else:
            sys.exit("Object is foreign")

        return 0


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


    def intendedMachine(self):
        """
        Simple function that exits the program
        if dataset is not available for reading.
        Used to clean up syntax while debugging.
        """
        systemName = os.uname()[1]
        myLaptopName          = "DESKTOP-MR1LV6A"
        clusterName           = "elephant"
        runningLocallyMessage = """\
        Running locally, and has reached the end of the rainbow.
        Time to upload and test! Now exiting.
        """
        unknownOrigin = " Instead, it seems this is r" \
                      + runningLocallyMessage[11:66]\
                      + "\n You may choose to debug program locally"\
                      + " if you wish."\
                      + "\n Is this your intention?"

        if systemName == myLaptopName:
            sys.exit(runningLocallyMessage)
        elif systemName.startswith(clusterName):
            pass
        else:
            print "\n\tNot running from intended machine(s)"\
                  + " (the 'elephant' cluster)."
            if self.errhand_userinput(unknownOrigin):
                self.okGo = True
                pass
            else:
                sys.exit("\n\tNow exiting.")
            pass

        return 0


    def bep(self):
        """
        "Better" Error Printer
        Simple module that prints error messages in a "better" way
        """
        nl              = "\n"
        prefix          = "\tPython's Error:"
        errorType       = "* " + str(sys.exc_info()[0])[18:-2]
        theBaseIndent   = textwrap.fill(prefix, replace_whitespace=False)[:-1]
        nextLineIndent  = " "*(len(theBaseIndent)/2 -2)
        messToScreen = textwrap.TextWrapper(initial_indent=nextLineIndent,
                                            subsequent_indent=nextLineIndent)
        errorDescr = "* " + str( sys.exc_info()[1] ).capitalize()
              
        print prefix
        print messToScreen.fill(errorType)
        print messToScreen.fill(errorDescr)
        print messToScreen.fill("* Error encountered inside function:")
        print messToScreen.fill(str("'"+self.funcNameOver("1up")+"'"))
        sys.exit()


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
        """
        return all([arg != 0, arg != False, arg != None])

if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")