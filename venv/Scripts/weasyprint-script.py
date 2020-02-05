#!F:\django\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'WeasyPrint==0.24','console_scripts','weasyprint'
__requires__ = 'WeasyPrint==0.24'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('WeasyPrint==0.24', 'console_scripts', 'weasyprint')()
    )
