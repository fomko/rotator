import worker
from checker import *


def main(argv):
    param_json = arg_parser(argv)
    log_files, log_file_size, archive = param_checker(param_json)
    for log in log_files:
        worker.rotate_file(log, log_file_size, archive)


if __name__ == '__main__':
    main(sys.argv[1:])
