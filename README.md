# GRAVIPY

General Routines for Analyzing and Visualizing Indra with PYthon

Software initialized by an intertwined class system, with call functionality.
May be initialized by way of a config file; not currently implemented.
Every option for post processing or parameter settings are included in the file
'pyread/testrun.py'

If the program ever starts quoting the movie The Princess Bride (1987),
then rest assured and know that you have done something horribly wrong.
Try restoring the configuration file. A script has been included for this 
purpose.

If you're interested in reading the code itself, you'll see that I've made
comments with abbreviations/acronyms in some places:
    DNN     = Declaration Not Needed (becase IDL source code _did_ need)
    DNC     = Declaration Need Confirmed (for python's interpretation)
    DT      = Debugging Tool (that I used myself)
    LDT     = Legacy Debug Tool (from IDL source code)
    LIDA    = LongID Assumed (hard coded; source code w/option for 32-bit ID)

And if you do indeed read through it, you may notice that the code has been
adapted for python 2.6, an intentional choice. It has also been made to work
as robustly as I can think of how to make it, with as much functionality as 
possible to be readily available.

- Project by
* Bridget Falck, ITA, UiO      (supervisor) - bridget.falck (at) astro.uio.no
* Magnus Chr. Bareid, ITA, UiO (developer)  - magnucb (at) astro.uio.no