str1 = '''    def ppro_oritagNfetch(self, otype='h'):
        """
        Post-Processing Routine Operation

        Runs through Origami output to retrieve requested tags.
        """
        oTag_dict = {
            'v' : 0,
            'w' : 1,
            'f' : 2,
            'h' : 3
        }
        if otype not in oTag_dict.keys(): sys.exit(" Invalid 'otype' (OrigamiParticleType) ")

        nOtags = N.zeros( len(self.sIndex), dtype=N.int64 )

        for si in self.sIndex:
            sn = self.subfolder_set[si]
            nOtags[si] = N.sum( # Sum(bools(type)) => N(type)
                self.dataAdict['origami'][self.iString][sn][0] == oTag_dict[otype]
            )
            continue

        return nOtags'''

str2 = '''    def ppro_oritagNfetch(self, otype='h'):
        """
        Post-Processing Routine Operation

        Runs through Origami output to retrieve requested tags.
        """
        oTag_dict = {
            'v' : 0,
            'w' : 1,
            'f' : 2,
            'h' : 3
        }
        if otype not in oTag_dict.keys(): sys.exit(" Invalid 'otype' (OrigamiParticleType) ")

        nOtags = N.zeros( len(self.sIndex), dtype=N.int64 )

        for si in self.sIndex:
            sn = self.subfolder_set[si]
            nOtags[si] = N.sum( # Sum(bools(type)) => N(type)
                self.dataAdict['origami'][self.iString][sn][0] == oTag_dict[otype]
            )
            continue

        return nOtags'''

for i, j in zip(str1, str2):
    print i, j, i is j, i == j