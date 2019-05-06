import worker
import sys
from checker import arg_parser, param_checker
from logger import logger


def main(argv):
    param_json = arg_parser(argv)
    param_dict = param_checker(param_json)
    input_files = param_dict["input_files"]
    output_folder = param_dict["output_folder"]
    rotated_file_size = param_dict["rotated_file_size"]
    need_to_be_archived = param_dict["need_to_be_archived"]
    for input_file in input_files:
        logger.info(f'Rotating file {input_file}')
        worker.rotate_file(input_file,
                           output_folder,
                           rotated_file_size,
                           need_to_be_archived)
        logger.info("Done!")


if __name__ == '__main__':
    main(sys.argv[1:])
