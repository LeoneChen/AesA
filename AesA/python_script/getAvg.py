import os
import numpy
import re
import sys

if not os.path.exists("../out/" + str(sys.argv[1]) + "/avg"):
    os.makedirs("../out/" + str(sys.argv[1]) + "/avg")

for fileSize in ("100b", "1k", "10k", "100k", "1m", "10m", "100m"):
    for coreNum in (2, 4, 6):
        for threadNum in (int(coreNum / 2), coreNum, coreNum * 2, coreNum * 4, coreNum * 8):
            fileNamePre = fileSize + "_" + str(sys.argv[1]) + "_" + str(coreNum) + "core_" + str(threadNum) + "thread_"
            EnThreadAvgList = []
            EnTimeList = []
            for roundNum in range(1, 6):
                with open("../out/" + str(sys.argv[1]) + "/" + fileNamePre + str(roundNum) + "round.txt",
                          "r") as fin:
                    for line in fin:
                        match_thread_avg = re.search("EnThreadAvg: ([0-9]*[.]?[0-9]*)", line)
                        if match_thread_avg:
                            EnThreadAvg = match_thread_avg.group(1)
                        match_time = re.search("EnTime: ([0-9]*[.]?[0-9]*)", line)
                        if match_time:
                            EnTime = match_time.group(1)
                EnThreadAvgList.append(float(EnThreadAvg))
                EnTimeList.append(float(EnTime))
            # print(fileNamePre, EnThreadAvgList, EnTimeList)
            with open("../out/" + str(sys.argv[1]) + "/avg/" + fileNamePre + "avg", "w") as fout:
                fout.write("EnThreadAvg: " + str(numpy.mean(EnThreadAvgList)) + " ms EnTimeAvg: " + str(
                    numpy.mean(EnTimeList)) + " ms")
