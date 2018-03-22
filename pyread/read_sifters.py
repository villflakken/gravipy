# ==============================================
# File interpreters for read.py's interface.
# ==============================================
import sys, glob
import numpy as N






class Sifters(object):
    """
    The down-to-the-byte data sifters.
    """
    def __init__(self):
        # self.bitmask      = N.int64(2**34 - 1) # these are both\
        self.bitshiftmask = (N.int64(1)<<34) - 1 # the same value!
        """
        shortest init yet... not a lot is needed! :/
        """

    def findCount(self, almostpath):
        """
        To figure out the count integer of last file:
        these filenames need to be sorted;
        by way of "human"/"natural" sorting.
        """
        pathstrlen  = len(almostpath) # i.e. snappath is 49 characters long
        filelist    = glob.glob(almostpath+'*')
        filenumbers = []

        for filename in filelist:
            filenumbers.append(filename[pathstrlen:])
            continue # Could have used numpy array ops for this

        filenumbers.sort(key=float)
        maxfileCount = N.int32(filenumbers[-1])

        return maxfileCount 


    def posvel_sifter(self, f):
        """
        Sifts through the position/velocities file's data content.
        'f' is the file object for data retrieval.
        """
        header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
        numpart     = N.fromfile(f, N.int32, 6)
        npart       = numpart[1] # Number of DM-particles in this file

        mass  = N.fromfile(f, N.float64, 6)
        pmass = mass[1]     # In units of 10^10 solar masses?
        
        scalefact, redshift     = N.fromfile(f, N.float64, 2)
        flag_sfr, flag_feedback = N.fromfile(f, N.int32, 2)
        
        numpart_tot = N.fromfile(f, N.int32, 6) # not used
        # ntotal = numpart_tot[1]                 # not used
        
        flag_cooling, num_files                   = N.fromfile(f, N.int32, 2)
        boxsize, omega0, omegal, hubble           = N.fromfile(f, N.float64, 4)
        flag_stellarage, flag_metals, hashtabsize = N.fromfile(f, N.int32, 3)
        # Read rest of header_size + 2 dummy integers:
        dummy = N.fromfile(f, dtype=N.int32, count=23)
        # So in total a count of 21 units of useless header info
        # w/in header_size, and 2 dummy ints.

        pos = N.fromfile(f, N.float32, 3*npart)
        pos = N.reshape(pos, [npart, 3])# .astype(N.float64)
        # This is the way to format for row-major use!
        """
        The velocities were initially listed in the 'redshift's else:section,
        because they're not needed in the "main" program,
        for which this was written
        (unless when redshift was investigated?)
        """
        dummy = N.fromfile(f, N.int32, 2)
        vel   = N.fromfile(f, N.float32, 3*npart)
        vel   = N.reshape(vel, [npart, 3])#.astype(N.float64)
        
        """
        Looking at read_indra_snap.pro and other snippet;    
        looks like this will read the assigned IDs:
        """
        dummy = N.fromfile(f, N.int32, 2)
        idarr = N.fromfile(f, N.int64, npart)

        # Next line for clarity on use of IDs as indexations:
        idarr = idarr - N.int64(1)
        # ...now they may be used with indexations on/over arrays!

        f.close()
        return pos, vel, idarr, npart, scalefact, redshift


    def fof_headersift(self, gtab_name=None):
        """
        Yields to the outside:
        * total number of groups/halos, in the set (of files)
        * number of files in the set
        """
        if gtab_name is None:
            " No tabfile-path-name has been given "
            gtab_name = self.fof_pathstrings()[0]
            pass # endIF

        with open(gtab_name + str(0), 'rb') as f:
            # 0; First file in sequence
            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
            f.close() # endWITH

        return TotNgroups, NTask


    def fof_tab_sifter(self, gtab_name=None):
        """
        Sifts through the group tab data.
        """
        if gtab_name is None:
            " No tabfile-path-name has been given "
            gtab_name = self.fof_pathstrings()[0]
            pass # endIF

        TotNgroups, NTask = self.fof_headersift(gtab_name)
        if TotNgroups == 0:
            " This snap has no friends... :( "
            return None, None, None # endIF
            # groupLen == None, groupOffset == None, TotNgroups == None

        else: 
            " Friends detected! "
            print "  - Browsing of FOF-files (tabs): Initiated..."
            groupLen    = N.zeros(TotNgroups, dtype=N.int32)
            groupOffset = N.zeros(TotNgroups, dtype=N.int32)
            istartGroup = 0
            istartIDs   = 0

            " NTask=256 files: "
            for i in N.arange(0, NTask):

                tabpath = gtab_name + str(i)
                with open(tabpath, 'rb') as f:

                    Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
                    if Ngroups > 0:
                        locLen    = N.fromfile(f,N.int32,Ngroups)
                        locOffset = N.fromfile(f,N.int32,Ngroups)
                        groupLen[    istartGroup : istartGroup+Ngroups ] = locLen  
                        groupOffset[ istartGroup : istartGroup+Ngroups ] = locOffset + istartIDs
                                                                                      # !! ^ !!
                            # !istartIDs was not there in the original, as implemented above!!
                        istartGroup += Ngroups
                        istartIDs   += Nids
                        pass  # endIF
                    f.close() # endWITH
                continue

            print "  . Browsing FOF-files (tabs): Complete!"
            pass # endELSE
        return groupLen, groupOffset, TotNgroups


    def fof_ids_sifter(self, gids_name, groupLen=None, groupOffset=None):
        """
        Sifts through the group ID data
        """
        if gids_name is None:
            " No tabfile-path-name has been given "
            gids_name = self.fof_pathstrings()[1]
            pass

        TotNgroups, NTask = self.fof_headersift(gids_name)
        if TotNgroups == 0:
            " This snap has no friends... :( "
            return None, None, None
            # groupLen == None, groupOffset == None, fofIDs == None

        else: 
            " Friends detected! (find them!) "
            print "  - Browsing of FOF-files (IDs): Initiated..."
            if groupLen is None and groupOffset is None:
                # Values not provided from the outside
                gtab_name             = self.fof_pathstrings()[0]
                groupLen, groupOffset = self.fof_tab_sifter(gtab_name)
                pass

            TotNids = N.sum(groupLen, dtype=N.int64)
            fofIDs  = N.zeros(TotNids, dtype=N.int64)
            istart  = 0

            for i in N.arange(0, NTask):

                gidpath = gids_name + str(i)
                with open(gidpath, 'rb') as f:

                    Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
                    if Nids > 0:

                        locIDs = N.fromfile(f, N.int64, Nids)
                        fofIDs[istart:(istart+Nids)] = \
                            N.bitwise_and(locIDs[:], self.bitshiftmask)
                        
                        istart += Nids
                        pass
                    f.close()        
                continue
        
            print "  . Browsing FOF-files (IDs): Complete!"
            pass # endELSE
        
        fofIDs -= 1 # Takes care of indexation discrepancy
        return fofIDs, groupLen, groupOffset


    def subh_headersift(self, stab_name=None, NTask=None):
        """
        Only opens the header of the first file in the set.
        Yields to the outside:
        * total number of subhalos, in the set (of files)
        * number of files in the set
        """
        if stab_name is None:
            " No tabfile-path-name has been given for subh files "
            stab_name = self.subh_pathstrings()[0]
            pass # endIF

        if NTask is None: # Retrieve NTask
            " User did not run fof_headersift before "
            with open(stab_name + str(0), 'rb') as f:
                Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
                f.close() # endWITH
            pass # endIF

        TotNsubs = 0  # Summation value to yield to the outside
        for i in N.arange(0, Ntask):
            with open(stab_name + str(i), 'rb') as f:
                Ngroups, Nids, TotNgroups, NTask, Nsubs = N.fromfile(f, N.int32, 5)
                TotNsubs += Nsubs
                f.close() # endWITH
            continue

        return TotNsubs, NTask


    def subh_cater(self, stab_name, TotNgroups, TotNsubs, NTask):
        """
        (The tab-file sifter)
        Creates a catalogue of the many variables found in the data.
        If there are subhalos in the data, then the data will be read from binary file,
        and then catalogued in a dictionary.
        """

        if TotNsubs == 0:
            " This snap has no subhs... :( "
            return None # endIF

        else: 
            # Sifts through the file
            " Subh detected! (find them!) "
            catalog = {}
            catalog['NsubPerHalo']    = N.zeros( TotNgroups,  dtype=N.int32   )
            catalog['FirstSubOfHalo'] = N.zeros( TotNgroups,  dtype=N.int32   ) # file specific!
            
            catalog['subLen']         = N.zeros( TotNsubs,    dtype=N.int32   )
            catalog['subOffset']      = N.zeros( TotNsubs,    dtype=N.int32   ) # file specific!
            catalog['subParentHalo']  = N.zeros( TotNsubs,    dtype=N.int32   ) # file specific!
            
            catalog['M200mean']       = N.zeros( TotNgroups,  dtype=N.float32 )
            catalog['R200mean']       = N.zeros( TotNgroups,  dtype=N.float32 )
            catalog['M200crit']       = N.zeros( TotNgroups,  dtype=N.float32 )
            catalog['R200crit']       = N.zeros( TotNgroups,  dtype=N.float32 )
            catalog['M200tophat']     = N.zeros( TotNgroups,  dtype=N.float32 )
            catalog['R200tophat']     = N.zeros( TotNgroups,  dtype=N.float32 )
            
            catalog['SubPos']         = N.zeros((TotNsubs,3), dtype=N.float32 )
            catalog['SubVel']         = N.zeros((TotNsubs,3), dtype=N.float32 )
            catalog['SubVelDisp']     = N.zeros( TotNsubs,    dtype=N.float32 )
            catalog['SubVmax']        = N.zeros( TotNsubs,    dtype=N.float32 )
            catalog['SubSpin']        = N.zeros((TotNsubs,3), dtype=N.float32 )
            catalog['SubMostBoundID'] = N.zeros((TotNsubs,2), dtype=N.int32   )
            catalog['SubHalfMass']    = N.zeros( TotNsubs,    dtype=N.float32 )

            # Loop over numfiles (NTask)
            istartSub   = 0
            istartGroup = 0
            istartIDs   = 0
            for i in N.arange(0,NTask):
                with open(stab_name + str(i), 'rb') as f:

                    Ngroups, Nids, TotNgroups, NTask, Nsubs = N.fromfile(f, N.int32, 5)
                    if Nsubs > 0:
                        # Read catalog: Indexes need to include 
                        #               offset from previous files (istarts).
                        # E.N.: This just won't become visually comprehensive, 
                        #       no matter how I edit it...

                        catalog['NsubPerHalo'][    istartGroup:(istartGroup+Ngroups) ] \
                            = N.fromfile(f,N.int32,Ngroups)

                        catalog['FirstSubOfHalo'][ istartGroup:(istartGroup+Ngroups) ] \
                            = N.fromfile(f,N.int32,Ngroups)+istartSub
                
                        catalog['subLen'][         istartSub:(istartSub+Nsubs)  ] \
                            = N.fromfile(f,N.int32,Nsubs)

                        catalog['subOffset'][      istartSub:(istartSub+Nsubs)  ] \
                            = N.fromfile(f,N.int32,Nsubs)+istartIDs

                        catalog['subParentHalo'][  istartSub:(istartSub+Nsubs)  ] \
                            = N.fromfile(f,N.int32,Nsubs)+istartGroup
                        
                        catalog['M200mean'][  istartGroup:(istartGroup+Ngroups)  ] \
                            = N.fromfile(f,N.float32,Ngroups)

                        catalog['R200mean'][  istartGroup:(istartGroup+Ngroups)  ] \
                            = N.fromfile(f,N.float32,Ngroups)

                        catalog['M200crit'][  istartGroup:(istartGroup+Ngroups)  ] \
                            = N.fromfile(f,N.float32,Ngroups)

                        catalog['R200crit'][  istartGroup:(istartGroup+Ngroups)  ] \
                            = N.fromfile(f,N.float32,Ngroups)

                        catalog['M200tophat'][  istartGroup:(istartGroup+Ngroups)  ] \
                            = N.fromfile(f,N.float32,Ngroups)

                        catalog['R200tophat'][  istartGroup:(istartGroup+Ngroups)  ] \
                            = N.fromfile(f,N.float32,Ngroups)

                        thisxyz = N.fromfile(f,N.float32,3*Nsubs)
                        catalog['SubPos'][          istartSub:(istartSub+Nsubs) , :  ] \
                            = N.reshape(thisxyz,[Nsubs,3])

                        thisxyz = N.fromfile(f,N.float32,3*Nsubs)
                        catalog['SubVel'][          istartSub:(istartSub+Nsubs) , :  ] \
                            = N.reshape(thisxyz,[Nsubs,3])

                        catalog['SubVelDisp'][      istartSub:(istartSub+Nsubs)  ] \
                            = N.fromfile(f,N.float32,Nsubs)

                        catalog['SubVmax'][         istartSub:(istartSub+Nsubs)  ] \
                            = N.fromfile(f,N.float32,Nsubs)

                        thisxyz = N.fromfile(f,N.float32,3*Nsubs)
                        catalog['SubSpin'][         istartSub:(istartSub+Nsubs) , :  ] \
                            = N.reshape(thisxyz,[Nsubs,3])

                        catalog['SubMostBoundID'][  istartSub:(istartSub+Nsubs) , :  ] \
                            = N.reshape(N.fromfile(f,N.int32,2*Nsubs), [Nsubs,2])

                        catalog['SubHalfMass'][     istartSub:(istartSub+Nsubs)  ] \
                            = N.fromfile(f,N.float32,Nsubs)

                        istartSub   += Nsubs
                        istartGroup += Ngroups
                        istartIDs   += Nids
                        pass  # endIF
                    f.close() # endWITH
                continue
            pass # endELSE

        return catalog # only the catalogue?


    def subh_idsifter(self, sids_name=None, TotNsubs=None, NTask=None):
        """
        Extract subhalo IDs from post processed data.
        If there are subhalos in the data, then the data will be read from binary file
        """
        stab_name = self.subh_pathstrings()[0]
        if sids_name is None:
            sids_name = self.subh_pathstrings()[1]
            pass # endIF

        # Check/get TotNsubs first!:
        if TotNsubs is None:
            TotNsubs, NTask = self.subh_headersift(stab_name)
            pass # endIF

        if TotNsubs == 0:
            " This snap has no subhs... :( "
            return None # endIF

        else: # And retrieve the appropriate IDs if needed
            " Subh detected! (find them!) "
            
            # Get total number of IDs (including unbound particle IDs)
            TotSubids = 0
            for i in N.arange(0,NTask):

                with open(idsfile + str(i), 'rb') as f:
                    Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
                    TotSubids += Nids
                    f.close() # endWITH
                
                continue

            subIDs = N.zeros(TotSubids,dtype=N.int64)
            
            # Store subIDs
            istart = 0
            for i in N.arange(0,NTask):

                with open(idsfile + str(i), 'rb') as f:
                    Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
                    if Nids > 0:
                        locIDs = N.fromfile(f,N.int64,Nids)
                        # Bitshift to remove the hash table info from the IDs
                        subIDs[istart:(istart+Nids)] = N.bitwise_and(locIDs[:], (N.int64(1)<<34) - 1)
                        istart += Nids
                        pass  # endIF
                    f.close() # endWITH

                continue
            pass # endELSE

        subIDs -= 1  # Indexation discrepancy correction
        return subIDs


    def fft_sifter(self, f):
        """
        Sifts through FFT data.
        """
        L       = N.int32(128)
        Lhalf   = L/2

        time2 = N.fromfile(f, N.float64, 1)
        nsize = N.fromfile(f, N.int32, 1) # long integer, should display value
                                          # (Lhalf+1)*(L+1)*(L+1)
        print 'time2:  ', time2
        print 'nsize:  ', nsize

        fft_re = N.fromfile(f, N.float32, (L+1)*(Lhalf+1)*(L+1) )
        fft_re =   N.reshape(fft_re, [L+1, Lhalf+1, L+1] ).astype(N.float64)

        fft_im = N.fromfile(f, N.float32, (L+1)*(Lhalf+1)*(L+1) )
        fft_im = N.reshape(fft_im, [L+1, Lhalf+1, L+1] ).astype(N.float64)

        f.close()

        return time2, nsize, fft_re, fft_im


    def origami_sifter(self, f):
        """
        Sifts through Origami binary data.
        """
        npart = N.fromfile(f, N.int32, 1)
        tag   = N.fromfile(f, N.int8, npart)
        return npart, tag

    def time_sifter(self, f):
        """
        Designed specifically to retrieve redshift data.
        * Reads a single .i-file.
        """
        header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
        numpart     = N.fromfile(f, N.int32, 6)
        npart       = numpart[1] # Number of DM-particles in this file

        mass = N.fromfile(f, N.float64, 6)
        
        scalefact, redshift = N.fromfile(f, N.float64, 2)

        return scalefact, redshift


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")
    # run read.py instead