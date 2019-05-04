import shutil
import gzip
import logging
import os


def rotate_file(file_path, dest_file_size, is_archived=False):
    if dest_file_size < 1024*1024:
        buffer_size = dest_file_size
    else:
        buffer_size = 1024*1024
    chunk = str()  # initial chunk
    writer = Writer("test/log", dest_file_size)
    with open(file_path, 'r') as fr:
        while True:
            string_buffer = fr.readline()
            if string_buffer:
                chunk_len = len(chunk)
                if chunk_len < buffer_size:
                    chunk += string_buffer
                else:
                    logger.debug("Chunk size = {}. Writing it in file".format(chunk_len))
                    writer.add_to_file(chunk, is_archived)
                    chunk = ""
            else:
                logger.debug("Chunk size = {}. Writing it in file. It's a last string!".format(chunk_len))
                writer.add_to_file(chunk, is_archived, last=True)
                break


class Writer:
    log_number = 1
    current_file_size = 0

    def __init__(self, file_name_pattern, file_size):
        self.log_name_pattern = file_name_pattern
        self.file_size = file_size
        logger.debug("file_size = {}".format(self.file_size))

    @property
    def log_name(self):
        return "{}{}.log".format(self.log_name_pattern, self.log_number)

    def add_to_file(self, content, archived=False, last=False):
        content_len = len(content)
        self.current_file_size += content_len
        logger.debug("current_file_size = {}".format(self.current_file_size))
        if self.current_file_size > self.file_size:
            write_to_file(self.log_name, content)
            if archived:
                archive_file(self.log_name, "test/archive{}.gz".format(self.log_number))
            self.log_number += 1
            self.current_file_size = 0

        else:
            write_to_file(self.log_name, content)
            if last:
                archive_file(self.log_name, "test/archive{}.gz".format(self.log_number))



def write_to_file(file_path, content):
    with open(file_path, 'a') as fw:
        logger.debug('writing in file: {} '.format(file_path))
        fw.write(content)


def archive_file(source_file_path, archived_file_path):
    with open(source_file_path, 'rb') as source_file:
        with gzip.open(archived_file_path, 'wb') as archived_file:
            shutil.copyfileobj(source_file, archived_file)
    os.remove(source_file_path)


logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
