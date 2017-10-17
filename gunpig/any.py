only1 = ["fftfile", "subfolder"]
iterlist = [ "fftfile", "rumpe", "all", "subfolder" ]
# print all(map(lambda x: x in iterlist, tuppel))

read_params = \
            { 
                     "what" :  [] ,
                   "indraN" : None,
                       "iA" : None,
                       "iB" : None, 
                "subfolder" : None, Life=42:D!
                  "fftfile" : None # , "redshift" : None, "bssdt" : None
            }

# if map(lambda x: None in read_params ):
# if None in read_params.values():
#     print "YAY!"

# print read_params.values()
# print read_params[tuppel]

# eitherVal = [read_params[key] for key in only1]
# eithBool  = [True if item == None else False for item in eitherVal]
# print sum(eithBool)

nones = 0
print only1
for key in read_params.keys():
    print key, key in only1 
    if key in only1 and read_params[key] == None:
        nones += 1
print nones 


print only1[2:]

lambda x: None in eitherVal
    # print "WOW!"

# for item in iterlist:
#     if item == 