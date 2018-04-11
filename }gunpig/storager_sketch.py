# First sketch of the storager()-method

    def sketch_of_storager(self, parsed_data, num):
        """
        # Sketching code with 2 algorithms,
        # which should be equivalent.

        Stores the data into some kind of logical structure
        (? - feedback needed)

        ### Current proposal:
        3-leveled/indexed nested dictionary structure, shown below
        
        output_dataset  # -> variable stored to outside (of this) script
            |
            |--> ["{task/data category}"]
                          |
                          |--> ["{iN}{iA}{iB}"]
                                      |
                                      |--> ["{snapshotnumber}"]
                                                    |
                                                    |--> parsed_data
        - where 'parsed_data' as a variable contains
        several items from the reading of a snapshot's data
        (pertaining to the data type/category/"task").
        """
        # self.datadict = {}      # Declared outside of this scope!
        task =     self.what    # -- --> Outermost dictionary key 
                                  #              (already string).
        iN   = str(self.indraN) # -- --> Together, these 3 form the middle key
        iA   = str(self.iA)       # --^
        iB   = str(self.iB)       # -^
        num  = num              # -- --> Innermost key.

        indra = "{0:1d}{1:1d}{2:1d}".format(iN, iA, iB)

        if task not in self.datadict.keys():
            
            " Declaration of task-name-key "
            # self.datadict.update() #?
            self.datadict[task] = {indra : {num : parsed_data}}
            pass

        else:

            " Case: dict already has the task-name-key "
            if indra not in self.datadict[task].keys():
                
                " Declaration of indra-key "
                self.datadict[task][indra] = {num : parsed_data}
                pass

            else:

                " Case: dict already has indra-key "
                self.datadict[task][indra][num] = parsed_data 
                pass # Out of 2nd if-test's else-block

            pass # Out of 1st if-test's else-block, back to function

        #### ALTERNATIVELY, bools rendered the other way around 
        #### (not finished)

        if task in self.datadict.keys():
            
            " Case: dict already has the task-name-key "
            if indra in self.datadict[task].keys():

                " Case: dict already has indra-key "
                self.datadict[task][indra][num] = parsed_data
                pass # Out of 2nd if's IF block

            else: # 'indra' _not_ in datadict['task'] 

                " Case: First entry of current indra-key "
                self.datadict[task][indra] = {num : parsed_data}
                pass # Out of 2nd if's ELSE block

            pass # Out of 1st if's IF block

        else:

            " Case: First entry of current task-name-key "
            self.datadict[task] = {indra : {num : parsed_data}}
            pass # Out of 1st if's ELSE block

        return 0