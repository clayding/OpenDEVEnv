import options
import getopt
import utils
import base

def parse_options(argv):
    exename = argv[0]
    dockpath= utils.os_get_rel_path('../')
    ab = Assembler(dockpath)
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
    #parse_options(utils.sys_get_allargs())
    try:
        config = base.BaseConfig()
        ret = config.setup()
    except Exception as esc:
        ret = 1
        import traceback
        traceback.print_exc()

