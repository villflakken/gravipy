import os, sys, glob
import numpy as np
import numpy as N
import textwrap
import pylab as pl
"""
        check that all vital parameters are given values. allows /only/ nonvitals to have
        value == None.
""" # should be completely redundant with section above
''' # and i've got better things to debug atm.
        # DT
        print
        for key in self.self.self.arglist:
            print "read_params[{key:>9}] : {param}".\
                format(key=key, param=self.read_params[key])

        for item in self.self.self.arglist:
            print
            print "on item:",item
            print "item in self.nonvitals, self.read_params[item] == 0:"
            print " "*4, (item in self.nonvitals), (self.read_params[item] == None)
            if item in self.nonvitals and self.read_params[item] == None:
                # only nonvitals have None
                print " "*4, "passing"
                pass
            
            # but False == 0 or 0.0 ; False != None (!!!)
            if item not in self.nonvitals and self.read_params[item] == False:
                # (R)[i] not in (NV)    == True     /and\
                # (R)[i] == False == 0  == True     -->
                #                       -->         continue
                print "item not in self.nonvitals and self.read_params[item] == False:"
                print " "*4, (item not in self.nonvitals), (self.read_params[item] == False)
                print " "*4, "continuing"
                pass
            else:
                print " "*4, "still on item?:", item
                sys.exit("4 " + self.inigo)
'''

# def open_thing():
#     path = os.getcwd()

#     return open(path+"/indra_corrfunc.py", 'r')
# def give(i):
#     if i == 7:
#         return False
#print "\n### gp.py ###\n"

#WOW = "WOW!"
#gpath = os.getcwd() # does not yield THIS document's path
# keys_not_read = []
# optcount = 0

def funcNameHere():
    """
    :return: name of current function in which this function is called
    """
    return sys._getframe(1).f_code.co_name

def errhand_userinput(problemstring):
    """
    error handling, with user input
    enabling: 
    * error message
    * user input
    * recursion in case of stupid
    """
    print func_name()
    ok2go = raw_input(problemstring+" Please input (1/0) or (y/n) : ")
    # triggeredy:
    print "FOO!"
    if ok2go == "n" or ok2go == "N" or ok2go == "0":
        sys.exit("""
            ---------------------------
             Dataset analysis aborted. 
            ---------------------------
                 Shutting down ISS
            """)
        # Could also return a False, leading error handling outside.
    elif ok2go == "y" or ok2go == "Y" or ok2go == "1":
        print "BAR!"
        print """
            +++++++++++++
             Continuing.
            +++++++++++++
            """
        pass
    else:
        errhand_userinput(problemstring)
    # except ValueError:
    #     print "Exception block"
    #     errhand_userinput(problemstring)

    return True




