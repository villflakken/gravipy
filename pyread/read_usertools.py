# ==============================================
# Read.& proc. toolkit for data sets' structure.
# ==============================================
import os, sys, time
import numpy as N






class UserTools(object):
    """
    User-activated tools that are used in the readProcedures instance.
    """
    def __init__(self):
        # Purely for debugging reasons
        if sys.platform in ("linux", "linux2"):
            self.uname = os.path.expanduser("~")+"/"

            pass

        elif sys.platform in ("win32", "win64"):
            self.uname = os.path.expanduser("~")+"\\"
            pass

        else:
            sys.exit("Error in UserTools' init.")
        """
        End of init
        """

    def box_indexer(self, pos, box_params):
        """
        Extracts slices of data, determined from 3D positions.
        self.box_params = [ [0.,20.],[0.,20.],[0.,5.] ]
        """
        print "  * Boxing indexation commenced "
        xmin, xmax = box_params[0]
        ymin, ymax = box_params[1]
        zmin, zmax = box_params[2]

        " Bool'ed indexation "
        box3D =  N.array( pos[:,0] >= xmin ) \
               * N.array( pos[:,1] >= ymin ) \
               * N.array( pos[:,2] >= zmin ) \
                                             \
               * N.array( pos[:,0] <= xmax ) \
               * N.array( pos[:,1] <= ymax ) \
               * N.array( pos[:,2] <= zmax )

        print "  * Boxing indexation retrieved "

        return box3D


    def arrboxes(self, IDs, pos, arr2, box_params):
        """
        Simple function to minimize command lines, returns a boxed array.
        """
        print "  * Applying box "
        box3D = self.box_indexer(pos, box_params)
        IDs   =  IDs[box3D]
        pos   =  pos[box3D]
        arr2  = arr2[box3D]
        print "  * Box applied \n"

        return IDs, pos, arr2 # Because 'arr2' could be a FoF-thing or something...


    def sort_from_IDsF(self, IDs, pos=None, vel=None, focus="what"):
        """
        Sorts IDs, and an accompanying array after sorted IDs.
        focus is meant to be a string object, taking arguments either:
        * "pos"    (- velocity array is returned as None          )
        * "vel"    (- position array is returned as None          )
        * "posvel" (- in case user wants both sorted and returned )
        """
        print "  * Sorting IDs now ..." # ..need this sorted anyway.
        t_argfind_start = time.time()

        IDsSortedArgs   = N.argsort(IDs)      # The actual ...

        t_argfind_end   = time.time()
        t_argfind_tot   = t_argfind_end - t_argfind_start
        print "    \=> IDs indexes sequenced. "
        print "      : dt = {0:g} s".format(t_argfind_tot)

        t_argsort_start = time.time()
        IDs             = IDs[IDsSortedArgs]  # ... sorting mechanism
        t_argsort_end   = time.time()
        t_argsort_tot   = t_argsort_end - t_argsort_start
        print "    \=> IDs sorted. "
        print "      : dt = {0:g} ss".format(t_argsort_tot)

        if focus == "pos":
            " Sorts positions "

            print "  * Sorting positions."
            t_possort_start = time.time()

            pos = pos[IDsSortedArgs]

            t_possort_end = time.time()
            t_possort_tot = t_possort_end - t_possort_start
            print "    \=> positions' array now sorted by ID tag."
            print "      : dt = {0:g} s".format(t_possort_tot)
            return IDs, pos, None

        elif focus == "vel":
            " Sorts velocities"

            print "  * Sorting velocities."
            vel = vel[IDsSortedArgs]
            print "    \=> velocities' array now sorted by ID tag.\n"
            return IDs, None, vel

        elif focus == "posvel":
            " Sorts both "
            self.sort_from_IDsF(IDs=IDs, pos=pos, focus="pos")
            self.sort_from_IDsF(IDs=IDs, vel=vel, focus="vel")
            # ------------------------------ #
            return IDs, pos, vel

        elif focus == "what":
            " User has not input anything to focus on, will assume positions.. "
            self.sort_from_IDsF(IDs=IDs, pos=pos, vel=None, focus="pos")
            return 0

        else:
            sort_of_errortext = " Sorting selector test failed (!?!) "
            pass

        print sort_of_errortext
        return 0


    #### REWRITE THESE TO BE LESS DEPENDENT ON INSTANCE VARIABLES

    def outputPather(self, folderPath, fileName):
        """
        Checks if output folder structure exists
        & creates output path for output file
        & filepath- & name based on env. params.
        * Note: based in user's home folder,
                folder structure based on intended task.
        """

        folderPath = folderPath+fileName

        self.fileName = fileName

        if not os.path.exists(self.uname + folderPath):
            os.makedirs(self.uname + folderPath)
            print "    Creating output folder structure: ", \
                   self.uname + folderPath
            pass
        else:
            print "    Output folder already exists: ", \
                   self.uname + folderPath
            pass

        self.outfilePath = self.uname + folderPath # This is easier, anyway.

        return self.outfilePath


    # Useful functions below

    def linewriter(self, datalist, w):
        """
        This is a function that will write listed data as needed
        """
        maxlen = len(datalist)

        lineToWrite = ""
        for i in range(len(datalist)):
            lineToWrite += "{0:>20}".format(datalist[i])
            continue

        w.write(lineToWrite)
        return 0


    def funcNameOver(self, where="1up"):
        """
        :return: Name of nested function in which this function is called.
        Useful for debugging.
        """
        ranks = {"inception": 0, "here": 1, "1up": 2, "2up": 3}
        return str(sys._getframe(ranks[where]).f_code.co_name)


    def boolcheck(self, arg):
        """ Don't want random user input cluttering;
        only allows 1 and True as boolean statements from user. """
        return any([arg == 1, arg == True])


    def not_NoneFalse(self, arg):
        """ I need SOME kind of check...
        Returns True when arg's value is true.
        """
        return all([arg != 0, arg != False, arg != None])




if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")