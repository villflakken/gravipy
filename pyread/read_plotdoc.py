# ==============================================
# Read.& proc. data sets' visualisation tools.
# ==============================================
import os, sys, time
import numpy as N
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc
rc('font',**{'family':'serif'})


class Plotter(UserTools):
    """
    Plotting Tools and Templates.
        # Outside-callable-pre-defined user plotting tools.
        # Basically: as I go along and develop plotting methods;
        #     put the finished methods in here.
        #         - In later versions: Methods may be merged / initialized into auto-pp.

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

    def plot_pos_oritag(self, pos, tags):
        """
        Plots positions of particles to 2D or 3D.
        Also uses Origami tagging to colour-code particles.
        """
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
        
        if 2 in self.plotdim:
            # 2D scatter plot
            time_2dplot_start = time.time()

            " Defaults to 2 dimensions in plot "
            fig = pl.figure("scatter2d", figsize=(10,10))#, dpi=200)
            ax  = fig.add_subplot(111)

            ax.scatter(posvoid[:,0], posvoid[:,1], s=1, c=voidc, marker='.', label=voidl)
            ax.scatter(poswall[:,0], poswall[:,1], s=1, c=wallc, marker='.', label=walll)
            ax.scatter(posfila[:,0], posfila[:,1], s=1, c=filac, marker='.', label=filal)
            ax.scatter(poshalo[:,0], poshalo[:,1], s=1, c=haloc, marker='.', label=halol)

            ax.set_xlabel('x-position Mpc/h')
            ax.set_ylabel('y-position Mpc/h')
            ax.set_aspect('equal','box')
            ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=10)
            ax.grid(True)
            fig.tight_layout()
            pl.show("scatter2d")

            time_2dplot_end = time.time()
            print "2D scatter plot time: {0:.2f} seconds".format((time_2dplot_end - time_2dplot_start))
            # pl.close("scatter2d")
            
            pass

        if 3 in self.plotdim:
            # 3D scatter plot
            time_3dplot_start = time.time()

            " In case of 3d "
            fig =  pl.figure("scatter3d", figsize=(20,20))#, dpi=200)
            ax  = fig.add_subplot(111, projection='3d')
            
            # In the voice of an authorative Patrick Stewart:
            " ENGAGE 3D VIZUALIZATION "
            ax.scatter(posvoid[:,0], posvoid[:,1], posvoid[:,2], s=1, c=voidc, marker=',', label=voidl)
            ax.scatter(poswall[:,0], poswall[:,1], poswall[:,2], s=1, c=wallc, marker=',', label=walll)
            ax.scatter(posfila[:,0], posfila[:,1], posfila[:,2], s=1, c=filac, marker=',', label=filal)
            ax.scatter(poshalo[:,0], poshalo[:,1], poshalo[:,2], s=1, c=haloc, marker=',', label=halol)
            
            ax.set_xlabel('x-position Mpc/h')
            ax.set_ylabel('y-position Mpc/h')
            ax.set_zlabel('z-position Mpc/h')
            ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=10)

            gplot.axisEqual3D(ax) # Axes aspect ratio correction
            pl.show("scatter3d")

            time_3dplot_end = time.time()
            print "3D scatter plot time: {0:.2f} seconds".format((time_3dplot_end - time_3dplot_start))
            # pl.close("scatter3d") # just because

            pass


        return 0





    # def plot_pos_scatter(self, IDsA, posA, box, plotdim=2,
    #                      plotname="misc_scatplot", plotpath="output_gravipy/"):
    #     """
    #     Plots positional data output.
    #     Example call:
    #     plot_pos_scatter(IDsA=IDs, posA=pos, plotdim=2,
    #                      plotname="funcScatterTest", plotpath="output_gravipy/")
    #     """
    #     print "  * Initiating {0} scatter plot of positions from simulation data"\
    #             .format((str(plotdim)+"d"))
        
    #     fig =  pl.figure(figsize=(10,10))

    #     " Scatter plot "
    #     if plotdim == 2:
    #         " Defaults to 2 dimensions in plot "
    #         ax  = fig.add_subplot(111) # 2d as default
    #         ax.scatter( posA[:,0], # x-elements
    #                     posA[:,1], # y-elements
    #                      s=1 )
    #         ax.set_xlabel('x-position Mpc/h')
    #         ax.set_ylabel('y-position Mpc/h')
    #         ax.set_aspect('equal','box')
    #         pl.grid(True)
    #         pass

    #     elif plotdim == 3:
    #         " In case of 3d "
    #         ax  = fig.add_subplot(111, projection='3d')
    #         # in the voice of an authorative Patrick Stewart:
    #         " ENGAGE 3D VIZUALIZATION "
    #         ax.scatter( posA[:,0], # x-elements
    #                     posA[:,1], # y-elements
    #                     posA[:,2], # z-elements
    #                     depthshade=True, s=1)
    #         ax.set_xlabel('x-position Mpc/h')
    #         ax.set_ylabel('y-position Mpc/h')
    #         ax.set_zlabel('z-position Mpc/h')
            
    #         # Axes
    #         self.axisEqual3D(ax)
    #         pass

    #     else:
    #         sys.exit(" * Unbelievable error. ")
        
    #     Saving, if wanted

    #     plotpath = self.outputPather(plotpath, plotname)
    #     plotpath = plotpath + "/" + plotname \
    #                + "_{0}d".format(plotdim) + ".png"
    #     print "    Saving plot (pos), {0:d}D. \n".format(plotdim)
    #     pl.savefig(plotpath, dpi=200, bbox_inches='tight')
    #     pl.close()
    # return 0


    if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
             Please run read.py instead.")