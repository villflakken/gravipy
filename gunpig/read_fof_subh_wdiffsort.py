# fof:
TotNgroups, NTask = getfofheader(X,Y,Z,snapnum,datadir=datadir)
groupLen, groupOffset = getfof(X,Y,Z,snapnum,datadir=datadir)
groupLen, groupOffset, groupids = getfofids(X,Y,Z,snapnum,datadir=datadir)

# subh:
TotNsubs, NTask = getsubheader(X,Y,Z,snapnum,datadir=datadir)
catalog = getsubcat(X,Y,Z,snapnum,datadir=datadir) # dict. w/ subLen and subOffset
subids = getsubids(X,Y,Z,snapnum,datadir=datadir)


"""
Halo and subhalo functions
"""

def getfofheader(X,Y,Z,snapnum,datadir=None):
    
    if (datadir == None): datadir = '/datascope/indra%s/%s_%s_%s/'%(str(X),str(X),str(Y),str(Z))

    sn = "%03d" % snapnum
    tabfile = datadir+'snapdir_'+sn+'/group_tab_'+sn+'.'

    f = open(tabfile+str(0),'rb')
    Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
    f.close()
    
    return TotNgroups,NTask

def getfof(X,Y,Z,snapnum,datadir=None):
    
    if (datadir == None): datadir = '/datascope/indra%s/%s_%s_%s/'%(str(X),str(X),str(Y),str(Z))

    sn = "%03d" % snapnum
    tabfile = datadir+'snapdir_'+sn+'/group_tab_'+sn+'.'

    # loop through NTask files (could read NTask from header...)
    # NTask = 256
    TotNgroups,NTask = getfofheader(X,Y,Z,snapnum,datadir)
    # Don't read if no groups...
    if TotNgroups == 0: return None
    else:
        groupLen = N.zeros(TotNgroups,dtype=N.int32)
        groupOffset = N.zeros(TotNgroups,dtype=N.int32)

        istartGroup = 0
        istartIDs = 0
        for i in N.arange(0,NTask):
            f = open(tabfile+str(i), 'rb')
    
            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
            if Ngroups > 0:
                locLen = N.fromfile(f,N.int32,Ngroups)
                locOffset = N.fromfile(f,N.int32,Ngroups)
                groupLen[istartGroup:(istartGroup+Ngroups)] = locLen
                groupOffset[istartGroup:(istartGroup+Ngroups)] = locOffset+istartIDs
                istartGroup += Ngroups
                istartIDs += Nids
            # else: print('No groups in file %d' % i)
            f.close()
    
    return groupLen,groupOffset

def getfofids(X,Y,Z,snapnum,datadir=None):

    if (datadir == None): datadir = '/datascope/indra%s/%s_%s_%s/'%(str(X),str(X),str(Y),str(Z))

    sn = "%03d" % snapnum
    idsfile = datadir+'snapdir_'+sn+'/group_ids_'+sn+'.'
 
    # loop through NTask files
    # NTask = 256
    TotNgroups,NTask = getfofheader(X,Y,Z,snapnum,datadir)
    # Don't read if no groups...
    if TotNgroups == 0: return None
    else:
        groupLen,groupOffset = getfof(X,Y,Z,snapnum,datadir)
        TotNids = N.sum(groupLen,dtype=N.int64)
        groupids = N.zeros(TotNids,dtype=N.int64)

        istart = 0
        for i in N.arange(0,NTask):
            f = open(idsfile+str(i),'rb')

            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
            if Nids > 0:
                locIDs = N.fromfile(f,N.int64,Nids)
                # bitshift to remove the hash table info from the IDs
                groupids[istart:(istart+Nids)] = N.bitwise_and(locIDs[:], (N.int64(1)<<34) - 1)
                istart += Nids
            # else: print('No groups in file %d' % i)
            f.close()
    
    return groupLen,groupOffset,groupids-1

def getsubheader(X,Y,Z,snapnum,datadir=None):

    if (datadir == None): datadir = '/datascope/indra%s/%s_%s_%s/'%(str(X),str(X),str(Y),str(Z))

    sn = "%03d" % snapnum
    tabfile = datadir+'postproc_'+sn+'/sub_tab_'+sn+'.'

    TotNsubs = 0
    f = open(tabfile+str(0),'rb')
    Ngroups,Nids,TotNgroups,NTask = N.fromfile(f,N.int32,4)
    f.close()
    
    for i in N.arange(0,NTask):
        f = open(tabfile+str(i),'rb')
        # print('opening file '+tabfile+str(i))
        Ngroups, Nids, TotNgroups, NTask, Nsubs = N.fromfile(f, N.int32, 5)
        TotNsubs += Nsubs
        f.close()

    return TotNsubs,NTask

