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
            pl.close("scatter2d")
            
            pass

        if 3 in self.plotdim:
            " 3D scatter plot "
            time_3dplot_start = time.time()

            fig =  pl.figure("scatter3d", figsize=(20,20))#, dpi=200)
            ax  = fig.add_subplot(111, projection='3d')
            
            # In the voice of an authorative Patrick Stewart:
            "- ENGAGE 3D VIZUALIZATION "

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
            
            ax.set_xlabel('x-position Mpc/h')
            ax.set_ylabel('y-position Mpc/h')
            ax.set_zlabel('z-position Mpc/h')

            ax.legend(bbox_to_anchor=(0,0.14, 1,-0.2), \
                      loc="upper left", mode="expand", ncol=4, prop={'size':15}, markerscale=10)

            self.axisEqual3D(ax) # Axes aspect ratio correction
            pl.show("scatter3d")

            time_3dplot_end = time.time()
            print "3D scatter plot time: {0:.2f} seconds".format((time_3dplot_end - time_3dplot_start))
            pl.close("scatter3d") # just because

            pass


        return 0





if __name__ == '__main__':
    sys.exit("Attempt at running code from unintended source. \n\
         Please run read.py instead.")