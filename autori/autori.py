import os, sys, subprocess, shlex, time, datetime
import pylab as pl

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
        print "  * Creating output folder structure:\n   ", folderPath
        pass
    else:
        print "  * Output folder already exists:\n   ", folderPath
        pass
    return folderPath

def returnFile_asString(current_totPath):
    """
    Opens the file at given path,
    returning its contents as a complete string variable.
    Boolean checks?
    """
    print "----------------------Filereading:----------------------"
    with open( current_totPath, "r") as pf: 
        textvar = ""
        for line in pf:
            textvar += line
            continue
        pf.close()
    return textvar.strip()

example_of_a_parameter_file_that_worked_some_time_ago = """
# General parameters
posfile     /datascope/indra2_tmp/2_0_0/snapdir_060/snapshot_060
outdir      /home/{user}/oriread/testrun/output_i200tmp_sf60
taglabel    origami
boxsize     1000.
np1d        1024
nsplit      4
numfiles    256

# Used by vozinit
buffer      0.1
ndiv        2

# Used by origamihalo
volcut      .01
npmin       20
halolabel   n256d100
"""

#### ### ### : Script effectively really begins here : ### ### ###

produced_directory_paths_examples = """# no temp vs. temp
posfile     /datascope/indra2/2_0_0/snapdir_000/snapshot_000     # no temp
posfile     /datascope/indra2_tmp/2_0_0/snapdir_000/snapshot_000 # temp

outdir      /home/{user}/oput_origami/i200/i200_sf00        # no temp
outdir      /home/{user}/oput_origami/i200tmp/i200tmp_sf00  # temp
""" # Included for user orientation/readability

# Alternatives of outdir variable 
outdir_sciserver = "/sciserver/vc/indra/origami/i{iN}{iA}{iB}{tmp}/i{iN}{iA}{iB}{tmp}_sf{sf:02d}"


# ... unless the folder structure itself was all that was needed.
outdir_homefoldr = "{homepath}/oput_origami/i{iN}{iA}{iB}{tmp}/i{iN}{iA}{iB}{tmp}_sf{sf:02d}"

# The raw parameter file template - let's attempt sciserver this time!
pf_templtxt = """
# General parameters
posfile     /datascope/indra{iN}{_tmp}/{iN}_{iA}_{iB}/snapdir_{sf:03d}/snapshot_{sf:03d}
outdir      /sciserver/vc/indra/origami/i{iN}{iA}{iB}{tmp}/i{iN}{iA}{iB}{tmp}_sf{sf:02d}
taglabel    _
boxsize     1000.
np1d        1024
nsplit      4
numfiles    256

# Used by vozinit
buffer      0.1
ndiv        2

# Used by origamihalo
volcut      .01
npmin       20
halolabel   n256d100
""".strip()


# "pfi" ~= "parameter file, indra [simulation]" or "parameters for indra [simulation]"
pfPath  = "{homepath}/pfs_origami/pfi{iN}{iA}{iB}{tmp}/"
pfName  = "pfi{iN}{iA}{iB}{tmp}_sf{sf:02d}.txt"


def parf_maker(iN, iA, iB, tmpf, sfs):
    """
    Parameter file creator, takes in different sets of snapshot numbers
    """
    print """
 [ORIGAMI parameter file creation: ENGAGED.]>"""
    homepath = os.path.expanduser("~")
        # yields '/home/{username}/'

    current_pfPath = pfPath.format(
          iN=iN,
          iA=iA,
          iB=iB,
          homepath=homepath,
          tmp="tmp" if tmpf == True else ""
        )
    print 
    print " [Checking if parameter file's folder structure exists.]"
    outputDirCheck(current_pfPath) 

    pfList      = [] # for debugging
    pfpathsList = [] # to be returned and used by sequential process caller

    for i in pl.arange(len(sfs)):
        # Current parameter file
        current_pftxt = pf_templtxt.format( # Inits paramter file's complete text
              iN=iN,
              iA=iA,
              iB=iB,
              sf=sfs[i],
              homepath=homepath,
              _tmp="_tmp" if tmpf == True else "",
              tmp = "tmp" if tmpf == True else ""
            )
        pfList.append(current_pftxt) # for debugging

        # Constructing the current parameter file's name string
        current_pfName = pfName.format( # Inits parameter file's name
              iN=iN,
              iA=iA,
              iB=iB,
              sf=sfs[i],
              tmp="tmp" if tmpf == True else ""
            )
        # Total file path w/ homedir + folder struct + file name, current parameter file
        current_totPath = current_pfPath+current_pfName
        pfpathsList.append(current_totPath) 


        # Below writer would/could be included in above '''str'''-section.
        with open( current_totPath, "w") as pf: # File created here
            pf.write(current_pftxt)             # File written here
            pf.close()                          # File closed  here

        # sys.exit("---------------------- Abbor at this point. ----------------------")
        continue # next file in the set of snapfolders


    print "\n :=> [ORIGAMI parameter file creation: COMPLETED.]"
    if len(pfpathsList) == len(sfs):
        print "     [All {0:02d} parameter file(s) have been created.]".format(len(sfs))
        pass
    else:
        " Maybe couple with suggested functionality above. "
        pass

    return pfpathsList

