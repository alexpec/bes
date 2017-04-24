import os

from Utils.TerminalRunner import TerminalRunner
import hashlib




def test_TerminalRunner():
    
    TR = TerminalRunner()
    file = os.path.realpath(__file__)
    
    cmd = 'md5sum %s' %file

    TR.Runner(cmd)
    file = open(file, 'r')
    lines = file.read()
    expected_str = hashlib.md5(lines).hexdigest()
    
    got_str = TR.buffer.ReadEntry().split()[0]
    last_str = TR.buffer._buffer[-1]
    
    assert got_str == expected_str
    assert last_str == None
    
    
