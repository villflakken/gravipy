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
    Tools that function when used in the readProcedures instance's automatic mode,
    as well as pp functions for automized runs.
    """
    def __init__(self):
        # Singular-type data readings' post-processing functions
        # WIP and prone to change!
        self.ppd_actionBasic = {
            "pos"     : self.pp_pos     , 
            "vel"     : self.pp_vel     , 
            "fof"     : self.pp_fof     , 
            "subhalo" : self.pp_subhalo ,
            "fft"     : self.pp_fft     ,
            "origami" : self.pp_origami
        }
        self.ppd_actionBasicLast = {
            "pos"     : self.pp_Lpos     ,
            "vel"     : self.pp_Lvel     ,
            "fof"     : self.pp_Lfof     ,
            "subhalo" : self.pp_Lsubhalo ,
            "fft"     : self.pp_Lfft     ,
            "origami" : self.pp_Lorigami
        }
        # Post-Processing Routine Dictionary for Action-Combination Routines: Single Snap
        self.pprd_actionCombSingle = { 
            "posor"   : self.ppr_posor   , # pos.s and Origami
            "pof"     : self.ppr_pof     , # pos.s and FoF
            "porifof" : self.ppr_porifof , # pos.s, Origami, and FoF
            "playOne" : self.ppr_playOne   # Dev. functions for testing
        }
        # Post-Processing Routine Dictionary for Action-Combination Routines: Several Snaps
        self.pprd_actionCombAll = { 
            "sufo"    : self.ppr_sufoIniter , # Pertaining to Subhalo Halos & FoF Halos
            "sofa"    : self.ppr_sofaIniter , # Pertaining to Subhalo, Origami, and FoF analysis
            "playAll" : self.ppr_playAll      # Dev. functions for testing  
        }
        """
        End of init
        """
    """
    The naming conventions of variables and functions contained herein are intended 
    wrt. a sort of hierarchical thinking, i.e.:
    
    pprd_<...> - pp routine dictionary, contains functions with named routine flows

    pp_<single/all snaps> - Initializes correct algorithm for single-snap pp.s or multi-snap,
        :                   from the outside program flow.
        :
        o ppr_<name> - Initializes Routine pertaining to <name> from user input.
            :
            o ppro_<oper. func> - Self-contained, smaller operation of a routine's flow.
            o ppmf_<misc. func> - Misc. Functions, useful on the whole.
    """




    ################################################################################
    # """ -------- Dev. Code Playground, all snaps, comes below here: -------- """ #    


    def pp_allSnaps(self, parsed_data, routine=None):
        """
        Initializes readings & processings for combined snapnumbers.
        """
        if routine != None: # Allows for calling stuff from the outside # DT
            self.what_set = routine
            pass

        self.pprd_actionCombAll[self.what_set](parsed_data)

        return 0


    def ppr_playAll(self, playdata):
        """
        Post-Processing Routine

        Playground pp-routine for post-processing of data sets,
        combining SubFind-, Origami, & FoF Analysis.

        Will figure out routines here, then move them around accordingly.
        """
        " Makes sure the temp. dict.s are updated with last run set "
        self.ppmf_tempStorage(playdata)

        if self.allCond == True:
            " Engage playground on last snapshot in the set "
            print "   o playAll pp-functions initialized ... "
            pass # end.IF: last snap & datatype in set is stored at this point,
                 # which means that the rest of the post-processing begins
                 # (after the else)
            
        else:
            print "   + playAll storage initialized "
            return 0 # end.ELSE: storage notifier,
                     # so script returns to continue with next snapshot's 
                     # data collection routines.

        # Data is accessable at dictionary addresses (in Jupyter):
        "| >>> self.tempAdict[ 'fof'     ][ self.iString ][ snapNumber ] "
        #| fofIDs, tNgrps, groupLen, groupOffset
        "| >>> self.tempAdict[ 'subhalo' ][ self.iString ][ snapNumber ] "
        #| subIDs, tNsubs, catalog
        "| >>> self.tempAdict[ 'origami' ][ self.iString ][ snapNumber ] "
        #| origamitag_array, N_of_particles



        # --- Put processing stuff here! ------------------------

        # Arrays are preferred over dictionaries to operate; so we build them:
        nfp, nsp, tng, tns \
            = self.ppro_subfofCount( self.subfolder_set, self.sIndex )
                                #  ( specific snaps, snap width range)

        # Origami-data turned into boolean arrays are turned into arrays of type
        # [sum(origamiParticleType) for each of (no. of snaps)]
        oNvtags = self.ppro_oritagNfetch('v')
        oNwtags = self.ppro_oritagNfetch('w')
        oNftags = self.ppro_oritagNfetch('f')
        oNhtags = self.ppro_oritagNfetch('h')



        print "Completed."
        # --- Put plotting  stuff here!  ------------------------
        print "   # allSnap plot process has begun"
        
        # Plot subhalo & fof data stuffs
        self.plot_sufoHcount(tng, tns)
        self.plot_sufoderiv(tng, tns)
        # Plot SubFind-subhalo-, Origami-halo, & FoF-halo- particle counts
        self.plot_sofa(nsp, oNhtags, nfp)
        # Plot Origami's quantities over time
        self.plot_quOri(oNvtags, oNwtags, oNftags, oNhtags) # Quantities of Origami (over time)
        
        print "   . playAll pp-functions completed . "
        # May now clear the temporary dictionary
        return 0






    ########################################################################################
    # """ -------- Dev. Code Playground's TOOLS, all snaps, comes below here: -------- """ #

    def ppro_subfofCount(self, snapSetLen, snapkeys, datadict=None):
        """
        A Post-Processing Routine Operation
        
        Produces arrays that are better to handle than dict items,
        returns items to the Post Processing Routine which called it.
        """
        snapSetLen = len(self.subfolder_set)

        # N of fof-group _particles_ , * all snaps
        nfp_all  = N.zeros( snapSetLen , dtype=N.int64 )
        # N of subhalo _particles_   , * all snaps
        nsp_all  = N.zeros( snapSetLen , dtype=N.int64 )

        # N of fof _groups_     , * all snaps
        tnf_all  = N.zeros( snapSetLen , dtype=N.int64 )
        # N of subhalo _groups_ , * all snaps
        tns_all  = N.zeros( snapSetLen , dtype=N.int64 )

        for si in snapkeys:
            sn = self.subfolder_set[si]
            " Numbers of FoF / Subhalo Particles == len of their ID arrays "
            nfp_all[si] = len( self.dataAdict[ "fof"     ][self.iString][sn][0] )
            nsp_all[si] = len( self.dataAdict[ "subhalo" ][self.iString][sn][0] )
            
            " Total Number of fof Groups "
            tnf_all[si] = self.dataAdict[ "fof"     ][self.iString][sn][1]
            tns_all[si] = self.dataAdict[ "subhalo" ][self.iString][sn][1]
            continue # Next snap

        return nfp_all, nsp_all, tnf_all, tns_all


    def ppro_oritagNfetch(self, otype='h'):
        """
        Post-Processing Routine Operation

        Runs through Origami output to retrieve requested tags.
        """
        oTag_dict = {
            'v' : 0,
            'w' : 1,
            'f' : 2,
            'h' : 3
        }
        if otype not in oTag_dict.keys(): sys.exit(" Invalid 'otype' (OrigamiParticleType) ")

        nOtags = N.zeros( len(self.sIndex), dtype=N.int64 )

        for si in self.sIndex:
            sn = self.subfolder_set[si]
            nOtags[si] = N.sum( # Sum(bools(type)) => N(type)
                self.tempAdict['origami'][self.iString][sn][0] == oTag_dict[otype]
            )
            continue

        return nOtags
    def ppro_oritagNfetch(self, otype='h'):
        """
        Post-Processing Routine Operation

        Runs through Origami output to retrieve requested tags.
        """
        oTag_dict = {
            'v' : 0,
            'w' : 1,
            'f' : 2,
            'h' : 3
        }
        if otype not in oTag_dict.keys(): sys.exit(" Invalid 'otype' (OrigamiParticleType) ")

        nOtags = N.zeros( len(self.sIndex), dtype=N.int64 )

        for si in self.sIndex:
            sn = self.subfolder_set[si]
            nOtags[si] = N.sum( # Sum(bools(type)) => N(type)
                self.dataAlldict['origami'][self.iString][sn][0] == oTag_dict[otype]
            )
            continue

        return nOtags









    ###################################################################################
    # """ -------- Dev. Code Playground, single snaps, comes below here: -------- """ #

    def ppr_singleSnaps(self, parsed_data, routine=None):
        """
        Initializes single-snap readings & processings
        """
        if routine != None: # Allows for calling stuff from the outside # DT 
            self.what_set = routine
            pass

        self.pprd_actionCombSingle[self.what_set](parsed_data)

        return 0


    def ppr_playOne(self, playdata):
        """
        Post-Processing Routine

        Playground pp-routine for post-processing of data sets,
        combining positions-, Subhalo-, Origami, & FoF-data to suit my needs.

        Will figure out routines here, then move them around accordingly.
        """
        " Makes sure the temp. dict.s are enriched "
        self.ppmf_tempStorage(playdata)

        if self.oneCond == True:
            " Engage playground on last snapshot in the set "
            print "   o playOne pp-functions initialized ... ", 
            pass # end.IF: last snap & datatype in set
            
        else:
            print "   + playOne storage initialized "
            return 0 # end.ELSE: storage notifier

        # Data is accessable at dictionary addresses:
        "| >>> self.tempSdata[ 'fof'     ][ self.iString ][ snapNumber ] "
        #| fofIDs, tNgrps, groupLen, groupOffset
        "| >>> self.tempSdata[ 'subhalo' ][ self.iString ][ snapNumber ] "
        #| subIDs, tNsubs, catalog
        "| >>> self.tempSdata[ 'origami' ][ self.iString ][ snapNumber ] "
        #| origamitag_array, N_of_particles

        # --- Put processing stuff here! ------------------------

        # Origami-data turned into boolean arrays are turned into arrays of type
        # [sum(origamiParticleType) for each of (no. of snaps)]
        oNvtags = self.ppro_oritagNfetch('v')
        oNwtags = self.ppro_oritagNfetch('w')
        oNftags = self.ppro_oritagNfetch('f')
        oNhtags = self.ppro_oritagNfetch('h')


        print "Completed."
        # --- Put plotting  stuff here!  ------------------------
        print "   # playOne plot process has begun "



        print "   . playOne pp-functions completed . " # Next snapshot, then!
        return 0

        
















    # -------- Misc. Func. util.s to pp-ing: --------


    def ppmf_tempStorage(self, parsed_data):
        """
        PP Misc. Func.: Handles !_TEMP_!orary storing of data.
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

            if not hasattr(self, "dataSdict"): # For first time creation (singleSnap)
                self.dataSdict = {}
                pass # end.IF

            self.dictMaker(parsed_data, self.tempSdict, task, indra, num)
            pass # end.IF single snap storage


        elif self.what_set in self.allSnapActions.keys():
            " Store data for all snaps in a set "

            if not hasattr(self, "dataAdict"): # For first time creation (allSnap)
                self.dataAdict = {}
                pass # end.IF

            self.dictMaker(parsed_data, self.tempAdict, task, indra, num)
            pass # end.ELIF all snap storage
        else:
            print " [...] Uh... error... maybe? But how? "
            pass # end.ELSE wtf-ery

        return 0

    




















    #############################################
    # -------- Initializers of pp-ing: -------- #

    def ppr_basic(self, parsed_data, num):
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
        self.ppActionBasic[self.what](parsed_data)

        return 0
    

    def ppr_basicLast(self, parsed_data, num):
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
        self.ppActionBasicLast[self.what](parsed_data)

        return 0



































    ##################################################################
    # """ -------- Here are "Single Snap pp functions": -------- """ #

    def ppr_posor(self):
        """
        Positions and Origami
        """

        return 0


    def ppr_pof(self):
        """
        
        """

        return 0

    def ppr_porifof(self):
        """
        
        """

        return 0

    def ppr_playOne(self):
        """
        
        """

        return 0


    ##################################################################
    # """ -------- Here are "combinatory pp functions": -------- """ #

    # Need revising; playAll may be working, but these calls still need updating

    def ppr_quori(self):
        """
        
        """

        return 0


    def ppr_sufoIniter(self, sufo_data):
        """
        PP Routine initializer: Subhalo & FoF.
        """
        " Makes sure the temp. dict.s are enriched "
        self.ppmf_tempStorage(sufo_data)

        if self.subfolder is self.subfolder_set[-1]:
            if self.what is self.allSnapActions[self.what_set][-1]:
                " Engage playground on last snapshot in the set "

                print " * Subhalo & FoF pp-ing initialized ! "
                self.pp_sufoCounters()
                print " . Subhalo & FoF pp-ing completed . "
                
                pass # end.IF last data in set
            pass # end.IF     last snap in set

        else:
            print " + Subhalo & FoF storage initialized "
            pass # end.ELSE storage notifier

        return 0


    def ppr_sofaIniter(self, sofa_data):
        """
        Some functions for post-processing of data sets,
        combining SubFind-, Origami, & FoF Analysis
        """
        " Makes sure the temp. dict.s are enriched "
        self.ppmf_tempStorage(sofa_data)

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

    
    def ppr_sofaSlouch(self): 
        """
        Collects Subhalo, Origami, & FoF Analysis functions
        """
        # Data is accessable at dictionary addresses:
        "| >>> self.tempAdata[ 'fof'    ][ self.iString ][ snapNumber ] "
        #| fofIDs, tNgrps, groupLen, groupOffset
        
        "| >>> self.tempAdata[ 'suhalo' ][ self.iString ][ snapNumber ] "
        #| subIDs, tNsubs, catalog

        # Arrays are preferred to operate; so we build them:
        ngp, nsp, tng, tns = self.sufoCounters( len(self.subfolder_set) ,
                                                self.sIndex             )
        nhtags = self.pp_oriFetch('h')
        # Plot SubFind-subhalo-, Origami-halo, & FoF-halo- particle counts
        self.plot_sofa(nsp, nhtags, ngp)
        return 0













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