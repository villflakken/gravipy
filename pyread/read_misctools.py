# ==============================================
# Reading toolkit for data sets' structure.
# ==============================================
import os, sys, glob, textwrap, platform
import numpy as N
import subprocess as sp
import matplotlib.pyplot as pl


class readMiscTools(object):
    """
    Miscellaneous tools that are used in the readProcedures instance.
    """
    def __init__(self):

        """
        End of init
        """
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
            " * Assigning (unsorted) {0:>8s} values to array"\
                .format(itername)\
                +" - set ({0:>3d} / {1}) ..."\
                .format(i, (iterLen-1))
            " Less spam in the terminal "
            self.itertextPrinter(itertext, i, iterLen, 20)
            outarr[ i, :NpartA[i] ] = inlist[i][:]
            continue
        print
        
        return outarr


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


    def pp_selector(self, parsed_data, num):
        """
          * Accessed when class system is given a set of parameters;
            in order to automatically post-process a predetermined,
            greater sequence of data.
        Selects a post process method depending on
        which task procedure is currently in the environment.
        # Unfinished.
        """
        self.outputPather(num)


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


    #   The next functions may have had sound ideas,
    # but are of negligible importance.

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


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")