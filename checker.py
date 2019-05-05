import json
import os
from convertor import convert_size_to_bytes
import sys


def param_checker(param_json_path):
    try:
        with open(param_json_path, 'r') as jr:
            param_json = json.load(jr)
    except FileNotFoundError:
        raise FileNotFoundError("No file with params has been found.")
    except ValueError:
        raise ValueError("Invalid Json file!")
    input_files = check_input_param(param_json["Input"])
    output_folder = param_json["Output"]
    rotated_file_size = check_rotated_file_size_param(param_json["RotatedFileSize"])
    need_to_be_archived = param_json["NeedToBeArchived"]
    if input_files and rotated_file_size and output_folder:
        return input_files, output_folder, rotated_file_size, need_to_be_archived


def check_input_param(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        elif os.path.isfile(path):
            files = [path]
        else:
            raise TypeError("Unsupported file type")
        return files
    else:
        print("No files for rotation has been found. "
              "Nothing to do")


def check_output_param(path):
    pass


def check_rotated_file_size_param(file_size):
    try:
        if type(int(convert_size_to_bytes(str(file_size)))) is int:
            return int(convert_size_to_bytes(str(file_size)))
    except ValueError:
        raise ValueError("Invalid RotatedFileSize param. "
                         "Should be like 12gb(mb/kb) or an integer")


def arg_parser(args):
    for arg in args:
        if ".json" in arg:
            return arg
    print("helper is here!")
    sys.exit()
