# ==============================================
# Reading toolkit for data sets' structure.
# ==============================================
import os, sys, textwrap, platform
import numpy as N
import matplotlib.pyplot as pl





class MiscTools(object):
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

            pass

        elif sys.platform in ("win32", "win64"):
            self.uname = os.path.expanduser("~")+"\\"
            pass

        else:
            sys.exit("Error in UserTools' init.")
        """
        End of init
        """

    def indraPathParser(self):
        """
        If program is supposed to run from 'indraX_tmp' data file structure,
        returns modified filepath for the reader.
        """

        if self.onElephant == True:
            # Path structure for elephant cluster
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
            
        elif self.onIdies == True:
            # Path structure for SciServer's Jupyter stuff
            indrapath = "/workspace/indra/{0:d}_{1:d}_{2:d}"
            indrapath = indrapath.format( self.indraN, self.iA, self.iB )

            self.origamipath = \
                "workspace/indra/origami/i{0:1d}{1:1d}{2:1d}{3:s}/i{0:1d}{1:1d}{2:1d}{3:s}_sf{4:02d}_tag.dat"
            self.origamipath = self.origamipath\
                .format(
                            self.indraN , self.iA , self.iB , 
                            "tmp" if self.tmpfolder == True else "" ,
                            self.subfolder
                       )
            pass

        return indrapath

    def origamiPathParser(self):
        """
        Handles how the script interprets 
        """
        if self.origamipath == False:
            # File name must be generated
            " Inital folder path, assuming on idies/SciServer machine "
            ifp = self.uname + "workspace/indra{iN}/".format(self.indraN) 
            
            " Folder w/ origami output. "
            foldp = ifp + "origami/i{iN}{iA}{iB}{tmp}/" 
            foldp = foldp.format(
                iN  = self.indraN,
                iA  = self.iA,
                iB  = self.iB,
                sf  = self.subfolder,
                tmp = "tmp" if self.tmpfolder == True else ""
                )

            " File name is determined the same way"
            filen = "i{iN}{iA}{iB}{tmp}sf{sf:02d}_tag.dat"
            filen = filen.format(
                iN  = self.indraN,
                iA  = self.iA,
                iB  = self.iB,
                sf  = self.subfolder,
                tmp = "tmp" if self.tmpfolder == True else ""
                )
            
            " Add the strings to complete the path "
            oridatpath = foldp  + filen 
            pass

        elif isinstance(self.origamipath, str) == True:
            " User has provided file path "
            oridatpath = self.origamipath
            pass

        else:
            " Invalid origamipathing "
            sys.exit("\n\t Let program generate origamipath," \
                        +" or specify the origamipath.")
        return oridatpath

    def auto_outputPather(self, num):
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
            folderPath = "output_gravipy/{0}_i{1}{2}{3}{4}_sf{5:02d}/"
            pass

        fileName = "{0}_i{1}{2}{3}{4}_sf{5:02d}"
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
            " folderpath : 'output_gravipy/{0}_i{1}{2}{3}{tmp}_sf{5:02d}/' "
            " filename   :                '{0}_i{1}{2}{3}{tmp}_sf{5:02d}'  "
            pass
        else:
            " When normal data structures are processed "
            folderPath = folderPath.format( 
                            self.what, self.indraN, self.iA, self.iB, "", num )
            fileName   = fileName.format(   
                            self.what, self.indraN, self.iA, self.iB, "", num )
            # Examples   : \
            " folderpath : 'output_gravipy/{0}_i{1}{2}{3}{None}_sf{5:02d}/' "
            " filename   :                '{0}_i{1}{2}{3}{None}_sf{5:02d}'  "
            pass
        
        " May be used for dictionary storage of datasets "
        self.fileName = fileName 
        
        outfilePath   = folderPath + fileName

        outdir_floor = self.uname # lowest hierarchy for user's folders, usually "~/"
        if self.onIdies == True:
            outdir_floor = outdir_floor + "workspace/persistent/"
            pass

        if any((self.w2f, self.plotdata)) == True:
            " If any kind of output is requested "
            " -> Check if folder already exists; if not then make it "
            if not os.path.exists(outdir_floor + folderPath):
                os.makedirs(outdir_floor + folderPath)
                print "Creating output folder structure: ", \
                       outdir_floor + folderPath, "\n"
                pass
            else:
                print "Output folder already exists: ", \
                       outdir_floor + folderPath, "\n"
                pass
            pass # Folders verified

        self.outfilePath = outdir_floor + outfilePath 

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
        errorstring =         """
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

    def arrval_equaltest(self, array):
        """
        Checks if all values of an array is the same value.
        ** For debugging.
        
        ''' # From google groups
        # How about the following?
        exact: numpy.all(a == a[0])
        inexact: numpy.allclose(a, a[0])

        # Looks like the following is even faster:
        np.max(a) == np.min(a)
        '''
        
        """
        # My own method
        firstvalue  = array[0]
        temparray   = N.ones(array.shape)*firstvalue
        return N.array_equal(array, temparray)



if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")