
import os
import re
import subprocess
import time
import logger
import options
import assembler

class BaseConfig(object):
    def __init__(self):
        # Any change in the listed items will triger a rebuild
        self.checkfilelist = "Dockerfile"
        self.checkvarslist = ''
        self.logger = logger.Logger()
        self.option = options.OptionsParser().default_options()
    
    def set_vars(self):
        self.buildpath = self.option.buildir
        if not self.buildpath:
            self.buildpath = os.path.dirname(os.path.abspath(__file__))

        self.buildstag = self.option.stage
        print(self.buildstag)
        self.imagename = self.option.tag
        if self.buildstag:
            self.imagename = '-s %s' % self.imagename
        else:
            self.imagename = '-t %s' % self.imagename

        self.hostname  = self.option.name
        self.mountdir  = self.option.mount
        print(self.mountdir)
        self.apcommand = self.option.command
        print(os.readlink(__file__))
        print(os.path.join("tools", "bash.h"))

        """ try:
            if os.readlink(__file__) != os.path.join("tools", "bash.h"):
                raise OSError("The link target does not exist.")
        except OSError:
            self.logger.error("setup script must be run in the top directory. (not in this docker directory)")
            exit(1) """
    
    def generate_dockerfile(self, dockerfile_path):
        self.assemb = assembler.Assembler(dockerfile_path)

    def _is_file_newer(self, file, timestamp):
        """
        Check if the file modify time newer than the timestamp
        """

        return True if os.stat(file).st_mtime > timestamp else False

    def check_docker(self):
        """
        Check if docker binary exists in PATH and its version
        is higher than 1.0
        """

        # Check docker binary
        dockerbin=""
        for p in os.getenv('PATH').split(':'):
            candidate = os.path.join(p, 'docker')
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                dockerbin = candidate
                if not os.path.isabs(dockerbin):
                    dockerbin = os.path.abspath(dockerbin)
                # Found the first executable docker
                break
        if not dockerbin:
            self.logger.error("Can not find docker in PATH. you must have docker installed!")
            exit(1)

        # Check docker version
        dockerver = subprocess.check_output("%s --version" % dockerbin, shell = True)
        dockerver = re.match("^.*([0-9][0-9]+\.[0-9]+\.[0-9]+).*$", dockerver.decode()).group(1)
        if int(dockerver.split('.')[0]) < 1:
            self.logger.error("docker version must be higher than 1.0, current is %s" % dockerver)
            exit(1)

    def build_image(self):
        """
        Build builder image if it does not exist, or compare its
        '.Created' information with the 'Modify' timestamp of all files
        in checkfilelist, and rebuild the image if any of the timestamp
        is later than image 'Created' time.
        """

        self.set_vars()
        
        rebuild = False
        nocache = "false"
        try:
            """ Get build timestamp """
            output = subprocess.check_output( \
                "docker inspect --format={{.Created}} builder:uml 2>/dev/null", \
                shell = True)
            m = re.match(r'(^[0-9]{4}-[0-9]{2}-[0-9]{2})[a-zA-Z ]{1}([0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}).*$', output)
            created = time.mktime(time.strptime('%s %s' % (m.group(1), m.group(2)), '%Y-%m-%d %H:%M:%S.%f'))

            # Check file 'Modify' timestamp of checkfilelist
            for l in self.checkfilelist.split():
                p = "%s/%s" % self.buildpath % l
                if os.path.isdir(p):
                    for root, _, files in os.walk(p):
                        for f in files:
                            file = os.path.join(root, f)
                            if self._is_file_newer(file, created):
                                rebuild = True
                                break
                elif os.path.isfile(p):
                    if self._is_file_newer(p, created):
                        rebuild = True
                        break

            # Check variable changes of checkvarslist
            data = ""
            for v in self.checkvarslist.split():
                data += str(eval("self.%s" % v)).strip()
            datahash = hashlib.md5(data.encode("utf-8")).hexdigest()
            try:
                if open(".sigdata", 'r').read() != datahash:
                    rebuild = True
                    nocache = "true"
            except IOError:
                rebuild = True
                nocache = "true"
            finally:
                open(".sigdata", 'w').write(datahash)

        except subprocess.CalledProcessError:
            rebuild = True

        if rebuild:
            cmd = "cd %s; docker build --no-cache=%s %s ./" \
                % (self.buildpath, nocache, self.imagename)
            self.logger.note("Building docker builder image... (This may take some time.)")
            print(cmd)
            #subprocess.check_output(cmd, shell = True)

    def start_image(self):
        """
        Start the builder image in docker
        """

        psedottyargs = "" if self.apcommand else "-t"
        cmd = "docker run --privileged=true --rm -h %s -e DISPLAY=:0 -i %s \
            -v %s/.ssh:/root/.ssh \
            -v /etc/localtime:/etc/localtime \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v /dev:/dev \
            %s %s" \
            % (self.hostname, psedottyargs, \
            os.getenv("HOME"), self.mountdir, self.apcommand)
        self.logger.note("Running build machine...")
        print(cmd)
        #return subprocess.call(cmd, shell = True)

    def setup(self):
        self.check_docker()
        self.build_image()
        return self.start_image()