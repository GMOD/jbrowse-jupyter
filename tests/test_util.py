from jbrowse_jupyter.util import is_url, guess_file_name


def test_is_url():
    # urls
    not_secure = "http://path/to/my/file"
    secure = "http://path/to/my/file"
    # local paths
    local = './this/is/a/local/path'
    assert is_url(not_secure)
    assert is_url(secure)
    assert not is_url(local)


def test_guess_file_name():
    url = "http://path/to/my/filename.gff"
    assert guess_file_name(url) == 'filename.gff'
