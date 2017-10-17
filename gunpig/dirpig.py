import os, sys, glob
print "\n### dirpig.py ###\n"

def cwdcpl():
    """
    creates the complete path to cwd,
    with a trailing slash for adress for completion.
    catches in case slash is present already.
    """
    return os.path.join(os.getcwd(), '')
stringthing = "ohai   = 100"
print stringthing.strip(" = ")
# exec("herrow")
pathHere = cwdcpl()

folderpath_cfgfile = pathHere+"/read_project/"
filepath_cfgfile   = folderpath_cfgfile+"read_cfg"

open_cfgfile = open(filepath_cfgfile, 'r')

# for line in open_cfgfile:
#     line = line.strip()
#     print line
    # and all that jazz





# print pathHere
# for item in sys.path:
#     print item

#boredpath = os.path.dirname("bored.py")
#print boredpath

# gpfoldername = "gunpig/"
# gpfpath       = pathHere+gpfoldername
# print gpfoldername
# print gpfpath

# import gunpig.gp # no strings. gunpig is folder name, and simply referred to like this
                 # gp.py is file, referred to as a submodule of the folder w/o ext.; .gp
# print "\n### dirpig.py again! ###\n"
# print gunpig.gp.gpath

