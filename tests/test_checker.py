import os
import shutil
import pytest
from .. import checker
from unittest import mock

@pytest.mark.parametrize('param', [
    {   # param0
        'file_size': "10GE"
    },
    {   # param1
        'file_size': 10.12
    }
])
def test_invalid_check_rotated_file_size_param(param):
    file_size = param['file_size']
    with pytest.raises(SystemExit):
        checker.check_rotated_file_size_param(file_size)


@pytest.mark.parametrize("param", [
    {   # param0
        'file_size': "10MB",
        'expected': 10485760
    },
    {   # param1
        'file_size': 100000,
        'expected': 100000
    }
])
def test_valid_check_rotated_file_size_param(param):
    file_size = param['file_size']
    expected = param['expected']
    assert checker.check_rotated_file_size_param(file_size) == expected

# test with mock
@mock.patch("os.path")
def test_valid_file_check_input_param(mock_os):
    mock_os.exist.return_value = True
    mock_os.isfile.return_value = True
    mock_os.isdir.return_value = False
    mock_os.abspath.return_value = "blabla"
    assert checker.check_input_param("blabla") == ["blabla"]


# test with real file system!
@pytest.fixture
def make_files_for_test():
    os.mkdir("temp")
    log_path = "temp/test1.log"
    with open(log_path, 'x') as t:
        t.write("123")
    yield make_files_for_test
    shutil.rmtree("temp")


def test_valid_dir_check_input_param(make_files_for_test):
    expected = [os.path.join(os.getcwd(), "temp", "test1.log")]
    assert checker.check_input_param("temp") == expected
