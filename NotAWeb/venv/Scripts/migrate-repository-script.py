#!C:\Users\Valentin\PycharmProjects\NotADevs\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sqlalchemy-migrate==0.7.2','console_scripts','migrate-repository'
__requires__ = 'sqlalchemy-migrate==0.7.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sqlalchemy-migrate==0.7.2', 'console_scripts', 'migrate-repository')()
    )
