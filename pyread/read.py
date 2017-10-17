# ==============================================
# Indra data sets' reading MO.
# ==============================================
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
        Actiondicts : commands for the program to act on
        """
        self.actionkeys = \
            [ # The types of data available to read.
                "posvel",  
                "pos",     
                "vel",     
                "fof",     
                "subhalo", 
                "fft"      
            ]
        self.action = \
            { # Function library for initializing data reading.
                "posvel"    : self.read_posvel  , 
                "pos"       : self.read_posvel  , 
                "vel"       : self.read_posvel  , 
                "fof"       : self.read_FOF     , 
                "subhalo"   : self.read_subhalo , 
                "fft"       : self.read_FFT
            }
        """
        end of init
        """

    def __call__(self, read_params):
        """
        Simplified read function for single-set readings.
        1 - Validate arguments given.
        2 - Begin reading and initiate corresponding output.
        """
        # print "\n"*3 # Clearing the screen
        tmp = sp.call('clear',shell=True)
        print
        
        # print """
        # Inside readDo __call__ function
        # """
        # print " Setting read_params to self.read_params"
        self.read_params = read_params
        # print " self.read_params:"
        # print self.read_params
        
        # print " Initializing self.callArgsChecker() "
        " 1. "
        self.callArgsChecker()
        # print " self.callArgsChecker() done! "
        
        # print " Initializing self.beginReading()"
        " 2. "
        # print 
        return self.beginReading()


    def beginReading(self):
        """
        Primary program flow:

        This is the function that runs through multiple sets of data.
        Extremely high potential for messy code production.
        Will try to avoid that. But then it will be ugly.
        Assumes that parameters in arglist have been set.
        """
        # print " * Inside self.beginReading()! "
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
                                " Allows for remote debugging up to this point "
                                pass 

                            if task != "fft":
                                """
                                No further safety nets should be needed for
                                checking of task names.
                                """
                                self.subfolder = num
                                # print self.outputPather(num)
                            else:
                                " When task is fft reading. "
                                self.fftfile   = num

                            self.progressPrinter(symbol, num, sett)

                            " Task function call: "
                            parsed_data = self.action[self.what]()
                            " >: Main component of program. "

                            " Function calls post processes as paramatrized: "
                            if any((self.w2f, self.plotdata)) == True:
                                self.pp_selector(parsed_data, num)
                            else:
                                parsed_datasets_list.append(parsed_data)
                            
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
        if self.what != "fft":
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
    print """
    Import 'read' and initialize, i.e.:
    'yourInstanceName = readDo()'
    'output = yourInstanceName(dictionaryOfDataParameters)'
    """