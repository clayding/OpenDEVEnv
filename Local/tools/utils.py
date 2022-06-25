import os
import sys
import platform
import distro

def os_concat_path(path1, path2):
    return os.path.join(path1, path2)

def os_get_rel_path(path):
    return os_concat_path(os.getcwd(), path)

def os_get_abs_path(path):
    return os.path.abspath(path)

def os_get_abs_dirname(path):
    return os.path.abspath(os.path.dirname(path))

def os_is_path_exist(path):
    return os.path.exists(path)

def os_sym_link(src, dst):
    if src:
        os.symlink(src, dst)
    else:
        os.unlink(dst)

def os_makedirs(dirname):
    return os.makedirs(dirname)

def sys_get_allargs():
    return sys.argv

def platform_dist():
    pversion=platform.python_version().split('.')
    ''' 3.8.1 '''
    if pversion[0] == '3':
        '''python version < 3.8'''
        if int(pversion[1]) < 8:
            return platform.dist()
        else:
            return distro.linux_distribution()
    else:
        print("platform.dist not supported")
