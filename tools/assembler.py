from jinja2 import Template
from yaml import safe_load
import shutil
import time
import utils

class Assembler(object):
    def __init__(self, dockfiles_path):
        self.devtool = 'Dockerfiles/Dockerfile.devtool'
        self.kerneld = 'Dockerfiles/Dockerfile.kerneldev'
        self.dependf = 'Dockerfiles/Dockerfile.dependency'
        self.current = dockfiles_path
        self.dt_path = utils.os_concat_path(self.current, self.devtool)
        self.kd_path = utils.os_concat_path(self.current, self.kerneld)
        self.dp_path = utils.os_concat_path(self.current, self.dependf)
        self.dockerf = utils.os_concat_path(self.current, 'Dockerfile')
        self.tempdir = utils.os_concat_path(self.current, 'Dockerfiles/temp')
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

        distinfo = utils.platform_dist()
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
        dirname = utils.os_get_abs_dirname(path)
        dirname = dirname.strip().rstrip('/')
        isexist = utils.os_is_path_exist(dirname)
        if not isexist:
            os.makedirs(dirname)
            print('Create new directory:{}' .format(dirname))
        return dirname
    
    def create_link(self, path):
        rootpath = self.dockerf
        if utils.os_is_path_exist(rootpath):
            utils.os_sym_link(None, rootpath)

        if utils.os_is_path_exist(path):
            utils.os_sym_link(path, rootpath)
            print('Create new symbol link to:{}' .format(path))
    
    def clean(self):
        rootpath = self.dockerf
        isexist = utils.os_is_path_exist(rootpath)
        if isexist:
            utils.os_sym_link(None, rootpath)
            #os.remove(rootpath)
            print('Deleted symbol link:{}' .format(rootpath))

        dirname = self.tempdir
        isexist = utils.os_is_path_exist(dirname)
        if isexist:
            shutil.rmtree(dirname)
            print('Deleted temporary folder:{}' .format(dirname))

    def generate_kernel(self):
        newfile =  self.tempdir + '/Dockerfile.' + str(int(time.time()))
        newpath = utils.os_concat_path(self.current, newfile)
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
        yamlvars = self.read_yaml(self.dp_path)
        distinfo = yamlvars[dist]
        if distinfo:
            return distinfo['version']
        else:
            print("Not support {}" .format(dist))
            return None
    
    def get_dist_dependency(self, dist):
        yamlvars = self.read_yaml(self.dp_path)
        distinfo = yamlvars[dist]
        if distinfo:
            return distinfo['dependency']
        else:
            print("Not support {}" .format(dist))
            return None

    def list_dist(self):
        yamlvars = self.read_yaml(self.dp_path)
        print('List suported distributions: ', end = '')
        for key in yamlvars:
            print('{} ' .format(key), end = '')
        print('')
        print('Current platform distribution: {}' .format(utils.platform_dist()))
