# ==============================================
# Read.& proc. toolkit for data sets' structure.
# ==============================================
import os, sys, gc
import numpy as N
import matplotlib.pyplot as pl
from read_usertools import UserTools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
rc('font',**{'family':'serif'})

class AutoTools(object):
    """
    Tools that function when used in the readProcedures instance's automatic mode.
    """
    def __init__(self):
        # Singular-type data readings' post-processing functions
        # WIP and prone to change!
        self.ppBasicActions = {
            "pos"     : self.pp_pos     , 
            "vel"     : self.pp_vel     , 
            "fof"     : self.pp_fof     , 
            "subhalo" : self.pp_subhalo ,
            # "fft"     : self.pp_fft     ,
            "origami" : self.pp_origami
        }
        self.ppBasicLastActions = {
            "pos"     : self.pp_Lpos     ,
            "vel"     : self.pp_Lvel     ,
            "fof"     : self.pp_Lfof     ,
            "subhalo" : self.pp_Lsubhalo ,
            "fft"     : self.pp_Lfft     ,
            "origami" : self.pp_Lorigami
        }
        # Post-processing functions, combining data types
        self.ppFuncsSingleSnaps = {
            "posor"   : self.pp_posor   , # pos.s and Origami
            "pof"     : self.pp_pof     , # pos.s and FoF
            "porifof" : self.pp_porifof , # pos.s, Origami, and FoF
            "playOne" : self.pp_playOne   # Dev. function for testing
        }
        # Post-processing functions, combining data types over several snaps
        self.ppFuncsAllSnaps = { 
            "sufo"    : self.pp_sufoIniter , # Pertaining to Subhalo Halos & FoF Halos
            "sofa"    : self.pp_sofaIniter , # Subhalo, Origami, and FoF analysis
            "playAll" : self.pp_playAll      # Dev. function for testing  
        }
        """
        End of init
        """


    def ppTempStorage(self, parsed_data):
        """
        Handles temporary storing of data.
        """
        task  = self.what           # -- --> Outermost dictionary key, str-type
        iN    = self.indraN         # -- --> These 3 form the middle key
        iA    = self.iA             # --^
        iB    = self.iB             # -^
        # indra = "{0:1d}{1:1d}{2:1d}".format(iN,iA,iB)
        indra = self.iString
        num   = self.subfolder
        
        " Selects the correct dictionary for combinated pp-ing "
        if   self.what_set in self.singleSnapActions.keys():
            " Store data for single snaps in a set"
            self.dictMaker(self.data1dict, task, indra, num)
            pass # end.IF single snap storage

        elif self.what_set in self.allSnapActions.keys():
            " Store data for all snaps in a set "
            self.dictMaker(self.dataAlldict, task, indra, num)
            pass # end.IF all snap storage
        else:
            print " [...] Uh... error... maybe? "
            pass # end.ELSE wtf-ery

        return 0


    # -------- Initializers of pp-ing: --------

    def ppBasic(self, parsed_data, num):
        """
        Initializes the simple readings & processings.
        """
        " Just prints whether or not plotting is involved: "
        if self.boolcheck(self.plotdata) == True:
            " Tells user if plots are made "
            self.plottingEngagedText = """
            Engaging plot method for the {0} data retriever.
            Plot location and name: ' {1} '"""
            self.plottingEngagedText.format(self.what, self.outfilePath+".png")
            pass

        " The actual pp-ing: "
        self.ppBasicActions[self.what](parsed_data)

        return 0
    

    def ppBasicLast(self, parsed_data, num):
        """
        Initializes the simple readings & processings, end of snap.
        """
        " Just prints whether or not plotting is involved: "
        if self.boolcheck(self.plotdata) == True:
            " Tells user if plots are made "
            self.plottingEngagedText = """
            Engaging plot method for the {0} data retriever.
            Plot location and name: ' {1} '"""
            self.plottingEngagedText.format(self.what, self.outfilePath+".png")
            pass

        " The actual pp-ing: "
        self.ppBasicLastActions[self.what](parsed_data)

        return 0


    def ppSingleSnaps(self, parsed_data):
        """
        Initializes single-snap readings & processings
        """
        " Just prints whether or not plotting is involved: "
        if self.boolcheck(self.plotdata) == True:
            " Tells user if plots are made "
            print " singleSnap plot process has begun "
            pass

        self.ppFuncsSingleSnaps[self.what_set](parsed_data)

        return 0


    def ppAllSnaps(self, parsed_data):
        """
        Initializes readings & processings for combined snapnumbers.
        """
        " Just prints whether or not plotting is involved: "
        if self.boolcheck(self.plotdata) == True:
            " Tells user if plots are made "
            print " allSnap plot process has begun"
            pass

        self.ppFuncsAllSnaps[self.what_set](parsed_data)

        return 0

    ##################################################################
    # """ -------- Here are "Single Snap pp functions": -------- """ #

    def pp_posor(self):
        """
        Positions and Origami
        """

        return 0

    def pp_pof(self):
        """
        
        """

        return 0
    def pp_porifof(self):
        """
        
        """

        return 0
    def pp_playOne(self):
        """
        
        """

        return 0


    ##################################################################
    # """ -------- Here are "combinatory pp functions": -------- """ #


    def pp_playAll(self, sofa_data):
        """
        Playground pp-routine for post-processing of data sets,
        combining SubFind-, Origami, & FoF Analysis.

        Will figure out routines here, then move them around accordingly.
        """
        " Makes sure the temp. dict.s are enriched "
        self.ppTempStorage(sofa_data)

        if self.allCond == True:
            " Engage playground on last snapshot in the set "
            print " * playAll initialized ! "
            pass # end.IF: last snap & datatype in set
            
        else:
            print " + playAll storage initialized "
            return 0 # end.ELSE: storage notifier

        # Data is accessable at dictionary addresses:
        "| >>> self.dataAlldict[ 'fof'    ][ self.iString ][ snapNumber ] "
        #| fofIDs, tNgrps, groupLen, groupOffset
        "| >>> self.dataAlldict[ 'suhalo' ][ self.iString ][ snapNumber ] "
        #| subIDs, tNsubs, catalog

        # Arrays are preferred to operate; so we build them:
        ngp, nsp, tng, tns = self.pp_sufoCounters( len(self.subfolder_set) ,
                                                   self.sIndex             )
        nhtags = pp_oriFetch('h')
        # Plot SubFind-subhalo-, Origami-halo, & FoF-halo- particle counts
        self.plot_sofa(nsp, nhtags, ngp)
        self.plot_quori(n)
        
        print " . playAll completed . "
        return 0


    def pp_sufoIniter(self, sufo_data):
        """
        Subhalo & FoF output pp routine.
        """
        " Makes sure the temp. dict.s are enriched "
        self.ppTempStorage(sufo_data)

        if self.subfolder is self.subfolder_set[-1]:
            if self.what is self.allSnapActions[self.what_set][-1]:
                " Engage playground on last snapshot in the set "

                print " * Subhalo & FoF pp-ing initialized ! "
                self.pp_sufoGoPlay()
                print " . Subhalo & FoF pp-ing completed . "
                
                pass # end.IF last data in set
            pass # end.IF     last snap in set

        else:
            print " + Subhalo & FoF storage initialized "
            pass # end.ELSE storage notifier

        return 0


    def pp_sufoGoPlay(self):
        """
        Playground for pp-ing with the Subhalo and FoF data sets!
        
        Currently :
        - Halo counting/comparing.
        - More to come!
        """
        # Data is accessable at dictionary addresses:
        "| >>> self.dataAlldict[ 'fof'    ][ self.iString ][ snapNumber ] "
        #| fofIDs, tNgrps, groupLen, groupOffset
        
        "| >>> self.dataAlldict[ 'suhalo' ][ self.iString ][ snapNumber ] "
        #| subIDs, tNsubs, catalog

        # Arrays are preferred to operate; so we build them:
        ngp, nsp, tng, tns = self.pp_sufoCounters( len(self.subfolder_set) ,
                                                   self.sIndex             )
        self.plot_haloCounts(ngp_all, nsp_all)

        return 0


    def pp_sufoAllCounters(self, snapSetLen, snapkeys):
        """
        Produces arrays that are better to handle than dict items,
        returns items to sufoGoPlay, a.k.a. sufo data Playground.
        """
        # N of fof-group _particles_ , * all snaps
        ngp_all  = pl.zeros( snapSetLen , dtype=pl.int64 )
        # N of subhalo _particles_   , * all snaps
        nsp_all  = pl.zeros( snapSetLen , dtype=pl.int64 )

        # N of fof _groups_     , * all snaps
        tng_all  = pl.zeros( snapSetLen , dtype=pl.int64 )
        # N of subhalo _groups_ , * all snaps
        tns_all  = pl.zeros( snapSetLen , dtype=pl.int64 )

        for sn in snapkeys:
            " Numbers of FoF / Subhalo Particles == len of their ID arrays "
            ngp_all[sn] = len( self.dataAlldict[ "fof"    ][self.iString][sn][0] )
            nsp_all[sn] = len( self.dataAlldict[ "suhalo" ][self.iString][sn][0] )
            
            " Total Number of fof Groups "
            tng_all[sn] = self.dataAlldict[ "fof"    ][self.iString][sn][1]
            tns_all[sn] = self.dataAlldict[ "suhalo" ][self.iString][sn][1]
            continue # Next snap

        return ngp_all, nsp_all, tng_all, tns_all


    def pp_sofaIniter(self, sofa_data):
        """
        Some functions for post-processing of data sets,
        combining SubFind-, Origami, & FoF Analysis
        """
        " Makes sure the temp. dict.s are enriched "
        self.ppTempStorage(sofa_data)

        if self.subfolder is self.subfolder_set[-1]:
            if self.what is self.allSnapActions[self.what_set][-1]:
                " Engage playground on last snapshot in the set "

                print " * Subhalo, Origami & FoF Analysis initialized ! "
                self.pp_sofaSlouch()
                print " . Subhalo, Origami & FoF Analysis completed . "
                
                pass # end.IF last data in set
            pass # end.IF     last snap in set
            
        else:
            print " + Subhalo, Origami & FoF storage initialized "
            pass # end.ELSE storage notifier

        return 0

    
    def pp_sofaSlouch(self):
        """
        Collects Subhalo, Origami, & FoF Analysis functions
        """
        # Data is accessable at dictionary addresses:
        "| >>> self.dataAlldict[ 'fof'    ][ self.iString ][ snapNumber ] "
        #| fofIDs, tNgrps, groupLen, groupOffset
        
        "| >>> self.dataAlldict[ 'suhalo' ][ self.iString ][ snapNumber ] "
        #| subIDs, tNsubs, catalog

        # Arrays are preferred to operate; so we build them:
        ngp, nsp, tng, tns = self.sufoCounters( len(self.subfolder_set) ,
                                                self.sIndex             )
        nhtags = self.pp_oriFetch('h')
        # Plot SubFind-subhalo-, Origami-halo, & FoF-halo- particle counts
        self.plot_sofa(nsp, nhtags, ngp)
        return 0


    def pp_oriFetch(self, otype):
        """
        Runs through Origami output to retrieve requested tags.
        """
        oTag_dict = {
            'v' : 0,
            'w' : 1,
            'f' : 2,
            'h' : 3
        }
        if otype not in oTag_dict.keys(): sys.exit(" Invalid 'otype' ")

        nOtags = N.zeros( self.sIndex[-1], dtype=pl.int64 )

        for si in self.sIndex:
            sn = self.subfolder_set[si]
            nOtags[si] = N.sum( # Sum(bools(type)) == N(type)
                self.dataAlldict['origami'][self.iString][sn] == oTag_dict[otype]
            )
            continue

        return nOtags

    ############################################################
    # """ -------- Here are "basic pp functions": -------- """ #

    def pp_pos(self, pos_data):
        """
        Positions post-processing function. 
        """
        IDs, pos, scalefactor, rs = pos_data

        if hasattr(self.box_params, '__iter__') == True:
            " Apply box parameters to the positions "
            # Plotting without boxing will take 26hours per plot.
            print " Box for the cut-out:", self.box_params, "Mpc/k"
            box3D = self.box_indexer(pos, self.box_params)
            IDs = IDs[box3D]
            pos = pos[box3D]
            pass

        if self.origamipath != False:
            " User wants ORIGAMI data available for further PP. "
            tags = self.read_origami()[1]
            tags = tags[IDs]

        if self.boolcheck(self.plotdata):
            " Engage plotting! "
            self.plot_pos_oritag(pos, tags)
            pass

        return 0


    def pp_vel(self, vel_data):
        """
        Post processing of velocitiy data output.
        """

        return 0


    def pp_fof(self, fof_data):
        """
        Post processing of friends of friends data output.
        """
        

        return 0


    def pp_subhalo(self, sub_data):
        """
        Post processing of subhalo data output.
        """

        return 0


    def pp_fft(self, fft_data):
        """
        Post processing of FFT data output.
        """

        return 0


    def pp_origami(self, origami_data):
        """
        Post processing template for ORIGAMI's output.
        """

        return 0


    # Here are "basic pp functions" that initialize 'Last'; after all snaps

    def pp_Lpos(self, pos_data):
        """
        Positions post-processing function. 
        """

        return 0


    def pp_Lvel(self, vel_data):
        """
        Post processing of velocitiy data output.
        """

        return 0


    def pp_Lfof(self, fof_data):
        """
        Post processing of friends of friends data output.
        """

        return 0


    def pp_Lsubhalo(self, sub_data):
        """
        Post processing of subhalo data output.
        """

        return 0


    def pp_Lfft(self, fft_data):
        """
        Post processing of FFT data output.
        """

        return 0


    def pp_Lorigami(self, origami_data):
        """
        Post processing template for ORIGAMI's output.
        """

        return 0




if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")