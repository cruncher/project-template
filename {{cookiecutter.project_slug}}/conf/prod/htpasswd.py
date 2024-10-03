# Script should be passed two paramters
# username and password
import crypt
import sys

if len(sys.argv) == 3:
    print("%s:%s" % (sys.argv[1], crypt.crypt(sys.argv[2], sys.argv[2])))
