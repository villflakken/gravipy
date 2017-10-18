# ==============================================
# Reading procedure for data sets' structure.
# ==============================================
import os, sys
import numpy as N
import pylab as pl
from read_sifters import readSifters
from read_tools import readTools

class readProcedures(readSifters, readTools):
    """
    Contains structures which read the data in question.
    I.o.w.: Every read_*-function shows the program flow of reading procedures.
    Misc. tools for post-processing or other functionalities 
      are imported from read_tools.
    """
    def __init__(self):
        """
        Inheritance and variables
        """
        readSifters.__init__(self)
        readTools.__init__(self)
        self.missingfiles = 0
            # Counter - assumes only 1 type of dataset will be read.

        self.dummypath1 = '/datascope/indra%d/%d_%d_%d' % (0, 0, 0, 0)
        self.dummypath2 = '/snapdir_%03d/snapshot_%03d.' % (0, 0)
        """
        Some fundamental filenames, lists, tuples, bools, and values.
        """
        self.dsp = "/datascope" # datascope path; base file structure path.
                                ### Only here to shorten further string
                                ### supplements also in case of base address
                                ### changes, easy to find.
                                ###### Modify as needed.

        """
        End of init           # but will halt if there's more, inside func below.
        """

    def read_posvel(self):
        """
        Analyzes positions and velocities dataset.
        """
        # indrapath = self.dsp + "/indra%d/%d_%d_%d" \
        #     % (self.indraN, self.indraN, self.iA, self.iB)
        # snappath = indrapath + '/snapdir_%03d/snapshot_%03d.' \
        #     % (self.subfolder, self.subfolder)
        indrapath = self.dsp + self.indraPathParser()
        snappath = indrapath + '/snapdir_{0:03d}/snapshot_{0:03d}.'\
                                .format(self.subfolder)
        # + particular count, comes in the for-loop ## dataset and indra path
        maxfileCount = self.findCount(snappath)
        iterLen      = maxfileCount + 1
        """
        Do a for-loop that counts particles and determines array size
            Let's try a variant that uses lists,
            and see how badly it affects memory... (not very, it seems!)
        """
        posL   = []
        velL   = []
        IDsL   = []
        NpartA = N.zeros(iterLen, dtype=N.int64)

        readtext = "\t Accessing file:\tindra{0}{1}/snap{2}/file.{3} ({4}) ..."
        tmpftxt = "tmp" if self.tmpfolder == True else ""

        for i in N.arange(0, iterLen):
            """
            Will cover all files.
            """
            filepath = snappath + str(i)
            try:
                with open(filepath, 'rb') as openfile:
                    readtext = readtext.format( self.indraN, tmpftxt, 
                                               self.subfolder, i, self.what )
                    # self.itertextPrinter(readtext, i, iterLen, 10)

                    pos, vel, IDsArr, Npart = self.posvel_sifter(openfile, i)
                    print "itertext:  ", readtext
                    print "a_filepath:", filepath
                    print "i:", i, "| Npart (before boxing):", Npart
                    """ Boxed parameters check here:
                    => Potentially strong reduction in memory usage!
                    """
                    print self.box_params
                    print "self.not_NoneFalse(self.box_params):",\
                           self.not_NoneFalse(self.box_params)
                    if self.not_NoneFalse(self.box_params):
                        " Overwerites current data extraction variables "
                        pos, vel, IDsArr, Npart = self.boxer(pos, vel, IDsArr)
                    print "i:", i, "| Npart  (after boxing):", Npart

                    posL.append( pos    )
                    velL.append( vel    )
                    IDsL.append( IDsArr )

                    NpartA[i] =  Npart
                continue

            except IOError:
                self.readLoopError(filepath, 1, 1, i)
                pass
            continue

        maxN         = N.max( NpartA )
        Intermission = """
        Byte sifter has done its job. 
        Max particle number:          {0}
        Sum of particles / (1024**3): {1} / {2}
        Maximum indra particles read?:          {3}
        => Now converting memory storage form from lists to arrays.
        """.format( maxN, N.sum(NpartA), 1024**3, (N.sum(NpartA)==1024**3) )
        print Intermission

        # """
        # Converts input list (with arrays)
        # into a single (bigger) array.
        # """
        IDsA = self.list_to_arrays(IDsL, NpartA, \
                    (iterLen, maxN   ), N.int64  , "IDs")
        posA = self.list_to_arrays(posL, NpartA, \
                    (iterLen, maxN, 3), N.float32, "pos")
        velA = self.list_to_arrays(velL, NpartA, \
                    (iterLen, maxN, 3), N.float32, "vel")


        # """
        # Release memory taken by lists.
        # """
        IDsL = None; posL = None; velL = None

        # TODO: check if all IDs are unique!
        # sys.exit("\nTest done\n")
        
        if self.boolcheck(self.sortIDs):
            SortMessage = """
            Array conversion completed, 
            now sorting particles by assigned 64-bit ID tag.
            """
            posA, velA, IDsA = self.sort_posvel_func(           \
                                    iterLen, maxN, NpartA,      \
                                    posA, velA, IDsA            )
            pass

        endread = "\nFinished reading '"+str(self.what)+"' of files, indra"\
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)    \
                +', snapshot='+str(self.subfolder)

        if self.boolcheck(self.sortIDs):
            endread+=",\n and matrices are now sorted after IDs' values.\n"
            pass

        # print posA[:5, :5,:]
        print endread
        matsizes = IDsA.nbytes + posA.nbytes + velA.nbytes + NpartA.nbytes
        # print " * Size of matrices IDsA, posA, velA, NpartA:", \
        #        (matsizes/(1024.**3.)), " GBs *\n"

        print " * Size of matrices IDsA, posA, velA, NpartA:" \
               + self.item_size_printer(matsizes) +" *\n"


        return IDsA, posA, velA, iterLen, NpartA


    def read_FOF(self):
        """
        Reads friend of friend/group files' id and tab files;
        Takes care of the loops,
        engages byte sifters in each loop.
        Basic error handling.
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" \
            % (self.indraN, self.indraN, self.iA, self.iB)
        snappath = indrapath + "/snapdir_%03d/" % (self.subfolder)
        gtb = snappath + "group_tab_%03d." % (self.subfolder)
        gid = snappath + "group_ids_%03d." % (self.subfolder)

        skip = 0
        maxfileCount_gtb = self.findCount(gtb)

        for i in N.arange(0, maxfileCount_gtb + 1):
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready.
            in case 2 intermediate files are missing, abort.
            """
            filepath = gtb + str(i)
            
            with open(filepath, 'rb') as openfile:
                
                try:
                    fts_output = self.fof_tab_sifter(openfile, i, skip)
                    Ngroups, Nids, TotNgroups, skip = fts_output

                    pass

                except IOError:
                    self.readLoopError(filepath, 1, 2, i)
                    pass

            continue

            # need matrices for these variables to be stored in?
            # file storage probably better

        # print "\n", "TotNgroups    =", TotNgroups, \
        #       "\n\nLargest group of length ", self.length

        if self.sub_asks_for_length == True: # enabling LDT
            return 0 # self.length has been set already, now exiting func 
                     # to continue down in read_sub.
        """
        --------select the biggest subhalo in the first group 
        --------load all of the IDs
        """

        skip = 0    # resetting the variable.
        maxfileCount_gid = self.findCount(gid)

        for i in N.arange(0, maxfileCount_gid + 1):
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready.
            in case 2 intermediate files are missing, abort.
            """
            filepath = gid + str(i)
            
            with open(filepath, 'rb') as openfile:
                
                try:
                    fis_output = self.fof_ids_sifter(openfile, i, skip)
                    skip = fis_output
                    pass

                    if self.bssdt == True: # Big Skip ShutDown Toggle
                        if skip > 1.01*self.length:
                            print "\n skip > 1.01*length - encountered;\n " \
                                    +"reading", self.what, "data;\n "       \
                                    +"for-loop aborted at \n"+filepath
                            return 0

                except IOError:
                    self.readLoopError(filepath, 2, 2, i)
                    pass

            continue

        self.GroupLen = None # Making sure this variable is clear before beginning
                             # of next case in case of multi-run set ups.
        print "Finished reading '"+str(self.what)+"', indra"       \
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)  \
                +', snapshot='+str(self.subfolder)
        
        return 0


    def read_subhalo(self):
        """
        Reads subhalo id and tab files.
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" \
            % (self.indraN, self.indraN, self.iA, self.iB)
        postpath = indrapath + "/postproc_%03d/" % (self.subfolder)
        stb = postpath + "sub_tab_%03d." % (self.subfolder) # sub tab file name
        sid = postpath + "sub_ids_%03d." % (self.subfolder)
        
        nnn         = N.int32(500000)
        # mass_sub   = N.zeros(nnn, dtype=N.float32)    # LDT
        # pos_sub    = N.zeros((3,nnn), dtype=float32)  # LDT
        # First need total # subhalos, not saved like TotNgroups...
        TotNsubs    = N.int32()
        
        self.missingfiles = 0
        maxfileCount_stb  = self.findCount(stb)
        for i in N.arange(0, maxfileCount_stb +1): # [0, 255]   
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready.
            in case 2 intermediate files are missing, abort.
            """
            filepath = stb + str(i)
            
            with open(filepath, 'rb') as openfile:
                
                try:
                    # sTc_output = self.sub_Totes_counter(openfile, TotNsubs)
                    # Ngroups, Nids, TotNgroups, NSubs, TotNsubs = sTc_output

                    # Rewriting this loop's contents into a function,
                    # is _not strictly very necessary_.
                    # The loop's contents is short enough.
                    # Will function as a good check for the tab-files, though.
                    # Keeping the check, simplifying:

                    Ngroups, Nids, TotNgroups, NTask, NSubs = \
                                        N.fromfile(openfile, N.int32, 5)
                    openfile.close()
                    TotNsubs += NSubs
                    pass

                except IOError:
                    self.readLoopError(filepath, 1, 3, i)
                    pass


            continue
        """    
        ### ----------------------- END OF LOOP 1/3 ABOVE
        ### TotNsubs NOW FOUND, as well as TotNgroups from last iteration
        ### ----------------------- NEXT LOOP   2/3 BELOW
        """
        skip        = 0
        count       = 0
        count_sub   = 0     # only used in commented lines
        # next declarations: necessary? -------------------------\
        SubLen      = N.zeros(TotNsubs, dtype=N.int32)          #| DNC
        SubOffset   = N.zeros(TotNsubs, dtype=N.int32)          #| DNC
        M200        = N.zeros(TotNgroups, dtype=N.float32)      #| DNC
        # pos         = N.zeros(TotNgroups*3, dtype=N.float32)    #| DNC
        pos         = N.zeros((TotNgroups,3), dtype=N.float32)  #| DNC
        # -------------------------------------------------------/
        self.missingfiles = 0
        for i in N.arange(0, maxfileCount_stb + 1): # [0, 255]

            filepath = stb + str(i)

            with open(filepath, 'rb') as openfile:

                try:
                    sts_output = self.sub_tab_sifter(openfile, SubLen, \
                                 SubOffset, M200, count, count_sub, pos, skip, i)
                    SubLen, SubOffset, M200, count, count_sub, pos, skip = sts_output
                    pass
                except IOError:
                    self.readLoopError(filepath, 2, 3, i)
                    pass
            continue
        # pos = N.reshape(pos, ) # Can't do it until it's filled!:)


        # mass_sub  = mass_sub[ 0:count_sub-1 ]
        # pos_sub   = pos_sub[ : , 0:count_sub-1 ]
        
        # print "\n ",  TotNgroups   =", TotNgroups
        # print ""\n ", Largest group of length ", GroupLen[0]
        """
        ### ----------------------- END OF LOOP 2/3 ABOVE
        ;-------select the biggest subhalo in the first group 
        ;-------load all of the IDs
        ### ----------------------- NEXT LOOP   3/3 BELOW
        """
        self.loadIDs = True # implement user argument if wanted.

        if keyword_set(self.loadIDs):
            
            if self.bssdt == True: # Big Skip ShutDown Toggle
                self.sub_asks_for_length = True ### should be logical consequence.
                self.read_FOF() # LDT - need to run a section of FOF to get this
                                      # one.
            skip    = 0
            self.missingfiles = 0
            maxfileCount_sid  = self.findCount(sid)

            for i in range(0, self.subidCount + 1):
 
                filepath = sid + str(i)
                with open(filepath, 'rb') as openfile:

                    try:
                        sis_output = self.sub_ids_sifter(openfile, \
                                                         TotNsubs, n, other, IDs, i, skip)
                        # exactly what output/input is needed?
                        dummy, IDs = sis_output
                        # DO SOMETHING ABOUT THIS (,) DUMMY! (heh, gedit?)
                        # need matrices for these variables to be stored in?
                        # file storage probably better
                    
                        if self.bssdt == True:
                            if skip > 1.01*self.length: # LDT !
                                print "\n skip > 1.01*length - encountered;\n " \
                                        +"reading", self.what, "data;\n "       \
                                        +"for-loop aborted at \n"+filepath
                                return 0

                    except IOError:
                        self.readLoopError(filepath, 3, 3, i)
                        pass
                continue
            pass

        print "Finished reading '"+str(self.what)+"', indra"      \
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)  \
                +', snapshot='+str(self.subfolder)
        return 0 # stenger

    def read_FFT(self):
        """
        reads FFT data relevant
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" \
            % (self.indraN, self.indraN, self.iA, self.iB)
        fftpath = indrapath + '/FFT_DATA/FFT_128_%03d.dat' % self.fftfile

        with open(fftpath, 'rb') as openfile:

            try:
                fft_output = self.fft_sifter(openfile)
                pass

            except IOError:
                self.readLoopError(filepath, 1, 1, i)
                pass
        
        dummy = fft_output # DO SOMETHING ABOUT THIS (,) DUMMY! (heh, gedit?)

        return 0



if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")
    # run read.py instead