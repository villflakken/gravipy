# ==============================================
# Indra data sets' reading MO.
# ==============================================
import os, sys, glob, time
import numpy as N
import subprocess as sp
from read_args import readArgs
from read_procedures import readProcedures



def read_ini( what="pos", indraN=0, iA=0, iB=0, subfolder=None, fftfile=None, 
              tmpfolder=False, sortIDs=False, lessprint=True,
              box_params=False, plotdim=2,
              w2f=False, plotdata=False,
              outputpath=False,
              origamipath=False
            ):
    """
    Simplified read function for importing externally;
    initializes class for the user.
    # WIP !
    """
    data_params = \
        { # Data structure parameters:
               "what" :( list(what) ),
             "indraN" :( indraN     ),
                 "iA" :( iA         ),
                 "iB" :( iB         ),
          "subfolder" :( subfolder  ),
            "fftfile" :( fftfile    ),
            # Reading options:
          "tmpfolder" :( tmpfolder  ),
              "sfset" :( sfset      ),
            "sortIDs" :( sortIDs    ),
          "lessprint" :( lessprint  ),
            # Extracts data from a coordinate box at positions specified:
         "box_params" :( box_params ),
            # Desired output filepath, 
            # or False (program storing to user's own folder).
         "outputpath" :( outputpath ),
            # Write 2 file: Probably a bad idea ...
                "w2f" :( w2f        ),
           "plotdata" :( plotdata   ),
            # Apply floats as "([min,max], [min,max], [min,max])" in Mpc/h units,
            # respectively for directions x, y, z. # Turned off w/: None/False
            "plotdim" :( plotdim    ), # Dimensions projected in plot
            # Origami functionality
        "origamipath" :( origamipath)
        }

    tmp = sp.call('clear',shell=True)

    ini = readDo()                # Initialize!
    ini.read_params = data_params # Set params
    " 1. "
    ini.callArgsChecker()         # Verify values
    " 2. "
    return ini.beginReading()     # Do the thing


class readDo(readArgs, readProcedures):
    """
    Commences data reading, sets into motion what to do.
    """
    def __init__(self):
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
                "pos",     
                "vel",     
                "fof",     
                "subhalo", 
                "fft",
                "origami",
                "time"
            ]
        self.action = \
            { # Function library for initializing data reading.
                "pos"     : self.read_posvel  , 
                "vel"     : self.read_posvel  , 
                "fof"     : self.read_FOF     , 
                "subhalo" : self.read_subhalo , 
                "fft"     : self.read_FFT     ,
                "origami" : self.read_origami ,
                "time"    : self.read_time
            }
        """
        end of init
        """

    def __call__(self, read_params):
        """
        Simplified read function for single-set readings.
        1 - Validate arguments given.
        2 - Begin reading and initiate corresponding output.
        # Not finished.
        """
        tmp = sp.call('clear',shell=True)
        
        self.read_params = read_params
        " 1. "
        self.callArgsChecker()
        
        " 2. "
        return self.beginReading()


    def beginReading(self):
        """
        Primary program flow:

        This is the function that runs through multiple sets of data.
        Extremely high potential for messy code production.
        Will try to avoid that. But then it will be ugly.
        Assumes that parameters in arglist have been set.
        """
        parsed_datasets_dict = {}
        """
        Prime example on how complex a set of permutations can become!
        """
        for task in self.what_set:
            " Current task as globvar (global variable) "
            self.what = task

            for iN in self.indraN_set:
                " Current indraN as globvar "
                self.indraN = iN

                for iA in self.iA_set:
                    " Current iA as globvar "
                    self.iA = iA

                    for iB in self.iB_set:
                        " Current iB as globvar "
                        self.iB = iB

                        sett, symbol = self.currentTaskParamsParser()

                        for num in sett:
                            " Current subfolder/fftfile as globvar "
                            if self.okGo == False:
                                self.intendedMachine()
                                " Allows for remote debugging up to this point "
                                pass 

                            if task != "fft":
                                " When task is non-fft-related. "
                                self.subfolder = num
                                pass

                            else:
                                " When task is fft reading. "
                                self.fftfile   = num
                                pass

                            self.progressPrinter(symbol, num, sett)

                            " Task function call: "
                            parsed_data = self.action[self.what]()
                            " >: Main component of program. "

                            " Creates 'candidate' for folder- and/or filename "
                            self.auto_outputPather(num)

                            " Function calls post processes as paramatrized: "
                            if any((self.w2f, self.plotdata)) == True:
                                """
                                The program handles data post processing
                                and storage thereof.
                                """
                                self.pp_selector(parsed_data, num)
                                pass
                            """
                            Output for user to manipulate.
                            * Base of filename seems a good candidate for 
                              dictionary's indexation names.
                              - Call on a list of the dictionary's keys, if confusion.
                            """
                            # Too Much Memory / TMM !!! 
                            # parsed_datasets_dict[self.fileName] = parsed_data
                            # Parsing 64 complete positional matrices with IDs:
                            # ~ 20GiBs * 64 = ~ 1 280 GiBs

                            continue # to next loop of 'num' (snapnum/fftfile)...
                        continue # to next loop of iB...
                    continue # to next loop of iA...
                continue # to next loop of iN...
            continue # to next loop of user-specified tasks...
        """
        Might be useful outside of function,
        that returned object is not mutable: return a tuple.
        """
        if len(parsed_datasets_dict.keys()) == 1:
            """
            So that user is given its tuple of values,
            without having to pack them out of a dictionary.
            """
            return parsed_datasets_dict[parsed_datasets_dict.keys()[0]]
        else:
            """
            Returns the whole dataset for the user
            to pack out from the dictionary.
            """
            return parsed_datasets_dict


    def currentTaskParamsParser(self):
        """
        Sets some reading parameters into the environment,
        because FFT and other 
        """
        if self.what != "fft":
            # Second condition probably redundant condition, but hey x)
            " if not 'fft', then 'subfolder' systems! "
            sett     = self.subfolder_set
            symbol   = "subfolder"
        elif self.what == "fft":
            " if 'fft', then fftfiles! "
            sett     = self.fftfile_set
            symbol   = "fftfile"
        else:
            sys.exit("Task name does not conform to any allowed.")
            # Safety nets should already have picked up on this;
            # maybe I'm coding this _too_ safe.
        return sett, symbol


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
        print progress.format(
              task=self.what,            set=taskSetStr,
                iN=self.indraN,    indraNset=self.indraN_set,
                iA=self.iA,            iAset=self.iA_set,
                iB=self.iB,            iBset=self.iB_set,
            symbol=symbol,    sn=num,  snset=sett             )

        return 0


if __name__ == '__main__':
    print """
    Import 'read' and initialize, i.e.:
    'yourInstanceName = readDo()'
    'output = yourInstanceName(dictionaryOfDataParameters)'
    """