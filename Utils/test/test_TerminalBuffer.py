from Utils.TerminalBuffer import TerminalBuffer
import pytest


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


def test_TerminalBuffer_Readline(text):
    term_buff = TerminalBuffer()
    
    data = text
    data.strip()
    data = data.split('\n')
    
    for line in data:
        term_buff.AddLine(line)
        
    
    for line in data:
        buff_line = term_buff.ReadEntry()
        assert buff_line == line
        
