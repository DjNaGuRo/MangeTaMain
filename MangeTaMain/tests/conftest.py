import pytest
import sys
import os

@pytest.fixture(scope='session', autouse=True)
def setup_tkinter_environment():
    if sys.platform == 'win32':
        os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python313\tcl\tcl8.6'
        os.environ['TK_LIBRARY'] = r'C:\Program Files\Python313\tcl\tk8.6'