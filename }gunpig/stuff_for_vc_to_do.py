
=================*Getting Started*=================
1. Log on to alpha01.sciserver.org/compute

2. Create container:
  - check boxes for user volumes "persistent" and "scratch"
  - check box for public volumes "Indra Simulations"

3. Create a new Jupyter notebook, terminal, etc. on the right
*Notes*
- From a terminal, cd to your home directory:
 > cd /home/idies/workspace/persistent 
- You can't make things executable. Run scripts using
 > sh scriptname
- In a notebook, when finished go to Kernel -> Restart & Clear Memory, 
can keep tab open, or File -> Close and Halt to close and exit.
- There is limited software installed! If there's something missing 
that you need, talk to Gerard or try to install it.


=================*To transfer large files:*=================
1. Log on to gwln1.pha.jhu.edu

2. Set the group that your session uses to 'nbody'. You can do that using:
 > chgrp nbody .
 (note that the . is required!)

3. Check if you can see the data. Note, use the full path:
 > cd /sciserver/vc/indra
(Don't try first 'cd /sciserver/vc' then 'cd indra'.)

4. Copy ORIGAMI files to /sciserver/vc/indra/origami. For example,
for a snapshot of the 2_0_0:
 > cp /home/magnucb/... /sciserver/vc/indra/origami/2_0_0/...

5. Make sure the uploaded files are world readable.


=================*To run batch jobs*=================
1. Log on to alpha01.sciserver.org/racm
2. Do some stuff...


=================*Notes*=================
jupyter folder dir: " /home/idies/workspace/ == ~/ "
# i.e.
/home/idies/workspace/indra                 # indra raw stuff
/home/idies/workspace/indra/origami   # origami raw stuff
/home/idies/workspace/persistent         # my stuff

-bash-4.1$ cp -r ~/oriread/* origami/
-bash-4.1$ pwd
/sciserver/vc/indra

