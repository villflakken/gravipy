# ==============================================
# Argument interpreter for read.py's interface.
# ==============================================
import sys, os



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
        self.ArgError1 = """ You have attempted to read either of the data sets: 
                                
            positions ("pos"),
            velocities ("vel"),
            both ("posvel");
            Incorrect cmdl arg usage.

              6 arguments are needed in total:
            1: What data to read            : str(<data set name string>)
            2: indraN                       : int(#) in [ 0,   7 ]
            3: iA                           : int(#) in [ 0,   7 ]
            4: iB                           : int(#) in [ 0,   7 ]
            5: snapshot directory           : int(#) in [ 0,  63 ]
            6: redshift toggle              : int(0, 1)

            Wanted to read "fof"/"subhalo"/"fft"?
            Then 5 arguments, where:
            5: snapshot directory (sdirC)   : int(#) in [ 0,  63 ]
            5: subhalo directory (subdirC)  : int(#) in [ 0,  63 ]
            5: FFT file (fftdirC)           : int(#) in [ 0, 504 ]
            =============================================================
            """

        self.ArgError2 = """ You have attempted to read either of the data sets:
                                
            friend of friend data ("fof"/"FOF"),
            subhalo ("subhalo"),
            FFT ("fft"/"FFT");
            Incorrect cmdl arg usage.

              5 arguments are needed in total:
            1: What data to read            : str(<data set name string>)
            2: indraN                       : int(#) in [ 0,   7 ]
            3: iA                           : int(#) in [ 0,   7 ]
            4: iB                           : int(#) in [ 0,   7 ]
            5: snapshot directory (sdirC)   : int(#) in [ 0,  63 ]
            5: subhalo directory (subdirC)  : int(#) in [ 0,  63 ]
            5: FFT file (fftdirC)           : int(#) in [ 0, 504 ]

            Wanted to read "pos"/"vel"/"posvel"?
            Then 6 arguments,  where:
            5: snapshot directory           : int(#) in [ 0,  63 ]
            6: redshift toggle              : int(0, 1)
            =============================================================
            """
        self.argsOKtext = """
        All necessary parameters have been set. Continuing...
        """
        self.arglisterror = \
            """\n\nSomething has changed the values in arglist if this comes up.
                Shutting down.\n\n"""

        self.inigo = "My name is Inigo Montoya. You killed my father. \
                        Prepare to die.\n\n\tExiting."
        # Error messages get boring after a while.        
        """
        end of init
        """

    def initArgs(self):
        """
        This class functionality's 'main' module.

        Initializes which dataset to read from and what to do with it.
        Will have to work on optional multiple dataset comparisons.
        Or modularize even further.
        """
        self.ErrorType1 = False
        self.ErrorType2 = False
        self.cfg_init_str = "\n Initializing read.py using config file.\n"

        """
        Course of action depending on how software is applied
        * if list(functioncall) contains any elements,
          args_from_function() engages.
        """
        if any(self.functioncall) == True:
            # When program is initialized from an imported function.
            self.args_from_function(self.functioncall)
            pass
        else:
            # When program is initialized from cmdline or file.
            self.cmdline_and_cfg()
            pass

        """
        Quick summary shows keys that are now read with their values.
        """
        self.loaded_parameters()

        """
        In case user screws up arguments in cfg or runs from cmdline
        - where not all values may be specified - ;
        ask here to load in some defaults.
        """
        self.properArgsChecker()

        """
        self.read_params' values should have been read successfully by now.
        Now: Verify bounds & ranges in self.read_params vs. absolute params.
        """
        self.boundCheckNValues()

        """
        Set program envornment's ranges,
        from the now double-checked user input
        """
        self.userRanges()

        print self.argsOKtext
        return 0

    def loaded_parameters(self):
        """
        Quick summary shows keys that are now read with their values.
        """
        print "\n Total parameters loaded:", len(self.keys_read)
        print " Parameters initialized with values:"
        for key in self.keys_read:
            print "{0:>10s} : {1:>5s}".format( key, \
                   str(self.read_params[key]).strip("[]") )
            continue
        return 0


    def args_from_function(self, plist):
        """
        When program is initialized by way of
        an outisde function call for reading.
        """
        self.taskNameAppender(         plist[0] )
        self.read_params[ "indraN" ] = plist[1] 
        self.read_params[ "iA" ]     = plist[2] 
        self.read_params[ "iB" ]     = plist[3] 
        
        if "fft" not in self.read_params[ "what" ]:
            " When subfolder structures are read "
            self.read_params[ "subfolder" ] = plist[4]
            pass
        else:
            " When fft-file is read "
            self.read_params[ "fftfile" ]   = plist[5]
            pass

        self.read_params["sortIDs"]    = plist[ 6]
        self.read_params["lessprint"]  = plist[ 7]
        self.read_params["tmpfolder"]  = plist[ 8]
        self.read_params["w2f"]        = plist[ 9]
        self.read_params["plotdata"]   = plist[10]
        self.read_params["outputpath"] = plist[11]

        self.paramsdict_keys_read()
        
        return 0

    def callArgsChecker(self):
        """
        I now have officially too many ways of reading arguments into the class.
        """
        # read_params has been updated directly into the class call
        " Stores which parameters have been defined by the user: "
        self.paramsdict_keys_read()
        " Summary of loaded parameters "
        self.loaded_parameters()
        self.properArgsChecker()
        self.boundCheckNValues()
        self.userRanges()
        print self.argsOKtext
        return 0


    def cmdline_and_cfg(self): 
        """ 
        When program is NOT initialized by way of 
        an outside function call for reading.
        """
        if len(sys.argv) > 2:
            """
            First investigate cmd-line versions of parameter settings.
            """
            self.argsFromCmdLine()
            pass


        elif len(sys.argv) == 2 or len(sys.argv) == 1:
            """
            Loading a script for more advanced options.
            """
            try:
                if str(sys.argv[1].lower()) == "cfg":
                    """
                    When 'cfg' is specified as cmdline arg, which means
                    when len(sys.argv) == 2, as per the following test:
                    """
                    pass
                else:
                    pass
                pass

            except IndexError:
                if len(sys.argv) == 1:
                    """
                    The other case,
                    blank cmdline arguments after script name.
                    """
                    pass
                else:
                    """
                    Just in case user typed some gibberish.
                    """
                    sys.exit("\nUnknown command. Exiting.\n")
                    # no pass >:(
                pass
            print self.cfg_init_str
            self.loadfile() # loads & reads cfg-file
            pass

        else:
            """
            For when no combination of arguments seem to work.
            """
            UnexErr = \
            "Unexpected error. Doom follows."\
            + "Try get your args straight..."\
            + " All of them."
            print "================="
            sys.exit(UnexErr*7 + UnexErr[:int(len(UnexErr)/2.)] + "\n\n"
                     + sys.exc_info())

        return 0


    def argsFromCmdLine(self):
        """
        What the program does to store arguments from cmdline
        """
        if sys.argv[1].lower() in ("pos", "vel", "posvel"):
            """
            When reading positions and velocities from argv.
            """
            self.ErrorType1           = True
            self.DataGroupErrorString = "Trouble in pos/vel/posvel"

            self.taskNameAppender(                sys.argv[1] )
            self.read_params["indraN"]    = eval( sys.argv[2] )
            self.read_params["iA"]        = eval( sys.argv[3] )
            self.read_params["iB"]        = eval( sys.argv[4] )

            self.read_params["subfolder"] = eval( sys.argv[5] )
            pass

        elif sys.argv[1].lower() in ("fof", "subhalo", "fft"):
            """
            When reading friend-of-friend data, 
            subhalo data, or fft data from argv.
            """
            self.ErrorType2            = True
            self.DataGroupErrorString  = "Trouble in fof/subhalo/fft"

            self.taskNameAppender(             sys.argv[1] )
            self.read_params["indraN"] = eval( sys.argv[2] )
            self.read_params["iA"]     = eval( sys.argv[3] )
            self.read_params["iB"]     = eval( sys.argv[4] )

            if self.read_params["what"][0]  == "fof"   or \
                self.read_params["what"][0] == "subhalo":
                " fof or subhalo reading "
                self.read_params["subfolder"] = eval( sys.argv[5] )
                pass

            elif self.read_params["what"][0] == "fft":
                " fft reading "
                self.read_params["fftfile"]   = eval( sys.argv[5] )
                pass

            else:
                print "Unrecognized name of data set"
                print "Consult either of below error messages:\n\n"
                print self.ArgError1
                print self.ArgError2
                print sys.exc_info()
                self.bep()
                sys.exit()
        else:
            pass

        self.paramsdict_keys_read()

        return 0


    def loadfile(self):
        """
        Attempts to read files, w/ all errors that i care to implement
        """
        filepath_cfgfile = os.path.join(os.path.dirname(__file__), '')\
                                        + "read_cfg"
        linecount           = 1

        with open(filepath_cfgfile, 'r') as open_cfgfile:
            """
            Open safely, as always! ^^
            """
            
            for line in open_cfgfile:
                """
                For every line in the cfg-file --
                """
                line = line.strip().lower()
                linecount += 1 # compare total lines read vs. key lines read
                errorstring = \
                """
                Something went wrong!
                Can't read line from read_cfg. Check syntax! Line below:
                ========================================================
                """+"\n"+line+"\n\n Continue anyway?"

                for key in self.arglist:
                    """
                    -- go through every keyword that should be
                    interpreted &/ found --
                    """
                    if line.startswith(key.lower()):
                        """
                        -- checks if the line starts with
                        one of the keywords given --
                        # .lower() here counters potential mix up from user
                          of uppercase letters in cfg variables..
                        """ 
                        self.keys_read += [key]
                        
                        try:
                            """
                            -- now interpret and set the value from that line,
                            with its corresponding keyword in the dictionary!
                            """
                            self.lineInterp(key, line)
                            # line interpreter further below

                        except:
                            print "\n\n    ",\
                                  "Exception in line's type recognition   \n\n"
                            print self.bep()

            open_cfgfile.close()

        return 0


    def paramsdict_keys_read(self):
        """
        Because I've implemented a check to compare read vs. unread
        arguments and/or keys;
        and to load default values into unread items!
        """
        for key in self.arglist:
            
            if self.read_params[key] == None:
                self.missingkeys.append(key)
                self.keys_read.append(key)
                pass
            
            elif self.read_params[key] != None:
                self.keys_read.append(key)
                pass

            else:
                print "Type-value error for key   " , \
                        key , ":" , self.read_params[key]
                pass

            continue
        return 0


    def taskNameAppender(self, stringOfTasks):
        """
        Very simple method, reads string of task names;
        splits these up into singular command functions;
        will be verified later.
        """
        tasklist = stringOfTasks.lower().split(',')
        for taskname in tasklist:
            self.taskNameSetter(taskname.strip())
            continue

        return 0


    def lineInterp(self, key, line):
        """
        Interprets each line's properties;
        depends on which key of read_params is active.
        / Remember: 
          * key is a 'key' for the dict containing
             the selection of parameter args.
          * obj becomes 'key' for the dict that determines
             what action to perform; the parameter arg's 
             value of what to read.
        """
        obj = line[line.find("=")+1:].strip().lower()
                # uppercase is lowered to conform with self.actionkeys
        
        ThereIsNoDotInHere = -1
        if obj.find(".") == ThereIsNoDotInHere:
            " No punctuations (.) are in the line " # or nipples
            pass
        else:
            print
            print "Reading line:"
            print line
            print 
            print 'Please do not use dot punctuations, ".", in cfg file.'
            sys.exit("\n\n Edit your cfg. Now exiting.")

        """
        ==============================
        |   WHAT string assignment   |
        ==============================
        """
        
        if key == "what":
            """
            Tupled or single task names!
            """
            self.taskNameAppender(obj)
            pass

            """
        All keys except "what":
        ============================
        |   TUPLES' values below   |
        ============================
        """
        elif key != "what"               and \
            isinstance(eval(obj), tuple) and \
            key not in self.toggles:
            """
            Catches on:
            * Items not expected to be strings for 'what'
            * Tupled items
            * Non-toggled items
            """

            if any(self.tuple_parameters) == False:
                " Create list with tupled key, if list is empty. "
                self.tuple_parameters = [key]
                self.read_params[key] = eval(obj)
                pass

            elif any(self.tuple_parameters) == True and \
                key not in self.tuple_parameters:
                """
                # 1. checks if list is already created
                # 2. does not allow for duplicate keys to be made
                ==> Success! Tuple added!
                """
                self.tuple_parameters.append(key)
                self.read_params[key] = eval(obj)
                pass

            else:
                " Failure. Do better. "
                sys.exit("\n\n Tuple key error!\n\n Exiting\n\n")
            pass


            """
        ===========================
        |   INTS' values below    |
        ===========================
        """
        elif isinstance(eval(obj), int) and \
            key != "what"               and \
            key not in self.toggles:
            """
            catches ints, non-self.toggles
            """
            self.read_params[key] = int(obj)

        elif isinstance(eval(obj), float)   and \
            key != "what"                   and \
            key not in self.toggles:
            """
            catches ints given as floats, non-self.toggles
            """
            self.read_params[key] = int(obj)
            pass


            """
        ==============================
        |   TOGGLES' values below    |
        ==============================
        """
        elif isinstance(eval(obj), int)     and \
            key != "what"                   and \
            key in self.toggles:
            """
            Catches ints, in self.toggles.
            """
            self.read_params[key] = int(obj)
            pass

        elif isinstance(eval(obj), float)   and \
            key != "what"                   and \
            key in self.toggles:
            """
            Catches ints given as floats, in self.toggles.
            """
            self.read_params[key] = int(obj)
            pass        

    
        else:
            """
            Honestly, if you've configured the cfg in a way that you 
            came to this point, then I have no idea what you're thinking.
            """
            print "\n\n\n         ### Impossible else!!!!!\n\n\n"
            if not self.errhand_userinput(errorstring):
                sys.exit("1 " + self.inigo)

        return 0


    def taskNameSetter(self, name):
        """
        Decides what to do with taks names;
        * keys whose name is already recorded to be missing should be skipped.
        * (func ONLY considers key "what"; numeral boundaries not included here)
        * name is task's name
        * key objects that are a single task are interpreted
        """
        key = "what"

        if key in self.missingkeys:
            """
            * key is in missing keys list
            so as NOT to create duplicate the keys in list;
            => ignores current key for the line
                    (some times i hate iterators)
            """
            pass

        elif key not in self.missingkeys and \
            name in self.actionkeys:
            """
            * key NOT missing (yet..?)
            * obj is recognized.
                Checks if user's input is part of the
                keywords that may be used for determining
                dataset to read.
            => Success! text assigned to dict[key], WITH
                  its correct interpretation!
            """
            self.read_params[key].append(name)
            pass

        elif key not in self.missingkeys and \
            name not in self.actionkeys:
            """
            * key is NOT missing (yet)
            * obj is NOT recognized!
              - obj does not correspond to keyword
            so, basically, user has input something
                unrecognized!
            => add key to missing keys list
            => add one to counter of missing keys
            => add obj to dict[key] anyway, will fix this later,
                  anyway!
            NOTE: if this actually happens; should ONLY happen ONCE
                    considering the first if-test here.
            """
            self.missingkeys.append(key)
            self.missingkeys_no        += 1
            self.read_params[key].append(name)
            print self.missingkeys
            pass

        else:
            print "\n\n\n========================="
            print       "I have to try and see how \
            this section would apply. Shutting down."
            sys.exit()
            # does not pass...

        return 0


    def properArgsChecker(self):
        """
        In case user screws up some stuff in cfg,
        ask to load in some defaults for these:
        """
        keys_not_read = list(set(self.read_params.keys()) - set(self.keys_read))
        self.missingkeys_no += len(keys_not_read)
        # Is actually declared further up! - only first modified down here
        
        """ Allows the arg-checker to have None-value in one instance,
        but not both """
        either = "fftfile", "subfolder" # only 1 is needed to actually run
        nones = 0 # 1 None allowed. More Nones than that, pffft.
        for key in self.read_params.keys():
            if key in either and self.read_params[key] == None:
                nones += 1
                pass
            continue

        if self.missingkeys_no >= 1 and nones > 1 and self.outputpath != None:
            """
            Something clever.
            """
            print "\n Total no. of parameters not read =", self.missingkeys_no
            print "keys not read", keys_not_read 
            print "\n Parameters not initialized:"
            for key in self.missingkeys:
                print "{0:>10s} : {1:>5s}".format( \
                        key, str(self.read_params[key]).strip('[]') )
                continue

            print "\n Can load default parameters for these, shown below:"
            for key in self.missingkeys:
                print "{0:>10s} : {1:>5s}".format( \
                        key, str(self.default_vals[key]) )
                continue

            if self.errhand_userinput("Continue with these values,"\
                                      +" or edit cfg properly first?"):
                print "\n Parameters being set to:"
                for key in self.missingkeys:
                    self.read_params[key] = self.default_vals[key]
                    print "{0:>10} : {1:>5}".format( \
                        key, self.read_params[key] )
                    continue
                pass
            else:
                sys.exit("3 " + self.inigo)
            pass

        return 0


    def boundCheckNValues(self):
        """
        Checks & confirms all user-assigned values vs. boundary conditions,
        then sets them to class' environmental set values.
        """
        # print # DT stuff
        # for key in self.arglist:
        #     print "{0:<10} : {1}".format(key, self.read_params[key])

        for key in self.arglist:
            """
            Multi's set-making values for:
            what indraN, iA, iB, subfolder, fftfile
            [  0,     1,  2,  3,         4,       5]
            """                
            kind = type(self.read_params[key]) # the type of object

            if key=="what":
                " This assigns a string of task name(s) "
                NoNumeralLimit = [0,0]

                self.borderControl(key, NoNumeralLimit, kind)
                setattr(self, key+"_set", self.read_params[key])         
                pass

                """
            Checking bounds of assigned values,
            based on self.arglist and expected values
            """
            elif key in self.arglist[1:4]:
                """
                indraN, iA, iB have range [ 0, ... , 7 ]
                """
                self.borderControl(key, [0,7], kind)
                setattr(self, key+"_set", self.read_params[key])
                pass

            elif key == "subfolder": # or self.arglist[4]
                """
                subfolders have range [ 0, ... , 63 ]
                """
                self.borderControl(key, [0,63], kind)
                setattr(self, key+"_set", self.read_params[key])
                pass

            elif key == "fftfile": # or self.arglist[5]
                """
                fftfiles have range [ 0, ... , 504 ]
                """
                self.borderControl(key, [0,504], kind)
                setattr(self, key+"_set", self.read_params[key])
                pass                        

            elif key in self.arglist[6:] and key in self.toggles:
                """
                Multi's self.toggles' values
                -> toggled functions remain named normally.
                redshift, bssdt #more? toggles' ranges: [0, 1]
                 [     6,     7   ...]
                """
                self.borderControl(key, [0,1], kind)
                setattr(self, key, self.read_params[key])
                pass

            elif key=="outputpath" and key in self.arglist[6:]:
                " This assigns a string user-defined output path "
                NoNumeralLimit = [0,0]

                self.borderControl(key, NoNumeralLimit, kind)
                setattr(self, key, self.read_params[key])         
                pass

            elif key=="box_params" and key in self.arglist[6:]:
                " Assigns slice box parameters "
                NoNumeralLimit = [0,0]
                # print self.read_params[key]
                self.borderControl(key, NoNumeralLimit, kind)
                setattr(self, key, self.read_params[key])
                pass


            else:
                sys.exit(self.arglisterror)

            continue
        
        " All boundary tests now passed, and values are set "

        " Here setting upper and lower boundary for user's reading preference "

        if all(self.borders):
            print " All values are within bounds!"
            pass
        else:
            " One (or more) parameter value assigned outside of allowed bounds."
            sys.exit("\n    Exiting\n") # darnit.

        return 0


    def borderControl(self, key, limits, kind):
        """
        May I see your passports, please?
        """
        success = None
        lowLim  = limits[0]
        highLim = limits[1] + 1
      

        print key, "type:", kind
        if key == "what" and kind == list:
            """
            Multiple task command names 
            * Tuples of strings AND ints are accepted here. Need check for both.
            """
            if all(map(lambda x: x in \
                       self.actionkeys, self.read_params[key])):
                success = True
                pass
            else:
                print "\n Command for key '%s' not included.\n" % key,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        elif key == "what" and kind == str:
            """
            Single task command name in string:
            * Redundant (potential error would be caught earlier),
              but included for more complete overview.
            """
            if self.read_params[key] in self.actionkeys:
                success = True
                pass

            else:
                print "\n Command for key '%s' not included.\n" % key,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        elif key == "outputpath" and kind == str:
            """
            Single task command name in string:
            """
            print key,":", key in self.actionkeys
            if self.read_params[key] in self.actionkeys:
                success = True
                pass

            else:
                print "\n Command for key '%s' not included.\n" % key,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        elif key == "outputpath" and kind == None:
            """
            Single task command name in string:
            """
            if self.read_params[key] in self.actionkeys:
                success = True
                pass

            else:
                print "\n Command for key '%s' not included.\n" % key,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        elif key == "box_params" and kind == list:
            """
            Single task command name in string:
            """
            if self.read_params[key] in self.actionkeys:
                success = True
                pass

            else:
                print "\n Command for key '%s' not included.\n" % key,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        elif key == "box_params" and kind == None:
            """
            Single task command name in string:
            """
            if self.read_params[key] in self.actionkeys:
                success = True
                pass

            else:
                print "\n Command for key '%s' not included.\n" % key,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass


        elif key != "what" and kind == tuple:
            """
            Int encounter for multi-valued parameters
            """
            if all(map(lambda x: x in \
                       range(lowLim,highLim), self.read_params[key])):
                success = True
                pass
            else:
                print "\n Value for key '%s' not within bounds.\n" % key,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        elif key != "what" and (kind == int or kind == bool):
            """
            Bounds-checking of int for the keys
            * Singe-valued parameters and toggles will be caught here.
            """            
            if self.read_params[key] in range(lowLim,highLim):
                success = True
                pass
            else:
                print "\n Value for key '%s' not within bounds.\n" % key ,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        elif key != "what" and kind == type(None):
            """
            Watch out. Should only be allowed to pass through here once.
            """
            if key in ("subfolder", "fftfile") and \
                    self.read_params[key] == None:
                success = True
                pass
            else:
                print "\n Value for key '%s' not within bounds.\n" % key ,\
                      " Edit cfg-file accordingly.\n"
                success = False
                pass
            pass

        else:
            sys.exit("\n\n No accepted type or range for assigned parameters. \n\n")

        self.borders.append(success)
        return 0


    def userRanges(self):
        """
        After user's input has passed control of absolute parameters:
        set specified ranges to planned data reading.
        * Not strictly necessary, but I find the for-loop through
          self.multi_param_actions nicer this way.
        """
        for name in self.keys_read:
            if name not in self.stringkeys and name not in self.toggles:
                " 'Literally' can't make a numeral set out of those strings "
                if hasattr(eval("self."+name+"_set"), '__iter__'):
                    """
                    sets, from strings, preparing them
                    """
                    setattr(self, name+"_low" , eval("self."+name+"_set")[0])
                    setattr(self, name+"_high", eval("self."+name+"_set")[1])
                    pass
                else:
                    setattr(self, name+"_low" , eval("self."+name+"_set"))
                    setattr(self, name+"_high", eval("self."+name+"_set"))
                    pass
            else:
                """
                Name of key is wither "what" or in toggles,
                no range needed.
                """
                pass

            continue

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


if __name__ == '__main__':
    import sys
    print sys.platform