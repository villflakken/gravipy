import sys
class Cat(object):
    def __init__(self, a):
        self.a = a
    def recurve(self):
        if self.a == "wow":
            # Step 1
            print    "changing self.a => 'first'"
            self.a = "first"
            self.recurve()
            # Step 2
            print    "changing self.a => 'second'"
            self.a = "second"
            self.recurve()
            pass

        elif self.a == "first":
            #
            self.first()
            pass

        elif self.a == "second":
            #
            self.second()
            pass

        else:
            sys.exit("\n No dice!")

        return 0

    def first(self):
        print "inside:", self.funcNameOver("here"),\
              ":", "self.a =", self.a
        return 0

    def second(self):
        print "inside:", self.funcNameOver("here"),\
              ":", "self.a =", self.a
        return 0 

    def funcNameOver(self, where="1up"):
        """
        Returns name of nested function in which this function is called.
        Useful for debugging.
        """
        ranks = {"inception": 0, "here": 1, "1up": 2, "2up": 3}
        return str(sys._getframe(ranks[where]).f_code.co_name)

test = Cat("wow")
test.recurve()

datasets = {"params_i200tmp_sf62": 0, "params_i200tmp_sf63": 1, "params_i201tmp_sf62": 2, "params_i201tmp_sf63": 3}
datasets_keylist = datasets.keys()
objects = tuple(datasets_keylist[:])
print objects
print type(objects)

