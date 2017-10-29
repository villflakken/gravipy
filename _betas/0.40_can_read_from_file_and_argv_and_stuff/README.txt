# ----------------------------------------------------------------------------|
# read.py reads data from INDRA-simulations or ORIGAMI post-processing.       |
# This is a README to explain how to use read.py for this purpose.            |
# ----------------------------------------------------------------------------|
                                                                            
- You may choose to read the data by way of several command line arguments
placed after read.py;
- Or you may configure parameters and options for the program to run with using 
the config file, read_cfg, which is interpreted by read.py by either specifying
cfg as a command line argument; 
- or by simply leaving _no_ command line arguments - read.py loads the cfg by 
default, unless specifically told otherwise.

The config file determines what data to read, with _all options available_ for
the user to vary.
Not all the options will have an effect on every single part of the script; 
the options' effects should be listed in the relevant areas.

To configure the reading options in read_cfg, open it in your favorite script
editor and set its variables to your requirements, save, and run read.py
accordingly.
                                                                            
Every option will be listed categorically, and the corresponding argument
to that option is then shown after a colon on the same line. Some options will
have several keyword arguments which will initiate the same procedure; simply
allowing for user's vocabulary preference.

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
as robustly as I can think of how to make it, some times with multiple 
redundancies of

- Project by
* Bridget Falck, ITA, UiO (supervisor)     - bridget.falck (at) astro.uio.no
* Magnus Chr. Bareid, ITA, UiO (developer) - magnucb(at)astro.uio.no