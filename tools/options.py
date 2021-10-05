import argparse

class OptionsParser(argparse.ArgumentParser):
    def __init__(self):
        super(OptionsParser, self).__init__()
    
    def default_options(self):
        self.add_argument('-b', '--buildir',
                          help = 'set build directory path',
                          type = str, 
                          default = '',)
        self.add_argument('-c', '--command',
                          help = 'append command to docker run',
                          type = str, 
                          default = '',
                          nargs = argparse.REMAINDER)
        self.add_argument('-d', '--distclean',
                          help = 'clean all',
                          action='store_true')
        self.add_argument('-n', '--name',
                          help = 'set hostname in container',
                          type = str,
                          default = 'Dev')
        self.add_argument('-k', '--kernel',
                          help = 'generate Dockerfile for Kernel',
                          action='store_true')
        self.add_argument('-m', '--mount',
                          help = 'mount host directories to conatiner',
                          type = str,
                          default = '')
        self.add_argument('-p', '--proxy',
                          help = 'set the http proxy to build image',
                          type = str,
                          default = '')
        self.add_argument('-s', '--stage',
                          help = 'build docker images in split stages',
                          action='store_true')
        self.add_argument('-t', '--tag',
                          help ='tag name of docker images to build',
                          type = str,
                          default = 'docker4dev:latest')
        return self.parse_args()
