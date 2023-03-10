# ==============================================
# Reading procedure for data sets' structure.
# ==============================================
import os, sys, time
import numpy as N
from read_sifters import Sifters
from read_misctools import MiscTools
from read_usertools import UserTools
from read_autotools import AutoTools
from read_plotdoc import Plotter


class readProcedures(Sifters, MiscTools, UserTools, AutoTools, Plotter):
    """
    Contains structures which read the data in question.
    I.o.w.: Every read_*-function shows the program flow of reading procedures.
    Misc. tools for post-processing or other functionalities 
      are imported from read_*tools classes.
    """
    def __init__(self):
        """
        Inheritance and variables
        """
        Sifters.__init__(self)
        AutoTools.__init__(self)
        MiscTools.__init__(self)
        UserTools.__init__(self)
        Plotter.__init__(self)
        self.missingfiles = 0
        # Counter - assumes only 1 type of dataset will be read.

        # DT
        self.dummypath1 = '/datascope/indra%d/%d_%d_%d' % (0, 0, 0, 0)
        self.dummypath2 = '/snapdir_%03d/snapshot_%03d.' % (0, 0)
        """
        End of init
        """

    def read_posvel(self):
        """
        Analyzes positions and velocities dataset.
        """
        t_pvread_start = time.time() # Time manager

        indrapath = self.dsp + self.indraPathParser()
        snappath = indrapath + '/snapdir_{0:03d}/snapshot_{0:03d}.'\
                                .format(self.subfolder)
        # + particular count, comes in the for-loop ## dataset and indra path
        maxfileCount = self.findCount(snappath)
        iterLen      = maxfileCount + 1
        
        " Total no. of particles is set: "
        Npart_tot = 1024**3

        posA      = N.zeros( (Npart_tot,3), dtype=N.float32 )
        velA      = N.zeros( (Npart_tot,3), dtype=N.float32 )
        IDsA      = N.zeros(  Npart_tot   , dtype=N.int64   )
        NpartA    = N.zeros(  iterLen     , dtype=N.int64   )
        scalefA   = N.zeros(  iterLen     , dtype=N.float64 )
        rsA       = N.zeros(  iterLen     , dtype=N.float64 )

        readtext = "  * Accessing file:\tindra{0}{1}/snap{2:02d}/file.{3:<3} ({4}) ..."
        tmpftxt  = "tmp" if self.tmpfolder == True else ""

        ci = 0 # Current index to update

        for i in N.arange(0, iterLen):
            """
            Will cover all files.
            """
            filepath = snappath + str(i)
            try:
                with open(filepath, 'rb') as openfile:
                    itertext = readtext.format( self.indraN, tmpftxt, 
                                                self.subfolder, i, self.what )
                    self.itertextPrinter(itertext, i, iterLen, 50)
                    
                    " Retrieval "
                    pos, vel, IDsArr, Npart, scalefact, redshift = \
                        self.posvel_sifter(openfile)
                    
                    " Inside-loop 'sorting' - by correct assignment: pos & vel "
                    if self.boolcheck(self.sortIDs):
                        posA[IDsArr, :]      = pos
                        velA[IDsArr, :]      = vel
                        pass

                    else:
                        posA[ci:ci+Npart, :] = pos
                        velA[ci:ci+Npart, :] = vel
                        IDsA[ci:ci+Npart]    = IDsArr
                        pass

                    NpartA[i]  = Npart
                    scalefA[i] = scalefact
                    rsA[i]     = redshift

                    ci += Npart

                continue # Next binary file's turn

            except IOError:
                self.readLoopError(filepath, 1, 1, i)
                pass

            continue # Next binary file's turn

        " Out-of-loop 'sorting' - by generation: IDs "
        # if self.boolcheck(self.sortIDs):
        #     IDsA = N.arange(0, Npart_tot, dtype=N.int64) # Readily sorted IDs! :)
        #     print "    \=> positions' array now sorted by ID tag."
        #     pass

        t_pvread_end = time.time()
        t_pvread_tot = t_pvread_end - t_pvread_start 
        print "      : dt = {0:g} s".format(t_pvread_tot)

        # DT - getting a handle on why so many files would include RS data
        if self.arrval_equaltest(scalefA) != True:
            print "All scalefactor elements are _not_ equal!"
            print "Scalefactor values retrieved:"
            print scalefA
            pass

        if self.arrval_equaltest(rsA) != True:
            print "All redshift elements are _not_ equal!"
            print "Redshift values retrieved:"
            print rsA
            pass

        # File reading loop completed; print status
        countedNpart = N.sum(NpartA)
        maxN         = N.max(NpartA)
        Intermission = """
    Byte sifter completed. 
    Max particle number in a file:      {0}
    Sum particles read / Tot. in sim.:  {1:g} / {2:g} ( {3:g}% )
    Maximum indra particles read?:      {4}""".format( 
            maxN, countedNpart, 1024**3, 100*countedNpart/(1024.**3.),
            (countedNpart==1024**3) )
        print Intermission
        matsizes = IDsA.nbytes + posA.nbytes + velA.nbytes + NpartA.nbytes
        print "    Size of array    IDsA = " + self.item_size_printer(IDsA.nbytes)
        print "    Size of matrix   posA = " + self.item_size_printer(posA.nbytes)
        print "    Size of matrix   velA = " + self.item_size_printer(velA.nbytes)
        print "    Size of array  NpartA = " + self.item_size_printer(NpartA.nbytes)
        print "    Total size of matrices IDsA, posA, velA, NpartA = " \
               + self.item_size_printer(matsizes) 

        # Old ID-pos-vel sorting block
        '''
        if self.boolcheck(self.sortIDs):
            print """
    Sifter has completed reading all {0} files of snap {1}.
    - Commencing method for sorting positions and velocities."""\
                            .format(iterLen, self.subfolder)
            IDsA, posA, velA = self.sort_from_IDsF(IDsA, posA, velA, self.what)
            pass
        '''

        # The reading is done, the bells have toll'd;
        # print out the stats, parameters, and all!
        endread = "\n    Finished reading '"+str(self.what)+"' of files, indra"\
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)    \
                +', snapshot='+str(self.subfolder)+"\n"
        if self.boolcheck(self.sortIDs):
            endread+="     - and matrices are sorted after IDs' values.\n"
            pass
        print endread

        " returns what user needs, specifically: "
        if self.what == "pos":
            return IDsA, posA, scalefA[0], rsA[0]

        elif self.what == "vel":
            return IDsA, velA, scalefA[0], rsA[0]

        else:
            sys.exit("\n    *** read_posvel task name error *** \n")


    def read_fof_old(self):
        """
        Reads friend of friend/group files' id and tab files;
        Takes care of the loops,
        engages byte sifters in each loop.
        Basic error handling.
        """
        indrapath = self.dsp + self.indraPathParser()
        snappath = indrapath + '/snapdir_{0:03d}/'.format(self.subfolder)

        gtb = snappath + "group_tab_{0:03d}.".format(self.subfolder)
        gid = snappath + "group_ids_{0:03d}.".format(self.subfolder)

        skip             = 0
        maxfileCount_gtb = self.findCount(gtb)
        iterLen          = maxfileCount_gtb + 1
        Ngroups_thusfar  = N.zeros(iterLen, dtype=N.int32)

        " Need header to get lengths of GroupLen&Offset "
        self.GroupLen    = None # Declare first to clear namespace,
        self.GroupOffset = None # just to be thorough.
        self.IDs         = None

        " Opens first file of snapshot set; retrieve partial header info "
        get_aheader = gtb + str(0) # First file in sequence
        with open(get_aheader, 'rb') as openfile:
            # , as in, the 'TotNgroups' variable
            glgo_lengths = N.fromfile(openfile, N.int32, 4)[2] 
            self.GroupLen    = N.zeros(glgo_lengths, dtype=N.int32)
            self.GroupOffset = N.zeros(glgo_lengths, dtype=N.int32)
            openfile.close()

        print "  * Browsing FOF-files (tabs):"
        headertext = """\
        ---------------------------------------------------------------------
        |  i  | NIDs    | Ngroups | sum(Ngroups) | TotNgroups | Completion: |
        ---------------------------------------------------------------------"""
        if self.subfolder % 7 == 0:
            " Don't print for every subfolder "
            print headertext
            pass

        readtext = """\
        | {0:>3d} | {1:>7d} | {2:>7d} | {3:>12d} | {4:>10d} | {5:>9.2f}%  |
        ---------------------------------------------------------------------"""

        for i in N.arange(0, iterLen):

            filepath = gtb + str(i)
            with open(filepath, 'rb') as openfile:
                fts_output = self.fof_tab_sifter(openfile, i, skip)
                Ngroups, Nids, TotNgroups, skip = fts_output
                
                Ngroups_thusfar[i] = Ngroups
                itertext = readtext.format( 
                    i,
                    Nids,
                    Ngroups,
                    N.sum(Ngroups_thusfar),
                    TotNgroups,
                    N.sum(Ngroups_thusfar[:i+1]) \
                        *100./float(TotNgroups)  \
                            if TotNgroups > 0 else 0
                )

            if self.subfolder % 7 == 0:
                " Don't print for every subfolder "
                self.itertextPrinter(itertext, i, iterLen, 50)
                pass

            continue

        print "  * Browsing FOF-files (tabs): Complete"

        if self.sub_asks_for_length == True: # enabling LDT
            return 0 # self.length has been set already, now exiting func 
                     # to continue down in read_sub.
  

        skip = 0    # resetting the variable.
        maxfileCount_gid = self.findCount(gid)
        iterLen          = maxfileCount_gid + 1

        print "\n  * Browsing FOF-files (IDs):"
        for i in N.arange(0, iterLen):

            filepath = gid + str(i)
            with open(filepath, 'rb') as openfile:
                fis_output = self.fof_ids_sifter(openfile, i, skip)
                skip       = fis_output
            
            continue


        self.IDs -= 1 # Correcting for indexing: [1,..,N] => [0,..,N-1]
        print "  * Browsing FOF-files (IDs): Complete"


        print " => Finished reading '"+str(self.what)+"', indra"       \
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)  \
                +', snapshot='+str(self.subfolder)
        
        return Ngroups, Nids, TotNgroups, self.GroupLen, self.GroupOffset, self.IDs


    def read_subhalo_old(self):
        """
        Reads subhalo id and tab files. But not in that order.
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
        TotNsubs    = N.int32(0)
        
        self.missingfiles = 0
        maxfileCount_stb  = self.findCount(stb)
        iterLen           = maxfileCount_stb + 1
        for i in N.arange(0, iterLen): 
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready.
            in case 2 intermediate files are missing, abort.
            """
            filepath = stb + str(i)
            
            try:
                with open(filepath, 'rb') as openfile:
                    " Building NSubs' value "
                    Ngroups, Nids, TotNgroups, NTask, NSubs = \
                        N.fromfile(openfile, N.int32, 5)
                    TotNsubs += NSubs
                    openfile.close()
                pass

            except IOError:
                self.readLoopError(filepath, 1, 3, i)
                pass

            continue
        # endfor

        """
        ### ----------------------- END OF LOOP 1/3 ABOVE
        ### TotNsubs NOW FOUND, as well as TotNgroups from last iteration
        ### ----------------------- NEXT LOOP   2/3 BELOW
        """
        skip        = 0
        count       = 0
        count_sub   = 0     # Is only used in commented lines
        # next declarations: necessary? -------------------------\
        SubLen      = N.zeros(TotNsubs,       dtype=N.int32)    #| DNC
        SubOffset   = N.zeros(TotNsubs,       dtype=N.int32)    #| DNC
        M200        = N.zeros(TotNgroups,     dtype=N.float32)  #| DNC
        # pos         = N.zeros(TotNgroups*3, dtype=N.float32)    #| DNC
        pos         = N.zeros((TotNgroups,3), dtype=N.float32)  #| DNC
        # -------------------------------------------------------/
        
        self.missingfiles = 0
        for i in N.arange(0, iterLen): # [0, 255]

            filepath = stb + str(i)
            try:

                with open(filepath, 'rb') as openfile:
                    sts_output = self.sub_tab_sifter(
                        openfile, SubLen, SubOffset, M200, 
                        count, count_sub, pos, skip, i
                    )
                    SubLen, SubOffset, M200, count, count_sub, pos, skip = sts_output
                pass

            except IOError:
                self.readLoopError(filepath, 2, 3, i)
                pass
            continue

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
            
        if self.bssdt == True: # Big Skip ShutDown Toggle
            self.sub_asks_for_length = True ### should be logical consequence.
            self.read_FOF() # LDT - need to run a section of FOF to get this
                            # one.
        skip    = 0
        self.missingfiles = 0
        maxfileCount_sid  = self.findCount(sid)

        for i in range(0, self.subidCount + 1):

            filepath = sid + str(i)
            try:
                with open(filepath, 'rb') as openfile:
                    sis_output = self.sub_ids_sifter(
                        openfile, TotNsubs, nnn, other, IDs, i, skip
                    )
                    dummy, IDs = sis_output
                
                    if self.bssdt == True:
                        if skip > 1.01*self.length: # LDT !
                            print "\n skip > 1.01*length - encountered;\n " \
                                    +"reading", self.what, "data;\n "       \
                                    +"for-loop aborted at \n"+filepath
                            return 0
                pass

            except IOError:
                self.readLoopError(filepath, 3, 3, i)
                pass

            continue

        print "Finished reading '"+str(self.what)+"', indra"                \
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB) \
                +', snapshot='+str(self.subfolder)
        return 0 

    def read_fft(self):
        """
        FFT data reading procedure
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


    def read_origami(self):
        """
        Reads ORIGAMI's data output
        """
        # --- --- --- --- Solely for data's filename/path mgmt

        oridatpath = self.origamiPathParser()

        ori_open_error_str = """
        Could not find origami file at specified path: {0:s}
        """.format(oridatpath)
        # --- --- --- --- Name parsing complete

        " Actual reading "
        try:
            with open(oridatpath, 'rb') as openfile:
                # Npart, tag = self.origami_sifter(openfile)
                Npart = N.fromfile(openfile, N.int32, 1)
                tags  = N.fromfile(openfile, N.int8, Npart)
            pass

        except IOError:
            sys.exit(ori_open_error_str)

        return tags, Npart[0]


    def read_time(self):
        """
        Designed specifically to retrieve scalefactor and redshift data.
        * Reads a single .i-file.
        """
        indrapath = self.dsp + self.indraPathParser()
        snappath = indrapath + '/snapdir_{0:03d}/snapshot_{0:03d}.'\
                                .format(self.subfolder)

        readtext = "  * Accessing file:\tindra{0}{1}/snap{2}/file.{3:<3} ({4}) ..."
        tmpftxt  = "tmp" if self.tmpfolder == True else ""

        filepath = snappath + str(0)
        with open(filepath, 'rb') as openfile:
            itertext = readtext.format( self.indraN, tmpftxt, 
                                       self.subfolder, 0, self.what )
            print itertext
            scalefact, redshift = self.time_sifter(openfile)
            
            openfile.close()

        return scalefact, redshift


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")
    # run read.py instead