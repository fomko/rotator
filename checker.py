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
    log_files = check_file_path_param(param_json["file_path"])
    log_file_size = check_log_file_size_param(param_json["log_file_size"])
    archive = param_json["archive"]
    if log_files and log_file_size:
        return log_files, log_file_size, archive


def check_file_path_param(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            log_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        elif os.path.isfile(path):
            log_files = [path]
        else:
            raise TypeError("Unsupported file type")
        return log_files
    else:
        print("No files for rotation has been found. Nothing to do")


def check_log_file_size_param(log_file_size):
    if type(int(convert_size_to_bytes(str(log_file_size)))) is int:
        return int(convert_size_to_bytes(str(log_file_size)))


def arg_parser(args):
    for arg in args:
        if ".json" in arg:
            return arg
    print("helper is here!")
    sys.exit()