def getsubcat(X,Y,Z,snapnum,datadir=None):
    
    if (datadir == None): datadir = '/datascope/indra%s/%s_%s_%s/'%(str(X),str(X),str(Y),str(Z))

    sn = "%03d" % snapnum
    tabfile = datadir+'postproc_'+sn+'/sub_tab_'+sn+'.'
    
    TotNgroups,NTask= getfofheader(X,Y,Z,snapnum,datadir)
    TotNsubs,NTask = getsubheader(X,Y,Z,snapnum,datadir)
    if TotNsubs == 0: return None
    else:
        # Initialize data containers. Group into structured array?? Dict??
        catalog = {}
        catalog['NsubPerHalo'] = N.zeros(TotNgroups,dtype=N.int32)
        catalog['FirstSubOfHalo'] = N.zeros(TotNgroups,dtype=N.int32) # file specific!
    
        catalog['subLen'] = N.zeros(TotNsubs,dtype=N.int32)
        catalog['subOffset'] = N.zeros(TotNsubs,dtype=N.int32) # file specific!
        catalog['subParentHalo'] = N.zeros(TotNsubs,dtype=N.int32) # file specific!
    
        catalog['M200mean'] = N.zeros(TotNgroups,dtype=N.float32)
        catalog['R200mean'] = N.zeros(TotNgroups,dtype=N.float32)
        catalog['M200crit'] = N.zeros(TotNgroups,dtype=N.float32)
        catalog['R200crit'] = N.zeros(TotNgroups,dtype=N.float32)
        catalog['M200tophat'] = N.zeros(TotNgroups,dtype=N.float32)
        catalog['R200tophat'] = N.zeros(TotNgroups,dtype=N.float32)
    
        catalog['SubPos'] = N.zeros((TotNsubs,3),dtype=N.float32)
        catalog['SubVel'] = N.zeros((TotNsubs,3),dtype=N.float32)
        catalog['SubVelDisp'] = N.zeros(TotNsubs,dtype=N.float32)
        catalog['SubVmax'] = N.zeros(TotNsubs,dtype=N.float32)
        catalog['SubSpin'] = N.zeros((TotNsubs,3),dtype=N.float32)
        catalog['SubMostBoundID'] = N.zeros((TotNsubs,2),dtype=N.int32)
        catalog['SubHalfMass'] = N.zeros(TotNsubs,dtype=N.float32)
        
        # loop over numfiles (NTask)
        istartSub = 0
        istartGroup = 0
        istartIDs = 0
        for i in N.arange(0,NTask):
            f = open(tabfile+str(i),'rb')
            Ngroups, Nids, TotNgroups, NTask, Nsubs = N.fromfile(f, N.int32, 5)
            
            if Nsubs > 0:
            # Read catalog: indexes need to include offset from previous files (istarts)
                catalog['NsubPerHalo'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.int32,Ngroups)
                catalog['FirstSubOfHalo'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.int32,Ngroups)+istartSub
       
                catalog['subLen'][istartSub:(istartSub+Nsubs)] = N.fromfile(f,N.int32,Nsubs)
                catalog['subOffset'][istartSub:(istartSub+Nsubs)] = N.fromfile(f,N.int32,Nsubs)+istartIDs
                catalog['subParentHalo'][istartSub:(istartSub+Nsubs)] = N.fromfile(f,N.int32,Nsubs)+istartGroup
                
                catalog['M200mean'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.float32,Ngroups)
                catalog['R200mean'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.float32,Ngroups)
                catalog['M200crit'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.float32,Ngroups)
                catalog['R200crit'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.float32,Ngroups)
                catalog['M200tophat'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.float32,Ngroups)
                catalog['R200tophat'][istartGroup:(istartGroup+Ngroups)] = N.fromfile(f,N.float32,Ngroups)

                thisxyz = N.fromfile(f,N.float32,3*Nsubs)
                catalog['SubPos'][istartSub:(istartSub+Nsubs),:] = N.reshape(thisxyz,[Nsubs,3])
                thisxyz = N.fromfile(f,N.float32,3*Nsubs)
                catalog['SubVel'][istartSub:(istartSub+Nsubs),:] = N.reshape(thisxyz,[Nsubs,3])
                catalog['SubVelDisp'][istartSub:(istartSub+Nsubs)] = N.fromfile(f,N.float32,Nsubs)
                catalog['SubVmax'][istartSub:(istartSub+Nsubs)] = N.fromfile(f,N.float32,Nsubs)
                thisxyz = N.fromfile(f,N.float32,3*Nsubs)
                catalog['SubSpin'][istartSub:(istartSub+Nsubs),:] = N.reshape(thisxyz,[Nsubs,3])
                catalog['SubMostBoundID'][istartSub:(istartSub+Nsubs),:] = N.reshape(N.fromfile(f,N.int32,2*Nsubs),[Nsubs,2])
                catalog['SubHalfMass'][istartSub:(istartSub+Nsubs)] = N.fromfile(f,N.float32,Nsubs)

                istartSub += Nsubs
                istartGroup += Ngroups
                istartIDs += Nids
            
            f.close()

    return catalog


def getsubids(X,Y,Z,snapnum,datadir=None):
    
    if (datadir == None): datadir = '/datascope/indra%s/%s_%s_%s/'%(str(X),str(X),str(Y),str(Z))

    sn = "%03d" % snapnum
    idsfile = datadir+'postproc_'+sn+'/sub_ids_'+sn+'.'
    
    TotNsubs,NTask = getsubheader(X,Y,Z,snapnum,datadir)
    if TotNsubs == 0: return None
    else:
        TotSubids = 0
        # Get total number of IDs (including unbound particle IDs)
        for i in N.arange(0,NTask):
            f = open(idsfile+str(i),'rb')
            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
            TotSubids += Nids
            f.close()
        subids = N.zeros(TotSubids,dtype=N.int64)
        
        # loop through numfiles (NTask)
        istart = 0
        for i in N.arange(0,NTask):
            f = open(idsfile+str(i),'rb')

            Ngroups, Nids, TotNgroups, NTask = N.fromfile(f, N.int32, 4)
            if Nids > 0:
                locIDs = N.fromfile(f,N.int64,Nids)
                # bitshift to remove the hash table info from the IDs
                subids[istart:(istart+Nids)] = N.bitwise_and(locIDs[:], (N.int64(1)<<34) - 1)
                istart = istart + Nids
            f.close()

    return subids-1