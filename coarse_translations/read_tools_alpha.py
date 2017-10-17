import sys
import glob

class readTools(object):
    """
    contains all toos necessary to read/evaluate the data in question
    """
    def __init__(self):
        """
        at the moment only used for testing some stuff
        """
        self.mult_miss_error = """
            Never expected there to be /more than one/ file missing.
            Maybe the dataset should be properly completed first?
            Aborting!
        """

        self.dummypath1 = '/datascope/indra%d/%d_%d_%d' % (0, 0, 0, 0)
        self.dummypath2 = '/snapdir_%03d/snapshot_%03d.' % (0, 0)
        """
        init end
        """


    def read_posvel_beta_tryexcept(self):
        """
        takes in filename, initializes dataset reading
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        snappath = indrapath + '/snapdir_%03d/snapshot_%03d.' % (self.sdirC, self.sdirC)
        # + particular count, comes in the for-loop ## dataset and indra path

        maxfileCount = self.find_count(snappath)

        for i in N.arange(0, maxfileCount):
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready
            """
            filepath        = snappath + str(i)
            try:
                f           = open(filepath, 'rb')

            except IOError:
                errorstring = """
                Whilst reading %s dataset,
                filepath :  %s  ;
                File no. %d seems to be missing.
                    """ % (self.what, filepath, i)

                skipfile_i = self.error_w_user_input(errorstring) # should return the integer 1.
                i += skipfile_i # maybe this and prev. line could/should be concatenated; later maybe
                
                filepath        = snappath + str(i)
                try:
                    f           = open(filepath, 'rb')
                except IOError:
                    sys.exit(self.mult_miss_error)


            # now, continue your glorious purpose!
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
            # so in total a count of 21 lines of useless header info, and 2 dummy ints (?)
            pos     = N.fromfile(f, N.float32, 3*npart)
            pos     = N.reshape(pos, [npart, 3])
            pos     = pos.astype(N.float64) # needed?

            # the velocities were initially listed in the rs:else section,
            #because they're not needed in the "main" program, for which this was written,
            #unless when redshift was investigated?
            dummy   = N.fromfile(f, N.int32, 2)
            vel     = N.fromfile(f, N.float32, 3*npart)
            vel     = N.reshape(vel, [npart, 3])
            
            if (rs==0):
                f.close()
                
            else:
                # redshift space mode
                vel                          = vel.astype(N.float64)/100*N.sqrt(scalefact)
                pos[:,rsdir]                 = pos[:,rsdir]+vel[:,rsdir]
                pos[N.where(pos < 0)]       += boxsize
                pos[N.where(pos>= boxsize)] -= boxsize

                f.close()

        print 'finished reading positions and velocities of particles, indra'\
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)+', snapshot='+str(self.sdirC)
        return 0

    def read_posvel_beta_whileversion(self):
        '''
        the while-loop idea i had for varying lengths of datasets
        '''
        """
        analyzes positions and velocities dataset
        """

        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        snappath = indrapath + '/snapdir_%03d/snapshot_%03d.' % (self.sdirC, self.sdirC)
        # + particular count, comes in the for-loop ## dataset and indra path


        # a straight-forward (but seriously ugly) file-numerated, flexible
        #way of doing this; reads _all_ files.
        i = N.int32(0) # counter
        try:
            while i > -1:
                """
                will loop infinitely,
                until it breaks from _not_ finding a loop's current file (!)
                => should work as long as file enumeration is continuous
                    (which it should be)
                """
                filepath    = snappath + str(i)
                f           = open(filepath, 'rb')

                header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
                numpart     = N.fromfile(f, N.int32, 6)
                npart       = numpart[1] # number of particles in this file

                mass    = N.fromfile(f, N.float64, 6)
                pmass   = mass[1] # in units of 10^10 solar masses?
                
                scalefact, redshift     = N.fromfile(f, N.float64, 2)
                flag_sfr, flag_feedback = N.fromfile(f, N.int32, 2)
                
                numpart_tot = N.fromfile(f, N.int32, 6)     # functions as dummy
                # ntotal = numpart_tot[1]               # not used
                
                flag_cooling, num_files                     = N.fromfile(f, N.int32, 2)
                boxsize, omega0, omegal, hubble             = N.fromfile(f, N.float64, 4)
                flag_stellarage, flag_metals, hashtabsize   = N.fromfile(f, N.int32, 3)

                # read rest of header_size + 2 dummy integers:
                dummy   = N.fromfile(f, dtype=N.int32, count=23)
                # so in total a count of 21 lines of useless header info, and 2 dummy ints (?)
                pos     = N.fromfile(f, N.float32, 3*npart)
                pos     = N.reshape(pos, [npart, 3])
                pos     = pos.astype(N.float) # needed?

                # the velocities were initially listed in the rs:else section,
                #because they're not needed in the "main" program, for which this was written,
                #unless when redshift was investigated?
                dummy   = N.fromfile(f, N.int32, 2)
                vel     = N.fromfile(f, N.float32, 3*npart)
                vel     = N.reshape(vel, [npart, 3])
                
                if (rs==0):
                    f.close()
                    
                else:
                    # redshift space mode
                    vel                         = vel.astype(N.float)/100*N.sqrt(scalefact)
                    pos[:,rsdir]                = pos[:,rsdir]+vel[:,rsdir]
                    pos[N.where(pos < 0)]       += boxsize
                    pos[N.where(pos>= boxsize)] -= boxsize

                    f.close()

                # pindex+=npart
                i += N.int32(1)

        except IOError:
            """
            when the counter runs out of files to access (normally around i=256)
            """
            print 'finished reading positions and velocities of particles, indra'\
                    +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)+', snapshot='+str(self.sdirC)
            return 0
            
    def read_posvel_alpha(self):
        '''
        the orignal translation of the legacy code
        '''
        """
        analyzes positions and velocities dataset
        """

        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        snappath = indrapath + '/snapdir_%03d/snapshot_%03d.' % (self.sdirC, self.sdirC)
        # + particular count, comes in the for-loop ## dataset and indra path

        for i in N.arange(0, self.snapCount): # [0, 255]
            filepath    = snappath + str(i)
            f           = open(filepath, 'rb')

            header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
            numpart     = N.fromfile(f, N.int32, 6)
            npart       = numpart[1] # number of particles in this file

            mass    = N.fromfile(f, N.float64, 6)
            pmass   = mass[1] # in units of 10^10 solar masses?
            
            scalefact, redshift     = N.fromfile(f, N.float64, 2)
            flag_sfr, flag_feedback = N.fromfile(f, N.int32, 2)
            
            numpart_tot = N.fromfile(f, N.int32, 6)     # functions as dummy
            # ntotal = numpart_tot[1] # not used
            
            flag_cooling, num_files                     = N.fromfile(f, N.int32, 2)
            boxsize, omega0, omegal, hubble             = N.fromfile(f, N.float64, 4)
            flag_stellarage, flag_metals, hashtabsize   = N.fromfile(f, N.int32, 3)

            # read rest of header_size + 2 dummy integers:
            dummy   = N.fromfile(f, dtype=N.int32, count=23) # so in total a count of 21 lines of useless header info, and 2 dummy ints (?)
            pos     = N.fromfile(f, N.float32, 3*npart)
            pos     = N.reshape(pos, [npart, 3])
            pos     = pos.astype(N.float) # needed?

            # the velocities were listed in the rs:else section, because they're not needed in the "main" program for which this was written, unless when redshift was investigated?
            dummy   = N.fromfile(f, N.int32, 2)
            vel     = N.fromfile(f, N.float32, 3*npart)
            vel     = N.reshape(vel, [npart, 3])
            
            if (rs==0):
                f.close()
                
            else:
                # redshift space mode
                vel                         = vel.astype(N.float)/100*N.sqrt(scalefact)
                pos[:,rsdir]                = pos[:,rsdir]+vel[:,rsdir]
                pos[N.where(pos < 0)]       += boxsize
                pos[N.where(pos>= boxsize)] -= boxsize

                f.close()

            # pindex+=npart
        print 'finished reading positions and velocities of particles, indra'\
            +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)+', snapshot='+str(self.sdirC)
        return 0

    def read_pos_only(self):
        """
        reads positions.
        ONLY positions are investigated;
        dummies are useful and used for sifting through useless information.
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        snappath = indrapath + '/snapdir_%03d/snapshot_%03d.' % (self.sdirC, self.sdirC)
                # + particular count, in the for-loop ## dataset and indra path
        """
        to figure out the count integer of last file
        """
        pathstrlen      = len(snappath) # snappath is 49 characters long
        filelist        = glob.glob(snappath+'*')
        maxfileCount    = N.int32(filelist[-1][:pathstrlen])

        for i in N.arange(0, maxfileCount):
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready
            """
            filepath        = snappath + str(i)
            try:
                f           = open(filepath, 'rb')

            except IOError:
                errorstring = """
                Whilst reading %s dataset,
                filepath :  %s  ;
                File no. %d seems to be missing.
                    """ % (self.what, filepath, i)

                skipfile_i = self.error_w_user_input(errorstring) # should return the integer 1.
                i += skipfile_i # maybe this and prev. line could/should be concatenated; later maybe
                
                filepath        = snappath + str(i)
                try:
                    f           = open(filepath, 'rb')
                except IOError:
                    sys.exit(self.mult_miss_error)

            header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
            numpart     = N.fromfile(f, N.int32, 6)
            npart       = numpart[1] # number of particles in this file

            mass    = N.fromfile(f, N.float64, 6)
            pmass   = mass[1] # in units of 10^10 solar masses?
            
            scalefact, redshift     = N.fromfile(f, N.float64, 2)
            flag_sfr, flag_feedback = N.fromfile(f, N.int32, 2)
            
            numpart_tot = N.fromfile(f, N.int32, 6)     # functions as dummy
            # ntotal = numpart_tot[1]               # not used
            
            flag_cooling, num_files                     = N.fromfile(f, N.int32, 2)
            boxsize, omega0, omegal, hubble             = N.fromfile(f, N.float64, 4)
            flag_stellarage, flag_metals, hashtabsize   = N.fromfile(f, N.int32, 3)

            # read rest of header_size + 2 dummy integers:
            dummy   = N.fromfile(f, dtype=N.int32, count=23)
            # so in total a count of 21 lines of useless header info, and 2 dummy ints (?)
            pos     = N.fromfile(f, N.float32, 3*npart)
            pos     = N.reshape(pos, [npart, 3])
            pos     = pos.astype(N.float) # needed?

            if (rs==0):
                f.close()
                
            else:
                # redshift space mode
                dummy   = N.fromfile(f, N.int32, 2)
                vel     = N.fromfile(f, N.float32, 3*npart)
                vel     = N.reshape(vel, [npart, 3])

                vel                         = vel.astype(N.float)/100*N.sqrt(scalefact)
                pos[:,rsdir]                = pos[:,rsdir]+vel[:,rsdir]
                pos[N.where(pos < 0)]       += boxsize
                pos[N.where(pos>= boxsize)] -= boxsize

                f.close()

        print 'finished reading positions and velocities of particles, indra'\
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)+', snapshot='+str(self.sdirC)
        return 0
        # finish this function - replace velocities with dummies where able


    def read_vel_only(self, snappath):
        """
        reads velocities.
        ONLY velocities are investigated;
        dummies are useful and used for sifting through useless information.
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        snappath = indrapath + '/snapdir_%03d/snapshot_%03d.' % (self.sdirC, self.sdirC)
        # + particular count, comes in the for-loop ## dataset and indra path
        """
        to figure out the count integer of last file
        """
        pathstrlen      = len(snappath) # snappath is 49 characters long
        filelist        = glob.glob(snappath+'*')
        maxfileCount    = N.int32(filelist[-1][:pathstrlen])

        for i in N.arange(0, maxfileCount):
            """
            will cover all files.
            in case an intermediate file is missing, have an option ready
            """
            filepath        = snappath + str(i)
            try:
                f           = open(filepath, 'rb')

            except IOError:
                errorstring = """
                Whilst reading %s dataset,
                filepath :  %s  ;
                File no. %d seems to be missing.
                    """ % (self.what, filepath, i)

                skipfile_i = self.error_w_user_input(errorstring) # should return the integer 1.
                i += skipfile_i # maybe this and prev. line could/should be concatenated; later maybe
                
                filepath        = snappath + str(i)
                try:
                    f           = open(filepath, 'rb')
                except IOError:
                    sys.exit(self.mult_miss_error)

            header_size = N.fromfile(f, N.int32, 1)[0] # = 256: error catch here?
            numpart     = N.fromfile(f, N.int32, 6)
            npart       = numpart[1] # number of particles in this file

            mass    = N.fromfile(f, N.float64, 6)
            pmass   = mass[1] # in units of 10^10 solar masses?
            
            scalefact, redshift     = N.fromfile(f, N.float64, 2)
            flag_sfr, flag_feedback = N.fromfile(f, N.int32, 2)
            
            numpart_tot = N.fromfile(f, N.int32, 6)     # functions as dummy
            # ntotal = numpart_tot[1]               # not used
            
            flag_cooling, num_files                     = N.fromfile(f, N.int32, 2)
            boxsize, omega0, omegal, hubble             = N.fromfile(f, N.float64, 4)
            flag_stellarage, flag_metals, hashtabsize   = N.fromfile(f, N.int32, 3)

            # read rest of header_size + 2 dummy integers:
            dummy   = N.fromfile(f, dtype=N.int32, count=23)
            # so in total a count of 21 lines of useless header info, and 2 dummy ints (?)
            pos     = N.fromfile(f, N.float32, 3*npart)
            pos     = N.reshape(pos, [npart, 3])
            pos     = pos.astype(N.float) # needed?

            # the velocities were initially listed in the rs:else section,
            #because they're not needed in the "main" program, for which this was written,
            #unless when redshift was investigated?
            dummy   = N.fromfile(f, N.int32, 2)
            vel     = N.fromfile(f, N.float32, 3*npart)
            vel     = N.reshape(vel, [npart, 3])
            
            if (rs==0):
                f.close()
                
            else:
                # redshift space mode
                vel                         = vel.astype(N.float)/100*N.sqrt(scalefact)
                pos[:,rsdir]                = pos[:,rsdir]+vel[:,rsdir]
                pos[N.where(pos < 0)]       += boxsize
                pos[N.where(pos>= boxsize)] -= boxsize

                f.close()

        print 'finished reading positions and velocities of particles, indra'\
                +str(self.indraN)+', iA='+str(self.iA)+', iB='+str(self.iB)+', snapshot='+str(self.sdirC)
        return 0
        # finish this function - replace positions with dummies where able


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
        fnr         = N.int32() # think this is friend(?) number, iterative counter for gr tab/id

        '''for i in N.arange(0, self.grouptabCount): # [0, 255] # the old for loop
            """
            f = Base+"/snapdir_"+exts+"/group_tab_"+exts +"."$
                +strcompress(string(fnr),/remove_all)
            openr,1,f
            """
            filepath    = gtb + str(i)
            f           = open(filepath, 'rb')
        '''

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
            filepath        = gtb + str(i)
            try:
                f           = open(filepath, 'rb')

            except IOError:
                errorstring = """
                Whilst reading %s dataset,
                filepath :  %s  ;
                File no. %d seems to be missing.
                    """ % (self.what, filepath, i)

                skipfile_i = self.error_w_user_input(errorstring) # should return the integer 1.
                i += skipfile_i # maybe this and prev. line could/should be concatenated; later maybe
                
                filepath        = gtb + str(i)
                try:
                    f           = open(filepath, 'rb')
                except IOError:
                    sys.exit(self.mult_miss_error)

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
            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4) # considering there are 4 items, i'm guessing to count 4 times. looks like that from previous example
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
        LONGID = 1 # well... how about that user input?

        '''for i in N.arange(0, self.groupidCount): # [0, 255]          # old loop
            """
            f = Base + "/snapdir_" + exts +"/group_ids_"+exts +"."$
                +strcompress(string(fnr),/remove_all)
            openr,1,f
            """
            filepath    = gid + str(i)
            f           = open(filepath, 'rb')
        '''
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
            try:
                f           = open(filepath, 'rb')

            except IOError:
                errorstring = """
                Whilst reading %s dataset,
                filepath :  %s  ;
                File no. %d seems to be missing.
                    """ % (self.what, filepath, i)

                skipfile_i = self.error_w_user_input(errorstring) # should return the integer 1.
                i += skipfile_i # maybe this and prev. line could/should be concatenated; later maybe
                
                filepath        = gid + str(i)
                try:
                    f           = open(filepath, 'rb')
                except IOError:
                    sys.exit(self.mult_miss_error)

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
                totnids = N.int64(0.)
            if i == 0 and TotNids > 0:
                # IDs = N.zeros(TotNids, dtype=N.int32)       # DNN
                # if (LONGID): # i'm guessing this is to check id-tag float type?
                #     IDs = N.zeros(TotNids, dtype=N.int64)
                """
                below check could intuitively be put in below if-test;
                though having it here leaves the possibility of an array,
                even when Nids == 0.
                """
                if (LONGID == False):
                    IDs = N.zeros(TotNids, dtype=N.int32)
                else:
                    IDs = N.zeros(TotNids, dtype=N.int64)
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


    def read_subhalo(self):
        """ YAY, 2 down, 2 to go!
        reads subhalo id and tab files
        """
        """
        PRO read_sub, Base,num,TotNgroups,TotNids,M200,pos,$
                  IDs,Sublen,Suboffset,loadIDs=loadIDs # resources that are loaded
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
        ; offset=groupoffset(0)
        LONGID=1
        """
        if keyword_set(loadIDs):
            skip    = N.int32(0)
            fnr     = N.int32(0)
            # length  = grouplen(0)
            # offset  = groupoffset(0)
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
                IF totNgroups GT 0 THEN totnids=total(Sublen,/double) ELSE totnids = 0.
                """
                if TotNgroups > 0:
                    TotNids = N.sum(SubLen, dtype=N.float32)
                else:
                    TotNids = N.float32(0)
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
                fnr++
                ; if skip gt 1.01*length then goto, last
                """
                #if skip > 1.01*length:
                #    return


            """
            endrep until fnr eq NTask
            ;particle IDs of halo N=10 
            ;N=10
            ;ids_group0=ids[groupoffset[N]:groupoffset[N]+grouplen[N]-1]
            """
            # particle IDs of halo N=10
            Number = 10
            ids_group0 = IDs[ groupoffset[Number] : groupoffset[Number]+grouplen[Number]-1 ]
        """
        ENDIF
        last:
        end
        """
        return 0


    def read_FFT(self):
        """
        reads FFT data relevant
        """
        indrapath = self.dsp + "/indra%d/%d_%d_%d" % (self.indraN, self.indraN, self.iA, self.iB)
        fftpath = indrapath + '/FFT_DATA/FFT_128_%03d.dat' % self.fftdirC
        """
        openr,1,fftpath
        """
        f   = open(fftpath, 'rb')

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
        return 0



if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. Please run read.py instead.")