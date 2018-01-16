# ==============================================
# Argument interpreter for read.py's interface.
# ==============================================
import sys, os
import numpy as N







class readArgs(object):
    """
    Initializes which method to use for parameter initialization;
    Cmd-line reading or cfg-file reading. Some error messages.
    """
    def __init__(self):
        """
        Some versatile error messages included to environment...
        though; fairly sure long strings are conventionally not included to init,
            with regard to common practice in python classes? who cares!
        """
        self.argsOKtext = """
            All necessary parameters have been set. Continuing...
            """
        self.arglisterror = """
            Argument list discrepancy.
            Shutting down.\n"""
        self.inigo = "My name is Inigo Montoya. You killed my father.\
                        Prepare to die.\n\n\tExiting."
        # Error messages get boring after a while.
        self.length              = None  # LDT (from IDL debugs)
        self.sub_asks_for_length = False # enabling LDT for subhalo
        self.okGo                = False # checker for remote debugging 
        self.missingkeys_no = 0
        self.missingkeys    = []
        self.keys_read      = []
        self.onElephant = False # ---> To determine filesystem.
        self.onIdies    = False # _/
        self.plotdim2n3 = False # => True, when user wants plots in 2D+3D
        """
        Definitions of keywords to be used, script's interpretation +++.
        When adding a new user input parameter, write it into the below
        init-lists.
        If a new type-checker is needed for an individual purpose;
        then write a new function into the group of functions below.
        """
        self.arglist = [ # Parameter keys available
                "what"       , 
                "indraN"     , 
                "iA"         , 
                "iB"         , 
                "subfolder"  , 
                "fftfile"    , 
              # Optional stuff
                "tmpfolder"  ,
                "sfset"      ,
                "sortIDs"    ,
                "lessprint"  ,
                "box_params" ,
              # Output related
                "outputpath" ,
                "w2f"        ,
                "plotdata"   ,
                "plotdim"    ,
                "origamipath"
            ]
        self.param_incorp = { # Function library: parameter validation
                     "what" : self.taskname_incorp   ,
                   "indraN" : self.integer_incorp    ,
                       "iA" : self.integer_incorp    ,
                       "iB" : self.integer_incorp    ,
                "subfolder" : self.integer_incorp    ,
                  "fftfile" : self.integer_incorp    ,
              # Optional stuff
                "tmpfolder" : self.toggles_incorp    ,
                    "sfset" : self.toggles_incorp    ,
                  "sortIDs" : self.toggles_incorp    ,
                "lessprint" : self.toggles_incorp    ,
               "box_params" : self.boxparams_incorp  ,
              # Output related
               "outputpath" : self.outputpath_incorp ,
                      "w2f" : self.toggles_incorp    ,
                 "plotdata" : self.toggles_incorp    ,
                  "plotdim" : self.plotdim_incorp    ,
              "origamipath" : self.in_path_incorp
            }
        self.intRange_dict = { # Ranges of integer numbers.
                "indraN" : N.arange(0,8),
                    "iA" : N.arange(0,8),
                    "iB" : N.arange(0,8),
             "subfolder" : N.arange(0,64),
               "fftfile" : N.arange(0,505),
               "plotdim" : N.arange(2,4)
            } # Rember format: [x0, ..., x1 - 1]
        """
        Dictionaries: some default parameter values
        """
        self.read_params = \
            { # None-types are ignored in flow after validation.
                     "what" :["pos"],
                   "indraN" :   0   ,
                       "iA" :   0   ,
                       "iB" :   0   , 
                "subfolder" :  None , 
                  "fftfile" :  None ,
              # Optional stuff
                "tmpfolder" :   0   ,
                    "sfset" :   0   ,
                  "sortIDs" :   1   ,
                "lessprint" :   1   ,
               "box_params" :   0   ,
              # Output related
               "outputpath" :  None ,
                      "w2f" :   0   ,
                 "plotdata" :   1   ,
                  "plotdim" :   2   ,
              "origamipath" : None
            }

        """
        end of init
        """

    def callArgsChecker(self):
        """
        1. Collect parameters are !=None.
           1.1) Show user collected parameters.
        2. Check type(s) of 1.;
            Individual check for each expected type.
           2.1) Tuples or not
            a] Not: Proceed to 3.
            b] Tuple: Check contents for 2.
        3. Check boundaries of value, 
            one range corresponding to each type.
        """
        " 1. "
        self.collect_userArgs()

        " 1.1) Program initialized with... "
        self.loaded_parameters() # Screen-printed overview
        
        for key in self.keys_read:
            " 2. & 3., individual functions " 
            self.param_incorp[key](self.read_params[key], key)
            continue # Less output is good news!
        
        print self.argsOKtext
        return 0


    def collect_userArgs(self):
        """
        Collects parameters defined by user (not 'None').
        """
        # print " ** Inside self.collect_userArgs()"
        for key in self.arglist:

            " ### ! #### (deviation from the standard algorithm): "
            if key == "sfset":
                """
                At the moment, it's useful to determine whether 'sf'
                should be a set / range -: !!!Pre-emptively!!!
                """
                # print key
                # print key in self.read_params.keys()
                # print self.read_params
                # print self.read_params[key]
                # self.param_incorp[key]("not valid", "also not") # DT

                self.param_incorp[key](self.read_params[key], key)
                pass

            " Simple method to check if user forgot either of them "
            if self.read_params[key] == None:
                self.missingkeys.append(key)
                # self.keys_read.append(key) # Not useful to the user
                pass
            
            elif self.read_params[key] != None:
                self.keys_read.append(key)
                pass

            else:
                print " WTFery-error for key   " , \
                    key , ":" , self.read_params[key]
                pass

            continue

        if ("subfolder" not in self.keys_read) and \
                ("fftfile" not in self.keys_read):
            # Oh no!
            neither_fft_sf = """
            Parameters specified contain neither a snapshot number,
            nor an FFT file number. Please include at least one of these.
            """
            sys.exit(neither_fft_sf)

        return 0


    def loaded_parameters(self):
        """
        Screen-printed summary shows what values that  the user 
        has assigned as parameters for the arguments.
        """
        print "\n Total parameters loaded:", len(self.keys_read)
        print " Parameters initialized with values:"
        for key in self.keys_read:
            print "{0:>12s} : {1:>6s}".format( key, \
                   str(self.read_params[key]).strip("") )
            continue
        return 0


    def taskname_incorp(self, uinput, name="what"):
        """
        Incorporates user input task name(s).
        """
        tasknameErrortext = """
        Invalid task name specification(s), or format(s) thereof: {0}
        Allowed task names listed below.
        """.format(uinput)
        column_of_actions = "\t"
        for action in self.actionkeys:
            column_of_actions = column_of_actions+action+"\n"+(8*" ")
            continue

        if (type(uinput) == tuple) or \
            (type(uinput) == list):
            " When multiple tasks are input. "
            
            for taskname in uinput:
                " Check if each name is in library. "
                
                if (type(taskname) == str) and \
                    (taskname in self.actionkeys):
                    " Task name(s) accepted"
                    pass
                else:
                    sys.exit(tasknameErrortext.format(uinput)+column_of_actions)
                    break

                continue

            setattr( self, "what_set" , uinput )
            # Returns, having checked & stored both items in the set.
            return 0

        elif (type(uinput) == str) and \
            (uinput in self.actionkeys):
            " String object recognized, input is compared & stored. "
            setattr( self, "what_set" , uinput )
            # After storing, returns to next item to be checked
            return 0

        else:
            sys.exit(tasknameErrortext.format(uinput)+column_of_actions)
            # Aborts


    def integer_incorp(self, uinput, name):
        """
        Incorporates user input integer number for any ints
        """
        integererrortext = """
        Invalid number specified for {0}: '{1}'.
        Allowed range: integer in [{2},{3}]
        """.format(name, uinput,
                   self.intRange_dict[name][0], self.intRange_dict[name][-1])
        
        print 
        if type(uinput) == tuple or \
            type(uinput) == list:
            print " When multiple numbers are input. "
            
            print " Check if user's unput is in specified ranges "
            print len(uinput) <= 2, self.sfset == True
            print uinput 
            if  (len(uinput) == 2 and self.sfset == False) or \
                (len(uinput) <= 2 and self.sfset == True):
                print " (Case: User has specified a range) or "
                print " (Case: User has specified a set  ) "
                
                for single_number in uinput:
                    print " Check each number by range. "
                    
                    if (type(single_number) == int) and \
                        (single_number in self.intRange_dict[name]):
                        print " Value of number checks out! "
                        # No need to store anything.
                        pass

                    else:
                        sys.exit(integererrortext)

                    continue
                pass

            else:
                " Multiple values, but not in form of (lower,upper) or (set)!"
                sys.exit("""
            Parameter {0} requires exactly 1
                - or 2 (in tuple or list as lower- and upper-) -
            integer(s) as input variable(s).
            """.format(name))

            " Now, incorporate user input as instance variables "
            if self.sfset == True \
                and any([name == "sfset", name == "plotdim"]):
                " User input's set is applied directly "
                setattr( self, name+"_set" , uinput )
                # Should already by in an iterable form :)
                pass

            else:
                " User input's range is generated and applied "
                userRange = N.arange(uinput[0], uinput[1]+1 )
                setattr( self, name+"_set" , userRange )
                pass

            pass # Into return statement
        
        elif type(uinput) == int and \
            uinput in self.intRange_dict[name]:
            " Single int object case recognized. "
            
            setattr( self, name+"_set" , N.arange(uinput, uinput+1) )
            pass                         # Single item list ^            

        else:
            sys.exit(integererrortext)
            # Aborts

        return 0


    def toggles_incorp(self, uinput, name):
        """
        Incorporates user input toggle's state.
        """
        # print " ** Inside self.toggles_incorp! "
        # print " ** key =", name, "| uinput =", uinput
        # print "type(1) ==", type(1), "type(True) ==", type(True)

        toggleserrortext = """
        Invalid value specified for {0}: '{1}'.
        Allowed values: [ 0 , 1 ] / [ False, True ]
        """.format(name, uinput)

        if (type(uinput) == int and uinput in N.range(0,2)) or \
            type(uinput) == bool:
            " Allowed object recognized then input is recognized. "
            setattr( self, name, uinput )
            return 0
            # After storing, returns to next item to be checked

        else:
            sys.exit(toggleserrortext)
            # Aborts


    def boxparams_incorp(self, uinput, name):
        """
        Incorporates box parameters' boundaries into the envirinonment.
        """
        # print " ** Inside self.boxparams_incorp! "
        # print " ** key =", name, "| uinput =", uinput
        if type(uinput) == list or type(uinput) == tuple:
            " So, uinput consists of some objects "
            
            for pair in uinput: # 3 items.
                " Check that all items in uinput are also on this form "
                
                if type(pair) == list or type(pair) == tuple:
                    " Now check if they contain 2 numbers "

                    if len(pair) == 2 and \
                        any(
                            [all(map(lambda x: hasattr(x, '__float__'), pair)),
                             all(map(lambda x: hasattr(x, '__int__'), pair))]
                           ):
                        " Makes sure that each numbers are float or int. "
                        setattr(self, name, uinput)
                        pass

                    pass
                continue # 3 items.
            pass

        elif uinput == False:
            pass

        else:
            sys.exit("""
        Parameters given for box invalid.
        Please provide 3 by 2 object (list or tuple).
        """)

        return 0


    def plotdim_incorp(self, uinput, name):
        """
        Interprets if user wants 1 plot of either 2D or 3D;
        or both.
        """
        if  hasattr(uinput, '__iter__')                       and    \
            all(map(lambda x: hasattr(x, '__int__'), uinput)) and    \
            all(map(lambda x: x in self.intRange_dict[name], uinput)):
            " Case 1.:  user wants both 2D _and_ 3D plot "
            " 1.1:      User's iterable's object contains int-types "
            " 1.2:      Are all numbers given either 2 or 3? "
            self.plotdim2n3 = True
            pass

        elif hasattr(uinput, '__int__')   and \
            uinput in self.intRange_dict[name]:
            " Case 2.:  User wants a single plot in either 2D _or_ 3D "
            " 2.1:      Is number input either 2 or 3?"
            pass

        else:
            sys.exit("\n Plot's dim: not int or iterable of ints \n")

        " All tests passed: apply dimension set to instance! "
        setattr(self, name, uinput)

        return 0 


    def outputpath_incorp(self, uinput, name):
        """
        Interprets where output should be stored
        """
        # print " ** Inside self.outputpath_incorp! "
        # print " ** key =", name, "| uinput =", uinput

        if uinput != False and \
            type(uinput) == str:
            " Then user has a specific output path in mind! "
            setattr(self, name, uinput)
        elif uinput == False:
            """
            Allows program to decide where output should be stored:
            [ ~/indraData/{what}_{indraN}{iA}{iB}{tmp/None}_sf{sf}/ ]
            """
            setattr(self, name, uinput)
            pass
        else:
            sys.exit("""
        Invalid address/type for specified output path.
        """)

        return 0


    def in_path_incorp(self, uinput, name):
        """
        Incorporates origami's path as environment variable.
        """
        if type(uinput) == str:
            setattr(self, name, uinput)
            pass
        # Well, how strict can one be with a user's own preferences?
        return 0 


    def errhand_userinput(self, problemstring):
        """
        Error handling, with user input enabling: 
        * Error message
        * User input
        * Recursion in case of stupid
        """
        ok2go = raw_input(problemstring+" Please input (1/0) or (y/n) : ").lower()
        if ok2go == "n" or ok2go == "0":
            
            sys.exit("""
                ---------------------------
                 Dataset analysis aborted. 
                ---------------------------
                """)
            return False

        elif ok2go == "y" or ok2go == "1":
            
            print """
                +++++++++++++
                 Continuing.
                +++++++++++++
                """
            return True # the only way out!

        else:
            self.errhand_userinput(problemstring)

        return 0


    def intendedMachine(self):
        """
        Simple function that exits the program...
          - in the case that indra/origami dataset
            is not available on the system -
          ...before further reading.
        Used to clean up syntax while debugging.
        """
        systemName = os.uname()[1]
        myLaptopName          = "DESKTOP-MR1LV6A"
        clusterName           = "elephant"
        runningLocallyMessage = """
        Running locally, and has reached the end of the rainbow.
        Time to upload and test! Now exiting.
        """
        unknownOrigin = " Instead, it seems this is r" \
                      + runningLocallyMessage[11:66]\
                      + "\n You may choose to debug program locally"\
                      + " if you wish."\
                      + "\n Is this your intention?"

        if systemName == myLaptopName:
            # ..going to assume that I indeed want to debug shit; commented out.
            # sys.exit(runningLocallyMessage)
            pass
        elif systemName == clusterName:
            # Datascope base file structure path.
            self.onElephant = True
            self.dsp = "/datascope" # indra pathing follows
            ###### Modify as needed.
            pass
    
        elif os.path.exists("/home/idies"):
            # On SciServer Idies etc
            self.onIdies = True
            self.dsp = "/home/idies" # indra follows

        else:
            print "\n\tNot running from intended machine(s)"\
                  + " ('elephant' cluster or SciServer)."
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
    # run read.py instead