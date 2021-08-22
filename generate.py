from jinja2 import Template
from yaml import safe_load
import os
import shutil
import time
import sys
import getopt
import platform

class Assembler(object):
    def __init__(self):
        self.devtool = 'Dockerfiles/Dockerfile.devtool'
        self.kerneld = 'Dockerfiles/Dockerfile.kerneldev'
        self.dependf = 'Dockerfiles/Dockerfile.dependency'
        self.current = os.getcwd()
        self.dt_path = os.path.join(self.current, self.devtool)
        self.kd_path = os.path.join(self.current, self.kerneld)
        self.dockerf = os.path.join(self.current, 'Dockerfile')
        self.tempdir = os.path.join(self.current, 'Dockerfiles/temp')
        self.readbuf = ''
        self.writbuf = ''
        self.signatu = 'clayding <gdskclay@gmail.com>'


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

        distinfo = platform.dist()
        print(self.get_dist_version(distinfo[0]))
        base_ver = distinfo[0] + ':' + str(self.get_dist_version(distinfo[0]))
        base_dep = self.get_dist_dependency(distinfo[0])

        template= Template(dstbuff)
        content = template.render(DOCKERFILE_DEVTOOL=srcbuff,
                                  DOCKERFILE_OS_VERSION=base_ver,
                                  DOCKERFILE_DEPENDENCIES=base_dep,
                                  DOCKERFILE_MAINTAINER=self.signatu)
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
        if os.path.exists(rootpath):
            os.unlink(rootpath)

        if os.path.exists(path):
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

    def read_yaml(self, filename):
        with open(filename, 'r') as f:
            buffer = f.read()
        f.close()
        vars = safe_load(buffer)
        return vars

    def get_dist_version(self, dist):
        yamlvars = self.read_yaml(self.dependf)
        distinfo = yamlvars[dist]
        if distinfo:
            return distinfo['version']
        else:
            print("Not support {}" .format(dist))
            return NULL
    
    def get_dist_dependency(self, dist):
        yamlvars = self.read_yaml(self.dependf)
        distinfo = yamlvars[dist]
        if distinfo:
            return distinfo['dependency']
        else:
            print("Not support {}" .format(dist))
            return NULL

    def list_dist(self):
        yamlvars = self.read_yaml(self.dependf)
        print('List suported distributions: ', end = '')
        for key in yamlvars:
            print('{} ' .format(key), end = '')
        print('')
        print('Current platform distribution: {}' .format(platform.dist()))

def parse_options(argv):
    exename = argv[0]
    ab = Assembler()
    ab.list_dist();
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
