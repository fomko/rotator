import shutil
import gzip
import os
import re
from logger import logger


def rotate_file(input_file_path,
                output_folder_path,
                rotated_file_size,
                need_to_be_archived=False):

    if rotated_file_size < 1024*1024:
        buffer_size = rotated_file_size
    else:
        buffer_size = 1024*1024
    logger.debug("buffer_size = {}".format(buffer_size))
    chunk = str()  # initial chunk
    input_file_name = os.path.basename(input_file_path)
    output_pattern = os.path.splitext(input_file_name)[0]
    writer = Writer(output_pattern,
                    output_folder_path,
                    rotated_file_size)
    with open(input_file_path, 'r') as fr:
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
                             "Writing it in file.".format(chunk_len))
                writer.add_to_file(chunk, need_to_be_archived, last=True)
                break


class Writer:
    log_number = 1
    current_file_size = 0

    def __init__(self, file_name_pattern, output_folder, file_size):
        self.log_name_pattern = file_name_pattern
        self.file_size = file_size
        self.output_folder = output_folder
        check_and_create_output_folder(self.output_folder)

    @property
    def log_path(self):
        filename = "{}_{}.log".format(self.log_name_pattern,
                                      self.log_number)
        return os.path.join(self.output_folder,
                            filename)

    @property
    def archive_path(self):
        filename = "{}_{}.gz".format(self.archive_path,
                                     self.log_number)
        return os.path.join(self.output_folder,
                            filename)

    def add_to_file(self, content, archived=False, last=False):
        content_len = len(content)
        self.current_file_size += content_len
        if self.current_file_size > self.file_size:
            write_to_file(self.log_path, content)
            if archived:
                archive_file(self.log_path, self.archive_path)
            self.log_number += 1
            self.current_file_size = 0
        else:
            write_to_file(self.log_path, content)
            if last and archived:
                archive_file(self.log_path, self.archive_path)


def check_and_create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        logger.info("Output folder {} doesn't exist. "
                    "Creating...".format(output_folder))
        os.mkdir(output_folder)
    else:
        logger.debug("Output folder already exist.")


def write_to_file(file_path, content):
    with open(file_path, 'a') as fw:
        logger.debug('Writing in file: {} '.format(file_path))
        fw.write(content)


def archive_file(source_file_path, archived_file_path):
    logger.debug("Archiving file {} to {}".format(source_file_path,
                                                  archived_file_path))
    with open(source_file_path, 'rb') as source_file:
        with gzip.open(archived_file_path, 'wb') as archived_file:
            logger.debug("Creating archive {}".format(archived_file_path))
            shutil.copyfileobj(source_file, archived_file)
    logger.debug("Deleting {}".format(source_file_path))
    os.remove(source_file_path)


