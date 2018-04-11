

    def read_FOF(self):
        """
        reads friend of friend/group files' id and tab files
        """

        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        snappath = indrapath + "/snapdir_%03d/" % (self.sdirC)
        gtb = snappath + "group_tab_%03d." % (self.sdirC)
        gid = snappath + "group_ids_%03d." % (self.sdirC)

        """
        skip = 0L
        skip_sub = 0L
        fnr = 0L
        """
        skip        = N.int32()
        skip_sub    = N.int32()

        """
        to figure out the count integer of last file
        """
        pathstrlen_gtb      = len(gtb)
        filelist_gtb        = glob.glob(gtb+'*')
        maxfileCount_gtb    = N.int32(filelist_gtb[-1][:pathstrlen_gtb])

        """
        repeat begin
        """
        for i in N.arange(0, maxfileCount_gtb):                 # THE NEW FOR LOOP!
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready
            """
            filepath    = gtb + str(i)
            f           = open(filepath, 'rb')

            """
            Ngroups = 0L
            TotNgroups = 0L
            Nids = 0L
            NTask = 0L
            """
            Ngroups     = N.int32() # these declarations are technically unnecessary
            TotNgroups  = N.int32()
            Nids        = N.int32()
            NTask       = N.int32()
            """
            readu,1, Ngroups, Nids, TotNgroups, NTask
            """
            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
            # considering there are 4 items, i'm guessing to count 4 times. looks like that from previous example
            # i'm assuming this information is sort of a "header" for the file

            # should then be a dummy distance between this and the next information, or..?
            """
            if fnr eq 0 AND TotNgroups GT 0 then begin
                GroupLen = lonarr(TotNgroups)
                GroupOffset = lonarr(TotNgroups)
            endif
            """
            if i == 0 and TotNgroups > 0:
                GroupLen    = N.zeros(TotNgroups, dtype=N.int32) # DNN
                GroupOffset = N.zeros(TotNgroups, dtype=N.int32) # DNN
                # offset? what is this' purpose?
            """
            if Ngroups gt 0 then begin
               
                locLen = lonarr(Ngroups)
                locOffset = lonarr(Ngroups)
         
                readu,1, loclen 
                readu,1, locOffset

                GroupLen[skip:skip+Ngroups-1] = locLen[*]
                GroupOffset[skip:skip+Ngroups-1] = locOffset[*]

                skip+= Ngroups
            endif
            """
            if Ngroups > 0:
                locLen      = N.zeros(Ngroups, dtype=N.int32) # DNN
                locOffset   = N.zeros(Ngroups, dtype=N.int32)

                loclen      = N.fromfile(f, N.int32, Ngroups)
                # wait, WHAT? the _original_ code has in fact "loclen" AND "locLen"?!
                locOffset   = N.fromfile(f, N.int32, Ngroups)

                GroupLen[    skip   : skip+Ngroups-1] = locLen[:]
                GroupOffset[ skip   : skip+Ngroups-1] = locOffset[:] # oooh-kayyyy..
                    # ... oh! oh? maybe? OH! yeah. no, i don't know.

                skip += Ngroups
            """
            close, 1
            """
            f.close()
            # end of for loop, actually...
            """
            fnr++ # yes, seems to be friend number iterator
            """

        """
        ;print
        ;print, "TotNgroups   =", TotNgroups
        ;print
        ;print, "Largest group of length ", GroupLen(0)
        """
        print "\n", "TotNgroups    =", TotNgroups, "\n\nLargest group of length ", GroupLen[0]
        


        """
        ;-------select the biggest subhalo in the first group ---------------------------
        ;-------load all of the IDs  ----------------------------------------------------
        skip = 0L
        fnr = 0L
        """
        skip = N.int32() # resetting the variable w.r.t. previous iterations
        """
        ;length=grouplen(0)
        ;offset=groupoffset(0)
        LONGID=1
        """

        pathstrlen_gid      = len(gid)
        filelist_gid        = glob.glob(gid+'*')
        maxfileCount_gid    = N.int32(filelist_gid[-1][:pathstrlen_gid])

        """
        repeat begin
        """
        for i in N.arange(0, maxfileCount_gid):                         # THE NEW FOR LOOP!
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready
            """
            filepath        = gtb + str(i)
            f           = open(filepath, 'rb')

            """
            Ngroups = 0L
            TotNgroups = 0L
            Nids = 0L
            NTask = 0L
            """
            Ngroups     = N.int32() # here we go again: and they're reset!
            TotNgroups  = N.int32()
            Nids        = N.int32()
            NTask       = N.int32()        
            """
            readu,1, Ngroups,Nids, TotNgroups,NTask
            ; print, "file=", fnr
            ; print, "Ngroups=", Ngroups, "  TotNgroups=", TotNgroups, " Nids=", Nids,$
            ;       "  NTask=", NTask
            """
            Ngroups, TotNgroups, Nids, NTask = N.fromfile(f, N.int32, 4)
            print "file=", i
            print "Ngroups=", Ngroups, "  TotNgroups=", TotNgroups, " Nids=", Nids,\
                  "  NTask=", NTask

            """
            IF totNgroups GT 0 THEN totnids=total(grouplen,/double) ELSE totnids = 0.

            if fnr eq 0 AND TotNids GT 0 then begin
                IDs = lonarr(TotNids)
                IF (LONGID) then Ids=lon64arr(TotNids)
            endif
            """
            if totNgroups > 0:
                totnids = N.sum(grouplen, dtype=N.float64)
            else:
                totnids = N.float64(0.)
            if i == 0 and TotNids > 0:
                # IDs = N.zeros(TotNids, dtype=N.int32)       # DNN
                # if (LONGID): # i'm guessing this is to check id-tag float type?
                #     IDs = N.zeros(TotNids, dtype=N.int64)
                """
                below check could intuitively be put in below if-test;
                though having it here leaves the possibility of an array,
                even when Nids == 0.
                """
                """
                if (LONGID == False):
                    IDs = N.zeros(TotNids, dtype=N.int32)
                else:
                    IDs = N.zeros(TotNids, dtype=N.int64)
                """
            """
            if Nids gt 0 then begin
            """
            if Nids > 0:
                """  
                locIDs =lonarr(Nids)
                ; locIDs =lonarr(Nids*2)
                """
                # locIDs  = N.zeros(Nids, dtype=N.int32)      # DNN
                # locIDs  = N.zeros(Nids*2, dtype=int32)
                """
                IF (LONGID) then locIDs=lon64arr(Nids)
                readu,1, locIDs
                """
                # if (LONGID): # so WHAT is LONGID? i need conclusive usage description!
                #     locIDs = N.zeros(Nids, dtype=N.int64)   # DNN 
                #         # - instead, make this condition activate correct fromfile statement
                # locIDs = N.fromfile(locIDs, N.int64, Nids) 
                        # surely, the counter here is to read Nids no. of numbers?
                        # ok, this should probably be arranged slightly differently, with
                        #   2 different fromfile statements instead.
                if (LONGID == False):
                    # locIDs = N.zeros(Nids, dtype=N.int32)      # DNN
                    locIDs = N.fromfile(locIDs, N.int32, Nids) 
                else:
                    # locIDs = N.zeros(Nids, dtype=N.int64)      # DNN
                    locIDs = N.fromfile(locIDs, N.int64, Nids) 

                """
                ; IDs[skip:skip+Nids-1] = locIDs[*]
                ; looks like the same as IDs = [IDs,locIDs]...
                ; IDs[skip:skip+Nids-1] = locIDs[indgen(Nids)*2]
                ; Remove the hash table info:
                IDs[skip:skip+Nids-1] = locIDs[*] AND (ishft(1LL,34)-1)
                skip += Nids
                """
                # IDs[ skip : skip+Nids-1 ] = locIDs[:]
                # # looks like the same as IDs = [IDs,locIDs]...
                # IDs[ skip : skip+Nids-1 ] = locIDs[range(Nids)*2]
                        # indgen? oh, it's python's range function!
                # # Remove the hash table info:
                IDs[   skip : skip+Nids-1 ] = locIDs[:] #and (ishft(1LL,34)-1)
                    # an AND-statement without a test? what's the initial idea about this?
                skip += Nids
            """
            endif
            close, 1
            fnr++
            ; if skip gt 1.01*length then goto, last
            """
            f.close()
            # if skip > 1.01*length:
                # return 0
                # python does not support "goto", but functions' return statement is neat!
        """
        endrep until fnr eq NTask

        ; particle IDs of halo N=10 
        ; N=10
        ; ids_group0=ids[groupoffset[N]:groupoffset[N]+grouplen[N]-1]
        """
        # particle IDs of halo N=10
        # Number = 10
        # ids_group0 = ids[ groupoffset[Number]] : groupoffset[Number]+grouplen[Number]-1 ]
        """
        last:
        end
        """
        return 0