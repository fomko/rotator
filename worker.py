import shutil
import gzip
import os
import re
from logger import logger


def rotate_file(input_file,
                output_folder,
                rotated_file_size,
                need_to_be_archived=False):

    if rotated_file_size < 1024*1024:
        buffer_size = rotated_file_size
    else:
        buffer_size = 1024*1024
    chunk = str()  # initial chunk
    output_pattern = re.split("\.(\d|\w)+$", input_file)[0]
    writer = Writer(output_pattern,
                    output_folder,
                    rotated_file_size)
    with open(input_file, 'r') as fr:
        while True:
            string_buffer = fr.readline()
            if string_buffer:
                chunk_len = len(chunk)
                if chunk_len < buffer_size:
                    chunk += string_buffer
                else:
                    logger.debug("Chunk size = {}. "
                                 "Writing it in file".format(chunk_len))
                    writer.add_to_file(chunk, need_to_be_archived)
                    chunk = ""
            else:
                logger.debug("Chunk size = {}. "
                             "Writing it in file. "
                             "It's a last string!".format(chunk_len))
                writer.add_to_file(chunk, need_to_be_archived, last=True)
                break


class Writer:
    log_number = 1
    current_file_size = 0

    def __init__(self, file_name_pattern, output_folder, file_size):
        self.log_name_pattern = file_name_pattern
        self.file_size = file_size
        self.output_folder = output_folder
        logger.debug("file_size = {}".format(self.file_size))
        check_and_create_output_folder(self.output_folder)

    @property
    def log_path(self):
        return "{}/{}_{}.log".format(self.output_folder,
                                     self.log_name_pattern,
                                     self.log_number)

    @property
    def archive_path(self):
        return "{}/{}_{}.gz".format(self.output_folder,
                                    self.log_name_pattern,
                                    self.log_number)

    def add_to_file(self, content, archived=False, last=False):
        content_len = len(content)
        self.current_file_size += content_len
        logger.debug("current_file_size = {}".format(self.current_file_size))
        if self.current_file_size > self.file_size:
            write_to_file(self.log_path, content)
            if archived:
                archive_file(self.log_path, self.archive_path)
            self.log_number += 1
            self.current_file_size = 0
        else:
            write_to_file(self.log_path, content)
            if last:
                archive_file(self.log_path, self.archive_path)


def check_and_create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)


def write_to_file(file_path, content):
    with open(file_path, 'a') as fw:
        logger.debug('writing in file: {} '.format(file_path))
        fw.write(content)


def archive_file(source_file_path, archived_file_path):
    with open(source_file_path, 'rb') as source_file:
        with gzip.open(archived_file_path, 'wb') as archived_file:
            shutil.copyfileobj(source_file, archived_file)
    os.remove(source_file_path)


