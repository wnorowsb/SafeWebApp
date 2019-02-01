import sys
if sys.version_info[0]<3:       # require python3
 raise Exception("Python3 required! Current version: '%s'" % sys.version_info)
sys.path.insert(0, '/home/bartek/flask/')
from moi import app as application
