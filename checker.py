import json
import os
from convertor import convert_size_to_bytes
import sys
from logger import logger


def param_checker(param_json_path):
    try:
        logger.debug("Opening param json file")
        with open(param_json_path, 'r') as jr:
            param_json = json.load(jr)
    except FileNotFoundError:
        logger.error("No file with params has been found.")
    except ValueError:
        logger.error("Invalid Json file!")
    param_dict = dict()
    param_dict["input_files"] = check_input_param(param_json["Input"])
    logger.debug("Input files param: {}".format(param_dict["input_files"]))
    param_dict["output_folder"] = check_output_param(param_json["Output"])
    logger.debug("Output folder param: {}".format(param_dict["output_folder"]))
    param_dict["rotated_file_size"] = check_rotated_file_size_param(param_json["RotatedFileSize"])
    logger.debug("Rotated file size param: {}".format(param_dict["rotated_file_size"]))
    need_to_be_archived = param_json.get("NeedToBeArchived")
    param_dict["need_to_be_archived"] =  need_to_be_archived if need_to_be_archived is True else False
    logger.debug("Need to be archived param: {}".format(param_dict["need_to_be_archived"]))
    if param_dict["input_files"] and \
       param_dict["output_folder"] and \
       param_dict["rotated_file_size"]:
        return param_dict


def check_input_param(path):
    files_list = list()
    if os.path.exists(path):
        if os.path.isdir(path):
            for root, dirs, files in os.walk(os.path.abspath(path)):
                for file in files:
                    files_list.append(os.path.join(root, file))
        elif os.path.isfile(path):
            files_list = os.path.abspath(path)
        else:
            logger.error("Unsupported file type")
            sys.exit(1)
        return files_list
    else:
        logger.warning("No files for rotation has been found. "
                       "Nothing to do")
        sys.exit(1)


def check_output_param(path):
    return os.path.abspath(path)


def check_rotated_file_size_param(file_size):
    try:
        if type(int(convert_size_to_bytes(str(file_size)))) is int:
            return int(convert_size_to_bytes(str(file_size)))
    except ValueError:
        logger.error("Invalid RotatedFileSize param. "
                     "Should be like 12gb(mb/kb) or an integer")
        sys.exit(1)


def arg_parser(args):
    for arg in args:
        if ".json" in arg:
            return arg
    print("helper is here!")
    sys.exit()
