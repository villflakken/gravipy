# ==============================================
# Reading toolkit for data sets' structure.
# ==============================================
import os, sys, glob, textwrap, platform
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


        # REWRITE BELOW INTO DICTIONARY FORM!!!
        # " Maybe engage plot like this? "
        # if self.boolcheck(self.plotdata) == True:
        #     self.plot_funcs[self.what]
        if self.what == "pos":
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
            " * Assigning (unsorted) {0:>9s} values to array"\
                .format(itername)\
                +" - Set ({1:>3d} / {2}) ..."\
                .format(itername, i, (iterLen-1))
            " Less spam in the terminal "
            self.itertextPrinter(itertext, i, iterLen, 20)
            outarr[ i, :NpartA[i] ] = inlist[i][:]
            continue
        print
        
        return outarr


    def boxer(self, pos, vel, IDs):
        """
        Extracts slices of data, determined from 3D positions.
        self.box_params = [ [0.,20.],[0.,20.],[0.,5.] ] 
        """
        xmin, xmax = self.box_params[0]
        ymin, ymax = self.box_params[1]
        zmin, zmax = self.box_params[2]
        # print "xmin, xmax:", xmin, xmax
        # print "ymin, ymax:", ymin, ymax
        # print "zmin, zmax:", zmin, zmax

        " Bool'ed indexation "
        box3D =  N.array( pos[:,0] >= xmin ) \
               * N.array( pos[:,1] >= ymin ) \
               * N.array( pos[:,2] >= zmin ) \
                                             \
               * N.array( pos[:,0] <= xmax ) \
               * N.array( pos[:,1] <= ymax ) \
               * N.array( pos[:,2] <= zmax )

        posMat, velMat, IDsM = pos[box3D], vel[box3D], IDs[box3D]


        return posMat, velMat, IDsM, N.sum(box3D)


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
        """
        # Prepare variables and arrays for sorting
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
                               inMat, IDsA ):
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
            itertext = " * Sorting {0:>9s} values, {1:>3d}/{2} ..."\
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


    def readLoopError(self, filepath, loop, loops, i):
        """
        *  In case an intermediate file is missing, have an option ready.
        ** In case 2 intermediate files are missing, abort.
        Missing-file-error-handler.
        ... Outdated; useless?!?
            ... Just in case.
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
        !!!Currently does not work reliably!!!
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


    def item_size_printer(self, byte):
        """ 
        Paired with 'item_size_calc'
        (which currently does not work reliably);
        takes number of bytes as int,
        then gives out string of human-readable size estimate.
        """
        if 0 <= byte < int(1.e3):
            return "{0:.2f} bytes".format(byte)
        elif int(1.e3) <= byte < int(1.e6):
            return "{0:.2f} KBs".format(byte)
        elif int(1.e6) <= byte < int(1.e9):
            return "{0:.2f} MBs".format(byte)
        elif int(1.e9) <= byte < int(1.e12):
            return "{0:.2f} GBs".format(byte)
        elif int(1.e12) <= byte < int(1.e15):
            return "{0:.2f} TBs".format(byte)
        elif int(1.e15) <= byte < int(1.e18):
            return "{0:.2f} PBs".format(byte)



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
            # sys.exit(runningLocallyMessage)
            pass
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
        Returns True when arg's value is true.
        """
        return all([arg != 0, arg != False, arg != None])


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")