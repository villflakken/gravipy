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
        Reads positions and velocities datasets.
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


        t_pvread_end = time.time()
        t_pvread_tot = t_pvread_end - t_pvread_start
        print "      : dt = {0:g} s".format(t_pvread_tot)


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

        # The reading is done, the bells have toll'd;
        # print out the stats, parameters, and all!
        return IDsA.astype(N.int32), posA, velA


    def read_fof(self):
        """
        Reads friend of friend/group files' id and tab files;
        this function is a playground for what ever I would want to do.
        """
        gtab_name, gids_name = self.fof_pathstrings() # Generating names
        # maxfileCount_gtb = self.findCount(gtab_name) # May be used for debugging
        # iterLen          = maxfileCount_gtb + 1

        TotNgroups, groupLen, groupOffset = self.fof_tab_sifter(gtab_name)
        fofIDs    , groupLen, groupOffset = self.fof_ids_sifter(gids_name, groupLen, groupOffset)
        # print "\tTotNgroups = ({0:>10d})".format(TotNgroups)

        # print "   . Finished reading 'FoF'"
        return fofIDs, TotNgroups, groupLen, groupOffset


    def read_subhalo(self):
        """
        Reads subhalo id and tab files. But not in that order.
        """
        gtab_name = self.fof_pathstrings()[0]
        stab_name, sids_name = self.subh_pathstrings()
        # s(ubhalo)tab_(file)name
        # s(ubhalo)IDs_(file)name

        " Need 'TotNgroups' from fof-reading, for the subh. catalog as well: "
        TotNgroups, NTask = self.fof_headersift(gtab_name)
        TotNsubs,   NTask = self.subh_headersift(stab_name, NTask=NTask)

        # Ca(talogue out)put
        catalog = self.subh_cater(stab_name, TotNgroups, TotNsubs, NTask)
        subIDs  = self.subh_idsifter(sids_name, TotNsubs, NTask)
        # print "\tTotNsubs   = ({0:>10d})".format(TotNsubs)

        # print "   . Finished reading 'SubHalo'"
        return subIDs, TotNsubs, catalog


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


        # print "   . Finished reading 'Origami'"
        return tags


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
            # print itertext
            scalefact, redshift = self.time_sifter(openfile)

            openfile.close()

        return scalefact, redshift


    # Not currently supported in the algorithm.
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


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")
    # run read.py instead