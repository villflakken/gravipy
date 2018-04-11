# Original file received before I got sick in February,
# now coarsely adapted for GRAVIPy after middle of March.
# Contains functions belonging to: 
# * read_procedures,
# * read_miscTools
# * read_sifters
# - Magnus, d:21 m:March y:18

#: read_procedures

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
        print "    TotNgroups = ({0:>10d})".format(TotNgroups)

        print "\n    Finished reading '"+str(self.what)+"' of files, indra" \
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB) \
                +', snapshot='+str(self.subfolder)+"\n"
        
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
        caput   = self.subh_cater(stab_name, TotNgroups, TotNsubs, NTask)
        catalog = caput # cataloguer output # I imagine I may want more variables as output?
        subIDs  = self.subh_idsifter(sids_name, TotNsubs, NTask)
        print "    TotNsubs = ({0:>10d})".format(TotNsubs)

        print "\n    Finished reading '"+str(self.what)+"' of files, indra" \
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB) \
                +', snapshot='+str(self.subfolder)+"\n"
                
        return subIDs, catalog


#: read_sifters

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
            return 0, None, None # endIF
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

            print "  . Browsing FOF-files (tabs): ...Complete!"
            pass # endELSE

        return TotNgroups, groupLen, groupOffset


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
        
            print "  . Browsing FOF-files (IDs): ...Complete!"
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
        for i in N.arange(0, NTask):
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

                with open(sids_name + str(i), 'rb') as f:
                    Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
                    TotSubids += Nids
                    f.close() # endWITH
                
                continue

            subIDs = N.zeros(TotSubids,dtype=N.int64)
            
            # Store subIDs
            istart = 0
            for i in N.arange(0,NTask):

                with open(sids_name + str(i), 'rb') as f:
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


#: read_misctools

    def fof_pathstrings(self):
        """
        Generates paths & filenames for tabs and ids
        """
        indrapath = self.dsp  +  self.indraPathParser()
        snappath  = indrapath +  "/snapdir_{0:03d}/".format(self.subfolder)
        gtab_name = snappath  + "group_tab_{0:03d}.".format(self.subfolder)
        gids_name = snappath  + "group_ids_{0:03d}.".format(self.subfolder)

        return gtab_name, gids_name


    def subh_pathstrings(self):
        """
        Generates paths & filenames for tabs and ids
        """
        indrapath = self.dsp  + self.indraPathParser()
        postpath  = indrapath + "/postproc_{0:03d}/".format(self.subfolder)
        stab_name = postpath  +   "sub_tab_{0:03d}.".format(self.subfolder)
        sids_name = postpath  +   "sub_ids_{0:03d}.".format(self.subfolder)

        return stab_name, sids_name
