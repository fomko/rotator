import os
import logging
from logger import logger
import worker
from checker import args_parsing, param_checker




def main():
    param_json = args_parsing()["config"]
    param_dict = param_checker(param_json)
    input_files = param_dict["input_files"]
    output_folder = param_dict["output_folder"]
    rotated_file_size = param_dict["rotated_file_size"]
    need_to_be_archived = param_dict["need_to_be_archived"]
    for input_file in input_files:
        logger.info(f'Rotating file {input_file}')
        input_file = worker.recreate_file(input_file)
        worker.rotate_file(input_file,
                           output_folder,
                           rotated_file_size,
                           need_to_be_archived)
        logger.info("Done!")
        os.remove(input_file)


if __name__ == '__main__':
    # Define logging level here. Will be moved in config file some day!
    logger.setLevel(logging.INFO)
    main()

