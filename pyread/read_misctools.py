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
                    self.indraN, "_tmp", self.iA, self.iB
                )
                pass

            else:
                " /indra{iN}{}/{iN}_{iA}_{iB} "
                print "normal folders acknowledged."
                indrapath = indrapath.format(
                    self.indraN, "", self.iA, self.iB
                )
                pass
            
        elif self.onIdies == True:
            # Path structure for SciServer's Jupyter stuff
            indrapath = "/workspace/indra/{0:d}_{1:d}_{2:d}"
            indrapath = indrapath.format(
                self.indraN, self.iA, self.iB
            )
            # Before I made origamiPathParser, below stuff was shortcut:

            # self.origamipath = \
            #     "workspace/indra/origami/i{0:1d}{1:1d}{2:1d}{3:s}/i{0:1d}{1:1d}{2:1d}{3:s}_sf{4:02d}_tag.dat"
            # self.origamipath = self.origamipath\
            #     .format(
            #                 self.indraN , self.iA , self.iB , 
            #                 "tmp" if self.tmpfolder == True else "" ,
            #                 self.subfolder
            #            )
            pass

        return indrapath


    def fof_pathstrings(self):
        """
        Generates paths & unnumerated filenames for tabs and ids: FOF
        """
        indrapath = self.dsp  +  self.indraPathParser()
        snappath  = indrapath +  "/snapdir_{0:03d}/".format(self.subfolder)
        gtab_name = snappath  + "group_tab_{0:03d}.".format(self.subfolder)
        gids_name = snappath  + "group_ids_{0:03d}.".format(self.subfolder)

        return gtab_name, gids_name


    def subh_pathstrings(self):
        """
        Generates paths & unnumerated filenames for tabs and ids: SUBHALO
        """
        indrapath = self.dsp  + self.indraPathParser()
        postpath  = indrapath + "/postproc_{0:03d}/".format(self.subfolder)
        stab_name = postpath  +   "sub_tab_{0:03d}.".format(self.subfolder)
        sids_name = postpath  +   "sub_ids_{0:03d}.".format(self.subfolder)

        return stab_name, sids_name


    def origamiPathParser(self):
        """
        Handles how the script interprets 
        """
        iN  = self.indraN
        iA  = self.iA
        iB  = self.iB
        sf  = self.subfolder
        tmp = "tmp" if self.tmpfolder == True else ""

        # print " 1up :", self.funcNameOver("1up")                            #
        # print "here :", self.funcNameOver("here")                           #
        # print "indraNAB:"                                                   #
        # print iN, iA, iB                                                    #
        # print "sf:"                                                         #
        # print sf                                                            #
        # print "self.origamipath:"                                           #
        # print self.origamipath                                              #
        # print                                                               #
        
        if self.origamipath == False:
            # File name must be generated
            " Inital folder path, assuming on idies/SciServer machine "
            ifp = self.uname + "workspace/indra/"
            # print ifp                                                       #

            " Folder w/ origami output. "
            foldp = ifp + "origami/i{iN}{iA}{iB}{tmp}/" 
            foldp = foldp.format(iN=iN, iA=iA, iB=iB, sf=sf, tmp=tmp)
            # print foldp                                                     #

            " File name is determined the same way"
            filen = "i{iN}{iA}{iB}{tmp}_sf{sf:02d}_tag.dat"
            filen = filen.format(iN=iN, iA=iA, iB=iB, sf=sf, tmp=tmp)
            # print filen                                                     #

            " Add the strings to complete the path "
            oridatpath = foldp  + filen
            # print oridatpath                                                #
            # print " Aut.ly gen.ed origamipath:"                             #
            pass

        elif isinstance(self.origamipath, str) == True:
            " User has provided file path "
            oridatpath = self.origamipath
            # print " User-provided origamipath:"                             #
            pass

        else:
            " Invalid origamipathing "
            sys.exit("\n\t Let program generate origamipath," \
                        +" or specify the origamipath.")

        # print oridatpath                                                    # DT
        # print                                                               # DT
        
        return oridatpath


    def auto_outputPather(self):
        """
        Checks if output folder structure exists
        & creates output path for output file 
        & filepath- & name based on env. params.
        * Note: based in user's home folder,
                folder structure based on intended task.
        """
        self.outfilePath = None # Clear variable

        # Determines format of output path
        if bool(self.outputpath) == True:
            " User input specified data output path "
            folderPath = self.outputpath
            pass
        else:
            folderPath = "/{data}_i{iN}{iA}{iB}{tmp}/"
            pass
        fileName = "{data}_i{iN}{iA}{iB}{tmp}"

        # Lowest hierarchy for user's folders, usually "~/"
        if self.onIdies == True:
            outdir_floor  = self.uname + "workspace/persistent/output_gravipy/"
        
            # Version-control-specific output variable
            outdir_floor += "{version}/".format(version=self.version)
            # example: "workspace/persistent/output_gravipy/{version}/"
            pass
        else:
            # Assuming to be on the elephant-cluster
            outdir_floor  = self.uname + "output_gravipy/"
            pass


        # The following test establishes these strings'(*) naming conventions:
        " folderpath : 'output_gravipy/{data}_i{iN}{iA}{iB}{tmp}/' "
        " filename   :                '{data}_i{iN}{iA}{iB}{tmp}'  "
        if any([ # Confirms combination procedure or not
                self.what_set in self.singleSnapActions.keys() ,
                self.what_set in self.allSnapActions.keys()     
            ]):
            operationName = self.what_set
            pass
        else:
            operationName = self.what
            pass

        tmpstr = "tmp" if self.tmpfolder == True else ""
        # ... (*) and here they are set:
        folderPath = folderPath.format( 
            data = operationName, 
            iN   = self.indraN, 
            iA   = self.iA, 
            iB   = self.iB, 
            tmp  = tmpstr 
        )
        fileName = fileName.format(   
            data = operationName, 
            iN   = self.indraN, 
            iA   = self.iA, 
            iB   = self.iB, 
            tmp  = tmpstr
        )
        
        " May be used for dictionary storage of datasets "
        self.fileName = fileName
        # Will need snap folder/number at times added to it!
        
        outfilePath   = folderPath + fileName

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
            pass # Folders are verified

        self.outfilePath = outdir_floor + outfilePath 
        ok = int(raw_input("Is this an OK output file path?:\n    "
                       + self.outfilePath))
        if not ok: sys.exit(" --- Filepath not ok :( ")
        return self.outfilePath


    def itertextPrinter(self, itertext, i, iterLen, modifier):
        " Less spam in terminal window "
        # print 
        # print "lessprint                         :", self.lessprint
        # print "i % (self.printNth*modifier) == 0 :", i % (self.printNth*modifier) == 0
        if self.boolcheck(self.lessprint) == False:
            # No output reduction:
            print itertext
            pass
        
        else:
            # Output reduction:
            if i % (modifier) == 0:
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
        ranks = {"inception": 0, "here": 1, "1up": 2, "2up": 3, "3up": 4}
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


    ###########################################################
    #   The next functions may have had sound ideas, but are  #
    # of negligible importance, and mainly used in debugging. #
    ###########################################################


    def measure_time(f):
        """
        Measures runtime of a function called thereafter
        Usage:
        '''
        @measure_time
        def foo():
            #content of function 
        '''
        URL: 'https://stackoverflow.com/a/25958593/8387070'
        """

        def timed(*args, **kw):
            ts = time.time()
            result = f(*args, **kw)
            te = time.time()

            print '%r (%r, %r) %2.2f sec' % \
                  (f.__name__, args, kw, te-ts)
            return result

        return timed


    def timeprint(totsecs, reverse=None):
        """
        Takes integer/float input: an amount of time (in seconds),
        returns string of hours, minutes, seconds. Usage:
        | >>> print "timetest: {0}".format(timeprint(4220.))
        | timetest:   1h , 10m , 20.00s
        | >>> print "timetest: {0}".format(timeprint(4220., reverse=True))
        | timetest: s:20.00 , m:10 , h:  1
        """   
        seconds_in_an_hour  = 3600.
        seconds_in_a_minute = 60.
        hours   = int(  totsecs // seconds_in_an_hour )
        minutes = int( (totsecs %  seconds_in_an_hour) // seconds_in_a_minute )
        seconds = int( (totsecs %  seconds_in_an_hour) %  seconds_in_a_minute )
        if reverse == True:
            timestring = "s:{s:>2.2f} , m:{m:>2d} , h:{h:>3d}"
            return timestring.format(s=seconds, m=minutes, h=hours)
        timestring = "{h:>3d}h , {m:>2d}m , {s:>2.2f}s"
        return timestring.format(h=hours, m=minutes, s=seconds)


    def readLoopError(self, filepath, loop, loops, i):
        """
        *  In case an intermediate file is missing, have an option ready.
        ** In case 2 intermediate files are missing, abort.
        Missing-file-error-handler.
        ... Outdated; useless?!?
            ... Just in case.
        """
        errorstring = """
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


    def objectDebug_print(self, obj, objstr):
        """
        Printer to show the properties of a variable that seems to
        making troubles
        ranks = {"inception": 0, "here": 1, "1up": 2, "2up": 3}
        """
        print
        print " Object:", objstr
        print " * Currently viewed in function:", self.funcNameOver("1up")
        print " * - which is called from      :", self.funcNameOver("2up")
        print " * --- called from             :", self.funcNameOver("3up")
        print

        " Print type of object "
        try:
            print " * type("+objstr+"):", type(obj)
            pass
        except:
            pass

        " Type length, if iterable "
        if hasattr(obj, '__iter__'):
            print " * len("+objstr+"):", len(obj)
            pass

        " The object's actual stored value"
        print " * "+objstr+":\n", obj
        print

        return 0


    def bep(self):
        """
        "Better" Error Printer
        Simple module that prints error messages in a "better" way
        """
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

        return 0



if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")