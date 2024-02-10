from intellifs import FileSystem
from intellifs.indexables import File

ifs_instance = FileSystem()

def test_index_file():
    file = File(__file__)
    assert ifs_instance.index(file) is None

def test_index_file():
    directory = File(__file__).directory & '..' 
    assert ifs_instance.index(directory) is None

def test_is_indexed():
    file = File(__file__)
    assert ifs_instance.is_indexed(file) is True

def test_search():
    directory = File(__file__).directory
    assert ifs_instance.search(
        query="Test If file is indexed.", directory=directory
    )