import worker
from checker import *
from logger import logger

def main(argv):
    param_json = arg_parser(argv)
    input_files, output_folder, rotated_file_size, need_to_be_archived = param_checker(param_json)
    for input_file in input_files:
        worker.rotate_file(input_file,
                           output_folder,
                           rotated_file_size,
                           need_to_be_archived)


if __name__ == '__main__':
    main(sys.argv[1:])
