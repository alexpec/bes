from Utils.REParser import REParser
import pytest
from Utils.TerminalBuffer import TerminalBuffer
import os

@pytest.fixture(scope='module')
def create_temporary_folder(tmpdir_factory):
    fn = tmpdir_factory.mktemp('tmp_data')
    
    return fn


@pytest.fixture
def text():
    txt = '''
    This is a test for regular expressions!
    
    WARNING: This is warning number 1;
    WARNING: This is warning number 2;
    INFO: This is only an information;
    WARNING: Trying again, warning number 3;
    INFO: The sky is blue!;
    WARNING: Uhuuu new test, warning number 4;
    INFO: Lottery numbers for this evening 22 35 56 11 05 03;
    ERROR: Halting the production!
    '''
    
    return txt


@pytest.fixture
def re_parser():
    re_parser = REParser()
    
    re_parser.AddPattern(
        'Warning', 
        '\s*WARNING:\s*(.*)', 
        _readWarning
    )
    
    re_parser.AddPattern(
        'Info',
        '\s*INFO:\s*(.*)',
        _readInfo
    )
    
    re_parser.AddPattern(
        'Error',
        '\s*ERROR:\s*(.*)',
        _readError
    )
    
    return re_parser
    


def _readWarning(match, lines, index):
    return match.group(1)
    
def _readInfo(match, lines, index):
    return match.group(1)

def _readError(match, lines, index):
    return match.group(1)


def _assertResults(results):
    infos_ex = [
        'This is only an information;',
        'The sky is blue!;',
        'Lottery numbers for this evening 22 35 56 11 05 03;' 
    ]
    
    warnings_ex = [
        'This is warning number 1;',
        'This is warning number 2;',
        'Trying again, warning number 3;',
        'Uhuuu new test, warning number 4;'
    ]
    
    errors_ex = [
        'Halting the production!'
    ]
    
    
    for info in infos_ex:
        assert info in results['Info']
        
    for warn in warnings_ex:
        assert warn in results['Warning']
        
    for error in errors_ex:
        assert error in results['Error']


def test_ReParser_File(text, re_parser, create_temporary_folder):
    temp_folder = str(create_temporary_folder)
    temp_file = os.path.join(temp_folder, 'data')
    
    file = open(temp_file, 'w')
    file.write(text)
    file.close()
    
    results = re_parser.ParseFile(temp_file)
    _assertResults(results)
    
    
    

def test_ReParser_Buffer():
    term_buff = TerminalBuffer()
     
    data = text()
    data.strip()
    data = data.split('\n')
     
    for line in data:
        term_buff.AddLine(line)
        
    term_buff.is_closed = True
     
    results = re_parser().ParseBuffer(term_buff)
     
    _assertResults(results)
    


def test_REParser_String(text, re_parser):
    results = re_parser.ParseString(text)
    
    _assertResults(results)
    
    
    