# Author: Liheng Chen
# Organization: ISCAS, China

import sys
import shutil

src_path = "../data/" + sys.argv[1] + ".txt"
dst_path = "../data/" + sys.argv[2] + ".txt"
shutil.copyfile(src_path, dst_path)
try:
    shutil.copyfile(src_path, dst_path)
except IOError as e:
    print("Unable to copy file. %s" % e)
    exit(1)
except:
    print("Unexpected error:", sys.exc_info())
    exit(1)

switch = {"100b": 100,
          "1k": 1024,
          "10k": 1024 * 10,
          "100k": 1024 * 100,
          "1m": 1024 * 1024,
          "10m": 1024 * 1024 * 10,
          "100m": 1024 * 1024 * 100,
          "1g": 1024 * 1024 * 1024,
          "10g": 1024 * 1024 * 1024 * 10,
          }
size = switch[sys.argv[2]]

with open(dst_path, "a+") as fileOut:
    fileOut.truncate(size)
    print(sys.argv[2], " Complete")
