# Current goals

## Code & programming:
Fix indexation in **fof** & **subh**
    - [ ] subtract **fof** IDs by 1 
    - [ ] subtract **subh** IDs by 1 

- [ ] Finish code update in **subh** 
    - From Bridget's `read_indra.py` => `read_indra_wdiffsort.py` 
    - Return all variables, not just those that `read_sub.pro` returns 

Comparing sorters: 
- [ ] Old sorting time 
- [ ] New sorting time 


## Halo statistics over time

### fof-statistics 
- [ ] number of halos found in every snapshot 

- [ ] number of halo particles found in every snapshot 

- [ ] isolate a single halo and track it backwards in time 
    - begin at *z = 0* 
    - [ ] retrieve halo's outermost coordinates at a step; store the "box" 
    - [ ] numbers retrieved and/or produced should be returned 

        - [ ] IDs of particles to the halo 
        - [ ] positions of particles to the halo 

    - [ ] should be able to return particle IDs belonging to halo in question 

### origami-statistics 
- [ ] numbers of categorized particles found in every snapshot 

## Plots 
- [ ] number of halo particles found in every snapshot 
    - both: **origami** and **fof** 
- [ ] number of h,f,w,v particles found in every snapshot 
- [ ] number of halos found in every snapshot (**fof**) 
- [ ] mass-binned power spectrum 