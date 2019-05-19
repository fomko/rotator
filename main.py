import os
import logging
import worker
from checker import args_parsing, param_checker


def logger_initializing(logging_level):
    _logger = logging.getLogger("rotator")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)
    _logger.setLevel(getattr(logging, logging_level.upper()))
    return _logger


def main():
    param_json = args_parsing()["config"]
    logging_level = args_parsing().get("logginglevel")
    if logging_level:
        logger = logger_initializing(logging_level)
    else:
        logger = logger_initializing("INFO")

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

        logger.info(f"File {input_file} has been rotated!")


if __name__ == '__main__':
    main()

