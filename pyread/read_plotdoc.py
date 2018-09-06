# ==============================================
# Read.& proc. data sets' visualisation tools.
# ==============================================
import os, sys, time
import numpy as N
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
rc('font',**{'family':'serif'})


class Plotter(object):
    """
    Plotting Tools and Templates.
        # Outside-callable-pre-defined user plotting tools.
        # Basically: as I go along and develop plotting methods;
        #     put the finished methods in here.
        #         - In later versions: Methods may be merged,
        #                              or initialized into auto-pp.

    ... Maybe the inheritance should go the other way..?
    """
    def __init__(self):
        # UserTools.__init__(self)
        """
        End of init
        """
    
    def axisEqual3D(self, ax):
        " Shamelessly stolen from StackOverflow "
        extents = N.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
        sz = extents[:,1] - extents[:,0]
        centers = N.mean(extents, axis=1)
        maxsize = max(abs(sz))
        r = maxsize/2
        for ctr, dim in zip(centers, 'xyz'):
            getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)
            continue

        return 0

    def plot_pos_oritag(self, pos, tags, dimtuple=None):
        """
        Plots positions of particles to 2D or 3D.
        Also uses Origami tagging to colour-code particles.
        """
        if dimtuple == None:
            " Outside use did not specify a dimension "
            dimtuple = self.plotdim # Defaults to (2)
            pass
        else:
            " User has provided plotdim "
            pass

        if not hasattr(dimtuple, '__iter__'):
            " Value provided is scalar; needs iterability "
            dimtuple = (dimtuple,)
            pass

        # Tag-specific plot variables
        voidc = 'k'
        wallc = 'b' 
        filac = 'm'
        haloc = 'r'    
        voidl = "Void"   #label
        walll = "Wall"   #label
        filal = "Filam." #label
        halol = "Halo"   #label

        # More boolean matrixes; [True, False, False, True, etc...]
        vtags = tags==0 
        wtags = tags==1
        ftags = tags==2
        htags = tags==3

        # Creating pos. matrixes for every category; not bools.
        posvoid = pos[vtags,:]
        poswall = pos[wtags,:]
        posfila = pos[ftags,:]
        poshalo = pos[htags,:]
        
        if 2 in dimtuple:
            " 2D scatter plot "
            time_2dplot_start = time.time()

            fig = pl.figure("scatter2d", figsize=(10,10))#, dpi=200)
            ax  = fig.add_subplot(111)

            " Voids "
            ax.scatter(posvoid[:,0], posvoid[:,1], 
                           s=1, c=voidc, marker='.', label=voidl)
            " Walls "
            ax.scatter(poswall[:,0], poswall[:,1], 
                           s=1, c=wallc, marker='.', label=walll)
            " Filaments "
            ax.scatter(posfila[:,0], posfila[:,1], 
                           s=1, c=filac, marker='.', label=filal)
            " Halos "
            ax.scatter(poshalo[:,0], poshalo[:,1], 
                           s=1, c=haloc, marker='.', label=halol)

            ax.set_xlabel('x-position Mpc/h')
            ax.set_ylabel('y-position Mpc/h')
            
            ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
                      loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=10)
            ax.grid(True)
            
            ax.set_aspect('equal','box')
            fig.tight_layout()
            pl.show("scatter2d")

            time_2dplot_end = time.time()
            print "2D scatter plot time: {0:.2f} seconds".format((time_2dplot_end - time_2dplot_start))
            pl.savefig(self.outfilePath + "_posori2d.png", dpi=200)
            pl.close("scatter2d")
            
            pass

        if 3 in dimtuple:
            " 3D scatter plot "
            # In the voice of an authorative Patrick Stewart:
            "- ENGAGE 3D VIZUALIZATION! "

            # Initialization
            time_3dplot_start = time.time()
            fig =  pl.figure("scatter3d", figsize=(20,20))#, dpi=200)
            ax  = fig.add_subplot(111, projection='3d')
            
            # Objects
            " Voids "
            ax.scatter(posvoid[:,0], posvoid[:,1], posvoid[:,2], 
                       s=1, c=voidc, marker=',', label=voidl)
            " Walls "
            ax.scatter(poswall[:,0], poswall[:,1], poswall[:,2], 
                       s=1, c=wallc, marker=',', label=walll)
            " Filaments "
            ax.scatter(posfila[:,0], posfila[:,1], posfila[:,2], 
                       s=1, c=filac, marker=',', label=filal)            
            " Halos "
            ax.scatter(poshalo[:,0], poshalo[:,1], poshalo[:,2], 
                       s=1, c=haloc, marker=',', label=halol)

            # Plot details
            ax.set_xlabel('x-position Mpc/h')
            ax.set_ylabel('y-position Mpc/h')
            ax.set_zlabel('z-position Mpc/h')
            ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
                      loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=10)

            # Fixing aspect ratio in 3D and savefig
            self.axisEqual3D(ax)
            # pl.savefig("somepath")

            # Terminal/display output
            pl.show("scatter3d")
            time_3dplot_end = time.time()
            print "3D scatter plot time: {0:.2f} seconds".format((time_3dplot_end - time_3dplot_start))
            pl.savefig(self.outfilePath + "_posori3d.png", dpi=200)
            pl.close("scatter3d")

            # Return to function
            pass

        else:
            sys.exit(" Please specify plot dimensions as '2', '3' or '(2,3)' ")


        return 0


    def plot_sufoHcount(self, tng, tns):
        """
        Is given TotalN(fof- or sub-) halo counts, and plots them over time.
        """
        redshifts = self.datadict["time"]["redshift"][self.subfolder_set] 
        scale_y = 1.*1e+6
        
        ### """ ---- 1st plot ---- """
        hcfig = pl.figure("sufoHcount", figsize=(10,10))
        ax1 = hcfig.add_subplot(111)
        ax1.plot( 
            redshifts    , 
            tng /scale_y , 
            label='FoF' ,
            linestyle='-',  linewidth=3, color='black'
        )
        ax1.plot( 
            redshifts    , 
            tns /scale_y , 
            label='Subhalo' ,
            linestyle='--', linewidth=3, color='gray'
        )
        ax1.set_xlabel(r"$z$ [redshift]")
        ax1.set_ylabel(r"Halo counts of type over time")
        ax1.plot()

        # ax1.set_xscale("log", nonposx='clip')
        # ax1.set_yscale("log", nonposy='clip')

        ax1.grid('on')
        # ax2.legend( 
        #     bbox_to_anchor=(0,0.14, 1,-0.2),
        #     loc="upper left", mode="expand",
        #     ncol=4, prop={'size':15}, markerscale=4
        # )
        ax1.legend(loc='best')

        # Ways to invert the axes:
        ax1.set_xlim([7.5, redshifts[-1]])

        plotfname = self.outfilePath + "_sufoHcount"
        pl.savefig( plotfname +".png", dpi=200 )
        pl.show(   "sufoHcount" )
        pl.close(  "sufoHcount" )


        ### """ ---- 2nd plot ---- """
        hcfig = pl.figure("sufoHcount_zoom", figsize=(10,10))
        ax2 = hcfig.add_subplot(111)
        ax2.plot( redshifts , tng/scale_y  , 
            label='FoF'    , linestyle='-' , linewidth=3, color='black'
        )
        ax2.plot( redshifts , tns/scale_y  , 
            label='Subhalo', linestyle='--', linewidth=3, color='gray'
        )
        ax2.set_xlabel(r"$z$ [redshift]")
        ax2.set_ylabel(r"Halo counts of type over time")

        # ax2.set_xscale("log", nonposx='clip')
        ax2.set_yscale("log", nonposy='clip')

        ax2.grid('on')
        # ax2.legend( 
        #     bbox_to_anchor=(0,0.14, 1,-0.2),
        #     loc="upper left", mode="expand",
        #     ncol=4, prop={'size':15}, markerscale=4
        # )
        ax2.legend(loc='best')

        # Ways to invert the axes:
        ax2.set_xlim([3, redshifts[-1]])
        ax2.set_ylim([4e-1, 3.1])


        plotfname = self.outfilePath + "_sufoHcount_zoom"
        pl.savefig( plotfname +".png", dpi=200)
        pl.show(   "sufoHcount_zoom" )
        pl.close(  "sufoHcount_zoom" )
        
        return 0


    def plot_sufoderiv(self, tng, tns):
        """
        Is given TotalN(fof- or sub-) halo counts,
        and plots their ratios and differientials over time.
        """
        scale_y = 1.
        redshifts = self.datadict["time"]["redshift"][self.subfolder_set] 
        suforatiofig = pl.figure("sufoHcount_ratio", figsize=(10,10))
        ax1 = suforatiofig.add_subplot(111)

        # ax1.plot(redshifts, (tng_all - tns)/scale_y, label='FoF-Subhalo', linestyle='-', color='green')
        ax1.plot(redshifts[tns != 0], (tng[tns != 0])/(tns[tns != 0].astype(N.float64)),
                 label='FoF/Subhalo', linestyle='-', color='green')
        ax1.set_xlabel(r"$z$ [redshift]")
        ax1.set_ylabel(r"Halo counts of type over time")

        # ax1.set_xscale("log")#, nonposy='clip')
        # ax1.set_yscale("log")#, nonposy='clip')

        ax1.grid('on')
        # ax1.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
        #                       loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=4)
        ax1.legend(loc='best')

        # Ways to invert the axes:
        # ax1.set_xlim([7.5, redshifts[-1]])
        # ax1.set_xlim([redshifts[0], redshifts[-1]]) 
        pl.gca().invert_xaxis()
        pl.gca().set_aspect(aspect='auto', adjustable='datalim')

        plotfname = self.outfilePath + "_sufoHcount_ratio"
        pl.savefig( plotfname +".png", dpi=200)
        pl.show(   "sufoHcount_ratio" )
        pl.close(  "sufoHcount_ratio" )

        #### ####
        # plot derivatives: d(tng)/dz, d(tns)/dz
        dz  = redshifts[1:] - redshifts[:-1] 
        dtng = tng[:-1] - tng[1:]
        dtns = tns[:-1] - tns[1:]
        
        sufoderivfig = pl.figure("sufoHcount_deriv", figsize=(10,10))
        ax2 = sufoderivfig.add_subplot(111)

        ax2.set_xlabel(r"$z$ [redshift]")
        ax2.set_ylabel(r"Ratio of halo counts of type over time")
        ax2.plot(redshifts[:-1], dtng/dz, label=r'd(FoF)/d$z$', linestyle='-', color='black')
        ax2.plot(redshifts[:-1], dtns/dz, label=r'd(Subhalo)/d$z$', linestyle='--', color='gray')

        # ax2.set_xscale("log")#, nonposy='clip')
        # ax2.set_yscale("log")#, nonposy='clip')

        ax2.grid('on')
        # ax2.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
        #                       loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=4)
        ax2.legend(loc='best')

        # Ways to invert the axes:
        ax2.set_xlim([7.5, redshifts[-1]])
        # ax2.set_xlim([redshifts[0], redshifts[-1]]) 
        # pl.gca().invert_xaxis()

        plotfname = self.outfilePath + "_sufoHcount_deriv"
        pl.savefig( plotfname +".png", dpi=200)
        pl.show(   "sufoHcount_deriv" )
        pl.close(  "sufoHcount_deriv" )

        return 0


    def plot_sofa(self, nsp, nhtags, ngp):
        """
        Plotting views of particles pertaining to structure classifications:
        * Subhalo groups
        * Origami tags
        * FoF halo groups
        """
        redshifts = self.datadict["time"]["redshift"][self.subfolder_set] 
        scale_y = 1024.**3


        fig = pl.figure("sofa_NpartH", figsize=(10,10))
        ax = fig.add_subplot(111)
        ax.plot( redshifts, ngp/scale_y,
                 label='FOF'     , linestyle='-' , linewidth=3, color='black' )
        ax.plot( redshifts, nsp/scale_y, 
                 label='Subhalo' , linestyle='--', linewidth=3, color='cyan'  )
        ax.plot( redshifts, nhtags/scale_y,
                 label='Origami' , linestyle=':' , linewidth=3, color='red'   )
        ax.set_xlabel(r"$z$ [redshift]")
        ax.set_ylabel(r"Halo particle counts / Total no. of particles")

        # ax.set_xscale("log")#, nonposy='clip')
        # ax.set_yscale("log")#, nonposy='clip')

        ax.grid('on')
        # ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
        #                       loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=4)
        ax.legend(loc='best')

        # Ways to invert the axes:
        # ax.set_xlim([redshifts[0], redshifts[-1]]) 
        # pl.gca().invert_xaxis()
        ax.set_xlim([7.5, redshifts[-1]]) 

        plotfname = self.outfilePath + "_sofa_NpartH"
        pl.savefig( plotfname +".png", dpi=200)
        pl.show(   "sofa_NpartH" )
        pl.close(  "sofa_NpartH" )
        return 0 


    def plot_quOri(self, nvtags, nwtags, nftags, nhtags):
        """
        Quantities of the Origami-tagged types
        """
        redshifts = self.datadict["time"]["redshift"][self.subfolder_set] 
        scale_y = float(max([nvtags.max(), nwtags.max(), nftags.max(), nhtags.max()]))
        
        fig = pl.figure("quOri", figsize=(10,10))
        ax = fig.add_subplot(111)
        ax.plot( redshifts, nvtags /scale_y, 
                 label='Void',     linestyle='-',  linewidth=3, color='black'   )
        ax.plot( redshifts, nwtags /scale_y,
                 label='Wall',     linestyle='-',  linewidth=3, color='blue'    )
        ax.plot( redshifts, nftags /scale_y, 
                 label='Filament', linestyle='-',  linewidth=3, color='magenta' )
        ax.plot( redshifts, nhtags /scale_y, 
                 label='Halo',     linestyle='-',  linewidth=3, color='red'     )
        ax.set_xlabel(r"$z$ [redshift]")
        ax.set_ylabel(r"Origami-tagged particles / All particles")

        # ax.set_xscale("log")#, nonposy='clip')
        # ax.set_yscale("log")#, nonposy='clip')

        ax.grid('on')
        # ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
        #           loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=4)
        ax.legend(loc='best')

        # Ways to invert the axes:
        # ax.set_xlim([redshifts[0], redshifts[-1]]) 
        # pl.gca().invert_xaxis()
        ax.set_xlim([7.5, redshifts[-1]]) 

        # Quantities of Origami-tagged particles
        plotfname = self.outfilePath + "_quOri"
        pl.savefig( plotfname +".png", dpi=200)
        pl.show("quOri")
        pl.close("quOri")
        return 0


    def plot_quOriG(self, nvtags, nwtags, nftags, nhtags, grp=0):
        """
        Quantities of the Origami-tagged types --- within a FoF Group
        """
        redshifts = self.datadict["time"]["redshift"][self.subfolder_set] 
        scale_y = float(max([nvtags.max(), nwtags.max(), nftags.max(), nhtags.max()]))
        
        fig = pl.figure("quOriG", figsize=(10,10))
        ax = fig.add_subplot(111)
        ax.plot( redshifts, nvtags /scale_y, 
                 label='Void',     linestyle='-',  linewidth=3, color='black'   )
        ax.plot( redshifts, nwtags /scale_y,
                 label='Wall',     linestyle='-',  linewidth=3, color='blue'    )
        ax.plot( redshifts, nftags /scale_y, 
                 label='Filament', linestyle='-',  linewidth=3, color='magenta' )
        ax.plot( redshifts, nhtags /scale_y, 
                 label='Halo',     linestyle='-',  linewidth=3, color='red'     )
        ax.set_xlabel(r"$z$ [redshift]")
        ax.set_ylabel(r"Origami-tagged particles / Sum of part. in FoF-group at $z=0$.")

        # ax.set_xscale("log")#, nonposy='clip')
        # ax.set_yscale("log")#, nonposy='clip')

        ax.grid('on')
        # ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
        #           loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=4)
        ax.legend(loc='best')

        # Ways to invert the axes:
        # ax.set_xlim([redshifts[0], redshifts[-1]]) 
        # pl.gca().invert_xaxis()
        ax.set_xlim([7.5, redshifts[-1]]) 

        # Quantities of Origami-tagged particles
        plotfname = self.outfilePath + "_quOriG" + str(grp)
        pl.savefig( plotfname +".png", dpi=200)
        pl.show("quOriG")
        pl.close("quOriG")
        return 0


    def plot_shippos(self, pos, fIDs=None, oIDs=None, subIDs=None):
        """
        A plot function for 
        "Spotting Haloes in Indra Particles' Positions, Origami and Subhalo",
        given positions and IDs.
        
        Takes optional argument for FoF IDs-array, to show for
        Also takes an optional Origami IDs-array, that will supply the plot with information about 
        nearby particles tagged by Origami;
        and another optional Subhalo IDs-array, for similar purposes.
        """

        return 0

if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
         Please run read.py instead.")