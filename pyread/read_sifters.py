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
        for which this was written,
        unless when redshift was investigated?
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

        f.close()
        return pos, vel, idarr, npart, scalefact, redshift


    def fof_tab_sifter(self, f, i, skip):
        """
        Sifts through the group tab data
        """
        # print "Before if of fof_tab_sifter"
        Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
        # should there be a dummy distance between this and the next information, or..?
        # 8==> apparently not!
        # print Ngroups, Nids, TotNgroups, NTask
        # print "\nBefore if-conditions:"
        # print "TotNgroups > 0: i=", i, "TotNgroups=", TotNgroups, \
        #         "Ngroups=", Ngroups, "\n"
        
        # print "i is simply a variable in python 2.6 environment.\nHere are some tests for bools. Have fun with this logic..."
        # print "i-test: * i is 0:", i is 0, ", * i == 0:", i == 0 
        # print "i-test: * i is not 0:", i is not 0, ", * i != 0:", i != 0 
        # print "str-test: * 'str' is 'str':", 'str' is 'str',\
        #       ", * 'str' == 'str':", 'str' == 'str' 

        # print "type-test: * type('str') is str:", type('str') is str,\
        #       ", * type('str') == str:", type('str') == str

        # print "str-test: * 'str' is not 'ok':", 'str' is not 'ok',\
        #       ", 'str' != 'ok':", 'str' != 'ok'
        # if i == 0:
        #     print "i          = " + str(i)          + "\n"+ \
        #           "Ngroups    = " + str(Ngroups)    + "\n"+ \
        #           "Nids       = " + str(Nids)       + "\n"+ \
        #           "TotNgroups = " + str(TotNgroups) + "\n"
            # self.linewriter(                        \
            #     ["Ngroups=" + str(Ngroups),     \
            #      "Nids="    + str(Nids),        \
            #      "TotNgroups="+str(TotNgroups)] , self.writeToFile)
                    # Header for file.

        if i == 0 and TotNgroups > 0:
            # print "inside first if"
            self.GroupLen    = N.zeros(TotNgroups, dtype=N.int32) # DNC 
            self.GroupOffset = N.zeros(TotNgroups, dtype=N.int32) # DNC
            pass 
        # print "Between if-conditions.\n"
        if Ngroups > 0:
            # print "Inside second if! \n"
            locLen      = N.fromfile(f, N.int32, Ngroups)
            locOffset   = N.fromfile(f, N.int32, Ngroups)
            # print "locLen", locLen
            # print "Ngroups > 0:", i, TotNgroups
            self.GroupLen[    skip:skip+Ngroups ] = locLen[:]
            self.GroupOffset[ skip:skip+Ngroups ] = locOffset[:]

            # raw_input("Ngroups > 0!")
            skip += Ngroups
            pass
        # print "After conditions\n"
        f.close()
        # self.linewriter([Ngroups, Nids, TotNgroups], self.writeToFile)

        # if self.bssdt == True:
        #     for item in self.GroupLen:
        #         """
        #         because GroupLen is 'iterable', even when GroupLen's empty;
        #         and we only need its first value.
        #         ... and it doesn't even raise errors when 'item' doesn't exist...
        #         """
        #         print "Len of GroupLen", len(self.GroupLen)
        #         setattr(self, length, item)
        #         break
        #     pass

        # if i == 255: # DT
        #     print "i          = " + str(i)          + "\n" + \
        #           "Ngroups    = " + str(Ngroups)    + "\n" + \
        #           "Nids       = " + str(Nids)       + "\n" + \
        #           "TotNgroups = " + str(TotNgroups) + "\n"

        # print "After if of fof_tab_sifter"
        print "######################"
        print "####### MARCO !!! #### i = ", i
        print "######################"
        return Ngroups, Nids, TotNgroups, skip


    def fof_ids_sifter(self, f, i, skip):
        """
        Sifts through the group ID data
        """
        print "######################"
        print "####### POLO  !!! #### i = ", i, self.GroupLen
        print "######################"
        Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
        if TotNgroups > 0:
            TotNids = N.sum(self.GroupLen, dtype=N.int64)
            pass
        else:
            TotNids = N.int64(0)
            pass

        if i == 0 and TotNids > 0:
            self.IDs = N.zeros(TotNids, dtype=N.int64)  # LIDA
            pass
        else:
            " Need some object for self.read_procedures to return, anyway... "
            self.IDs = N.zeros(1, dtype=N.int64)
            # --- At least it's consistent!
            pass
            # ^ Though this kind of removes the requirement
            # of the whole if-block, I guess.


        if Nids > 0:
            locIDs = N.fromfile(f, N.int64, Nids)  # LIDA
            

            try:

                self.IDs[ skip:skip+Nids ] = \
                        N.bitwise_and(locIDs[:], self.bitshiftmask)
                skip += Nids  # \___|: Reading binary/bitwise. Not all of the data
                pass          #  \__|  is what we're actually looking for.


            except:
                self.objectDebug_print(self.GroupLen, "self.GroupLen")
                self.objectDebug_print(TotNids, "TotNids")
                print " --- --- --- --- --- --- --- --- --- "
                self.objectDebug_print(Nids, "Nids")
                self.objectDebug_print(locIDs, "locIDs")
                self.objectDebug_print(skip, "skip")
                self.objectDebug_print(self.IDs, "self.IDs")
                self.objectDebug_print(N.bitwise_and(locIDs[:], self.bitshiftmask), "bitwise-result")


                sys.exit("  *** abort *** ")

        f.close()
        return skip


    def sub_Totes_counter(self, f, TotNSubs):
        """
        Counts TotNsubs.
        Last value of TotNgroups is also produced.
        Necessary to construct arrays properly in next sifter.
        Decided against using this, the 3 necessary lines are now in read_tools.
        """
        Ngroups, Nids, TotNgroups, NTask, NSubs = N.fromfile(f, N.int32, 5)
        f.close()
        TotNsubs += NSubs
        return Ngroups, Nids, TotNgroups, NSubs, TotNsubs


    def sub_tab_sifter(self, f, SubLen, SubOffset, M200, count, count_sub, pos, skip, i):
        """
        Sifts through tab files.
        Collects identifications of no. of sub halos and structures?
        """
        Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
        # print 'Ngroups      = ', Ngroups
        # print 'TotNgroups   = ', TotNgroups
        Nsubs = N.fromfile(f, N.int32, 1)
        """
        ; Why would Nsubs be 0? ... in this certain file?
        """
        if Nsubs > 0:

            NsubPerHalo     = N.fromfile(f, N.int32, Ngroups)
            FirstSubOfHalo  = N.fromfile(f, N.int32, Ngroups)
            locLen          = N.fromfile(f, N.int32, Nsubs)
            locOffset       = N.fromfile(f, N.int32, Nsubs)
            SubParentHalo   = N.fromfile(f, N.int32, Nsubs)

            SubLen[    skip:skip+Nsubs ] = locLen[:]
            SubOffset[ skip:skip+Nsubs ] = locOffset[:]
                
            skip += Nsubs
            # print "Nsubs= ", Nsubs, N.sum(loclen, dtype=N.float64) # LDT

            Halo_M_Mean200   = N.fromfile(f, N.float32, Ngroups)
            Halo_R_Mean200   = N.fromfile(f, N.float32, Ngroups)
            Halo_M_Crit200   = N.fromfile(f, N.float32, Ngroups)
            Halo_R_Crit200   = N.fromfile(f, N.float32, Ngroups)
            Halo_M_TopHat200 = N.fromfile(f, N.float32, Ngroups)
            Halo_R_TopHat200 = N.fromfile(f, N.float32, Ngroups)

            M200[ count:count+Ngroups ] = Halo_M_Crit200

            SubPos          = N.fromfile(f, N.float32, Nsubs*3)
            SubVel          = N.fromfile(f, N.float32, Nsubs*3)
            SubVelDisp      = N.fromfile(f, N.float32, Nsubs)
            SubVmax         = N.fromfile(f, N.float32, Nsubs)
            SubSpin         = N.fromfile(f, N.float32, Nsubs*3)
            SubMostBoundID  = N.fromfile(f, N.int32  , Nsubs*2)
            Subhalfmass     = N.fromfile(f, N.float32, Nsubs)

            SubPos          = N.reshape(SubPos, [Nsubs, 3])#.astype(N.float64)
            SubVel          = N.reshape(SubVel, [Nsubs, 3])#.astype(N.float64)
            SubSpin         = N.reshape(SubSpin, [Nsubs, 3])#.astype(N.float64)
            SubMostBoundID  = N.reshape(SubMostBoundID, [Nsubs, 2])#.astype(N.float64)
                                            # should these be converted to float64?
            
            print "i:", i
            print "FirstSubOfHalo             :", FirstSubOfHalo
            print "len(FirstSubOfHalo)        :", len(FirstSubOfHalo)
            print
            print "uniques FirstSubOfHalo     :", N.unique(FirstSubOfHalo)
            print "len(uniques FirstSubOfHalo):", len(N.unique(FirstSubOfHalo)),"\n"

            print
            print "differences that SHOULD >= 0 ?? :"
            print "----------------------------------------------------------"
            print "len(FSOH) - len(FSOH.uniq)                 =", \
                  len(FirstSubOfHalo) - len(N.unique(FirstSubOfHalo))
            print "len(SubPos[FSOH]) - len(SubPos[FSOH.uniq]) =", \
                  "not testable"
                  # len(SubPos[FirstSubOfHalo,0]) - len(SubPos[N.unique(FirstSubOfHalo)])

            print 
            print "differences that SHOULD == 0:"
            print "----------------------------------------------------------"
            print "shape(SubPos) :",\
                  N.shape(SubPos)
            print "shape(SubPos[N.unique(FirstSubOfHalo) , 0]) :",\
                  N.shape(SubPos[N.unique(FirstSubOfHalo) , 0])

            print "len(pos[sel]) - len(SubPos[FSOH.uniq])     =", \
                  len(pos[ count:count+Ngroups , 0 ]) - \
                  len(SubPos[N.unique(FirstSubOfHalo) , 0])
            print "len(pos[sel]) - len(SubPos[FSOH])          =", \
                  len(pos[ count:count+Ngroups , 0 ]) - \
                  len(SubPos[FirstSubOfHalo , 0])

            print
            print "shapes:"
            print "pos:", N.shape(pos), " - SubPos:", N.shape(SubPos)
            print "pos[   sele:ction , : ]:", N.shape(pos[count:count+Ngroups,:])
            print "SubPos[ FSOH.uniq , : ]:", N.shape(SubPos[N.unique(FirstSubOfHalo),:])
            print "SubPos[      FSOH , : ]:", N.shape(SubPos[FirstSubOfHalo,:])
            print 
            print "=========================================================="
            print 

            if i == 5:
                pvc = 0 # Paired Valuces Counter
                pairedValsIn = [] # indices
                for in1 in range(len(FirstSubOfHalo)):
                    if FirstSubOfHalo[in1] == N.unique(FirstSubOfHalo)[pvc]:
                        print "in1: {0:>4} := FSOH[in1]: {1:>4} --- ".format(  \
                                      in1, FirstSubOfHalo[in1]           ) +   \
                              "in2: {0:>4} := FSOH.uniq[in2] {1:>4}".format(   \
                                      pvc, N.unique(FirstSubOfHalo)[pvc] )
                        pairedValsIn.append(pvc)
                        pvc += 1
                        pass
                    else:
                        print "in1: {0:>4} := FSOH[in1]: {1:>4} --- ".format(  \
                                      in1, FirstSubOfHalo[in1]           )
                        pass
                    continue
                pass

            pos[ count:count+Ngroups , : ] = SubPos[ FirstSubOfHalo, : ]
            count += Ngroups
            pass


        # else:
        #     print 'Nsubs = 0'
        f.close()

        # Below running into indexing errors
        # # ind = N.where(sublen > 20) # wait, no, surely you mean:
        # ind = N.argwhere(sublen > 20)
        # if (ind[0] != -1):
        #     num_chos = len(ind)
        #     mass_sub[ count : count+num_chos-1]     = sublen[ind]
        #     pos_sub[ : , count : count+num_chos-1 ] = subpos[ : , ind ]
        #     count_sub = count_sub + num_chos

        # mass_sub[ count : count+ngroups-1 ]     = halo_m_mean200[ : ]
        # pos_sub[ : , count : count+ngroups-1 ]  = subpos[ :, FirstSubOfHalo ]
        # count   = count + ngroups
        # count1  = count1 + nsubs

        return SubLen, SubOffset, M200, count, count_sub, pos, skip

    def sub_ids_sifter(self, SubLen, skip):
        """
        Sifts through ID files.
        Collects IDs. I guess?
        """
        Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
        # print "file=", i
        # print "Ngroups=", Ngroups, "  TotNgroups=", TotNgroups, " Nids=", Nids,\
        #     "  NTask=", NTask

        if TotNgroups > 0:
            TotNids = N.sum(SubLen, dtype=N.float64)
            pass
        else:
            TotNids = N.int64(0)
            pass

        if i == 0 and TotNids > 0:
            IDs = N.zeros(TotNids, dtype=N.int64)   # LIDA
            pass

        if Nids > 0:
            locIDs  = N.fromfile(f, N.int64, Nids)  # LIDA
            # Remove the hash table info:
            IDs[ skip:skip+Nids ] = \
                    N.bitwise_and(locIDs[:], self.bitshiftmask)
            
            skip += Nids
            pass

        # SHOULD PROBABLY WRITE SOMETHING TO FILE HERE, TOO!?!!

        f.close()

        return return_variables # FIGURE THESE OUT TOMORROW

    def fft_sifter(self, f):
        """
        Sifts through FFT data.
        """
        """ # keep this for orientation purposes

        ; fft_re=fltarr(Lhalf+1,L+1,L+1) 
            # looks like a zeros-function, specifically float32
        ; fft_im=fltarr(Lhalf+1,L+1,L+1) 
            # if IDL does j,i,k - then python does i,j,k ...?
        
        #=> becomes the below statements, and shows dimensions:
            IDL IS COL-MAJOR,
            PYTHON IS ROW-MAJOR
        """
        # PMGRID  = N.int32(640) # not used for anything...
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
        fft_im =   N.reshape(fft_im, [L+1, Lhalf+1, L+1] ).astype(N.float64)

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

        mass  = N.fromfile(f, N.float64, 6)
        
        scalefact, redshift = N.fromfile(f, N.float64, 2)

        return scalefact, redshift


if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")
    # run read.py instead