class Rawr(object):
    def __init__(self):
        self.val = 10

    def do(self):

        read_these = {  "what" :        None, \
                        "indraN" :      None, \
                        "iA" :          None, \
                        "iB" :          None, \
                        "subfolder" :   None, \
                        "fftfile" :     None, \
                        "redshift" :    None, \
                        "bssdt" :       None  \
                                                }
        default_vals = {"what" :    "pos", \
                        "indraN" :      0, \
                        "iA" :          0, \
                        "iB" :          0, \
                        "subfolder" :   0, \
                        "fftfile" :     0, \
                        "redshift" :    0, \
                        "bssdt" :       0  \
                                                }
        filepath_cfgfile = os.path.join(os.path.dirname(__file__), '') + "dummy_cfg"
        keys_read = []
        linecount = 0
        lineread = 0
        toggles = ("redshift", "bssdt")
        with open(filepath_cfgfile, 'r') as open_cfgfile:

            for line in open_cfgfile:
                linecount += 1 # debug tool, compare total lines read vs. lines with keys
                line = line.strip()
                for key in read_these.keys():
                    if line.startswith(key):
                        keys_read += [key]
                        try:
                            obj = line[line.find("=")+1:].strip()

                            if isinstance(obj, str) and key == "what":
                                # catches only data type.
                                read_these[key] = obj
                            
                            elif isinstance(eval(obj), tuple) and key != "what" and key not in toggles:
                                # catches non-toggles that are tuples
                                read_these[key] = eval(obj)
                            
                            elif isinstance(eval(obj), int) and key != "what" and key not in toggles:
                                # catches non-toggles that are ints
                                read_these[key] = int(obj)

                            elif isinstance(eval(obj), int) and key != "what" and key in toggles:
                                # catches ints that toggle
                                read_these[key] = int(obj)

                        except:
                            errorstring = \
                            """
                            Something went wrong!
                            Can't read line from read_cfg. Check syntax! Line below:
                            """+"\n"+line+"\n\n Continue anyway?"
                            print "error"
                            if not errhand_userinput(errorstring):
                                sys.exit("My name is Inigo Montoya. You killed my father. Prepare to die.\n\nExiting.")
                                
            open_cfgfile.close()

        print "\nTotal parameters loaded:", len(keys_read)
        print "Parameters initialized with values:"
        for key in keys_read:
            print "{:>10s} : {:>5s}".format(key, str(read_these[key]))

        keys_not_read = list(set(read_these.keys()) - set(keys_read))
        missingkeys = len(keys_not_read)
        if missingkeys == True:
            print "\nTotal parameters not read =", missingkeys
            print "Parameters not initialized:"
            for key in keys_not_read:
                print "{:>10s} : {:>5s}".format(key, str(read_these[key]))

            print "Can load default parameters for these, shown below:"
            # print default_vals["bssdt"]
            print "Parameters and their values set:"
            for key in keys_not_read:
                print "{:>10s} : {:>5s}".format(key, str(default_vals[key]))
            if not errhand_userinput("Continue with this/these values?"):
                sys.exit("My name is Inigo Montoya. You killed my father. Prepare to die.\n\nExiting.")

        self.arglist =      ["what"     , \
                        "indraN"    , \
                        "iA"        , \
                        "iB"        , \
                        "subfolder" , \
                        "fftfile"   , \
                        "redshift"  , \
                        "bssdt"       ]
        pos = None
        print "\n exec for these vals, setting global values:"
        # for key in self.arglist:
        #     print "{:>10s} = {:>5s}".format(key, str(read_these[key]))
        #     exec("self.%s_set = '%s'" % (key, read_these[key]))

        # print "\n global values now verified as set to:"
        # for key in self.arglist:
        #     # print key, eval(key)
        #     print "{:>10s} : {:>5s}".format(key, eval("self."+key+"_set"))




        # self.default_vals = { key: "pos" if key=="what" else 0 for key in self.arglist }
        # self.default_vals = dict((key, "pos") if key=="what" else 0 for key in self.arglist)
        # print
        # self.self.arglist = self.arglist
        # count = 0
        # for param in self.self.arglist[1:]:
        #     print
        #     print "test for", param
        #     print "straight:", "self."+param
        #     print "eval    :", eval(eval("self."+param))
        #     print "type straight:", type("self."+param)
        #     print "type eval    :", type(eval(eval("self."+param)))
            
        #     if isinstance(eval(eval("self."+param)), tuple):
        #         print "yay!"

        # # print "\n subfolder test"
        # # print "straight:", self.subfolder
        # # print "eval    :", eval(self.subfolder)
        # # print "type straight:", type(self.subfolder)
        # # print "type eval    :", type(eval(self.subfolder))

        # print 
        # print 
        # print 
        # print 
        # print "non-loop objects, but put 2gether from strings, look like ---"
        # print "string:", "self."+param
        # print
        # print "eval          :", eval("self."+param)
        # print "type eval     :", type(eval("self."+param))
        # print
        # print "eval eval     :", eval(eval("self."+param))
        # print "type eval eval:", type(eval(eval("self."+param)))
        # exec("self."+param+"= 1000")

        # print self.bssdt

        # print "triple eval        :", eval(eval(eval("self."+param)))
        # print "type if triple eval:", type(eval(eval(eval("self."+param))))

        # print "non-loop objects, directly from file look like ---"
        # print "string:", obj
        # print
        # print "eval          :", eval(obj)
        # print "type eval     :", type(eval(obj))
        # print
        # print "eval eval     :", eval(eval(obj))
        # print "type eval eval:", type(eval(eval(obj)))

        # for name in self.arglist[1:4]:

        #     if isinstance(eval(eval("self."+name+"_set")), tuple):

        #         exec("%s_low  = int(eval(self.%s_set)[0])" % (name, name))
        #         exec("%s_high = int(eval(self.%s_set)[1])" % (name, name))
        #     else:
        #         exec("%s_low, %s_high = int(self.%s_set), int(self.%s_set)" % (name, name, name, name))

        # print indraN_low, type(indraN_low)
        # print indraN_high, type(indraN_high)
        # for iN in range(indraN_low, indraN_high+1):
        #     print "yay!", iN

        print
        print
        joy = "hoy"
        love = "sadness..."
        text = " %s and %s " % (joy, love)
        print text

        print
        print
        love = "cuteness"
        print text

        text = "This {program:<12} is {really} {boring}"
        program = "program"
        really = "really"
        boring = "boring"
        print \
        text.format(program=program, really=really, boring=boring)
        # text.format(program=program)
        # text.format(really=really, boring=boring)
        print
        print "pure print"
        print sys._getframe().f_code.co_name  # AMAZING DT TOOL
        print "as func call and type"
        # print func_name(), type(func_name())

        print 
        setattr(self, "rumpe", "oh")
        setattr(self, "laar", (1,2))
        print self.rumpe, type(self.rumpe)
        print self.laar, type(self.laar)

        print
        self.actionkeys =  ["posvel",   \
                            "pos",      \
                            "vel",      \
                            "fof",      \
                            "group",    \
                            "subhalo",  \
                            "fft"       ]
        
        trues = lambda x: x in self.actionkeys
        
        print all(map(lambda x: x in self.actionkeys, ("group", "fft", "subhalo")))


        # print self.here()
        print
        print sys.argv
        print 
        # try:
        #     errorthing = eval(self.actionkeys[0][15])
        # except:
        #     self.bep()

        with open(os.path.join(os.path.dirname(__file__), '')+"gp.txt", \
                  'w') as self.writeToFile:
            for i in np.arange(0,6):
                self.writer([i, i**2, i**3, i**4], self.writeToFile)
                continue

        i = 0
        print i is 0, i == 0, "i-test" 

        return 0


    def writer(self, datalist, w):
        """
        this is a function that will write relevant data as input by the program
        """
        maxlen = len(datalist)

        lineToWrite = ""
        for i in range(len(datalist)):
            lineToWrite += "{0:>20}".format(datalist[i])
            continue

        w.write(lineToWrite)
        return 0


    def bep(self):
        """
        Better Error Printer
        Simple module that prints error messages in a better way (subjectively)
        """

        nl              = "\n"
        prefix          = "\tPython Error:"
        errorType       = "* " + str(sys.exc_info()[0])[18:-2]
        theBaseIndent   = textwrap.fill(prefix, replace_whitespace=False)[:-1]
        nextLineIndent  = " "*(len(theBaseIndent)/2 -2)
        messToScreen = textwrap.TextWrapper(initial_indent=nextLineIndent,
                                               subsequent_indent=nextLineIndent)
        errorDescr = "* " + str( sys.exc_info()[1] ).capitalize()

        print prefix
        print messToScreen.fill(errorType)
        print messToScreen.fill(errorDescr)
        print messToScreen.fill("* Error located inside function:")
        print messToScreen.fill("    '%s'"% str(self.funcNameOver()))
        print 

        print sys.argv
        if sys.argv[1] == None:
            print "YAY!"
        return 0

    def funcNameOver(self):
        """
        :return: name of current function in which this function is called
        """
        return sys._getframe(2).f_code.co_name

