import os
import sys
import platform

def os_concat_path(path1, path2):
    return os.path.join(path1, path2)

def os_get_rel_path(path):
    return os_concat_path(os.getcwd(), path)

def os_get_abs_dirname(path):
    return os.path.abspath(os.path.dirname(path))

def os_is_path_exist(path):
    return os.path.exists(path)

def os_sym_link(src, dst):
    if src:
        os.symlink(src, dst)
    else:
        os.unlink(dst)

def sys_get_allargs():
    return sys.argv

def platform_dist():
    return platform.dist()