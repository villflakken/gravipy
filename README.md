### **GRAVIPy**    

**G**eneral **R**esource for **A**nalyzing and **V**isualizing **I**ndra with **Py**thon  

---
### About:  

GRAVIPy is a pythonic companion toolkit for reading and processing INDRA's output data. A general description, INDRA is a set of numerical simulations that have modelled matter distributions over time in the universe, as affected by gravity.  

More elaborated, INDRA simulations are spatially large-scale ($1Gpc$) representations that show how the universe's matter content has evolved over time. The time frame begins at a point where the matter distribution of the universe is almost homogeneous (around time at redshift $z=127$), after which cosmological structures are accumulating *very* slowly at first. However, after redshift values $z\simeq7$ and beyond until today ($z=0$), structure formation seems to build up rather aggressively, resulting in the formation of what we today call [The Cosmic Web](https://www.google.no/search?q=cosmic+web&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjyyfLOt4baAhWIHJoKHRKDCv0Q_AUICigB&biw=1094&bih=944).  

All necessary scripts are located in folder **pyread/**.  
Other folders and files are my own resources for project overview and debug
sketching.  

Some IDL source scripts were initially provided, which were translated into Python.  

GRAVIPy is designed to be initialized through an intertwined class system, which will also sport call functionality.  
Every option/parameter for post processing or setting the reader's parameters are included in the file **`pyread/read.py`**'s function **`read_ini`**.  
Parameters will be added and removed as needed.

[Output repository](https://github.uio.no/magnucb/output_gravipy)  

---
### Current features:  
* Reads binary INDRA, FoF, SubFind, and ORIGAMI data. It may then:  
  * Return these data out for the user to handle.
    - Format depends on the requested command:  
      + **Dictionary**: Multi-snapshot &/ multi-dataset runs; user opts to 'store' data.  
        * Values at dictionary's keys will be empty if user opts to 'wipe' data instead; which may be preferrable &/ necessary if user intends to work with large numbers of sets.
      + **Tuple**: Single dataset, single snapshot.
  * Currently reads:  
    - INDRA data: positions, velocities, particle IDs.  
    - FoF data: clustered groups, group IDs, particle IDs for these.  
    - Subhalo data: smaller-scale structures (within FoF-groups), particle IDs for these.  
    - ORIGAMI data: structural type tags, ordered by particle ID.  
* Contains methods for post processing of the data, specifically to compare outputs from the two.  

---
### Task list for current tier of changelog:  
[Task list on this gist](https://gist.github.uio.no/magnucb/44923531ed82979a0b465cdc5fb19cdd#file-current_goals-md)


### Changelog:

**FSU01, from FSU00**: *(FSU = **F**of **S**ubhalo **U**pdate)* (WIP)
> * Implement current plot functionalities from Jupyter, to be performed iteratively in the GRAVIPy framework.
> * See task list.


**FSU00, from 0.52**: *(FSU = **F**oF **S**ubhalo **U**pdate)*
> * Friends-of-Friends-reader method has received major update.
>   - Each of the components that go into reading FoF-data have been more generalized; as long as the class instance is initialized, and values for `iN`, `iA`, `iB`, and snapshot numbers are given, then the FoF-reader-methods will be able to read corresponding data.  
> * SubFind's data-reader method has also received a major update, which in this case means that it is actually working as intended (as far as I can see)!  
>   - Almost as independent as the FoF-reader - may finish independence at a later date.  
> * Currently, all data-readers return a dictionary with their accumulated data.
>   - W.r.t. the positions vectors, these occupy ~**12**GiBs of RAM by themselves **per snapshot** (and the particle IDs are 8GiBs themselves). As such, when working on (i.e.) a Jupyter system, if any particles' position plots are to be made with FoF- and Origami tags, then these plots will have to be made individually (rather than loading up a whole range of snapshots of 64*(8+12)=~1280TiB), before memory is then released.  
>     + The reason to include IDs every time, is in the case one does not want to sort the particles by ID, in their arrays; then you need the IDs in the same respective order.  


**0.52, from 0.51**:
> * Added the file and corresponding class `read_autotools.py` for when automated reading&postprocessing is wanted, but made `read_usertools.py` as a toolkit for live data manipulation w/ Jupyter - so that the latter's functions are less dependent on the parameters associated with the class' initialization.  
>   - [x] Check: some of the most important tools now work as class-independent functions; but will need more work in the future.  
> 
> * Allowing the automated initialization-system to work out wether it is run from a Jupyter instance on SciServer, or that script is run from the elephant clusters - in order to get the INDRA data retrieved - unless the user specifies some datapath for these variables.  
> 
> * Verified that the currently written method for reading of ORIGAMI works!  
>   - Also allows color-tagging plots of particles' positions.  
>     + This method will be worked in as a cleanly automatic function.  
> 
> * `read_function` as a simplified reading caller may be implemented.  


**0.51, from 0.50**:  
> * Differentiated between `read_misctools.py`, and `read_usertools.py` - making it easier to go in and view user-relevant tools.  
> * Fixed array structure from  
>   `positions = 256(number of read files) * N_i(the i'th file's particle count) * 3(xyz coords)`   
>   into the more manageable   
>   `positions = N(total particle number in simulation) * 3(xyz coords)`.  
> 
> * Implementing binary reading of **Origami** output (particle tagging, sorted by ID).  
> * Left the config file- and command line initializations behind as legacy features that may be re-implemented in the future. Now put in `_betas/` folder.  
> * Particle boxing based on positions currently placed in reading procedures.  


**0.50, from scratch**:
> * Intrinsic structure initially designed to simply get input, process all data automatically, and yield output in forms of text and/or plots, with the least amount of interaction to be necessary from a user.  
>   * `read.py` is the class system's initiator. It handles the general flow depending on wether the class was initialized to be used as a function call, or a pre-determined set of INDRA-variables to be read and processed. Then it sifts through the INDRA data as set by the user, and, if enabled, engages post processing.  
>   * `read_args.py` handles reading of arguments. In the beginning, this was designed to process  
>     * command line variables for the INDRA parameters.  
>     * config file initialization containing INDRA parameter variables (called `read_cfg`).  
>       * ...with a corresponding program to restore a "default parameter" config file (called `restore_default_cfg.py`).  
>     * user input INDRA parameters through class' call function.
>     * user input INDRA parameters through and outside function which initializes the class system for the user.  
>     At the time this script contained all these functions at the same time, it was well over 1k lines, and desperately needed tidying up... O.O  
>   * `read_procedures.py` outlines each data type's reading's program flow.  
>   * `read_misctools.py` contains miscellaneous tools; tools that would help the scripts function as intended - in most cases simply used as a a script in which to put smaller functions, thus increasing the programmer's ability to read the main program flow.  
>   * `read_sifters.py` contains all the binary data sifters, as directly translated from the IDL source code (the found in `src_scripts/`).  
>   * `testrun.py` is a simple script that shows an example of how one may initiate the system, and contains all the parameters one could need - a user is meant to run this function or copy-paste its contents, with as much parameters as the user would need.  

---
###### If the program ever starts quoting the movie The Princess Bride (1987), then rest assured of the fact, and know this, that you have done something horribly wrong.  

If you're interested in reading the code itself, you'll see that I've made
comments with abbreviations/acronyms in some places:  
```
DNN  = Declaration Not Needed (becase IDL source code _did_ need)
DNC  = Declaration Need Confirmed (for python's interpretation)
DT   = Debugging Tool (that I used myself)
LDT  = Legacy Debug Tool (from IDL source code)
LIDA = LongID Assumed (hard coded; source code w/option for 32-bit ID)
```

And if you do indeed read through it, you may notice that the code has been adapted for python 2.6, an intentional choice. It has also been made to work as robustly as I can think of how to make it, with as much functionality as possible to be readily available.  

------
###### Project by
**Bridget Falck, ITA, UiO**      (supervisor) - bridget.falck (at) astro.uio.no

**Magnus Chr. Bareid, ITA, UiO** (developer)  - magnucb (at) astro.uio.no
