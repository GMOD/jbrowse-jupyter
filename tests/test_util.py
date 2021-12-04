import pytest
from jbrowse_jupyter.util import is_URL, guess_file_name,get_name

def test_is_url():
    # urls
    not_secure = "http://path/to/my/file"
    secure = "http://path/to/my/file"
    # local paths
    local = './this/is/a/local/path'
    assert is_URL(not_secure) == True
    assert is_URL(secure) == True
    assert is_URL(local) == False

def test_guess_file_name():
    url = "http://path/to/my/filename.gff"
    assert guess_file_name(url) == 'filename.gff'
