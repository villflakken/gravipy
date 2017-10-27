### **GRAVIPy**

---

### **G**eneral **R**esource for **A**nalyzing and **V**isualizing **I**ndra with **P**ython

GRAVIPy is a pythonic companion toolkit for reading and processing INDRA's output data; INDRA being a set of numerical simulations that have modelled matter distributions in the universe over time, as affected gravity.

All necessary scripts are located in folder **pyread/**.
Other folders and files are my own resources for project overview and debug
sketching.

Scripts were initially translated from IDL into Python.

Python software initialized through an intertwined class system with call 
functionality.
Every option/parameter for post processing or setting the reader's parameters are 
included in the file '**pyread/testrun.py**'.

[Output repository](https://github.uio.no/magnucb/output_gravipy)

---
### Current features:
* Reads binary INDRA and ORIGAMI data, and projects it out to the user for post-processing.
* Contains methods for post processing of the data, specifically to compare outputs from the two.

---
### Changelog:

  All changes currently reflect the state of the function handling reading of positions.

###### To consider:
* Thinking of making a specific document for the general plotting tools only, as syntax with that may be quite long-winded indeed - even if these do not need to be included; data may be simply plotted outside of the class structure (for overly specific visualizations)...
  * or basically, if I write very specific plot functions underway that I may want to use again at a later point; this is where they may be stored.

* Figure out the best way with which to return the data when finished with the reading;
  1. For a single-set reading, only returning the that set's data, pure and simple.
  2. For multi-set reading, return a dictionary..? Would be hard to handle with predetermined scripts, maybe?...  
    * But controlling these on Jupyter would be simple, to keep the datasets apart - just refer to the indexes from a printed list of said dictionary's keys! :D

------
**0.52 from 0.51** (WIP):
* Added the file and corresponding class `read_autotools.py` for when automated reading&postprocessing is wanted, but made `read_usertools.py` as a toolkit for live data manipulation w/ Jupyter - so that the latter's functions are less dependent on the parameters associated with the class' initialization.

* Allowing the automated initialization-system to work out wether it is run from a Jupyter instance on SciServer, or wether the script is run from the elephant clusters - in order to get the INDRA data retrieved - unless the user specifies datapath for these.

* Verifying that the currently written method for reading of ORIGAMI works.

------
**0.51, from 0.50**:
* Differentiated between `read_misctools.py`, and `read_usertools.py` - making it easier to go in and view user-relevant tools.
* Fixed array structure from   
  `positions = 256(number of read files) * N_i(the i'th file's particle count) * 3(xyz coords)`   
  into the more manageable   
  `positions = N(total particle number in simulation) * 3(xyz coords)`.

* Implementing binary reading of **Origami** output (particle tagging, sorted by ID).

* Left the config file- and command line initializations behind as legacy features that may be re-implemented in the future. Now put in `betas/` folder.

* Particle boxing based on positions currently placed in reading procedures.

------
**0.50, from scratch**:
* Intrinsic structure initially designed to simply get input, process all data automatically, and yield output in forms of text and/or plots, with the least amount of interaction to be necessary from a user.
  * `read.py` is the class system's initiator. It handles the general flow depending on wether the class was initialized to be used as a function call, or a pre-determined set of INDRA-variables to be read and processed. Then it sifts through the INDRA data as set by the user, and, if enabled, engages post processing.
  * `read_args.py` handles reading of arguments. In the beginning, this was designed to process
    * command line variables for the INDRA parameters.
    * config file initialization containing INDRA parameter variables (called `read_cfg`).
      * ...with a corresponding program to restore a "default parameter" config file (called `restore_default_cfg.py`).
    * user input INDRA parameters through a call function.
    
  At the time this script contained all these functions at the same time, it was well over 1k lines, and desperately needed tidying up... O.O
  * `read_procedures.py` outlines each data type's reading's program flow.
  * `read_misctools.py` contains miscellaneous tools; tools that would help the scripts function as intended - in most cases simply used as a a script in which to put smaller functions, thus increasing the programmer's ability to read the main program flow.
  * `read_sifters.py` contains all the binary data sifters, as directly translated from the IDL source code (the found in `src_scripts/`).
  * `testrun.py` is a simple script that shows an example of how one may initiate the system, and contains all the parameters one could need - a user is meant to run this function or copy-paste its contents, with as much parameters as the user would need.

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

And if you do indeed read through it, you may notice that the code has been
adapted for python 2.6, an intentional choice. It has also been made to work
as robustly as I can think of how to make it, with as much functionality as 
possible to be readily available.

------
###### Project by
**Bridget Falck, ITA, UiO**      (supervisor) - bridget.falck (at) astro.uio.no

**Magnus Chr. Bareid, ITA, UiO** (developer)  - magnucb (at) astro.uio.no