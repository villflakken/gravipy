

Current work:

= Make the imported function thing use a dictionary instead of a list

= Check unique IDs for every i \in [0,256)
    \ if yes:
        Create array for particles á là: pl.zeros(1024**3)

Sorry, I was a bit riled up/restless when I was talking to you, so I knew that I'd be better off getting written answers:

1) Do you want me to copy the contents of _your_ "../b100/" folder, in order to have the files which "posfile"-parameter's string refers to - considering running origami requires these binaries, and I haven't these produced in my folders (and your parameters example show a path into your folder system)?

2) I'm assuming "boxsize"'s default values in "parameters_example.txt" are ok parameters.

3) I'm not sure about what to set "np1d" to. Do you want me to set it to i.e. "the maximum number of particles encountered in a reading of 256 files"?
    3.a) I'm wondering about this, because I've printed out the values of "npart" encountered in every binary file; and "npart" varies from every file to the next.

4) "numfiles" is the the number of relevant files to be read, that much is fairly obvious.
    4.a) What is "Gadget", really? From Table 1 , it kind of sounds like it's the difference between the program concentrating on snapshotdirs and ffts, making "numfiles" not then the number count of the cores applied - but the number of relevant files, instead. 
    4.b) Though I this probably has something to do with the problem you were talking about over the summer: that the reading of the files is delegated across a set of cores, and there was a problem with switching from 8 to 12.
