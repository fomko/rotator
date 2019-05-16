import json
import os
import sys
import re
import argparse
from logger import logger


def param_checker(param_json_path):
    try:
        logger.debug("Opening param json file")
        with open(param_json_path, 'r') as jr:
            param_json = json.load(jr)
    except FileNotFoundError:
        logger.error("No file with params has been found.")
        sys.exit(1)
    except ValueError:
        logger.error("Invalid Json file!")
        sys.exit(1)
    param = {}
    param["input_files"] = check_input_param(param_json["Input"])
    logger.debug(f'Input files param: {param["input_files"]}')

    param["output_folder"] = check_output_param(param_json["Output"])
    logger.debug(f'Output folder param: {param["output_folder"]}')

    param["rotated_file_size"] = check_rotated_file_size_param(param_json["RotatedFileSize"])
    logger.debug(f'Rotated file size param: {param["rotated_file_size"]}')

    need_to_be_archived = param_json.get("NeedToBeArchived")
    param["need_to_be_archived"] = need_to_be_archived or False

    logger.debug(f'Need to be archived param: {param["need_to_be_archived"]}"')
    if param["input_files"] and param["output_folder"] and param["rotated_file_size"]:
        return param


def check_input_param(path):
    if not os.path.exists(path):
        logger.warning('No files for rotation has been found. Nothing to do')
        sys.exit(1)

    files_list = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(os.path.abspath(path)):
            for file in files:
                files_list.append(os.path.join(root, file))
    elif os.path.isfile(path):
        files_list = os.path.abspath(path)
    else:
        logger.error('Unsupported file type')
        sys.exit(1)

    return files_list


def check_output_param(path):
    return os.path.abspath(path)


def check_rotated_file_size_param(file_size):
    try:
        file_size = str(file_size)
        result = int(convert_size_to_bytes(file_size))
        return result
    except ValueError:
        logger.error('Invalid RotatedFileSize param. Should be like 12gb(mb/kb) or an integer')
        sys.exit(1)


def convert_size_to_bytes(size):
    suffixes = "", "k", "m", "g", "t"
    multipliers = {f'{l}b': 1024 ** i for i, l in enumerate(suffixes)}
    sre = re.compile("(\d+)({})".format("|".join(x + "b" for x in suffixes)), re.IGNORECASE)

    def subfunc(m):
        return str(int(m.group(1)) * multipliers[m.group(2).lower()])

    return sre.sub(subfunc, size)


def args_parsing():
    args_parser = argparse.ArgumentParser(description='Rotator rotates files!')
    args_parser.add_argument('-c', '--config', type=str, metavar='',
                             required=True, help='Path to json with params')
    args = args_parser.parse_args()

    return vars(args)
