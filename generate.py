import jinja2
from jinja2 import Template
import os
import shutil
import time

class Assembler(object):
    def __init__(self):
        self.devtool = 'Dockerfiles/Dockerfile.devtool'
        self.kerneld = 'Dockerfiles/Dockerfile.kerneldev'
        self.current = os.getcwd()
        self.dt_path = os.path.join(self.current, self.devtool)
        self.kd_path = os.path.join(self.current, self.kerneld)
        self.dockerf = os.path.join(self.current, 'Dockerfile')
        self.tempdir = os.path.join(self.current, 'Dockerfiles/temp')
        self.readbuf = ''
        self.writbuf = ''


    def read(self, file):
        buffer=''
        with open(file, 'r+') as f:
            buffer=f.read()
        f.close()
        return buffer
    
    def write(self, file, buffer):
        with open(file, 'w+') as f:
            f.write(buffer)
        f.close()

    def assemble(self, src, dst, new):
        srcbuff = self.read(src)
        dstbuff = self.read(dst)
        template= Template(dstbuff)
        content = template.render(DOCKFILE_DEVTOOL=srcbuff)
        #print(content)

        self.write(new, content)
    
    def check_dir(self, path):
        dirname = os.path.abspath(os.path.dirname(path))
        dirname = dirname.strip().rstrip('/')
        isexist = os.path.exists(dirname)
        if not isexist:
            os.makedirs(dirname)
            print('Create new directory:{}' .format(dirname))
        return dirname
    
    def create_link(self, path):
        rootpath = self.dockerf
        isexist = os.path.exists(rootpath)
        if isexist:
            os.unlink(rootpath)
        os.symlink(path, rootpath)
        print('Create new symbol link to:{}' .format(path))
    
    def clean(self):
        rootpath = self.dockerf
        isexist = os.path.exists(rootpath)
        if isexist:
            os.unlink(rootpath)
            #os.remove(rootpath)
            print('Deleted symbol link:{}' .format(rootpath))

        dirname = self.tempdir
        isexist = os.path.exists(dirname)
        if isexist:
            shutil.rmtree(dirname)
            print('Deleted temporary folder:{}' .format(dirname))

    def generate_kernel(self):
        newfile =  self.tempdir + '/Dockerfile.' + str(int(time.time()))
        newpath = os.path.join(self.current, newfile)
        self.check_dir(newpath)
        self.assemble(self.dt_path, self.kd_path, newpath)
        self.create_link(newpath)

import sys, getopt

def parse_options(argv):
    exename = argv[0]
    ab = Assembler()
    try:
        opts, args = getopt.getopt(argv[1:], "hck", ["kernel=", "clean="])
    except getopt.GetoptError:
        print ('{} [-h]<-k/-c>' .format(exename))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('{} [-h]<-k/-c>' .format(exename))
            sys.exit()
        elif opt in ("-k", "--kernel"):
            ab.generate_kernel()
        elif opt in ("-c", "--clean"):
           ab.clean()

if __name__ == "__main__":
    parse_options(sys.argv)