" Strings useful to the ORIGAMI caller below this line: "
# ORIGAMI tagger call phrase
ocall_templ = "{homepath}/origami-2.0/code/./origamitag {pfpath}"
# Call process log files
logfpath_templ = "{homepath}/logs_origami/logi{iN}{iA}{iB}{tmp}/"
logfname_templ = "logi{iN}{iA}{iB}{tmp}_sf{sf:02d}.txt"
# Will be updated for every snapshot completed

# Sequential screen print (will update every time an ORIGAMI tagging run is done)
osd_oput = """
----------------------   ORIGAMI output:   ----------------------
{out}
----------------------  ORIGAMI complete:  ----------------------
                                |         
---------------------- Errors encountered: ----------------------
{err}
"""
# Want to enable making origamo outdir before origami begins
outdirp_tmpl = "/sciserver/vc/indra/origami/i{iN}{iA}{iB}{tmp}/"
# outdirp_tmpl = "{homepath}/oput_origami/i{iN}{iA}{iB}{tmp}/"

def origami_caller(pfpathsList):
    """
    Calls bash cmds for running ORIGAMI sequentially,
    through pre-defined set of parameterfiles.
    """
    homepath = os.path.expanduser("~")

    print """
 [ORIGAMI particle tagger: ENGAGED.]>
    """
    # ... Might be an issue where these folders do not exist yet...
    outdirp = outdirp_tmpl.format( iN=iN, iA=iA, iB=iB, tmp="tmp" if tmpf == True else "" )
    print " [Checking if ORIGAMI output's folder structure exists.]"
    outputDirCheck(outdirp) # else there will be no log
    print

    # Log file name conventions and path creator
    logfpath = logfpath_templ\
        .format( homepath=homepath, iN=iN, iA=iA, iB=iB, tmp="tmp" if tmpf == True else "" )
    print " [Checking if screen output logs' folder structure exists.]"
    outputDirCheck(logfpath) # else there will be no log
    print

    
    print " :=> [ORIGAMI particle tagger begins looping over snapshots.]"

    for i in range(len(pfpathsList)):
        " Loopy-loop's commencement! "

        time_iter_start = time.time()
        print "| --- --- ---: Analyzing snapshot: {sf:02d} :--- --- ---".format(sf=i)

        # Subprocess call details
        commandstring_i = ocall_templ.format(homepath=homepath, pfpath=pfpathsList[i])
        cmdcall = shlex.split(commandstring_i)
        print "   Now calling command through bash:"
        print "[ ' >$", cmdcall[0]
        print "      ", cmdcall[1], "' ]"
        print
        process = subprocess.Popen(cmdcall, shell=False, stdout=subprocess.PIPE)
            
        # # Prints ORIGAMI oput to screen, and prints potential ORIGAMI error message.
        call_oput = process.communicate()
        print osd_oput.format(out=call_oput[0], err=str(call_oput[1]))
        
        # ORIGAMI screen output log to file: filename
        logfname = logfname_templ.format( iN=iN, iA=iA, iB=iB, sf=i, tmp="tmp" if tmpf == True else "" )
        logfptot = logfpath+logfname

        # # Log file writing
        with open(logfptot, 'w') as lf: 
            lf.write( "----------------------   ORIGAMI output:   ----------------------\n" )
            lf.write( call_oput[0] )      # Screen-part
            lf.write( "----------------------  ORIGAMI complete:  ----------------------\n" )
            lf.write( "                                | \n" )
            lf.write( "---------------------- Errors encountered: ----------------------\n" )
            lf.write( str(call_oput[1]) ) # Error-part
            lf.close()

        # Ending a cycle & tracking time
        print
        print "| --- --- ---: Snapshot  analyzed: {sf:02d} :--- --- ---".format(sf=i)

        time_iter_end = time.time()

        # Prints runtime of current iteration
        iter_time_s = time_iter_end-time_iter_start
        iter_time_m = iter_time_s/60.
        iter_time_h = iter_time_m/60.
        print """
    [    Iteration's run time in hours]:  {h:1.2g}"""\
            .format(h=iter_time_h)

        # Prints total runtime up until this point:
        sofar_time_s = time_iter_end-beginning
        sofar_time_m = sofar_time_s/60.
        sofar_time_h = sofar_time_m/60.
        sofar_time_d = sofar_time_h/24.
        print """\
    [ Total run time thus far in hours]:  {h:1.2g}
    [                         in days ]:  {d:1.2g}"""\
            .format(h=sofar_time_h, d=sofar_time_d)

        # Prints a very-basic-rough-estimate of remaining time;
        # depending on current iteration's runtime
        rem_run_time = iter_time_h*(len(pfpathsList)-(i+1))
        print """    [     Estimated remaining run time]:  {h:1.2g} hours //  {d:1.2g} days."""\
            .format(h=rem_run_time, d=rem_run_time/24.)

        now = datetime.datetime.now()
        print """
    [ORIGAMI tagger completed snapshot {sf:02d} at time]:
      (y{y:04d}/m{m:02d}/d{d:02d}) ~ {h:02d}:{min:02d}
        """.format( y=now.year, m=now.month, d=now.day, h=now.hour, min=now.minute, sf=i )

        continue


    print """ :=> [ORIGAMI particle tagger: COMPLETED] """
    return 0

