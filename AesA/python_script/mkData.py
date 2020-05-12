# Author: Liheng Chen
# Organization: ISCAS, China

import os
import sys

path = "../data/" + sys.argv[1] + ".txt"

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
size = switch[sys.argv[1]]

with open(path, "w") as fileOut:
    for i in range(1, 100000000000000):
        fileOut.write(str(i))
        if size < switch["1m"]:
            fileOut.flush()
        if i % 10 == 0:
            fileOut.write("\n")
        print("\r" + sys.argv[1] + " Ratio: %.2f" % (os.path.getsize(path) * 100.0 / size), end="%")
        if os.path.getsize(path) >= size:
            break
    print()
    fileOut.truncate(size)
