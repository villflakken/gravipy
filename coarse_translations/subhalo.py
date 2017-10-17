

    def read_subhalo(self):
        """ YAY, 2 down, 2 to go!
        reads subhalo id and tab files
        """
        """
        PRO read_sub, Base,num,TotNgroups,TotNids,M200,pos,$
                  IDs,Sublen,SubOffset,loadIDs=loadIDs # resources that are loaded
        ;Base="/datascope/indra3/0_0_0/"
        """
        """ # looks like text formatting for iterative string counter
            # useless w.r.t. python for loop and str format
        ;num = 25 ; snapnum
        if num ge 1000 then begin
            exts='0000'
            exts=exts+strcompress(string(Num),/remove_all)
            exts=strmid(exts,strlen(exts)-4,4)
        endif else begin
            exts='000'
            exts=exts+strcompress(string(Num),/remove_all)
            exts=strmid(exts,strlen(exts)-3,3) ; snapnum string
        endelse
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        postpath = indrapath + "/postproc_%03d/" % (self.subdirC)
        stb = postpath + "sub_tab_%03d." % (self.subdirC) # sub tab file name
        sid = postpath + "sub_ids_%03d." % (self.subdirC)
        """
        skip = 0L
        skip_sub = 0L
        fnr = 0L
        nnn=500000L
        ;mass_sub=fltarr(nnn)
        ;pos_sub=fltarr(3,nnn)
        count=0L
        count1=0L
        count_sub = 0L
        ; First need total # subhalos, not saved like TotNgroups...
        TotNSubs = 0L
        """
        skip        = N.int32()
        skip_sub    = N.int32()
        nnn         = N.int32(500000)
        # mass_sub   = N.zeros(nnn, dtype=N.float32)
        # pos_sub    = N.zeros((3,nnn), dtype=float32)
        count       = N.int32()
        count1      = N.int32()
        count_sub   = N.int32()
        TotNSubs    = N.int32()
        """
        repeat begin
        """
        for i in N.arange(0, self.subtabCount): # [0, 255]   
            """
            f = Base+"/postproc_"+exts+"/sub_tab_"+exts +"."$
                 +strcompress(string(fnr),/remove_all)
            openr,1,f
            """
            filepath    = stb + str(i) # /postproc_xyz/sub_tab_xyz.i
            f           = open(filepath, 'rb')
            """
            Ngroups = 0L
            TotNgroups = 0L
            Nids = 0L
            NTask = 0L
            NSubs = 0L
            readu,1, Ngroups, Nids, TotNgroups, NTask, NSubs
            """
            Ngroups     = N.int32()
            TotNgroups  = N.int32()
            Nids        = N.int32()
            NTask       = N.int32()
            NSubs       = N.int32()
            # again, just a preperation line, as if reading a header or something?
            Ngroups, Nids, TotNgroups, NTask, NSubs = N.fromfile(f, N.int32, 5)
                # 5 variables
            """
            close,1
            TotNSubs += NSubs
            fnr++
            """
            f.close()
            TotNSubs += NSubs
        """    
        endrep until fnr eq NTask
        """
        """
        fnr = 0L
        SubLen = lonarr(TotNsubs)
        SubOffset = lonarr(TotNsubs)
        M200 = fltarr(totNgroups)
        pos = fltarr(3,totNgroups)
        """
        SubLen      = N.zeros(TotNsubs, dtype=N.int32)
        SubOffset   = N.zeros(TotNsubs, dtype=N.int32)
        M200        = N.zeros(totNgroups, dtype=N.float32)
        pos         = N.zeros((totNgroups,3), dtype=N.float32)
        """
        repeat begin
        """
        for i in N.arange(0, self.subtabCount): # [0, 255]
            """
            f = Base+"/postproc_"+exts+"/sub_tab_"+exts +"."$
                 +strcompress(string(fnr),/remove_all)
            openr,1,f
            """
            filepath    = stb + str(i)
            f           = open(filepath, 'rb')
            """
            Ngroups = 0L
            TotNgroups = 0L
            Nids = 0L
            NTask = 0L
            readu,1, Ngroups, Nids, TotNgroups, NTask
            ; print,'Ngroups = ', Ngroups
            ; print,'TotNgroups = ', TotNgroups
            Nsubs = 0L
            readu,1,Nsubs
            """
            Ngroups     = N.int32()
            TotNgroups  = N.int32()
            Nids        = N.int32()
            NTask       = N.int32()
            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
            # print 'Ngroups      = ', Ngroups
            # print 'TotNgroups   = ', TotNgroups
            Nsubs       = N.int32()
            N.fromfile(f, N.int32, 1)
            """
            ; Why would Nsubs be 0? ... in this certain file?
            IF Nsubs GT 0 THEN BEGIN
            """
            if Nsubs > 0:
                """
                NsubPerHalo = lonarr(Ngroups)
                FirstSubOfHalo = lonarr(Ngroups)
                locLen=lonarr(Nsubs)
                locOffset=lonarr(Nsubs)
                SubParentHalo= lonarr(Nsubs)
                """
                NsubPerHalo     = N.zeros(Ngroups, dtype=N.int32)
                FirstSubOfHalo  = N.zeros(Ngroups, dtype=N.int32)
                locLen          = N.zeros(Nsubs, dtype=N.int32)
                locOffset       = N.zeros(Nsubs, dtype=N.int32)
                SubParentHalo   = N.zeros(Nsubs, dtype=N.int32)
                """
                readu,1, NsubPerHalo , FirstSubOfHalo, locLen, locOffset, SubParentHalo
                """
                # NsubPerHalo , FirstSubOfHalo, locLen, locOffset, SubParentHalo = N.fromfile(f, N.int32, 5)
                    # wait: the information is potentially arranged with different byte lengths, count != 5 (!!!), count=Ngroups & count=Nsubs
                NsubPerHalo, FirstSubOfHalo = N.fromfile(f, N.int32, Ngroups*2)
                    # Ngroups*2, right? since there are 2*(bytelength of 1 array) being read?
                locLen, locOffset, SubParentHalo = N.fromfile(f, N.int32, Nsubs*3)
                    
                """    # why is there indentation here?
                    # don't think it matters for IDL, so i'm cancelling it out;
                    #it matters to python
                    SubLen[skip:skip+Nsubs-1] = locLen[*]
                    SubOffset[skip:skip+Nsubs-1] = locOffset[*]
                    skip+= Nsubs
                """
                SubLen[     skip : skip+Nsubs-1 ] = locLen[:]
                SubOffset[  skip : skip+Nsubs-1 ] = locOffset[:]
                    
                skip += Nsubs
                """
                ; print,"Nsubs= ", Nsubs,total(loclen)
                Halo_M_Mean200 = fltarr(Ngroups)
                Halo_R_Mean200 = fltarr(Ngroups)
                Halo_M_Crit200 = fltarr(Ngroups)
                Halo_R_Crit200 = fltarr(Ngroups)
                Halo_M_TopHat200 = fltarr(Ngroups)
                Halo_R_TopHat200 = fltarr(Ngroups)
                """
                # print "Nsubs= ", Nsubs, N.sum(loclen, dtype=N.float64)
                Halo_M_Mean200      = N.zeros(Ngroups, dtype=N.float32)
                Halo_R_Mean200      = N.zeros(Ngroups, dtype=N.float32)
                Halo_M_Crit200      = N.zeros(Ngroups, dtype=N.float32)
                Halo_R_Crit200      = N.zeros(Ngroups, dtype=N.float32)
                Halo_M_TopHat200    = N.zeros(Ngroups, dtype=N.float32)
                Halo_R_TopHat200    = N.zeros(Ngroups, dtype=N.float32)
                """
                readu,1, Halo_M_Mean200, Halo_R_Mean200 
                readu,1, Halo_M_Crit200, Halo_R_Crit200 
                readu,1, Halo_M_TopHat200, Halo_R_TopHat200
                """
                Halo_M_Mean200, Halo_R_Mean200 = N.fromfile(f, N.float32, Ngroups*2)
                # yeah, still unsure about that *2-thing.
                # does numpy divide the arrays into equal parts?
                Halo_M_Crit200, Halo_R_Crit200 = N.fromfile(f, N.float32, Ngroups*2)
                Halo_M_TopHat200, Halo_R_TopHat200 = N.fromfile(f, N.float32, Ngroups*2)
                """
                M200[count:count+Ngroups-1] = Halo_M_Crit200
                SubPos = fltarr(3, Nsubs)
                SubVel = fltarr(3, Nsubs)
                SubVelDisp = fltarr(Nsubs)
                SubVmax = fltarr(Nsubs)
                SubSpin = fltarr(3, Nsubs)
                SubMostBoundID = lonarr(2, Nsubs)
                Subhalfmass=fltarr(Nsubs)
                """
                M200[ count : count+Ngroups-1 ] = Halo_M_Crit200
                SubPos          = N.zeros((Nsubs,3), dtype=N.float32)
                SubVel          = N.zeros((Nsubs,3), dtype=N.float32)
                SubVelDisp      = N.zeros(Nsubs, dtype=N.float32)
                SubVmax         = N.zeros(Nsubs, dtype=N.float32)
                SubSpin         = N.zeros((Nsubs,3), dtype=N.float32)
                SubMostBoundID  = N.zeros((Nsubs,2), dtype=N.int32)
                Subhalfmass     = N.zeros(Nsubs, dtype=N.float32)
                """
                readu,1, SubPos, SubVel, SubVelDisp, SubVmax, SubSpin, SubMostBoundID, $
                  Subhalfmass
                pos[*,count:count+Ngroups-1] = subpos[*,firstsubofhalo]
                count += Ngroups
                """
                # CORRECT DIM INSERTIONS ATTEMPT - FIRST TRY
                SubPos          = N.fromfile(f, N.float32, Nsubs*3)
                SubPos          = N.reshape(SubPos, [Nsubs, 3])
                
                SubVel          = N.fromfile(f, N.float32, Nsubs*3)
                SubVel          = N.reshape(SubVel, [Nsubs, 3])

                SubVelDisp      = N.fromfile(f, N.float32, Nsubs)
                SubVmax         = N.fromfile(f, N.float32, Nsubs)

                SubSpin         = N.fromfile(f, N.float32, Nsubs*3)
                SubSpin         = N.reshape(SubSpin, [Nsubs, 3])

                SubMostBoundID  = N.fromfile(f, N.int32, Nsubs*2)
                SubMostBoundID  = N.reshape(SubMostBoundID, [Nsubs, 2])

                Subhalfmass     = N.fromfile(f, N.float32, Nsubs)

                pos[:, count : count+Ngroups-1 ] = subpos[ :, firstsubofhalo ]

            else:
                print 'Nsubs = 0'
            f.close()
            """
            ENDIF; ELSE print,'nsubs = 0'
            
            close, 1
            ; Below running into indexing errors
            ; ind=where(sublen gt 20)
            ; if (ind[0] ne -1 ) then begin
            ;     num_chos=n_elements(ind)
            ;     mass_sub[count:count+num_chos-1L]=sublen[ind]
            ;     pos_sub[*,count:count+num_chos-1L]=subpos[*,ind]
            ;     count_sub=count_sub+num_chos
            ; endif
            """
            # # ind = N.where(sublen > 20) # wait, no, surely you mean:
            # ind = N.argwhere(sublen > 20)
            # if (ind[0] != -1):
            #     num_chos = len(ind)
            #     mass_sub[ count : count+num_chos-N.int32(1)] = sublen[ind]
            #     pos_sub[ : , count : count+num_chos-N.int32(1) ] = subpos[*,ind]
            #     count_sub = count_sub + num_chos
            """
            ; mass_sub(count:count+Ngroups-1L)=halo_m_mean200(*)
            ; pos_sub(*,count:count+Ngroups-1L)=subpos(*,firstsubofhalo)
            ; count=count+Ngroups
            ; count1=count1+nsubs
            fnr++
            """
            mass_sub[ count : count+Ngroups-N.int32(1) ] = halo_m_mean200[:]
            pos_sub[ : , count : count+Ngroups-N.int32(1) ] = subpos[ :, firstsubofhalo ]
            count   = count + Ngroups
            count1  = count1 + nsubs
        

        """
        endrep until fnr eq NTask
        ; mass_sub=mass_sub[0:count_sub-1L]
        ; pos_sub=pos_sub[*,0:count_sub-1L]
        """
        # mass_sub = mass_sub[0 : count_sub-N.int32(1) ]
        # pos_sub = pos_sub[ :, 0 : count_sub-N.int32(1) ]

        """
        ; print
        ; print, "TotNgroups   =", TotNgroups
        ; print
        ; print, "Largest group of length ", GroupLen(0)
        """
        # print
        # print "TotNgroups   =", TotNgroups
        # print
        # print "Largest group of length ", GroupLen(0)

        """
        ;-------select the biggest subhalo in the first group ---------------------------
        ;-------load all of the IDs  ----------------------------------------------------
        IF keyword_set(loadIDs) THEN BEGIN
        skip = 0L
        fnr = 0L
        ; length=grouplen(0)
        ; Offset=GroupOffset(0)
        LONGID=1
        """
        if keyword_set(loadIDs):
            skip    = N.int32(0)
            fnr     = N.int32(0)
            # length  = grouplen(0)
            # Offset  = GroupOffset(0)
            LONGID  = 1
            """
            repeat begin
            """
            for i in range(0, self.subidCount):
                """
                f = Base + "/postproc_" + exts +"/sub_ids_"+exts +"."$
                     +strcompress(string(fnr),/remove_all)
                openr,1,f
                """
                filepath    = sid + str(i) # /postproc_xyz/sub_ids_xyz.i
                f           = open(filepath, 'rb')
                """
                Ngroups = 0L
                TotNgroups = 0L
                Nids = 0L
                NTask = 0L
                readu,1, Ngroups,Nids, TotNgroups,NTask
                ; print, "file=", fnr
                ; print, "Ngroups=", Ngroups, "  TotNgroups=", TotNgroups, " Nids=", Nids,$
                ;        "  NTask=", NTask
                """
                Ngroups     = N.int32()
                TotNgroups  = N.int32()
                Nids        = N.int32()
                NTask       = N.int32()
                Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
                """
                IF totNgroups GT 0 THEN TotNids=total(Sublen,/double) ELSE TotNids = 0.
                """
                if TotNgroups > 0:
                    TotNids = N.sum(SubLen, dtype=N.float32)
                else:
                    TotNids = N.float32(0)
                """
                if fnr eq 0 AND TotNids GT 0 then begin
                    IDs = lonarr(TotNids)
                    IF (LONGID) then IDs=lon64arr(TotNids)
                endif
                """
                if i == 0 and TotNids > 0:
                    if (LONGID != True):
                        IDs = N.zeros(TotNids, dtype=N.int32)
                    else:
                        IDs = N.zeros(TotNids, dtype=N.int64)
                """
                if Nids gt 0 then begin
                    locIDs =lonarr(Nids)
                    IF (LONGID) then locIDs=lon64arr(Nids)
                    readu,1, locIDs
                ;    IDs[skip:skip+Nids-1] = locIDs[*]
                ;    looks like the same as IDs = [IDs,locIDs]...
                ; Remove the hash table info:
                    IDs[skip:skip+Nids-1] = locIDs[*] AND (ishft(1LL,34)-1)
                    skip+= Nids
                endif
                """
                if Nids > 0:
                    if (LONGID == False):
                        # locIDs  = N.zeros(Nids, dtype=N.int32)  # DNN
                        locIDs  = N.fromfile(f, N.int32, Nids)
                    else:
                        # locIDs = N.zeros(Nids, dtype=N.int64)   # DNN
                        locIDs  = N.fromfile(f, N.int64, Nids)
                    # Remove the hash table info:
                    IDs[ skip : skip+Nids-1 ] = locIDs[:] #and (isfht()) # wtf-ery.... wtf!?
                    skip += Nids

                f.close()

                """
                close, 1
                fnr++
                ; if skip gt 1.01*length then goto, last
                """
                #if skip > 1.01*length:
                #    return


            """
            endrep until fnr eq NTask
            ;particle IDs of halo N=10 
            ;N=10
            ;ids_group0=IDs[GroupOffset[N]:GroupOffset[N]+grouplen[N]-1]
            """
            # particle IDs of halo N=10
            Number = 10
            ids_group0 = IDs[ GroupOffset[Number] : GroupOffset[Number]+grouplen[Number]-1 ]
        """
        ENDIF
        last:
        end
        """
        return 0