def main(iNs, iAs, iBs, sfs, tmpfs):
    """
    1:  Script flow intended to **mass produce parameter files for ORIGAMI**,
    as initialization of each & every numerical analysis to be performed by ORIGAMI,
    on a corresponding snapshot dataset from the INDRA simulations...
        * Function: "parfmaker".

        1a: To help python do this, a functionality is included to check if required
        paths to these parameter files exist beforehand; creating directories as needed.
            * Function: "outputDirCheck". Takes in a suggested folder structure's path.
                ==> Sets path for parameter files to be put in: "~/pfs_origami"

        1b: If there's a reason for determining whether a parameter file's contents are
        correct, or parameter file already exists
            {   i.e.: 
                
                * Run ORIGAMI on a snapshot again with a corrected parameter string. 
                        (Previous attempt may have failed because of this?)
                    -[__Not implemented!__]-
                
                * If existing parameter file's contents are identical with python's
                    current paramater string; one may assume ORIGAMI has already run on
                    that specific snapshot. (???)
                    ==> Then ***not*** to include that snapshot to be processed by
                        ORIGAMI; saving computational time
                        (which I'm sure other users would be pleased with)
                    -[__Not implemented!__]-
            }
        there's a line to booleanly check this, and the function 
        "returnFile_asString(current_totPath)" provides the existing parameter file's
        contents as a string.

    2:  ... Until the script intends to continue by calling ORIGAMI and perform these
    analyses sequentially, until all specified snapshots have been analyzed.
        * Function: "origami_caller".
    """
    " Loops through everything "
    for iN in iNs:
        # iN = iN

        for iA in iAs:
            # iA = iA

            for iB in iBs:
                # iB = iB

                for tmpf in tmpfs:
                    # tmpf = tmpf

                    # User orientation:
                    print """
                  Currently processing data from set of files:
                 [...]/indra{iN:d}{tmp}/i{iN:d}{iA:d}{iB:d}/snap_[ {sf0:02d}, ... , {sf1:02d} ]"""\
                        .format( iN=iN, iA=iA, iB=iB, tmp="_tmp" if tmpf == True else "",
                                 sf0=sfs[0], sf1=sfs[-1] )
                    print "\n# === === === === === === === === === === === === === === === === |"

                    # Creates parameter files
                    pfpathsList = parf_maker(iN, iA, iB, tmpf, sfs)

                    print "\n# === === === === === === === === === === === === === === === === |"

                    # Runs ORIGAMI sequentially within this function
                    origami_caller(pfpathsList)

                    print "\n# === === === === === === === === === === === === === === === === |"
                    
                    continue
                continue
            continue
        continue
    
    print """
### All scripts completed successfully!!! :D"""

    return 0

    # A small attempt at variable name explanation:
    # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    # i(N,A,B): simulation         (N,A,B) , (N,A,B) \in [1,512] different simulations
    #           number in base8, so 512_10 == 1000_8 :=> max(N,A,B)=(7,7,7)
    # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    # sf      : snapfolder & file  sf , sf  \in  [0,63] time snapshots
    # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    # pf      : parameters' file
    # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

if __name__ == '__main__':
    beginning = time.time()
    
    now = datetime.datetime.now()

    print """
 ***          |: You are using AutOriPy :|          ***
 ***                                                ***
 *** the 'Automatic ORIGAMI' parameter file creator ***
 ***       &  ORIGAMItag shell command caller       ***
 ***              ( ...with 'Python' )              ***

        [Initialized at time]:
         (y{0:04d}/m{1:02d}/d{2:02d}) ~ {3:02d}:{4:02d}"""\
          .format(now.year, now.month, now.day, now.hour, now.minute)
    
    """
        (: You are using OPaFiPaTa ! :)
 *** ORIGAMI Par.File-maker & Particle-Tagger *** 
    """ # Early-stage name.
    
    indraNs   = pl.array([2])
    indraAs   = pl.array([0])
    indraBs   = pl.array([2,3])
    tempfolds = pl.array([True])

    snapfiles = pl.arange(0,64) # the actual interesting range

    main(   iNs=indraNs, iAs=indraAs, iBs=indraBs, sfs=snapfiles, tmpfs=tempfolds  )
    
    end = time.time()

    tot_time_s = end-beginning
    tot_time_m = tot_time_s/60.
    tot_time_h = tot_time_m/60.
    tot_time_d = tot_time_h/24.

    print """
    [Total run time in hours]:  {h:.2e}
    [               in days ]:  {d:.2e}
    """.format(m=tot_time_m, h=tot_time_h, d=tot_time_d)

    sys.exit("### [Shutting down.]\n")
    # ...It kinda feels like concluding this script _decisively_ will be a good thing.