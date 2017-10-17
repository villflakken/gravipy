import sys
import glob
import numpy as N


class Sifters(object):
    """
    the down-to-the-byte data sifters
    Abbreviations in comments:

    DNN     = Declaration Not Needed
    DNC     = Declaration Need Confirmed
    LDT     = Legacy Debug Tool
    LIDA    = LongID Assumed (hard coded)
    """
    def __init__(self):
        """
        don't yet know what to put here
        """

    def findCount(self, almostpath):
        """
        to figure out the count integer of last file
        """
        pathstrlen      = N.len(almostpath) # i.e. snappath is 49 characters long
        filelist        = glob.glob(almostpath+'*')
        maxfileCount    = N.int32(filelist[-1][:pathstrlen])

        return maxfileCount


    def posvel_sifter(self, f, i):
        """
        sifts through the position/velocities'
        file's data content.
        f is the file object for data retrieval.
        """
        header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
        numpart     = N.fromfile(f, N.int32, 6)
        npart       = numpart[1] # number of particles in this file

        mass    = N.fromfile(f, N.float64, 6)
        pmass   = mass[1] # in units of 10^10 solar masses?
        
        scalefact, redshift     = N.fromfile(f, N.float64, 2)
        flag_sfr, flag_feedback = N.fromfile(f, N.int32, 2)
        
        numpart_tot = N.fromfile(f, N.int32, 6)     # functions as dummy reader
        # ntotal = numpart_tot[1]               # not used
        
        flag_cooling, num_files                     = N.fromfile(f, N.int32, 2)
        boxsize, omega0, omegal, hubble             = N.fromfile(f, N.float64, 4)
        flag_stellarage, flag_metals, hashtabsize   = N.fromfile(f, N.int32, 3)
        # read rest of header_size + 2 dummy integers:
        dummy   = N.fromfile(f, dtype=N.int32, count=23)
        # so in total a count of 21 units of useless header info w/in header_size,
        # and 2 dummy ints

        pos     = N.fromfile(f, N.float32, 3*npart)
        pos     = N.reshape(pos, [npart, 3]).astype(N.float64)
        # this is the way to format with row-major
        # pos     = pos.astype(N.float64) # needed?

        # the velocities were initially listed in the rs:else section,
        #because they're not needed in the "main" program, for which this was written,
        #unless when redshift was investigated?
        dummy   = N.fromfile(f, N.int32, 2)
        vel     = N.fromfile(f, N.float32, 3*npart)
        vel     = N.reshape(vel, [npart, 3]).astype(N.float64)
        
        if (self.rs==0):
            f.close()
            
        else:
            # redshift space mode
            vel                          = vel/100.*N.sqrt(scalefact)
            # rsdir == redshift direction? if i'm not to take this into consideration:
            # pos[:,rsdir]                 = pos[:,rsdir]+vel[:,rsdir]
            pos                          = pos + vel
            pos[N.where(pos < 0)]       += boxsize
            pos[N.where(pos>= boxsize)] -= boxsize

            f.close()

        return pos, vel


    def fof_tab_sifter(self, f, i, skip):
        """
        sifts through the group tab data
        """
        """
        skip = 0L   ; global outside the loop
        skip_sub = 0L ; not even used
        
        Ngroups = 0L
        TotNgroups = 0L
        Nids = 0L
        NTask = 0L
        """
        # these declarations are technically unnecessary
        # Ngroups     = N.int32() # DNN
        # TotNgroups  = N.int32() # DNN
        # Nids        = N.int32() # DNN
        # NTask       = N.int32() # DNN
        """
        readu,1, Ngroups, Nids, TotNgroups, NTask
        """
        # considering there are 4 items, i'm guessing to count 4 times.
        # looks like that from previous example.
        # i'm assuming this information is sort of a "header" for the file.
        Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
        # should there be a dummy distance between this and the next information, or..?
        """
        if fnr eq 0 AND TotNgroups GT 0 then begin
            GroupLen = lonarr(TotNgroups)
            GroupOffset = lonarr(TotNgroups)
        endif

        if Ngroups gt 0 then begin
           
            locLen = lonarr(Ngroups)
            locOffset = lonarr(Ngroups)
     
            readu,1, locLen 
            readu,1, locOffset

            GroupLen[skip:skip+Ngroups-1] = locLen[*]
            GroupOffset[skip:skip+Ngroups-1] = locOffset[*]

            skip+= Ngroups
        endif
        """
        if i == 0 and TotNgroups > 0:
            GroupLen    = N.zeros(TotNgroups, dtype=N.int32) # DNN ???
            GroupOffset = N.zeros(TotNgroups, dtype=N.int32) # DNN ???
            # offset? what is this' purpose?
        if Ngroups > 0:
            # locLen      = N.zeros(Ngroups, dtype=N.int32) # DNN
            # locOffset   = N.zeros(Ngroups, dtype=N.int32) # DNN
            locLen      = N.fromfile(f, N.int32, Ngroups)
            locOffset   = N.fromfile(f, N.int32, Ngroups)
            # wait, WHAT? the _original_ code has in fact "locLen" AND "locLen"?!

            GroupLen[    skip   : skip+Ngroups-1] = locLen[:]
            GroupOffset[ skip   : skip+Ngroups-1] = locOffset[:]
            # oooh-kayyyy..
            # ... oh! oh? maybe? OH! yeah. no, i don't know.

            skip += Ngroups

        f.close()

        return Ngroups, Nids, TotNgroups, locLen, locOffset, GroupLen, GroupOffset, skip


    def fof_ids_sifter(self, f, i, skip):
        """
        sifts through the group id data
        """
        """
        Ngroups = 0L
        TotNgroups = 0L
        Nids = 0L
        NTask = 0L
        readu,1, Ngroups,Nids, TotNgroups,NTask
        ; print, "file=", fnr
        ; print, "Ngroups=", Ngroups, "  TotNgroups=", TotNgroups, " Nids=", Nids,$
        ;       "  NTask=", NTask
        
        IF TotNgroups GT 0 THEN TotNids=total(GroupLen,/double) ELSE TotNids = 0.

        if fnr eq 0 AND TotNids GT 0 then begin
            IDs = lonarr(TotNids)
            IF (LONGID) then IDs=lon64arr(TotNids)
        endif
        """
        # skip        = N.int32() # injected from global
        # Ngroups     = N.int32() # here we go again: and they're reset!
        # TotNgroups  = N.int32() # DNN
        # Nids        = N.int32() # DNN
        # NTask       = N.int32() # DNN 
        Ngroups, TotNgroups, Nids, NTask = N.fromfile(f, N.int32, 4)
        # print "file=", i
        # print "Ngroups=", Ngroups, "  TotNgroups=", TotNgroups, " Nids=", Nids,\
        #       "  NTask=", NTask

        if TotNgroups > 0:
            TotNids = N.sum(GroupLen, dtype=N.float64)  # fix GroupLen so it is available!!!!
        else:
            TotNids = N.float64(0)
        if i == 0 and TotNids > 0:
            IDs = N.zeros(TotNids, dtype=N.int64)       # LIDA
        """
        if Nids gt 0 then begin
        """
        if Nids > 0:
            """  
            locIDs =lonarr(Nids)
            ; locIDs =lonarr(Nids*2)
            """
            # locIDs  = N.zeros(Nids, dtype=N.int32)      # DNN
            # locIDs  = N.zeros(Nids*2, dtype=int32)      # LDT?
            """
            IF (LONGID) then locIDs=lon64arr(Nids)
            readu,1, locIDs
            """
            locIDs = N.fromfile(locIDs, N.int64, Nids)  # DNC, LIDA
            """
            ; IDs[skip:skip+Nids-1] = locIDs[*]
            ; looks like the same as IDs = [IDs,locIDs]...
            ; IDs[skip:skip+Nids-1] = locIDs[indgen(Nids)*2]
            ; Remove the hash table info:
            IDs[skip:skip+Nids-1] = locIDs[*] AND (ishft(1LL,34)-1)
            skip += Nids
            """
            # IDs[   skip : skip+Nids-1 ] = locIDs[:]                 # LDT
            # IDs[   skip : skip+Nids-1 ] = locIDs[range(Nids)*2]     # LDT
            # # Remove the hash table info:
            IDs[   skip : skip+Nids-1 ] = locIDs[:] #and (ishft(1LL,34)-1) !!!!!!!!!!!!!!
                # an AND-statement without a test? what's the initial idea about this?
                # 1LL = int64(1), what exactly does ishft do?
            skip += Nids
        """
        endif
        close, 1
        fnr++
        ; if skip gt 1.01*length then goto, last
        """
        f.close()

        return Ngroups, Nids, TotNgroups, TotNids, IDs, locIDs, skip


    def sub_Totes_counter(self, f, TotNSubs):
        """
        counts TotNsubs.
        last value of TotNgroups is also produced.
        necessary to construct arrays properly in next sifter.
        decided against using this, the 3 necessary lines are now in read_tools
        """
        """
        Ngroups = 0L
        TotNgroups = 0L
        Nids = 0L
        NTask = 0L
        NSubs = 0L
        readu,1, Ngroups, Nids, TotNgroups, NTask, NSubs
        """
        # again, just a preperation line, as if reading a header or something?
        Ngroups, Nids, TotNgroups, NTask, NSubs = N.fromfile(f, N.int32, 5)
            # 5 variables
        """
        close,1
        TotNsubs += NSubs
        fnr++
        """
        f.close()
        TotNsubs += NSubs

        return Ngroups, Nids, TotNgroups, NSubs, TotNsubs


    def sub_tab_sifter(self, f, SubLen, SubOffset, M200, pos, skip):
        """
        sifts through tab files.
        collects identifications of no. of sub halos and structures?
        """

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
        Nsubs = N.fromfile(f, N.int32, 1)
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
                
            """
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
            # ALL OF THESE
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
        ; mass_sub(count:count+ngroups-1L)=halo_m_mean200(*)
        ; pos_sub(*,count:count+ngroups-1L)=subpos(*,firstsubofhalo)
        ; count=count+ngroups
        ; count1=count1+nsubs
        fnr++
        """
        mass_sub[ count : count+ngroups-N.int32(1) ] = halo_m_mean200[:]
        pos_sub[ : , count : count+ngroups-N.int32(1) ] = subpos[ :, firstsubofhalo ]
        count   = count + ngroups
        count1  = count1 + nsubs

        return something

    def sub_ids_sifter(self, lots, of, arguments):
        """
        sifts through ID files.
        collects IDs. i guess?
        also some positions.
        """


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
        IF TotNgroups GT 0 THEN totnids=total(SubLen,/double) ELSE totnids = 0.
        """
        if TotNgroups > 0:
            TotNids = N.sum(SubLen, dtype=N.int64)
        else:
            TotNids = N.int64(0)
        """
        if fnr eq 0 AND TotNids GT 0 then begin
            IDs = lonarr(TotNids)
            IF (LONGID) then Ids=lon64arr(TotNids)
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
        ; if skip gt 1.01*length then goto, last
        """
        #if skip > 1.01*length:
        #    return

        return return_variables # FIGURE THESE OUT TOMORROW

    def fft_sifter(self, openfile):
        """
        sifts through FFT data
        """

        """
        PMGRID=640L
        L=128L
        """
        # PMGRID  = N.int32(640) # not used for anything...
        L       = N.int32(128)
        Lhalf   = L/2

        """ # this is just declaring the memory for the arrays
        ; fft_re=fltarr(Lhalf+1,L+1,L+1) # looks like a zeros-function, specifically float32
        ; fft_im=fltarr(Lhalf+1,L+1,L+1) # if IDL does j,i,k - then python does i,j,k ...?
        """
        #=> becomes the below statements, and shows dimensions: IDL IS COL-MAJOR, PYTHON IS ROW-MAJOR
                            # ask if this results in correct dimensions
        # fft_re = N.zeros((L+1, Lhalf+1, L+1), dtype=N.float32)
        # fft_im = N.zeros((L+1, Lhalf+1, L+1), dtype=N.float32)
        """
        time2 = 0.d0  # this is double precision float, right? float64?
        nsize = long((Lhalf+1)*(L+1)*(L+1))
        """
        time2 = N.float64(0.0) # declaring a double-precision
        nsize = N.int32((Lhalf+1)*(L+1)*(L+1))
        """
        readu,1,time2
        readu,1,nsize # nsize? what is nsize?!
        """
        time2 = N.fromfile(f, N.float64, 1) # reading
        nsize = N.fromfile(f, N.int32, 1) # so, at least it's just a dummy
        print 'time2:  ', time2
        """
        readu,1,fft_re
        readu,1,fft_im
        close,1
        """
        # it seems numpy reads all components of the 3-dim array after each other
        # -> reshape to fix
        fft_re = N.fromfile(f, N.float32, (L+1)*(Lhalf+1)*(L+1) )
        fft_re = N.reshape(fft_re, [L+1, Lhalf+1, L+1] )
        fft_re = ffte_re.astype(N.float64) # <- i seriously doubt this is necessary...
                                         # but here we go, this converts TO float64.
                                         #    as per previous program
        fft_im = N.fromfile(f, N.float32, (L+1)*(Lhalf+1)*(L+1) )
        fft_im = N.reshape(fft_im, [L+1, Lhalf+1, L+1] )
        fft_im = ffte_im.astype(N.float64)
                    # why those +1's all over the place?
        f.close()
        # other than incidental binary dummy data skippers that have to be implemented, or this is finished

        return time2, nsize, fft_re, fft_im

if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. Please run read.py instead.")