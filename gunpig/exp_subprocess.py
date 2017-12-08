import subprocess, shlex, os, sys

def OPU():
    " os.path usage "
    import os 
    path = os.getcwd() # placeholder in this case, shhhh
    dir_path = "Examples below"
    os.path.dirname(os.path.realpath(__file__))
        #: Full path to the directory a Python file is contained in
    os.path.realpath(path)
        #: Returns "the canonical path of the specified filename, eliminating any symbolic links encountered in the path"
    os.path.dirname(path)
        #: Returns "the directory name of pathname path"
    os.getcwd() 
        #: Returns "a string representing the current working directory"
    os.chdir(path)
        #: "change the current working directory to path"
    return 0

def SPU():
    " Subprocess usage "
    import subprocess # Of course

    command = " ...needs to be defined "
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    ' No! shell=False is much better convention/security '
    process.wait()
    ' Shouldnt it wait by itself? '
    
    print process.returncode
    ' Shows output of call? '
    return 0

def outputDirCheck(folderPath):
    """
    Checks if output folder structure exists
    & creates output path for output file 
    & filepath- & name based on env. params.
    * Note: based in user's home folder,
            folder structure based on intended task.
    """
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        print "    Creating output folder structure:\n    ", folderPath
        pass
    else:
        print "    Output folder already exists:\n    ", folderPath
        pass
    return folderPath

def SPU_test():
    """
    Tests queuing of sequential bash called-processes initiated through subprocess module
    """
    # Some 'globals'
    homepath = os.path.expanduser("~")
    tmpf     = True
    callnum  = 0 # Remove later / replace with sfs

    # Belonging to debugging
    foldPath = os.getcwd()+"/"
    callFile = foldPath + "printing_over_time.py" # this file specifically to be called by subprocess!

    # Log file name conventions and path creator
    logfpath_templ = "{homepath}/logs_origami/logi{iN}{iA}{iB}{tmp}/"
    logfname_templ = "logi{iN}{iA}{iB}{tmp}_sf{sf:02d}.txt"
    
    # Log file pathing
    logfpath = logfpath_templ.format(
                homepath=homepath,
                iN=1,
                iA=2,
                iB=3,
                tmp="tmp" if tmpf == True else "")
    print 
    outputDirCheck(logfpath) # else there will be no log
    print
    

    print " Loop begins now!"
    print
    for sf in range(0,5):
        print "--- --- ---: Beginning callnum:", sf, ":--- --- ---"

        
        # Subprocess call details
        commandstring_templ = "python {callFile} {sf}"
        commandstring_i = commandstring_templ.format(callFile=callFile, sf=sf)
        cmdcall = shlex.split(commandstring_i)
        process = subprocess.Popen(cmdcall, shell=False, stdout=subprocess.PIPE)
    
        # Screen output section
        # process.wait()
            # \=> Should be swapped out with "process.communicate()", in case of deadlock.
        # print "returncode:", process.returncode, "type:", type(process.returncode), "bool:", process.returncode
            # Not necessary w/ process.communicate()
        
        call_oput = process.communicate()
        print """'''
{out}
'''
--- --- ---
'''
{err}
'''""".format(out=call_oput[0], err=call_oput[1])
        # Prints ORIGAMI oput to screen, and prints potential ORIGAMI error message.
        
        # Writing ORIGAMI screen output log to file
        logfname = logfname_templ.format( iN=1, iA=2, iB=3, sf=sf, tmp="tmp" if tmpf == True else "" )
        logfptot = logfpath+logfname

        with open(logfptot, 'w') as lf: 
            lf.write( "----------------------   ORIGAMI output:   ----------------------\n" )
            lf.write( call_oput[0] )
            lf.write( "----------------------  ORIGAMI complete:  ----------------------\n\n" )
            lf.write( "---------------------- Errors encountered: ----------------------\n" )
            lf.write( str(call_oput[1]) )
            lf.close()

        # Ending a cycle
        print
        print "--- --- ---: Ending    callnum:", sf, ":--- --- ---"
        print
        raw_input("Continue to next loop?")
        print
        continue

    return 0

if __name__ == '__main__':
    SPU_test()
    sys.exit("--- Script done >=> Exiting --- ")