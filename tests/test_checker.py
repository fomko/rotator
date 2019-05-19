import pytest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from checker import check_rotated_file_size_param


@pytest.mark.parametrize('param', [
    {   #param0
        'file_size': "10GE"
    },
    {   #param1
        'file_size': 10.12
    }
])
def test_invalid_check_rotated_file_size_param(param):
    file_size = param['file_size']
    with pytest.raises(SystemExit):
        check_rotated_file_size_param(file_size)


@pytest.mark.parametrize("param", [
    {   #param0
        'file_size': "10MB",
        'expected': 10485760
    },
    {   #param1
        'file_size': 100000,
        'expected': 100000
    }
])
def test_valid_check_rotated_file_size_param(param):
    file_size = param['file_size']
    expected = param['expected']
    assert check_rotated_file_size_param(file_size) == expected
