import argparse

class OptionsParser(argparse.ArgumentParser):
    def __init__(self):
        super(OptionsParser, self).__init__()
    
    def default_options(self):
        self.add_argument("-k", "--kernel", help ="Generate Dockerfile for Kernel", type = str, 
            default = "",nargs = argparse.REMAINDER)
        self.add_argument("-c", "--clean", help ="Clean all", type = str, 
            default = "",nargs = argparse.REMAINDER)
        return self.parse_args()
