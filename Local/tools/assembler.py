from jinja2 import Template
from yaml import safe_load
import shutil
import time
import utils

##############################################ADD NEW HERE##############################################################
global_dfdict = {"devtool":'Dockerfiles/Dockerfile.devtool',        "kernel":'Dockerfiles/Dockerfile.kerneldev',
                 "dependency":'Dockerfiles/Dockerfile.dependency',  "beauty":'Dockerfiles/Dockerfile.beauty',
                 "base":'Dockerfiles/Dockerfile.base',              "lede":'Dockerfiles/Dockerfile.lede'
                }
########################################################################################################################

class Assembler(object):
    def __init__(self, dockfiles_path, http_proxy, checkfilelist):
        self.current = dockfiles_path
        self.filelist = checkfilelist
        self.dockerf = utils.os_concat_path(self.current, 'Dockerfile')
        self.tempdir = utils.os_concat_path(self.current, 'Dockerfiles/temp')
        self.signatu = 'clayding <gdskclay@gmail.com>'
        self.proxycf = http_proxy

    def find_dockerfile_path(self, key):
        for k, v in global_dfdict.items():
            if k == key:
                file_path = utils.os_concat_path(self.current, v)
                self.filelist.append(file_path)
                return file_path
        print('Not found the pair to key:{}' .format(key))
        return ""

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

    def _assmble_render(self, dst, render_dict):
        '''Remove NULL value'''
        for key in list(render_dict.keys()):
            if not render_dict[key]:
                render_dict.pop(key)

        template= Template(dst)
        content = template.render(render_dict)

        return content

    def assemble_base(self):
        devbuff = self.read(self.find_dockerfile_path("devtool")) # devtool path
        mbebuff = self.read(self.find_dockerfile_path("beauty")) # beauty path
        dstbuff = self.read(self.find_dockerfile_path("base")) # base path

        base_ver = str(self.get_dist_dependency("", "distribution")) + \
                ':' + str(self.get_dist_dependency("", "version"))
        src_list = str(self.get_dist_dependency("", "sourcelist"))
        if src_list:
            base_dep = src_list + " && \ \n"
        else:
            base_dep = str()
        base_dep += self.get_dist_dependency("", "dependency")

        render_dict = dict(DOCKERFILE_DEVTOOL=devbuff,
                           DOCKERFILE_BEAUTY=mbebuff,
                           DOCKERFILE_OS_VERSION=base_ver,
                           DOCKERFILE_HTTP_PROXY=self.proxycf,
                           DOCKERFILE_DEPENDENCIES=base_dep,
                           DOCKERFILE_MAINTAINER=self.signatu)

        return  self._assmble_render(dstbuff, render_dict)

    def assemble(self, desc, new):
        basebuffer = self.assemble_base()
        destbuffer = self.read(self.find_dockerfile_path(desc))

        if desc != "base":
            render_dict = dict(DOCKERFILE_BASE=basebuffer)
##############################################ADD NEW HERE##############################################################
            # For kernel development
            if desc == "kernel":
                kernel_dep = self.get_dist_dependency("", "kernel_depend")
                render_dict['DOCKERFILE_KERNEL_DEP'] = kernel_dep
            # For lede development
            if desc == "lede":
                lede_dep = self.get_dist_dependency("", "lede_depend")
                render_dict['DOCKERFILE_LEDE_DEP'] = lede_dep
########################################################################################################################

            content = self._assmble_render(destbuffer, render_dict)
        else:
            content = basebuffer

        self.write(new, content)

    def check_dir(self, path):
        dirname = utils.os_get_abs_dirname(path)
        dirname = dirname.strip().rstrip('/')
        isexist = utils.os_is_path_exist(dirname)
        if not isexist:
            utils.os_makedirs(dirname)
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

    def _generate_dockerfile(self, desc):
        newfile =  self.tempdir + '/Dockerfile.' + str(int(time.time()))
        newpath = utils.os_concat_path(self.current, newfile)
        self.check_dir(newpath)
        self.assemble(desc, newpath)
        self.create_link(newpath)

    def generate(self, desc):
        self._generate_dockerfile(desc)


    def read_yaml(self, filename):
        with open(filename, 'r') as f:
            buffer = f.read()
        f.close()
        vars = safe_load(buffer)
        return vars

    def get_dist_dependency(self, dist, key):
        disinfo_hdr = dist
        if not dist:
            distinfo = utils.platform_dist()
            if not distinfo:
                return
            disinfo_hdr=distinfo[0].lower()

        if key == "distribution":
            return disinfo_hdr

        yamlvars = self.read_yaml(self.find_dockerfile_path("dependency"))
        distinfo = yamlvars[disinfo_hdr]
        if distinfo:
            return distinfo[key]
        else:
            print("Not support {} key {}" .format(dist, key))
            return None

    def list_dist(self):
        yamlvars = self.read_yaml(self.find_dockerfile_path("dependency"))
        print('List suported distributions: ', end = '')
        for key in yamlvars:
            print('{} ' .format(key), end = '')
        print('')
        print('Current platform distribution: {}' .format(utils.platform_dist()))
