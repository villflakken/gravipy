# ==============================================
# Indra data sets' reading MO.
# ==============================================
import os, sys, glob, time
import numpy as N
import subprocess as sp
from read_args import readArgs
from read_procedures import readProcedures



def read_ini( what = "pos",   indraN = 0, iA = 0, iB=0,
              subfolder   = None,    fftfile = None, 
              tmpfolder   = False,
              sfset       = False,
              sortIDs     = False,
              lessprint   = True,
              multiset    = False,
              box_params  = False,
              outputpath  = False,
              w2f         = False,
              plotdata    = False,
              plotdim     =  [2] ,
              origamipath = False
            ):

    data_params = \
        { # Data structure parameters:
               "what" :( list(what)  ),
             "indraN" :( indraN      ),
                 "iA" :( iA          ),
                 "iB" :( iB          ),
          "subfolder" :( subfolder   ),
            "fftfile" :( fftfile     ),
            # Reading options:
          "tmpfolder" :( tmpfolder   ),
              "sfset" :( sfset       ),
            "sortIDs" :( sortIDs     ),
          "lessprint" :( lessprint   ),
           "multiset" :( multiset    ),
            # Extracts data from a coordinate box at positions specified:
         "box_params" :( box_params  ),
            # Desired output filepath, 
            # or False (program storing to user's own folder).
         "outputpath" :( outputpath  ),
            # Write 2 file: Probably a bad idea ...
                "w2f" :( w2f         ),
           "plotdata" :( plotdata    ),
            # Apply floats as "([min,max], [min,max], [min,max])" in Mpc/h units,
            # respectively for directions x, y, z. # Turned off w/: None/False
            "plotdim" :( plotdim     ), # Dimensions projected in plot
            # Origami functionality
        "origamipath" :( origamipath )
        }

    tmp = sp.call('clear',shell=True)

    ini = readDo()                # Initialize!
    ini.read_params = data_params # Set params
    " 1. "
    ini.callArgsChecker()         # Verify values
    " 2. "
    return ini.beginReading(), ini     # Do the thing


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
        self.teststring = "\n   This is the test \n"
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
        
        self.datadict = {} # cf. function self.storager()
        
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
                            " Current subfolder/fftfile as globvar. "
                            # if self.okGo == False: # DT
                            #     self.intendedMachine()
                            #     " Allows for remote debugging up to this point "
                            #     pass 

                            if task != "fft":
                                " When task is non-fft-related. "
                                self.subfolder = num
                                print "self.subfolder =", self.subfolder # DT
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

                            # DT /*
                            # parsed_datasets_dict[self.fileName] = parsed_data
                            # print "sett:", sett
                            # print
                            # print "snap number :", num
                            # print " Ngroups    :", parsed_data[0]
                            # print " Nids       :", parsed_data[1]
                            # print " TotNgroups :", parsed_data[2]
                            # DT */

                            " Clear variable memory allocation, or store in dict"
                            parsed_data = self.dataparser_iter(parsed_data, num)

                            continue # to next 'num' (snapnum/fftfile)...
                        continue # to next iB...
                    continue # to next iA...
                continue # to next iN...
            continue # to next user-specified task...

        print "    Done with loop, now returning data. "
        # returns 'None'
        return self.datareturner(parsed_data)


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


    def dataparser_iter(self, parsed_data, num):
        """
        Handles the three cases of how data will be stored or not,
        through an iteration.

        * Long, multi-valued sets expected to blow out RAM should yet
          still be postprocessed before the iterating variable 'parsed_data'
          is wiped.
        
        * Small sets may be stored and returned to outerlying structure,
          i.e. on jupyter notebooks, to interact with after reading in
          a rather manual manner.
           # RAM availability is key to how many sets may be read at any
           # one time. 
             - Make a function to read RAM availability and allocate number?
               %TODO !

        * Single set runs should only return raw, non-post-processed data,
          for interpretation outside.
        """
        if   self.multiset == "wipe":
            " Case: Wipe the variable, return None "
            # When auto-post-processing functions are involved ahead of this
            return None

        elif self.multiset == "store":
            " Don't wipe completely; re-locate for storage "
            # self.parsed_datasets_dict[self.fileName] = parsed_data
            # return None   # temporary easy solution
            return self.storager(parsed_data, num) # proper solution, WIP

        elif self.multiset == False:
            " Single set case, return parsed data "
            return parsed_data
        else:
            print "Parse error"

        return 0


    def storager(self, parsed_data, num):
        """
        Stores the data into some kind of logical structure
        (? - feedback needed)

        ### Current proposal:
        3-leveled/indexed nested dictionary structure, shown below
        
        output_dataset  # -> variable stored to outside (of this) script
            |
            |--> ["{task/data category}"]
                          |
                          |--> ["{iN}{iA}{iB}"]
                                      |
                                      |--> ["{snapshotnumber}"]
                                                    |
                                                    |--> parsed_data
        - where 'parsed_data' as a variable contains
        several items from the reading of a snapshot's data
        (pertaining to the data type/category/"task").

        # Current function contains redundancies,
        # readability attempt.
        """
        task  =     self.what       # -- --> Outermost dictionary key 
                                       #   (already string).
        iN    = self.indraN         # -- --> These 3 form the middle key
        iA    = self.iA             # --^
        iB    = self.iB             # -^
        indra = "{0:1d}{1:1d}{2:1d}".format(iN,iA,iB)

        num   = "{0:02d}".format(num)   # -- --> Innermost key.

        if task not in self.datadict.keys():
            
            " Declaration of task-name-key "
            self.datadict[task] = { indra : { num : parsed_data } }
            pass # Out of 1st if's IF block

        else:

            " Case: dict already has the task-name-key "
            if indra not in self.datadict[task].keys():
                
                " Declaration of indra-key "
                self.datadict[task][indra] = { num : parsed_data }
                pass # Out of 2nd if's IF block

            else:

                " Case: dict already has indra-key "
                self.datadict[task][indra][num] = parsed_data
                pass # Out of 2nd if's ELSE block

            pass # Out of 1st if's ELSE block

        return 0


    def datareturner(self, parsed_data):
        """
        Handles the three cases of how data will be stored or not,
        through an iteration.

        * Long, multi-valued sets expected to blow out RAM should yet
          still be postprocessed before the iterating variable 'parsed_data'
          is wiped.
        
        * Small sets may be stored and returned to outerlying structure,
          i.e. on jupyter notebooks, to interact with after reading in
          a rather manual manner.
           # RAM availability is key to how many sets may be read at any
           # one time. 
             - Make a function to read RAM availability and allocate number?
               %TODO !

        * Single set runs should only return raw, non-post-processed data,
          for interpretation outside.
        """
        if   self.multiset == "wipe":
            " No need to return anything "
            pass

        elif self.multiset == "store":
            " Small set is returned "
            return self.datadict

        elif self.multiset == False:
            " Single set case, return parsed data "
            return parsed_data
            # (equal to:) return self.parsed_datasets_dict[self.fileName]

        else:
            print "Parse error"

        return 0



    def progressPrinter(self, symbol, num, sett):
        """
        Printout of programs current progress through folder systems
        """
        progress = """
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- 
        Currently reading:
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
            symbol=symbol,    sn=num,  snset=str(sett[0])+"..."+str(sett[-1])
            ).strip("[]")

        return 0


if __name__ == '__main__':
    print """
    Import 'read' and initialize, i.e.:
    'yourInstanceName = readDo()'
    'output = yourInstanceName(dictionaryOfDataParameters)'
    """