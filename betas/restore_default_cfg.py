###############################
# cfg-file restoration script #
###############################

def restorecfg(fileobject):
    """
    manipulates file object with this function's stored text
    """
    defaultcfg = '''
# --------------------------------------------------------------------------- |
#  * This is a script for configuring how read.py will run.                   |
# read.py reads data from indra-simulations or origami post-processing.       |
#                                                                             |
#  * The script determines what data to read, with all options available.     |
# Most of these options for read.py are actually parameters which navigate    |
# the simulations' file structure(s).                                         |
#  * Not all the options will have an effect on every single part of the      |
# script; the options' effects should be listed in their explanations.        |
#                                                                             |
#  * Immediately below you will find the main options/parameters, and below   |
# them is written an explanation on how to use each of them.                  |
#  * Beneath that again, follows more advanced options or legacy debugging    |
# tools that you may choose to use; by default, these will be turned off.     |
#                                                                             |
#  * Every option will be listed categorically, and the corresponding         |
# argument to that option is then shown after a colon on the same line.       |
#  * A default value has been assigned to each of them, in the case of a need |
# to reset.                                                                   |
#  * Some options will have several keyword arguments which will initiate the |
# same procedure; simply allowing for user's vocabulary preference.           |
#                                                                             |
#  * If the program ever starts quoting the movie The Princess Bride (1987),  |
# then rest assured and know that you have done something horribly wrong.     |
# Try restoring the configuration file. A script has been included for this   |
# purpose.                                                                    |
# --------------------------------------------------------------------------- |

what      = posvel
indraN    = 0
iA        = 0
iB        = 0
subfolder = 0
fftfile   = 0

# """
# # WHAT DATA TYPE - what:
#  * What kind of data do you want to read? Type in desired data type name.
#   You may choose from several options:
#     * positions        : "pos"
#     * velocities       : "vel"
#     * pos & vel        : "posvel"
#     * friend-of-friend : "fof" / "FOF"
#     * subhalo          : "subhalo"
#     * fft              : "fft" / "FFT"

# # INDRA number - indraN:
#  * What number of indraN (INDRA simulation) would you like to read from?
# indraN ranges from 0 to 7, a sum of 8 sets in total.
#   You may choose to read data from _a single_ INDRA number:
#     * Specify a number from 0 to 7.
#   If you would like to read more than one data set:
#     * Specify the lowest and highest indraN, seperated by a comma.
#       Example: 1,4

# # INDRA SUBSTRUCTURE - iA, iB:
#  * 2 more data folder structure combination arguments: iA, iB. Ranging from
# 0 to 7 as well, a sum of 8 sets in total.
#   As above, you may choose to read one or more sets of data. Specify:
#     * A number from 0 to 7.
#     * Or the lowest and highest iA and/or iB, seperated by a comma.

# # SUBFOLDER:
#  * Options pos, vel, posvel, fof, and subhalo also have an additional
# subfolder which you can instruct read.py to read from. These range in number
# from 0 to 63, a sum of 64 folders in total.
#   As above, you may read a single subfolder or several of them. Specify:
#     * A subfolder number from 0 to 7.
#     * Or the lowest and highest subfolder number, seperated by a comma.

# # FFT:
#  * In the case of reading FFT data, there are no subfolders, and the program 
# will thus ignore subfolder specification, but the FFT-files are enumerated 
# from 0 to 504, a sum of 505 files in total.
#   As above, read a single FFT-file, or several of them. Specify:
#     * A file number from 0 to 504.
#     * Or lowest and highest file number, seperated by a comma.
# """

# """
# -ADVANCED OPTIONS-------------------------------------------------------------
# Here begin the advanced options, below this bulletin.
# All below options are activated by binary toggle: 1/0 // True/False.
# Individually listed, explanations listed above them:

# # SORT IDS:
#  * If you would like to have positions / velocities output of particles
# sorted by their 64-bit assigned ID tag. Def. value: 0 .

# # LESSPRINT:
#  * So that a bash terminal isn't cluttered in too much unnecessary lines 
# of useless information. Def. value: 1 .

# # TMP FOLDER:
#  * Not all datasets under processing are necessarily included in the indraN
# folder structure; this option accesses these. Def. value: 0 .
sortIDs   = 0
lessprint = 1
tmpfolder = 0


# ----- TO BE REDACTED -----:
# # REDSHIFT:
#  * In the case of the pos, vel, or posvel data, the data have an option
# available to calculate a relevant red shift.

# # BIG SKIP SHUTDOWN TOGGLE
#  * In an early reading build, if an iterating skip variable became too big,
# a condition reaching 1.01*skip, this would result the program to abort.
# """
redshift  = 0 # will be disabled completely
bssdt     = 0 # will be disabled completely
'''.strip()

    filepath_cfgfile = os.path.join(os.path.dirname(__file__), '') + "read_cfg"
    with open(filepath_cfgfile, 'w') as open_cfgfile:
        open_cfgfile.write(defaultcfg)
        open_cfgfile.close()

    return 0

def errhand_userinput(problemstring):
    """
    error handling, with user input
    enabling: 
    * error message
    * user input
    * recursion in case of stupid
    """
    ok2go = raw_input(problemstring+" Please input (1/0) or (y/n) : ").lower()
    if ok2go == "n" or ok2go == "0":
        sys.exit("""
            -------------------------------
             cfg-file restoration aborted. 
            -------------------------------
            """)
    elif ok2go == "y" or ok2go == "1":
        print """
            +++++++++++++
             Continuing.
            +++++++++++++
            """
        return True # the only way out!

    else:
        self.errhand_userinput(problemstring)


if __name__ == '__main__':
    import os, sys

    warning = " \n\
                \n    You are initiating to reset the cfg-file to its\
                \n    original format and its default values.\
                \n    Do you wish to proceed? "
    if errhand_userinput(warning):
        # restorecfg()
        pass

    sys.exit("\n    read_cfg restored to default format and values!\n")