# <type 'exceptions.
test = Rawr()

test.do()






# wtf1, wtf2 = os.path.split(os.path.abspath(sys.argv[0]))
# print WOW
# print gpath
# print wtf1, wtf2
# print os.path.abspath(sys.argv[0])
# print os.path.join(os.path.dirname(__file__), sys.argv[0])
# print os.path.dirname(__file__), " <--- this is path? not file? yes"
# print os.path.join(os.path.dirname(__file__), ''), "<--- with completion"
# next thing will be awesome
"""
print 
path = os.getcwd() + "/"
# print type(path)
# print path
# f = open_thing()

print
pathstrlen      = len(path) # i.e. snappath is 49 characters long
filelist        = glob.glob(path+'*.py')
maxfileCount    = len(filelist)
for i in filelist:
    print i
print
for i in N.arange(0, maxfileCount):
    with open(filelist[i], 'r') as f:
        infile = f.read()
        print infile[:15]
count = 0
for i in N.arange(0,8):
    print
    print "i: ", i
    if i > 3:
        count += 1

    if (count < 2):
        print "triggered!"
        print "count: ", count
    elif (int(raw_input("1: "))):
        print "ohai!"
    else:
        sys.exit("count = 2")
"""

'''
if __name__ == '__main__':
    
    """
    # fucking with binary numbers?
    arr2 = np.zeros(5, dtype=np.int64)
    # arr2[0, ( 1, 2, 3 ), 4, 5] = arr1[ 0, 1, 2, 3 ] and etcetc
    skip = 1
    print

    maxbit = '{:b}'.format( 2**63-1 )
    print 4*" ", "bit-to-int!"
    print "int:", np.int64(maxbit, 2)
    print "bit:", maxbit # is of type str
    # print 4*" ", arr2.astype(str).any[0:1]

    shifted = np.int64(2**34)
    bitmask = np.int64(2**34 - 1) # should become a mask array at some point?
    print
    print " A - this is no. after bitshift, 1 to 34:          ", shifted
    print " B - this is no. after bitshift, 1 to 34, minus 1: ", bitmask
    print 
    print " A - as unformatted bitstring:", '{:b}'.format(shifted)
    print " B - as unformatted bitstring: ", '{:b}'.format(bitmask)
    print
    print " A - as int64-formatted bitstring:", '{0:0>64b}'.format(shifted)
    print " B - as int64-formatted bitstring:", '{0:0>64b}'.format(bitmask)
    print

    rnd_str = ""
    for i in range(63):
        rnd_str += str(np.random.randint(low=0, high=2))
    print
    print "generated string:       ", rnd_str
    rnd_int = np.int64(rnd_str, 2)
    
    print '"random" string converted to int:', rnd_int

    print "size of rnd_str[-33]", sys.getsizeof(rnd_str[-33])
    print
    print '"rand" int64-formatted bitstring: ', '{0:0>64b}'.format(rnd_int)
    print

    print " ##### TEST DAY INCOMING #### "
    arr1            = np.array([rnd_int, rnd_int, rnd_int])
    bitmask         = np.int64(2**34 - 1)
    bitshiftmask    = (np.int64(1)<<34)-1
    print "first: test if my arithmetic is True, bitmask == bitshiftmask:"
    print bitmask == bitshiftmask
    print 
    print "then we start with arr1, an array of 3 items with a scrambled binary value:"
    print arr1
    print
    print "which in binary looks like these values:"
    for item in arr1:
        print np.binary_repr(item)
    print
    print "we now create arr2, that uses the bitshifted-subtracted-by-1 mask on arr1 values:"
    arr2[ skip: skip+3 ] = np.bitwise_and(arr1[:], bitmask)

    print arr2
    print "which in binary looks like this:"
    for item in arr2:
        print np.binary_repr(item)
    print
    print "are the values in arr2 masked correctly? let's try side-by-side comp. (64bit):"
    print '{0:0>63b}'.format(arr1[0]), "scrambled    value"
    print '{0:0>63b}'.format(arr2[1]), "manipilated  value"
    print '{0:0>63b}'.format(bitmask), "bit mask     value"
    print
    print maxbit,                      "max possible value"
    """ # IT WOOOORKS

    """ # shows that IDL and python don't work the same way
    for i in np.arange(len(arr1)):
        arr2[ skip+i ] = arr1[ i ] and ( (np.int64(1)<<34) - 1)
    print
    print 4*" ", arr1[0]
    print 4*" ", arr1[0] and ( (np.int64(1)<<34) - 1)
    print 4*" ", arr2[1]
    print 4*" ", 
    print
    print '{0:0>64b}'.format( arr1[0] and ( (np.int64(1)<<34) - 1) )
    print '{0:0>64b}'.format( arr2[1] )
    """

    """
    print 
    print 'str("")  =', sys.getsizeof('' ), 'bytes'
    print 'str(" ") =', sys.getsizeof(' '), 'bytes'
    print 'str("a") =', sys.getsizeof('a'), 'bytes'
    print 'str("0") =', sys.getsizeof('0'), 'bytes'
    print 'str("1") =', sys.getsizeof('1'), 'bytes'
    print 
    print 'str("{:b}") ='.format(shifted), sys.getsizeof('{:b}'.format(shifted)), 'bytes'
    print '"{:b}" ='.format(bitmask), sys.getsizeof('{:b}'.format(bitmask)), 'bytes'
    print
    print 'str("{:0>64b}") ='.format(shifted), sys.getsizeof('{:0>64b}'.format(shifted)), 'bytes'
    print 'str("{:0>64b}") ='.format(bitmask), sys.getsizeof('{:0>64b}'.format(bitmask)), 'bytes'
    """
'''

pl.figure()
pl.plot([1,2,3],[4,5,6])
pl.savefig("3.png")
# pl.show()
pl.close()

fig = pl.figure()
pl.plot([1,2,3],[6,5,6])
pl.savefig("4.png")
pl.close()

tmpfolder = True
readtext = "\t Accessing file:\tindra{0}{1}/snap{2}/file.{3} ({4}) ..."
tmpftxt = "tmp" if tmpfolder == True else ""
indraN = 2
subfolder = 63
i = 52
what = "pos"
Npart = 928
readtext = readtext.format( indraN, tmpftxt, 
                           subfolder, i, what )
print "i:", i, "| Npart (before boxing):", Npart
print "itertext:  ", readtext