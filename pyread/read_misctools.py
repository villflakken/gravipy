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
        """
        End of init
        """

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
            return "{0:.2f} KBs".format(byte/1e3)
        elif int(1.e6) <= byte < int(1.e9):
            return "{0:.2f} MBs".format(byte/1e6)
        elif int(1.e9) <= byte < int(1.e12):
            return "{0:.2f} GBs".format(byte/1e9)
        elif int(1.e12) <= byte < int(1.e15):
            return "{0:.2f} TBs".format(byte/1e12)
        elif int(1.e15) <= byte < int(1.e18):
            return "{0:.2f} PBs".format(byte/1e15)
        elif int(1.e18) <= byte < int(1.e21):
            return "{0:.2f} EBs".format(byte/1e18)


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


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")