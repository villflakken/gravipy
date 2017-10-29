# ==============================================
# Indra data sets' reading MO.
# ==============================================
""" # Abbreviations in comments:
DNN  = Declaration Not Needed
DNC  = Declaration Need Confirmed
DT   = Debugging Tool (that I used myself)
LDT  = Legacy Debug Tool
LIDA = LongID Assumed (hard coded)
"""
import os, sys, glob
import numpy as N
import subprocess as sp
from read_args import readArgs
from read_procedures import readProcedures

def read_particles( data=None, indraN=None, iA=None, iB=None,     \
                    foldNum=None, fftNum=None,                    \
                    sortIDs=None, lessprint=None, tmpfolder=None, \
                    w2f=None, plotdata=None,                      \
                    outputpath=None ):
    """
    Simplified read function for importing externally
    """
    paramslist = \
        [ 
           data, indraN, iA, iB, 
           foldNum, fftNum, 
           sortIDs, lessprint, tmpfolder,
           w2f, plotdata, outputpath 
        ]

    redrum = readDo(paramslist) # insert parameters
    redrum.initArgs()           # check parameters
    redrum.beginReading()       # read data
    redrum.stuff = "The Stuff That You Want"

    return 


class readDo(readArgs, readProcedures):
    """
    Commences data reading, sets into motion what to do.
    """
    def __init__(self, functioncall=[]):
        """
        If args initialized through function import
        """
        self.functioncall = functioncall
        """
        Inherits two other scripts' classes and functionality.
        """
        readArgs.__init__(self)
        readProcedures.__init__(self)
        """
        Some fundamental filenames, lists, tuples, bools, and values.
        """
        self.uname = "/home/"+os.environ['USER']+"/"
        self.dsp = "/datascope" # datascope path; base file structure path.
                                ### Only here to shorten further string
                                ### supplements also in case of base address
                                ### changes, easy to find.
                                ###### Modify as needed.
        self.sub_asks_for_length = False # enabling LDT for subhalo
        self.okGo                = False # checker for remote debugging 
        self.borders          = [] # items True/False for in/out of boundary
        self.tuple_parameters = [] #    bool(any([])) => False \\\
                                   # iow any(emptylist) returns False;
                                   #    list w/ items returns True!
        self.keys_read      = []
        self.missingkeys    = []
        self.missingkeys_no = 0
        self.printNth       = 5
        self.length         = None  # LDT
        self.toggles        = "sortIDs", "lessprint", "tmpfolder", "w2f", "plotdata"
        self.nonvitals      = self.toggles[:], "outputpath", "box_params"
        self.stringkeys     = "what", "outputpath"
        # * \==> These keys do not necessarily NEED specification
        """
        Definitions of keywords to be used, cfg-file interpretation
        """
        self.arglist = \
            [
                "what"      , 
                "indraN"    , 
                "iA"        , 
                "iB"        , 
                "subfolder" , 
                "fftfile"   , 
                "sortIDs"   ,
                "lessprint" ,
                "tmpfolder" ,
                "w2f"       ,
                "plotdata"  ,
                "outputpath",
                "box_params" # , "redshift", "bssdt"
            ]
        """
        Dictionaries: parameter values, cfg-file interpretation
        """
        # python 2.7 : SO ELEGANT... but indra sits on 2.6.6...
        # self.read_params = { key: [] if key=="what" else 0 for key in self.arglist }
        self.read_params = \
            { 
                     "what" :  [] ,
                   "indraN" : None,
                       "iA" : None,
                       "iB" : None, 
                "subfolder" : None, 
                  "fftfile" : None, 
                  "sortIDs" : None,
                "lessprint" : None,
                "tmpfolder" : None,
                      "w2f" : None,
                 "plotdata" : None,
               "outputpath" : None,
               "box_params" : None  # , "redshift" : None, "bssdt" : None
            }
        # Python 2.7 : 
        # self.default_vals = { key:"pos" if key=="what" else 0 for key in self.arglist }
        self.default_vals = \
            {
                     "what" :"posvel", 
                   "indraN" :  0  ,
                       "iA" :  0  , 
                       "iB" :  0  , 
                "subfolder" :  0  , 
                  "fftfile" :  0  , 
                  "sortIDs" :  0  ,
                "lessprint" :  1  ,
                "tmpfolder" :  0  ,
                      "w2f" :  0  ,
                 "plotdata" :  1  ,
               "outputpath" :  None  ,
               "box_params" :  None # , "redshift" : 0, "bssdt" : 0
            }
        """
        Dictionaries: commands for the program to act on
        """
        self.actionkeys =  \
            [
                "posvel",  
                "pos",     
                "vel",     
                "fof",     
                "subhalo", 
                "fft"      
            ]
        self.action = \
            { 
                "posvel"    : self.read_posvel  , 
                "pos"       : self.read_posvel  , 
                "vel"       : self.read_posvel  , 
                "fof"       : self.read_FOF     , 
                "subhalo"   : self.read_subhalo , 
                "fft"       : self.read_FFT
            }
        self.plot_funcs = \
            {
                "pos"       : self.plot_pos     , 
                "vel"       : self.plot_vel     , 
                "fof"       : self.plot_fof     , 
                "subhalo"   : self.plot_subhalo , 
                "fft"       : self.plot_fft
            }
        """
        end of init
        """


    def __call__(self, read_params):
        """
        Simplified read function for single-set readings
        """
        self.read_params = read_params

        self.callArgsChecker()
        """
        If any parameters are tuples,
        might want to do self.beginReading instead;
        """
        return self.beginReading()

    def beginReading(self):
        """
        Primary program flow:

        This is the function that runs through multiple sets of data.
        Extremely high potential for messy code production.
        Will try to avoid that. But then it will be ugly.
        Assumes that parameters in arglist have been set.
        """
        print "\n"*3 # Clearing the screen
        tmp = sp.call('clear',shell=True)
        print

        parsed_datasets_list = []
        """
        Prime example on how complex a set of permutations can become!
        """
        for task in self.what_set:
            " Current task as globvar (global variable) "
            self.what = task

            for iN in N.arange(self.indraN_low, self.indraN_high + 1):
                " Current indraN as globvar "
                self.indraN = iN

                for iA in N.arange(self.iA_low, self.iA_high + 1):
                    " Current iA as globvar "
                    self.iA = iA

                    for iB in N.arange(self.iB_low, self.iB_high + 1):
                        " Current iB as globvar "
                        self.iB = iB

                        lowerLim, upperLim, sett, symbol = \
                            self.currentTaskParamsParser()

                        for num in N.arange(lowerLim, upperLim + 1):
                            " Current subfolder/fftfile as globvar "
                            if self.okGo == False:
                                self.intendedMachine()
                                pass 
                                # Allows for remote debugging up to this point

                            if task != "fft":
                                """
                                No further safety nets should be needed for
                                checking of task names.
                                """
                                self.subfolder = num
                            else: # When task is !indeed! fft reading.
                                self.fftfile   = num

                            self.progressPrinter(symbol, num, sett)

                            # Task function call:
                            parsed_data = self.action[self.what]()
                              # (and the main component of this entire system)

                            # Function calls post processes as paramatrized:
                            if any((self.w2f, self.plotdata)) == True:
                                self.pp_selector(parsed_data, num)
                            else:
                                parsed_datasets_list.append(parsed_data)

                            # writepath = self.outputPather(num)
                            # with open(writepath, 'w') as self.writeToFile:
                            #     # Should write SOME output, somewhere, right?
                            #     self.action[self.what]() # Task function call.
                            #     self.writeToFile.close()
                            #     # Redundant w/ with present, but I'm specific.
                            
                            continue
                        continue
                    continue
                continue
            continue
        """
        Might be useful outside of function,
        that returned object is not mutable: return a tuple.
        """
        return tuple(parsed_datasets_list)


    def currentTaskParamsParser(self):
        """
        Sets some reading parameters into the environment,
        because FFT and other 
        """
        if self.what != "fft" and self.what in self.actionkeys:
            # Second condition probably redundant condition, but hey x)
            " if not 'fft', then 'subfolder' systems! "
            lowerLim = self.subfolder_low
            upperLim = self.subfolder_high
            sett     = self.subfolder_set
            symbol   = "subfolder"
        elif self.what == "fft":
            " if 'fft', then fftfiles! "
            lowerLim = self.fftfile_low
            upperLim = self.fftfile_high
            sett     = self.fftfile_set
            symbol   = "fftfile"
        else:
            sys.exit("Task name does not conform to any allowed.")
            # Safety nets should already have picked up on this;
            # maybe I'm coding this _too_ safe.
        return lowerLim, upperLim, sett, symbol


    def progressPrinter(self, symbol, num, sett):
        """
        Printout of programs current progress through folder systems
        """
        progress = """        Currently reading:
        Data type   : {task:>6}   (/out of sets: {set:^10} )
        indraN      : {iN:>6}             ( /: {indraNset:^10} )
        iA          : {iA:>6}             ( /: {iAset:^10} )
        iB          : {iB:>6}             ( /: {iBset:^10} )
        {symbol:<12}: {sn:>6}             ( /: {snset:^10} )
        """
        # Text formatting of program's 'progress bar' placeholder
        taskSetStr = str(self.what_set).strip("[]")
        print progress.format(\
              task=self.what,            set=taskSetStr,      \
                iN=self.indraN,    indraNset=self.indraN_set, \
                iA=self.iA,            iAset=self.iA_set,     \
                iB=self.iB,            iBset=self.iB_set,     \
            symbol=symbol,    sn=num,  snset=sett             )

        return 0










if __name__ == '__main__':
    test = readDo()
    test.initArgs()
    test.beginReading()

    print
