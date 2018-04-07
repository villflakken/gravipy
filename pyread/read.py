# ==============================================
# Indra data sets' reading MO.
# ==============================================
import os, sys, glob, time, gc
import numpy as N
import subprocess as sp
from read_args import readArgs
from read_procedures import readProcedures



def read_ini( what        = "pos" ,
              indraN      =  0    , 
              iA          =  0    , 
              iB          =  0    ,
              subfolder   = None  ,    
              fftfile     = None  ,
              tmpfolder   = False ,
              sfset       = False ,
              sortIDs     = False ,
              lessprint   = True  ,
              multiset    = False ,
              box_params  = False ,
              outputpath  = False ,
              w2f         = False ,
              plotdata    = False ,
              plotdim     =  [2]  ,
              origamipath = False
            ):

    data_params = { # Data structure parameters:
               "what" :([ what       ]),
             "indraN" :(  indraN      ),
                 "iA" :(  iA          ),
                 "iB" :(  iB          ),
          "subfolder" :(  subfolder   ),
            "fftfile" :(  fftfile     ),
            # Reading options:
          "tmpfolder" :(  tmpfolder   ),
              "sfset" :(  sfset       ),
            "sortIDs" :(  sortIDs     ),
          "lessprint" :(  lessprint   ),
           "multiset" :(  multiset    ),
            # Extracts data from a coordinate box at positions specified:
         "box_params" :(  box_params  ),
            # Desired output filepath, 
            # or False (=> program storing to user's own folder).
         "outputpath" :(  outputpath  ),
            # Write 2 file: Probably a bad idea ...
                "w2f" :(  w2f         ),
           "plotdata" :(  plotdata    ),
            # Apply floats as "([min,max], [min,max], [min,max])" in Mpc/h units,
            # respectively for directions x, y, z. # Turned off w/: None/False
            "plotdim" :(  plotdim     ), # Dimensions projected in plot
            # Origami functionality
        "origamipath" :(  origamipath )
    }

    tmp = sp.call('clear',shell=True)

    ini = readDo()                  # Initialize!
    ini.read_params = data_params   # Set params
    " 1. "
    ini.callArgsChecker()           # Verify values
    " 2. "
    return ini.beginReading(), ini  # Do the thing


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
        # self.version = "fsu00" # Earlier version of the system
        self.version = "fsu01" # Version-control-notation, wrt. output folders
        """
        Actiondicts : commands for the program to act on
        """
        # Function library for initializing actual data _reading_.
        self.action  = { 
            "pos"     : self.read_posvel  , 
            "vel"     : self.read_posvel  , 
            "fof"     : self.read_fof     , 
            "subhalo" : self.read_subhalo , 
            # "fft"     : self.read_fft     ,
            "origami" : self.read_origami ,
            "time"    : self.read_time
        }
        self.actionkeys = [ # Types of data available to read.
            "pos"     ,
            "vel"     ,
            "fof"     ,
            "subhalo" , 
            "origami" ,
            # "fft"     , # currently not a feature
            "time"
        ]
        
        # Specific processing routines (c.f.: 'read_autotools.py'),
        # format: dict = {'user input command' : ('data', 'types', 'involved') }
        self.singleSnapActions = {
            "posor"    : [ "pos", "origami"            ] ,
            "pof"      : [ "pos", "fof"                ] ,
            "porifof"  : [ "pos", "origami", "fof"     ] ,
            "playOne"  : [ "pos", "origami", "fof"     ] # Dev. tests
        }
        self.allSnapActions = {
            "sufo"     : [ "subhalo", "fof"            ] ,
            "sofa"     : [ "subhalo", "origami", "fof" ] ,
            "playAll"  : [ "subhalo", "origami", "fof" ] # Dev. tests
        }
        # self.allSnapActions[self.what_set] => substitutes
        self.singleSnapActions_bools = { # Used for checking 'ppSingleSnaps' status;
        }                                # is modified in 'read_args.py'
        self.allSnapActions_bools = {    # Used for checking 'ppAllSnaps' status;
        }                                # is modified in 'read_args.py'

        # Determines which datasets are allowed to store variables:
        self.AllowedDataAccumulation = [
            "fof"     ,
            "subhalo" ,
            "origami"
        ] #( i.e.: storing 64 snaps of 'pos'-data will definitely kill the RAM!)

        self.teststring = "\n   This is the test \n"
        """
        End of init
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
        self.datadict = {} # cf. function 'self.generalStorager()': The final, returned dict.
        self.theTimeData() # Adds 'scale factor' & 'redshift data' to the set
        # Useful by only being declared _once_. # snap Index:
        self.sIndex = N.arange(0, len(self.subfolder_set))
        """
        Prime example on how complex a set of permutations can become!:
        """
        for iN in self.indraN_set:
            " Current indraN as globvar "
            self.indraN = iN
            for iA in self.iA_set:
                " Current iA as globvar "
                self.iA = iA
                for iB in self.iB_set:
                    " Current iB as globvar "
                    self.iB = iB
                    # Useful for dictionary addresses & file names
                    self.iString = "{0:1d}{1:1d}{2:1d}".format(iN,iA,iB)
                    
                    # Indra variables set. Check task set:
                    if   self.what_set in self.singleSnapActions.keys():
                        " Calls algorithm that avoids RAM overload "
                        parsed_data = self.performSingleSnaps()
                        pass

                    elif self.what_set in self.allSnapActions.keys():
                        " Calls algorithm that potentially stores all given snapshots "
                        parsed_data = self.performAllSnaps()
                        pass

                    else:
                        " Basic indra data reading "
                        parsed_data = self.performBasicOps()

                    continue #:next iB
                continue #:next iA
            continue #:next iN
        # end.FOR:all
        
        self.keychainer() # Adds the keys for self.datadict, & its subdicts,
                          # to be items in the (outermost) dictionary itself,
                          # in a readable &/ sorted manner.

        print "    Done with loop, now returning data. "
        return self.datareturner(parsed_data) # Requested data returned here
            # Program is done!


    def performBasicOps(self):
        """
        Performs the basic Indra reading, data structure building, etc.
        * May return single pos-sets, or single/lesser/all sofa data sets
        """
        for subfolder in self.subfolder_set:
            " Current subfolder/fftfile as globvar. "
            self.subfolder = subfolder

            for task in self.what_set:
                " Current task as globvar (global variable) "
                self.what = task
                self.progressPrinter(subfolder)

                " Task function call: "
                parsed_data = self.action[self.what]()
                # \=>: Main component of entire program: Reading.

                " IF-block below handles pp and output "
                if any([self.w2f, self.plotdata]) == True:
                    " Handles data post processing - during. "
                    self.ppBasic(parsed_data, self.subfolder)
                    
                    if subfolder == self.subfolder_set[-1]:
                        " Handles data post processing - end of subfolder set. "
                        self.ppBasicLast(parsed_data, self.subfolder)
                        pass # end.IF: last snap

                    pass # end.IF: pp & output
                
                " Clear variable's memory allocation, or store in dict"
                parsed_data = self.dataParserIter(parsed_data, self.subfolder)

                continue #:next task

            continue #:next snapnum...

        return parsed_data


    def performSingleSnaps(self):
        """
        Performs reading and processing for multiple tasks, on a single snap.
        * Combinations' operations determined through:
            - user inputs name of a specific combination,
            - 'readDo.__init__'s structure,
            - contents of pp-function in question

        any([self.autocombo_bools[key] 
            for key in self.autocombo.keys()])
        """
        # TODO not done

    
        # May develop this one into a function that retrieves a set of tasks to do 
        self.taskSingles = self.singleSnapActions[self.what_set] 
        
        for subfolder in self.subfolder_set:
            " Current subfolder/fftfile as globvar. "
            self.subfolder = subfolder

            " Data dict for processing in type combination - singular snaps "
            self.data1dict = {}

            for task in self.taskSingles:
                " Current task as globvar (global variable) "
                self.what = task
                self.progressPrinter(self.subfolder)

                " Task function call: "
                parsed_data = self.action[self.what]()
                # \=>: Main component of entire program: Reading.

                " IF-block below handles pp and output "
                if any([self.w2f, self.plotdata]) == True:
                    " Handles data post processing - during. "
                    self.ppSingleSnaps(parsed_data, self.subfolder)
                        # temp. storage for pp-data is self-contained
                        # inside self.'ppSingleSnaps'
                    pass # end.IF: pp & output
                
                " Clear variable's memory allocation, or store in dict"
                parsed_data = self.dataParserIter(parsed_data, self.subfolder)
                continue #:next task

            " Clears dict for next iteration, if there is one "
            self.data1dict.clear() 
                # i.e.: Positions take up a lot of memory!
            continue #:next snapnum...

        return parsed_data

        
    def performAllSnaps(self):
        """
        Performs reading and processing for multiple tasks, on a single snap.
        * Combinations' operations determined through:
            - user inputs name of a specific combination,
            - 'readDo.__init__'s structure,
            - contents of pp-function in question

        any([self.autocombo_bools[key] 
            for key in self.autocombo.keys()])
        """

        " Data dict. for processing in type combination - all snaps in set "
        self.dataAlldict = {}

        # taskAlls = ...

        for subfolder in self.subfolder_set:
            " Current subfolder/fftfile as globvar. "
            self.subfolder = subfolder

            for task in self.allSnapActions[ self.what_set ]:
                " Current task as globvar (global variable) "
                self.what = task
                self.progressPrinter(subfolder)
                self.auto_outputPather() # Creates fitting strings
                # Declare the condition for beginning pp at end of set
                self.allCond = subfolder is self.subfolder_set[-1] \
                    and task is self.allSnapActions[ self.what_set ][-1]

                " Task function call: "
                parsed_data = self.action[self.what]()
                # \=>: Main component of entire program: Reading.

                " IF-block below handles pp and output "
                if any([self.w2f, self.plotdata]) == True:
                    " Handles data post processing - during. "
                    self.ppAllSnaps(parsed_data, self.subfolder) 
                    # Function will initiate more specific processing
                    pass # end.IF: pp & output
                
                " Clear variable's memory allocation, or store in dict"
                parsed_data = self.dataParserIter(parsed_data, self.subfolder)

                continue #: Next task
            continue     #: Next snapnum...

        " Clears dict and pp cond for next outside iteration "
        self.dataAlldict.clear()
        self.allCond = False

        return parsed_data


    def dataParserIter(self, parsed_data, num):
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

        * This function's output is then sent along to self.generalStorager(X,Y);
          iow.: this function's output is what potentially be stored within 
          object's instance (and also)/(or simply) returned objects.
        """
        if   self.multiset == "wipe":
            " Case: Wipe the variable, return None "
            # i.e.: When auto-post-processing functions are performed
            return None # Namespace will be overwritten on the outside

        elif self.multiset == "store":
            " Don't wipe completely; re-locate for storage "
            return self.generalStorager(parsed_data) # proper solution
                                                   # WIP (# done..!(?))

        elif self.multiset == False:
            " Single set case, return parsed data "
            return parsed_data

        else:
            print "Parse error"
            pass # function returns 0/False

        return 0


    def generalStorager(self, parsed_data):
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
        """
        task  = self.what           # -- --> Outermost dictionary key, str-type
        iN    = self.indraN         # -- --> These 3 form the middle key
        iA    = self.iA             # --^
        iB    = self.iB             # -^
        # indra = "{0:1d}{1:1d}{2:1d}".format(iN,iA,iB)
        indra = self.iString
        num   = self.subfolder      # -- --> Innermost key.

        # NB: self.datadict was declared in 
        #     the beginning of self.beginReading()

        " See if current task's data is _allowed_ to store "
        if task in self.AllowedDataAccumulation:
            " Then put in its correct dictionary "
            self.dictMaker(parsed_data, self.datadict, task, indra, num)
            pass # end.IF 0

        return 0


    def dictMaker(self, parsed_data, dictname, task, indra, num):
        """
        Contains the versatile if tests that make up
        the dictionary updating sequence.
        """
        if task not in dictname.keys():
            " Declaration of task-name-key "
            dictname[task] = { indra : { num : parsed_data } }
            pass # end.IF 1

        else:
            " Case: dict already has the task-name-key "
            if indra not in dictname[task].keys():
                
                " Declaration of indra-key "
                dictname[task][indra] = { num : parsed_data }
                pass # end.IF 2

            else:

                " Case: dict already has indra-key "
                dictname[task][indra][num] = parsed_data
                pass # end.ELSE 2
            pass # end.ELSE 1

        return 0


    def keychainer(self):
        """
        Adds the keys for self.datadict, & its subdicts,
        to be items in the (outermost) dictionary itself,
        in a readable &/ sorted manner - and as strings!
        """
        " 1: Best tasks-key sorting: the order in which they were input "
        self.datadict["tasks"] = N.array(self.what_set)

        " 2: Sorting indra-keys by numeral value " # Only relevant for multiple simulations
        if self.multiset == True: 
            
            self.datadict["indrakeys"] = N.array(sorted(
                self.datadict[self.what_set[0]].keys(),
                key=float 
            ))
            # NB: No. of indra simulations is equal
            #     for each performed task in self.what_set!
            pass

        " 3: Sorting snap-keys by their numeral value "
        # self.datadict["snapkeys"] = N.array(self.subfolder_set)
        # # Would already be sorted
        # => But not flexible enough w.r.t. potential fft-files.

        if "fft" in self.what_set:
            self.datadict["fftkeys"] = N.array(self.fftfile_set)
            pass

        # Preparing the next, iterative IF-block
        not_fft_actions = self.actionkeys[:] # Element copy; not reference copy!
        not_fft_actions.remove("fft")
        if any(map(lambda x: x in self.what_set, not_fft_actions)):
            self.datadict["snapkeys"] = N.array(self.subfolder_set)
            # There will only be one set of subfolders, anyway.
            pass

        # %TODO
        # Make documentation entry in dict structure somehow like this;
        # and make it parallell to some function in class that may return similar
        # information.
        self.datadict["--help"] = {}

        self.datadict["--help"]["pos"] = """\
          * output object of a 'pos'-related object is:
        tuple(
            IDs         , # numpy array
            pos         , # numpy array
            scalefactor , # scalar value
            rs_value      # scalar value
        )
        """

        self.datadict["--help"]["fof"] = """\
          * output object of a 'fof'-related object is:
        tuple(
            fofIDs      , # numpy array
            TotNgroups  , # scalar value
            GroupLen    , # numpy array
            GroupOffset   # numpy array
        )
        """

        self.datadict["--help"]["fof"] = """\
          * output object of a 'fof'-related object is:
        tuple(
            subIDs      , # numpy array
            TotNgroups  , # scalar value
            catalog       # dictionary with LOTS of details
        )
        """

        self.datadict["--help"]["origami"] = """\
          * output object of an 'origami'-related object is:
        tuple(
            tags  , # numpy array
            Npart   # scalar value
        )
        """

        print " Returned dictionary's keychain complete "
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
            # (equal to:) return self.datadict[self.fileName]

        else:
            print "Parse error"
            pass

        return 0


    def progressPrinter(self, num):
        """
        Printout of programs current progress through folder systems
        """
        progress = """ * i{iN:1d}{iA:1d}{iB:1d} > {task:8} (/{oftasks}) > snap:{sn:02d}"""
        print progress.format(
            task    = self.what,     
            oftasks = self.what_set, 
            iN      = self.indraN,   
            iA      = self.iA,       
            iB      = self.iB,       
            sn      = num
        )
        return 0


    def theTimeData(self):
        """
        Simply adds the redshift values to the dataset
        """
        scalefactors = N.array([0.0078125,    0.0123457,    0.0196078,
        0.0322581,    0.0478106,    0.0519654,    0.0564194,    0.0611881,
        0.066287,     0.0717322,    0.0775397,    0.0837254,    0.0903055,
        0.0972961,    0.104713,     0.112572,     0.120887,     0.129675,
        0.13895,      0.148724,     0.159012,     0.169824,     0.181174,
        0.19307,      0.205521,     0.218536,     0.232121,     0.24628,
        0.261016,     0.27633,      0.292223,     0.308691,     0.32573,
        0.343332,     0.361489,     0.380189,     0.399419,     0.419161,
        0.439397,     0.460105,     0.481261,     0.502839,     0.524807,
        0.547136,     0.569789,     0.59273,      0.615919,     0.639314,
        0.66287,      0.686541,     0.710278,     0.734031,     0.757746,
        0.781371,     0.804849,     0.828124,     0.851138,     0.873833,
        0.896151,     0.918031,     0.939414,     0.960243,     0.980457, 1])

        redshifts = N.array([127, 79.9999, 50.0001, 30, 19.9159, 18.2436,
        16.7244   , 15.343    , 14.0859   , 12.9407   , 11.8966   , 10.9438 ,
        10.0735   , 9.2779    , 8.54991   , 7.8832    , 7.27219   , 6.71159 ,
        6.19683   , 5.72386   , 5.28883   , 4.88845   , 4.51956   , 4.17947 ,
        3.86568   , 3.57591   , 3.3081    , 3.06042   , 2.83118   , 2.61886 ,
        2.42204   , 2.23949   , 2.07003   , 1.91263   , 1.76634   , 1.63027 ,
        1.50364   , 1.38572   , 1.27585   , 1.17342   , 1.07787   , 0.988708,
        0.905462  , 0.827699  , 0.755036  , 0.687109  , 0.62359   , 0.564177,
        0.508591  , 0.456577  , 0.407899  , 0.36234   , 0.319703  , 0.279802,
        0.242469  , 0.207549  , 0.174898  , 0.144383  , 0.115883  , 0.0892878, 
        0.0644934 , 0.0414031 , 0.0199325 , 2.22045e-16])

        self.datadict["time"] = {"scale" : scalefactors, "redshift" : redshifts}
        return 0


    def currentTaskParamsParser(self):
        """
        Sets some reading parameters into the environment's current scope,
        because FFT as a task would be different than others, bla bla.
        Also, working along with self.progressPrinter(X,Y,Z).
        """
        if self.what != "fft":
            # Second condition probably redundant condition, but 
            " if not 'fft', then 'subfolder' systems! "
            sett     = self.subfolder_set
            symbol   = "subfolder"
            pass

        elif self.what == "fft":
            " if 'fft', then fftfiles! "
            sett     = self.fftfile_set
            symbol   = "fftfile"
            pass

        else:
            sys.exit("Task name does not conform to any allowed.")

        return sett, symbol


if __name__ == '__main__':
    print """
    Import 'read' and initialize, i.e.:
    'yourInstanceName = readDo()'
    'output = yourInstanceName(dictionaryOfDataParameters)'
    """